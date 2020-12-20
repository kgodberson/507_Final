# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 19:37:17 2020

@author: kmgod
"""

import streamlit as st

import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import time



@st.cache
def load_hospitals():
    df_hospital_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_hospital_2.csv')
    return df_hospital_2

@st.cache
def load_inatpatient():
    df_inpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_inpatient_2.csv')
    return df_inpatient_2

@st.cache
def load_outpatient():
    df_outpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_outpatient_2.csv')
    return df_outpatient_2


st.title('Medicare Evaluation- State of New Jersey- Kaitlyn Godberson')



    
    
# FAKE LOADER BAR TO STIMULATE LOADING    
# my_bar = st.progress(0)
# for percent_complete in range(100):
#     time.sleep(0.1)
#     my_bar.progress(percent_complete + 1)
  

st.write('Statistics for Health Professionals, *HHA 507*') 
  
# Load the data:     
df_hospital_2 = load_hospitals()
df_inpatient_2 = load_inatpatient()
df_outpatient_2 = load_outpatient()







hospitals_ny = df_hospital_2[df_hospital_2['state'] == 'NJ']


#Bar Chart
st.subheader('Percentage of Acute Care Hospitals in New Jersey')
bar1 = hospitals_ny['hospital_type'].value_counts().reset_index()
st.dataframe(bar1)

st.markdown('80% of the Hospitals in New Jersey are for Acute Care')


st.subheader('With a PIE Chart:')
fig = px.pie(bar1, values='hospital_type', names='index')
st.plotly_chart(fig)



st.subheader('Map of New Jersey Hospital Locations')

hospitals_ny_gps = hospitals_ny['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'lon', 2:'lat'}) 	
hospitals_ny_gps['lon'] = hospitals_ny_gps['lon'].str.strip('(')
hospitals_ny_gps = hospitals_ny_gps.dropna()
hospitals_ny_gps['lon'] = pd.to_numeric(hospitals_ny_gps['lon'])
hospitals_ny_gps['lat'] = pd.to_numeric(hospitals_ny_gps['lat'])

st.map(hospitals_ny_gps)


#Timeliness of Care
st.subheader('NJ Hospitals - Ownership affiliation')
bar2 = hospitals_ny['hospital_ownership'].value_counts().reset_index()
fig2 = px.bar(bar2, x='index', y='hospital_ownership')
st.plotly_chart(fig2)

st.markdown('The Bar Chart above shows that New Jersey hospitals are primarily owned by Voluntary non-profit- private organizations')

st.subheader('NJ Hospitals - Readmission National Comparison')
bar2 = hospitals_ny['readmission_national_comparison'].value_counts().reset_index()
fig2 = px.bar(bar2, x='index', y='readmission_national_comparison')
st.plotly_chart(fig2)

st.markdown('New Jersey hospitals are below average for the national readmission rate. Their patients go home with less of a chance of returning to the hospital. With a vast majority of NJ hospitals being Voluntary non-profit-private facilites, perhaps it can be concluded that this type of hospital ownership offers care with less of chance for patient readmission.')


#Drill down into INPATIENT and OUTPATIENT just for NY 
st.title('Inpatient Data')

inpatient_ny = df_inpatient_2[df_inpatient_2['provider_state'] == 'NJ']
total_inpatient_count = sum(inpatient_ny['total_discharges'])

st.header('Total Count of Discharges: New Jersey Inpatient Stays' )
st.header( str(total_inpatient_count) )



##Common D/C 

##Common D/C
 
common_discharges = df_inpatient_2[df_inpatient_2['provider_state'] == 'NJ']
common_discharges = inpatient_ny.groupby('provider_name')['total_discharges'].sum().reset_index()

st.markdown('The chart below displays the total number of discharges per specific hospital in the state of New Jersey. ATLANTICARE REGIONAL MEDICAL CENTER - CITY CAMPUS has the most discharges and ST FRANCIS MEDICAL CENTER has the least.')


top10 = common_discharges.head(10)
bottom10 = common_discharges.tail(10)




st.header('Providers')
st.dataframe(common_discharges)


col1, col2 = st.beta_columns(2)

col1.header('Top 10 Hospitals by discharges')
col1.dataframe(top10)

col2.header('Bottom 10 Hospitals by discharges')
col2.dataframe(bottom10)

st.subheader('Discharges by Hospital')
st.markdown('The bar chart below shows the number of patient discharges per hospital provider in NJ')
bar3 = px.bar(common_discharges, x='provider_name', y='total_discharges')
st.plotly_chart(bar3)






#Bar Charts of the costs 

costs = inpatient_ny.groupby('provider_name')['average_total_payments'].sum().reset_index()
costs['average_total_payments'] = costs['average_total_payments'].astype('int64')


costs_medicare = inpatient_ny.groupby('provider_name')['average_medicare_payments'].sum().reset_index()
costs_medicare['average_medicare_payments'] = costs_medicare['average_medicare_payments'].astype('int64')


costs_sum = costs.merge(costs_medicare, how='left', left_on='provider_name', right_on='provider_name')
costs_sum['delta'] = costs_sum['average_total_payments'] - costs_sum['average_medicare_payments']


st.title('Costs- Inpatient')
st.header("Hospital's average payments and costs paid by Medicare, New Jersey State - ")

bar4 = px.bar(costs_medicare, x='provider_name', y='average_medicare_payments')
st.plotly_chart(bar4)




#Costs by Condition and Hospital / Average Total Payments
costs_condition_hospital = inpatient_ny.groupby(['provider_name', 'drg_definition'])['average_total_payments','average_medicare_payments'].sum().reset_index()
st.header("Costs by Condition and Hospital - Average Total Payments and Average Medicare Payments in New Jersey Hospitals")
st.dataframe(costs_condition_hospital)



# hospitals = costs_condition_hospital['provider_name'].drop_duplicates()
# hospital_choice = st.sidebar.selectbox('Select your hospital:', hospitals)
# filtered = costs_sum["provider_name"].loc[costs_sum["provider_name"] == hospital_choice]
# st.dataframe(filtered) 

#add in information for outpatient care

st.title('Outpatient Data')

outpatient_ny = df_outpatient_2[df_outpatient_2['provider_state']== 'NJ']
total_outpatient_count = sum(outpatient_ny['average_total_payments'])

st.header('Average Payments for Outpatient services: State of New Jersey ')
st.header(str(total_outpatient_count) ) 

outpatient_ny = df_outpatient_2[df_outpatient_2['provider_state'] == 'NJ']
bar5 = px.bar(outpatient_ny, x='provider_name', y='outpatient_services')
st.plotly_chart(bar5) 

costs_outpatient_services = outpatient_ny.groupby(['provider_name', 'outpatient_services'])['average_total_payments'].sum().reset_index()
st.header('Outpatient service payment totals')
st.dataframe(costs_outpatient_services)

