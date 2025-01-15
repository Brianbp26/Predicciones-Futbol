import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
from datos import obtener_clasificacion, mostrar_clasificacion, obtener_partidos, agrupar_partidos_por_jornadas, mostrar_partidos
# Configuración de la página
st.set_page_config(
    page_title="Predicciones Fútbol",
    page_icon="⚽",
    layout="wide"
)

st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
    }
    .main {
        background-color: #101820;
        color: #ffffff;
    }
    .match-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #1e272e;
        color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .team-logo img {
        width: 80px;
        height: 80px;
    }
    .team-name {
        margin-top: 10px;
        font-size: 1.2rem;
        text-align: center;
    }
    .match-info {
        text-align: center;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        background-color: #f39c12;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar para selección de liga
st.sidebar.title("⚽ Predicciones Fútbol")
liga_seleccionada = st.sidebar.selectbox(
    "Selecciona una liga",
    ["LaLiga", "Premier League", "Serie A", "Bundesliga", "Ligue 1"]
)

# Header principal con logo de la liga
st.markdown(f"""
<div style="display: flex; align-items: center; gap: 1rem;">
    <h1 style="margin: 0;">Predicciones {liga_seleccionada}</h1>
    <img src="{logos_ligas[liga_seleccionada]}" alt="{liga_seleccionada}" style="width: 50px; height: 50px;">
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# Diccionario de logos de ligas
logos_ligas = {
    "LaLiga": "https://raw.githubusercontent.com/Brianbp26/Logos/d6015e93917a71eee579fca028b9e03c5cfe0067/laliga.png",
    "Premier League": "https://raw.githubusercontent.com/Brianbp26/Logos/038dae8a150d6cd90da2c99b08c461f3887b6095/premier.png",
    "Serie A": "https://raw.githubusercontent.com/Brianbp26/Logos/d6015e93917a71eee579fca028b9e03c5cfe0067/serie a.png",
    "Bundesliga": "https://raw.githubusercontent.com/Brianbp26/Logos/d6015e93917a71eee579fca028b9e03c5cfe0067/bundesliga.png",
    "Ligue 1": "https://raw.githubusercontent.com/Brianbp26/Logos/59347f45da1c564258e4e9084414772207443bbd/ligue 1.png",
}

liga_ids = {
    "LaLiga": "PD",  # Primera División Española
    "Premier League": "PL",  # Premier League
    "Serie A": "SA",  # Serie A
    "Bundesliga": "BL1",  # Bundesliga
    "Ligue 1": "FL1"  # Ligue 1
}

# Lógica principal
if liga_seleccionada:
    liga_id = liga_ids.get(liga_seleccionada)
    if liga_id:
        clasificacion = obtener_clasificacion(liga_id)
        mostrar_clasificacion(clasificacion,liga_seleccionada)
        partidos = obtener_partidos(liga_id)
        mostrar_partidos(partidos, liga_seleccionada)
        




        




