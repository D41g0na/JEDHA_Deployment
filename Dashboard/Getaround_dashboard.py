import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(
    page_title="GetAround_Dashboard",
    page_icon="une-analyse.png",
    layout="wide",
)

DATA_URL= "/home/app/get_around_delay_analysis_copy.xlsx"

st.title('Dashboard Getaround')
st.markdown("Bienvenue sur ce dashboard! Nous allons déterminer s'il est possible d'avoir un temps minimum entre deux locations.")

@st.cache_data
def load_data():
    data = pd.read_excel(DATA_URL)      
    return data

data_load_state = st.text('Loading data...')
data = load_data()

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader("Analyse sur les delais entre locations:")
st.write("**Y a-t-il du retard au check-out?**")
fig = px.histogram(data, x = 'plage_interval', color= 'state', text_auto =True).update_xaxes(categoryorder= 'total descending')
st.plotly_chart(fig)

median_checkout_time = data['delay_at_checkout_in_minutes'].median()
average_checkout_time = data['delay_at_checkout_in_minutes'].mean()
median_time_between_rentals = data['time_delta_with_previous_rental_in_minutes'].median()
average_time_between_rentals = data['time_delta_with_previous_rental_in_minutes'].mean()

st.write('**Quel est le retard moyen et médian pour un check-out? Quel est le temps moyen et médian entre 2 locations?**')

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.write('Temps moyen de retard de check-out')
        fig = go.Figure(go.Indicator(
        mode="number",
        value=average_checkout_time,
        ))
        st.plotly_chart(fig)

        st.write('Temps moyen entre deux locations')
        fig = go.Figure(go.Indicator(
        mode="number",
        value=average_time_between_rentals,
        ))
        st.plotly_chart(fig)

    with col2:
        st.write('Temps médian de retard de check-out')
        fig = go.Figure(go.Indicator(
        mode="number",
        value=median_checkout_time,
        ))
        st.plotly_chart(fig)

        st.write('Temps médian entre deux locations')
        fig = go.Figure(go.Indicator(
        mode="number",
        value=median_time_between_rentals,
        ))
        st.plotly_chart(fig)

#Garder uniquement les lignes avec un delais de checkout >0
to_keep = data["delay_at_checkout_in_minutes"] > 0
min_delay = data.loc[to_keep,:]

#Calcul pour connaître l'impact des retards sur les locations suivantes
min_delay.loc[:, "impacted_by_delay"] = (min_delay["delay_at_checkout_in_minutes"]
    - min_delay["time_delta_with_previous_rental_in_minutes"]) > 0

st.write('**Y a-t-il beaucoup de locations impactés par les retards de check-out?**')
fig = px.histogram(min_delay, x = 'impacted_by_delay', color= 'checkin_type', text_auto =True).update_xaxes(categoryorder= 'total descending')
st.plotly_chart(fig)

#Calcul du pourcentage de véhicules impactés par retard
interval = min_delay['plage_interval'].unique().tolist()
result_list=[]
pourcent_list=[]

for i in interval:
    to_keep = (min_delay["impacted_by_delay"] == True) & (min_delay['plage_interval'] == i)
    result= len(min_delay.loc[to_keep,:])
    pourcent= ((len(min_delay.loc[to_keep,:])/len(data))*100)
    result_list.append(result)
    pourcent_list.append(pourcent)

data_dict={ "plage_interval": interval, "nombre_de_vehicules_impactés": result_list, "pourcentage_de_véhicules_impactés": pourcent_list}

result_df=pd.DataFrame(data_dict)
result_df['pourcentage_de_véhicules_impactés'] = result_df['pourcentage_de_véhicules_impactés'].round(2)

st.write("**Analyse de l'impact des retards sur la location de véhicules**")

selected_interval = st.selectbox("Sélectionnez une plage horaire :", interval)
pourcentage = result_df[result_df['plage_interval'] == selected_interval]['pourcentage_de_véhicules_impactés'].values[0]

st.write(f"Pourcentage de véhicules impactés pour un retard {selected_interval}: {pourcentage:.2f}%")