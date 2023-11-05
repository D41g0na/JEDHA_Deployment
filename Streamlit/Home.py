import streamlit as st
import pandas as pd
from PIL import Image
import os

st.set_page_config(
    page_title="GetAround_Dashboard",
    page_icon="une-analyse.png",
    layout="wide",
)

def main():
    st.header("HOME PAGE")
    st.title("GetAround_Dashboard")
    choix = st.sidebar.radio("SubMenu", ["Description", "Documentation"])
    if choix == "Description":
        st.subheader("Bienvenue sur l'application GetAround_Dashboard")

        st.write("Découvrez des analyses de données et des estimations de tarification pour votre expérience de location de voitures")
        image = Image.open('craiyon.png')

        st.image(image, caption='car_dashboard')
      
    if choix == "Documentation":
        st.subheader("Comment se déplacer au sein de l'application")

        st.write("L'application est divisé en 3 pages: Data, Analyse et API")
        st.write("Tout d'abord, sur la page Data, vous pourrez voir les datasets qui nous ont permis de faire les Analyses et qui renseignent l'API")
        st.write("pour faire une estimation du prix de la location journalière.")
        st.write(" ")
        st.write("Ensuite, sur la page Analyse, vous aurez un dashboard avec des visualisations concernant les véhicules dans le parc locatif du site. ")        
        st.write("Vous pourrez également visualiser les données concernant l'importance des retard lors des check-out. ")
        st.write(" ")
        st.write("Enfin, sur la page API, vous pourrez, à l'aide d'un dataset fournit sur le github, faire des estimations de prix de location à la journée.")
   
    @st.cache_data
    def load_data1():
        data1 = pd.read_csv("/home/app/get_around_pricing_project.csv")
        return data1

    @st.cache_data
    def load_data2():
        data2 = pd.read_csv("/home/app/get_around_delay_analysis_copy.csv")
        return data2

# Charger les données dans la session Streamlit
    if 'data1' not in st.session_state:
        st.session_state.data1 = load_data1()

    if 'data2' not in st.session_state:
        st.session_state.data2 = load_data2()

if __name__ == "__main__":
    main()