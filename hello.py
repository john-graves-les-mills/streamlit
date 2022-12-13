import pandas as pd
import streamlit as st
import snowflake.connector

from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

conn_sflake = snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )
snowflake_cursor = conn_sflake.cursor() 

# Perform query.
# Cache the dataframe so it's only loaded once
@st.experimental_memo
def run_query(query):
    query_pandas = snowflake_cursor.execute(query).fetch_pandas_all()
    return query_pandas

# Boolean to resize the dataframe, stored as a session state variable
# st.checkbox("Use container width", value=False, key="use_container_width")

df = run_query("SELECT * FROM LMI_TEST.APPFIGURES.STREAMLIT_20221214 LIMIT 10")

# Display the dataframe and allow the user to stretch the dataframe
# across the full width of the container, based on the checkbox value
# st.dataframe(df, use_container_width=st.session_state.use_container_width)
AgGrid(df)