import datetime
import pandas as pd
import plotly.express as px
import snowflake.connector
import streamlit as st


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
    return title


def run_query(query):
    query_pandas = snowflake_cursor.execute(query).fetch_pandas_all()
    return query_pandas

conn_sflake = snowflake.connector.connect(**st.secrets["snowflake"], client_session_keep_alive=True)
snowflake_cursor = conn_sflake.cursor()   
df = run_query(f"SELECT * FROM LMI_TEST.APPFIGURES.STREAMLIT_20221214 LIMIT 10")
st.write(df)

# title = t(f"Acquisitions (N={len(df):,})")
# fig = px.bar(df, x=df.columns[0], y='ROW_COUNT', width=940)
# fig.update_layout(title=title,
#     xaxis_title='Date',
#     yaxis_title='Count') #,legend_title_text='')

# st.plotly_chart(fig)