import pandas as pd
import streamlit as st
import snowflake.connector
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )
conn = init_connection()
# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall() # Returns a list of lists


data = run_query("SELECT * FROM LMI_TEST.APPFIGURES.STREAMLIT_20221214 LIMIT 10")
df = pd.DataFrame(data)
st.write(f"Connected to Snowflake with {len(df)} rows")
st.write(str(type(df)))
st.write(str(df.columns)) # AttributeError: 'list' object has no attribute 'columns'
df.columns = ['A', 'B', 'C']
AgGrid(df)