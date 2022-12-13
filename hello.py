import streamlit as st
import snowflake.connector

conn_sflake = snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )
snowflake_cursor = conn_sflake.cursor() 

# Perform query.
def run_query(query):
    query_pandas = snowflake_cursor.execute(query).fetch_pandas_all()
    return query_pandas

my_variable = run_query("SELECT * FROM LMI_TEST.APPFIGURES.STREAMLIT_20221214")
my_df = st.dataframe(my_variable)
st.write(f"Connected to Snowflake with {len(my_variable)} rows")

                        
if st.button("Click me"):
  st.write("Hello world 20221214 1113")

my_pick = st.text_input("Pick a number:")
if my_pick:
  st.write(f"You picked: {my_pick}")
