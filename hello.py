import streamlit as st
import pandas as pd
import snowflake.connector
import plotly.express as px


def run_query(query):
    query_pandas = snowflake_cursor.execute(query).fetch_pandas_all()
    return query_pandas




conn_sflake = snowflake.connector.connect(**st.secrets["snowflake"], client_session_keep_alive=True)
snowflake_cursor = conn_sflake.cursor()   
st.write("20221214 1609 ")
df = run_query(f"SELECT * FROM LMI_TEST.APPFIGURES.STREAMLIT_20221214 LIMIT 10")
st.write(df)

fig = px.bar(df.head(10), x=df.columns[0], y='ROW_COUNT', width=940)
fig.update_layout(title="Acquisitions",
    xaxis_title='Date',
    yaxis_title='Count') #,legend_title_text='')
st.plotly_chart(fig)