import streamlit as st
import snowflake.connector

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
        return cur.fetchall()

my_variable = run_query("SELECT * FROM LMI_TEST.APPFIGURES.STAGE_SALESFORCE_STREAMLIT_TARGET")
my_df = st.dataframe(my_variable)
st.write(f"Connected to Snowflake with {len(my_variable)} rows")

                        
if st.button("Click me"):
  st.write("Hello world 20221214 1113")

my_pick = st.text_input("Pick a number:")
if my_pick:
  st.write(f"You picked: {my_pick}")
