import datetime
import streamlit as st
import pandas as pd
import snowflake.connector
import plotly.express as px

today = datetime.datetime.today().date()

def run_query(query):
    query_pandas = snowflake_cursor.execute(query).fetch_pandas_all()
    return query_pandas

def t(title_string, no_year=False, silent=False):
    """Add "as at {today}" to title. Usage: t(title_sting)

    @title_string text to preceed the "as at" part
    """
    if no_year == False:
        today = datetime.datetime.today().strftime('%d %b %Y')
        title = f"{title_string} as at {today}"
    else:
        today = datetime.datetime.today().strftime('%d %b')
        title = f"{title_string} - {today}"


conn_sflake = snowflake.connector.connect(**st.secrets["snowflake"], client_session_keep_alive=True)
snowflake_cursor = conn_sflake.cursor()   
st.write("20221214 1609 ")
df = run_query(f"SELECT * FROM LMI_TEST.APPFIGURES.STREAMLIT_20221214")
st.write(f"Fetched {len(df)} Days of Data through {max(df.CREATED_DATE)}")
df2021 = df[(df.CREATED_DATE >= datetime.date(2021,11,25)) & (df.CREATED_DATE <= datetime.date(2022,1,25))].copy()
df2022 = df[(df.CREATED_DATE >= datetime.date(2022,11,25)) & (df.CREATED_DATE <= datetime.date(2023,1,25))].copy()
# datetime.date(2022,11,29) - datetime.date(2021,11,30) # 364 days
df2022['CREATED_DATE'] = df2022['CREATED_DATE'] - datetime.timedelta(days=364)
df2022.rename(columns={'ROW_COUNT':'2022'}, inplace=True)
df2021.rename(columns={'ROW_COUNT':'2021'}, inplace=True)
df2 = df2021[['CREATED_DATE', '2021']].merge(df2022[['CREATED_DATE', '2022']], how='left')
title = t(f"Acquisitions 2021 v 2022 (N={len(df2):,})")

fig = px.bar(df2, x=df2.columns[0], y=df2.columns[1:], width=940)
fig.update_layout(title=title,
                 xaxis_title='Created Date (minus 1 year for 2022)',
                 yaxis_title='Count',
                  legend_title_text='Year',
                 barmode='group')
st.plotly_chart(fig)