import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="GetAround_Dashboard",
    page_icon="une-analyse.png",
    layout="wide",
)

if 'data1' in st.session_state and 'data2' in st.session_state:
    df1 = st.session_state.data1
    df2 = st.session_state.data2

st.header("ANALYSE")
        
st.subheader( "Analyse sur le parc de voitures en location:")
st.write("**Quelles marques de voitures et quels types de motorisation sont sur la plateforme?**")
selected_fuel = st.selectbox('Sélectionnez le type de carburant', df1['fuel'].unique())
filtered_df = df1[df1['fuel'] == selected_fuel]
fig = px.histogram(filtered_df, x = 'model_key', text_auto =True).update_xaxes(categoryorder= 'total descending')
st.plotly_chart(fig)

st.write('')
st.write('')

type_counts=df1['car_type'].value_counts()
st.write('**Quel type de véhicules?**')       
plt.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%',
                colors = sns.color_palette('Set2'))
st.pyplot(plt)

st.write('')
st.write('')

st.write("**Quelles options?**")
features = ['private_parking_available', 'has_gps', 'has_air_conditioning', 'automatic_car', 'has_getaround_connect', 'has_speed_regulator', 'winter_tires']
selected_feature = st.selectbox('Sélectionnez une fonctionnalité', features)

grouped = df1.groupby(['model_key', selected_feature]).size().unstack()
fig, ax = plt.subplots(figsize=(12, 8))
grouped.plot(kind='bar', stacked=True, ax=ax)
ax.set_title(f'Nombre de véhicules par marque ({selected_feature})')
ax.set_ylabel('Nombre de véhicules')
st.pyplot(fig)

st.write('')
st.write('')

st.subheader("Analyse sur les delais entre locations:")
st.write("**Y a-t-il du retard au check-out?**")
fig = px.histogram(df2, x = 'plage_interval', color= 'state', text_auto =True).update_xaxes(categoryorder= 'total descending')
st.plotly_chart(fig)
st.write("6819 véhicules sont ramenés en avance par rapport à l'heure du check-out.")
st.write("1988 locations ont un retard de check-out entre 1m et 15 m et seulement 122 locations se terminent à l'heure.")
st.write("3264 locations ont été annulé lorsque le retard de check-out était supérieur à 9h.")
    
st.write('')
st.write('')

median_checkout_time = df2['delay_at_checkout_in_minutes'].median()
average_checkout_time = df2['delay_at_checkout_in_minutes'].mean()
median_time_between_rentals = df2['time_delta_with_previous_rental_in_minutes'].median()
average_time_between_rentals = df2['time_delta_with_previous_rental_in_minutes'].mean()

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

st.write('')
st.write('')

#Garder uniquement les lignes avec un delais de checkout >0
to_keep = df2["delay_at_checkout_in_minutes"] > 0
min_delay = df2.loc[to_keep,:]

#Calcul pour connaître l'impact des retards sur les locations suivantes
min_delay.loc[:, "impacted_by_delay"] = (min_delay["delay_at_checkout_in_minutes"]
    - min_delay["time_delta_with_previous_rental_in_minutes"]) > 0

st.write('**Y a-t-il beaucoup de locations impactés par les retards de check-out?**')
fig = px.histogram(min_delay, x = 'impacted_by_delay', color= 'checkin_type', text_auto =True).update_xaxes(categoryorder= 'total descending')
st.plotly_chart(fig)
st.write('Nous pouvons constater que seulement 270 locations sont impactés, soit 1,27% des locations totales.')
st.write('6,8% des locations ayant du retard ont été faite par le système connect, dont 0,37% dans les locations impactées par le delais.')

st.write('')
st.write('')

#Calcul du pourcentage de véhicules impactés par retard
interval = min_delay['plage_interval'].unique().tolist()
result_list=[]
pourcent_list=[]

for i in interval:
    to_keep = (min_delay["impacted_by_delay"] == True) & (min_delay['plage_interval'] == i)
    result= len(min_delay.loc[to_keep,:])
    pourcent= ((len(min_delay.loc[to_keep,:])/len(df2))*100)
    result_list.append(result)
    pourcent_list.append(pourcent)

data_dict={ "plage_interval": interval, "nombre_de_vehicules_impactés": result_list, "pourcentage_de_véhicules_impactés": pourcent_list}

result_df=pd.DataFrame(data_dict)
result_df['pourcentage_de_véhicules_impactés'] = result_df['pourcentage_de_véhicules_impactés'].round(2)

st.write('')
st.write('')

st.write("**Analyse de l'impact des retards sur la location de véhicules**")

selected_interval = st.selectbox("Sélectionnez une plage horaire :", interval)
pourcentage = result_df[result_df['plage_interval'] == selected_interval]['pourcentage_de_véhicules_impactés'].values[0]

st.write(f"Pourcentage de véhicules impactés pour un retard {selected_interval}: {pourcentage:.2f}%")

st.write('')
st.write('')

st.subheader("Conclusion")
st.write('')
st.write('Notre analyse des données de location de voitures montre que la majorité des check-out se produisent dans les 10 minutes (temps médian de 9 min).')
st.write('Cependant, des retards plus long, avec une moyenne de 59 min, restent rares et ont un impact faible (1,27% des locations impactées).')
st.write("Pour améliorer l'exprérience des utilisateurs, nous pourrions envisager un intervalle de 2 heures entre les locations, offrant ainsi plus")
st.write("de flexibilité pour le retour et l'entretien des véhicules. La décision finale devrait impliquer les propriétaires et les utilisateurs, garantissant")
st.write('un équilibre entre rapidité et qualité de service.')
st.write('')
st.write('En outre, notre analyse a révélé que le système Connect contribue à un faible pourcentage de locations avec retards, représentant seulement 6,84% ')
st.write('des locations avec des retards non impactants pour les locations suivantes, tandis que seulement 0,37% des locations totales ont été influencé négativement')
st.write("par le système.")
st.write("Ces résultats suggèrent que privilégier le système Connect est une option viable, tout en maintenant un excellent service pour la grande majorité des utilisateurs.")
st.write('')
st.write("**Axe d'amélioration : Exploration des facteurs de retard spécifiques**")
st.write('Notre analyse actuelle met en lumière la prévalence des retards de check-out de courte durée. Cependant, pour optimiser davantage notre service, nous pourrions envisager')
st.write('une analyse plus approfondie des facteurs spécifiques qui influencent ces retards. Une consolidation des données pour explorer les impacts des marques de véhicules,')
st.write('de la puissance, du type de moteur et de la motorisation pourrait apporter des informations précieuses pour des améliorations ciblées.')
st.write('')
st.write("Malheureusement, en raison de l'absence d'informations sur les revenus des propriétaires, nous ne pouvons pas quantifier précisément l'impact financier de la nouvelle fonctionnalité. ")
st.write('Cependant, notre analyse approfondie des retards et des annulations met en lumière des tendances significatives qui peuvent aider à prendre des décisions éclairées.')
st.write('Nous avons répondu de manière satisfaisante à plusieurs questions du projet, en identifiant les locations problématiques et en examinant la fréquence des retards.')
st.write('Cette analyse constitue une base solide pour des améliorations futures visant à optimiser le service.')
