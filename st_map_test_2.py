import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import os

db_file = 'climbing_database.db'
conn = sqlite3.connect(db_file)

def run_query():
    st.markdown("# Mapping Mountains I've Climbed")
    
    # Can use lambda function to create a list of databases in the directory!
    #sqlite_dbs = [file for file in os.listdir('.') if file.endswith('.db')]
    #db_filename = st.selectbox('DB Filename', sqlite_dbs)
    #st.write('Pulling climbing data from git database')
    
    query = "Select * from sals_climbs"

    submitted = st.button('Click to pull climbing data from SQLite Database')

    if submitted:
        
        prt_sum = pd.read_sql_query('Select * from Partner_Summary',conn)
        st.bar_chart(prt_sum, x = 'Partner',y = 'Total_Pitches')
        
        try:
            query = conn.execute(query)
            cols = [column[0] for column in query.description]
            results_df= pd.DataFrame.from_records(
                data = query.fetchall(), 
                columns = cols
            )
            
            results_df[['lat','lon']] = results_df['GPS'].str.split(',', n=1, expand=True).apply(pd.to_numeric)
            st.dataframe(results_df)
            
            #map_df = results_df[['lat','lon']]
            #map_df[['lat', 'lon']] = map_df[['lat', 'lon']].apply(pd.to_numeric)
            
            st.map(data=results_df,size='Pitches',)
            
        except Exception as e:
            st.write(e)

    st.sidebar.markdown("# Run Query")

run_query()