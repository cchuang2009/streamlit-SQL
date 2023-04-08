import pandas as pd
import streamlit as st
import altair as alt
import duckdb

con = duckdb.connect(database='Job.db', read_only=True) 

# Countries
query="""
   SELECT * 
   FROM job
"""
Countries=list(con.execute(query).df().columns)[2:]

st.subheader('Job Postings Investigation')

col1, col2 = st.columns(2)

with col1:
    query="""
            SELECT 
                 DISTINCT variable
            FROM job        
            ORDER BY variable       
          """
    kinds=con.execute(query).df()
    kind = st.selectbox('Kind of Statistics',kinds['variable'])

with col2: 
    countries = st.multiselect('Select Countries', Countries)

if len(countries) == 0:
    st.warning("Please select at least one country.")
elif len(kind) == 0:
    st.warning("Please select a statistic.")
else:
    query = f"""
            SELECT
                date,
                {', '.join([f"{c}" for c in countries])}
            FROM Job
            WHERE variable = ?
            """
    result_df = con.execute(query, [kind]).df()
    melted_df = pd.melt(result_df, id_vars=['date'], var_name='Country', value_name='Value')

    chart = alt.Chart(melted_df).mark_line().encode(
        x='date',
        y='Value',
        color='Country',
        tooltip=['Country', 'Value']
    ).interactive()

    st.altair_chart(chart, use_container_width=True)
