import streamlit as st
import pandas as pd
import snowflake.connector



def run_query(query):
    query_pandas = snowflake_cursor.execute(query).fetch_pandas_all()
    return query_pandas




conn_sflake = snowflake.connector.connect(**st.secrets["snowflake"], client_session_keep_alive=True)
snowflake_cursor = conn_sflake.cursor()   
# query1 = run_query(f"select distinct SALESPERSON from LMI_TEST.APPFIGURES.STAGE_SALESFORCE_STREAMLIT_TARGET")
st.write("20221214 1534 ")