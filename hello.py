import streamlit as st
import datetime
import pandas as pd
import snowflake.connector

def run_query(query):
    query_pandas = snowflake_cursor.execute(query).fetch_pandas_all()
    return query_pandas

conn_sflake = snowflake.connector.connect(**st.secrets["snowflake"], client_session_keep_alive=True)
snowflake_cursor = conn_sflake.cursor()   
df = run_query(f"SELECT * FROM LMI_TEST.APPFIGURES.STREAMLIT_20221214 LIMIT 10")
st.write(str(type(df)))
st.write(df)
exit()