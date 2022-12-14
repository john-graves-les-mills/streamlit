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
st.header("Year on Year Daily Acquisitions")
df = run_query(f"""SELECT * FROM LMI_TEST.APPFIGURES.DAILY_ACQUISITIONS_20221215""")

st.subheader(f"LM+ Acquisitions 2021 v 2022 (to {max(df.CREATED_DATE)})")
st.write(f"Fetched Data from {min(df.CREATED_DATE)} to {max(df.CREATED_DATE)} and shifted 2022 data back 364 days to align with 2021")
st.write(f"Tip: 2022 Columns are split by Base and Premium Tier - hover mouse on bars to see separate counts")

# 2021
df2021 = df[(df.CREATED_DATE >= datetime.date(2021,11,25)) & 
            (df.CREATED_DATE <= datetime.date(2022,1,25)) &
            (df.TIER == 'TIER#premium')].copy()
df2021.rename(columns={'ROW_COUNT':'2021'}, inplace=True)

# 2022
df2022 = df[(df.CREATED_DATE >= datetime.date(2022,11,25)) & (df.CREATED_DATE <= datetime.date(2023,1,25))].copy()
# datetime.date(2022,11,29) - datetime.date(2021,11,30) # 364 days
df2022['CREATED_DATE'] = df2022['CREATED_DATE'] - datetime.timedelta(days=364)
df2022b = df2022.pivot(index='CREATED_DATE' , columns='TIER' , values='ROW_COUNT')
col_map = {'TIER#base':'2022 Base', 'TIER#premium':'2022 Premium'}
df2022b.columns = [col_map[col] for col in list(df2022b.columns)]
df2022b.reset_index(inplace=True)
df2 = df2021[['CREATED_DATE', '2021']].merge(df2022b, how='left')
df3 = pd.melt(df2, id_vars='CREATED_DATE', value_vars=['2021', '2022 Base', '2022 Premium'])
df3['Year'] = df3.variable.apply(lambda row: row[:4])

fig = px.bar(df3, x=df3.columns[0], y=df3.columns[2], width=940, hover_name='variable', color='Year')
fig.update_layout(xaxis_title='Created Date (minus 1 year for 2022)',
                  yaxis_title='Count',
                  legend_title_text='Year',
                  barmode='group')
st.plotly_chart(fig)