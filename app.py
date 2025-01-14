import streamlit as st
from datetime import datetime
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Predicciones Fútbol",
    page_icon="⚽",
    layout="wide"
)

# CSS para mejorar el estilo de la página
st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f0f2f6;
        color: #333;
    }
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #008CBA;
        color: white;
        font-size: 16px;
        border: none;
        padding: 10px;
        border-radius: 8px;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #005f73;
    }
    .match-container {
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        padding: 2rem;
        margin: 1.5rem 0;
    }
    .match-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #004d40;
    }
    .match-teams {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .match-teams img {
        width: 50px;
        height: 50px;
    }
    .match-info {
        text-align: center;
        font-size: 1.2rem;
        margin-top: 1rem;
    }
    .sidebar-title {
        font-size: 1.8rem;
        color: #008CBA;
    }
    .sidebar-select {
        font-size: 1.2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar para selección de liga
st.sidebar.title("⚽ Predicciones Fútbol")
liga_seleccionada = st.sidebar.selectbox(
    "Selecciona una liga",
    ["LaLiga", "Premier League", "Serie A", "Bundesliga", "Ligue 1"],
    key="liga_seleccionada",
    index=0
)

# Diccionario de logos por liga
URL_LOGOS_LALIGA = {
    "athletic": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/athletic.png",
    "atleticomadrid": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/atleticomadrid.png",
    "barcelona": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/barcelona.png",
    "alaves": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/alaves.png",
    "betis": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/betis.png",
    "celta": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/celta.png",
    "espanyol": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/espanyol.png",
    "getafe": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/getafe.png",
    "girona": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/girona.png",
    "laspalmas": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/laspalmas.png",
    "leganes": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/leganes.png",
    "mallorca": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/mallorca.png",
    "osasuna": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/osasuna.png",
    "rayovallecano": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/rayovallecano.png",
    "realmadrid": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/realmadrid.png",
    "realsociedad": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/realsociedad.png",
    "sevilla": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/sevilla.png",
    "valencia": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/valencia.png",
    "valladolid": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/valladolid.png",
    "villarreal": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/villarreal.png"
}
URL_LOGOS_PREMIER = {
    "newcastle": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/newcastle.png",
    "bournemouth": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/bournemouth.png",
    "arsenal": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/arsenal.png",
    "astonvilla": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/astonvilla.png",
    "brentford": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/brentford.png",
    "brighton": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/brighton.png",
    "chelsea": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/chelsea.png",
    "crystalpalace": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/crystalpalace.png",
    "everton": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/everton.png",
    "ipswich": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/ipswich.png",
    "nottinghamforest": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/nottinghamforest.png",
    "fulham": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/fulham.png",
    "leicester": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/leicester.png",
    "liverpool": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/liverpool.png",
    "manunited": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/manunited.png",
    "mancity": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/mancity.png",
    "southampton": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/southampton.png",
    "tottenham": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/tottenham.png",
    "westham": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/westham.png",
    "wolves": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/wolves.png"
}

URL_LOGOS_SERIE_A = {
    "atalanta": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/atalanta.png",
    "bolonia": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/bolonia.png",
    "cagliari": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/cagliari.png",
    "empoli": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/empoli.png",
    "fiorentina": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/fiorentina.png",
    "hellasverona": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/hellasverona.png",
    "genoa": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/genoa.png",
    "inter": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/inter.png",
    "juventus": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/juventus.png",
    "lazio": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/lazio.png",
    "lecce": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/lecce.png",
    "milan": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/milan.png",
    "monza": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/monza.png",
    "napoles": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/napoles.png",
    "roma": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/roma.png",
    "parma": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/parma.png",
    "como": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/como.png",
    "torino": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/torino.png",
    "udinese": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/udinese.png",
    "venezia": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/venezia.png"
}

URL_LOGOS_LIGUE_1 = {
    "angers": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/angers.png",
    "auxerre": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/auxerre.png",
    "estrasburgo": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/estrasburgo.png",
    "havre": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/havre.png",
    "lens": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/lens.png",
    "lille": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/lille.png",
    "lyon": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/lyon.png",
    "marsella": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/marsella.png",
    "monaco": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/monaco.png",
    "montpellier": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/montpellier.png",
    "nantes": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/nantes.png",
    "niza": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/niza.png",
    "psg": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/psg.png",
    "saintetienne": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/saintetienne.png",
    "stadebretois": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/stadebretois.png",
    "stadereims": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/stadereims.png",
    "staderennais": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/staderennais.png",
    "toulouse": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/toulouse.png"
}

URL_LOGOS_BUNDESLIGA = {
    "augsburgo": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/augsburgo.png",
    "bayerleverkusen": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/bayerleverkusen.png",
    "bayernmunich": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/bayernmunich.png",
    "bochum": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/bochum.png",
    "borussiadortmund": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/borussiadortmund.png",
    "borussiamgladbach": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/borussiamgladbach.png",
    "eintrachtfrankfurt": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/eintrachtfrankfurt.png",
    "friburgo": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/friburgo.png",
    "heidenheim": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/heidenheim.png",
    "hoffenheim": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/hoffenheim.png",
    "holsteinkiel": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/holsteinkiel.png",
    "mainz": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/mainz.png",
    "rbleipzig": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/rbleipzig.png",
    "st_pauli": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/st_pauli.png",
    "stuttgart": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/stuttgart.png",
    "unionberlin": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/unionberlin.png",
    "werderbremen": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/werderbremen.png",
    "wolfsburgo": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/wolfsburgo.png"
}


# Mostrar información de la liga seleccionada
st.markdown(f"## Predicciones para **{liga_seleccionada}**")
st.markdown("---")

# Generar y mostrar los partidos de la liga seleccionada
if liga_seleccionada == "LaLiga":
    equipos = list(URL_LOGOS_LALIGA.keys())
elif liga_seleccionada == "Premier League":
    equipos = list(URL_LOGOS_PREMIER.keys())
elif liga_seleccionada == "Serie A":
    equipos = list(URL_LOGOS_SERIE_A.keys())
elif liga_seleccionada == "Bundesliga":
    equipos = list(URL_LOGOS_BUNDESLIGA.keys())
else:
    equipos = list(URL_LOGOS_LIGUE_1.keys())

# Ejemplo de cómo mostrar un partido
st.markdown("### Partido de ejemplo")
col1, col2 = st.columns(2)

with col1:
    st.image(URL_LOGOS_LALIGA["barcelona"], width=80)
    st.markdown("**Barcelona**")

with col2:
    st.image(URL_LOGOS_LALIGA["athletic"], width=80)
    st.markdown("**Athletic Club**")

# Contenedor de predicción para el partido
st.markdown("""
    <div class="match-container">
        <div class="match-header">Próximo partido</div>
        <div class="match-teams">
            <div>
                <img src="https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/barcelona.png" alt="Barcelona">
                <p>Barcelona</p>
            </div>
            <div>
                <img src="https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/athletic.png" alt="Athletic Club">
                <p>Athletic Club</p>
            </div>
        </div>
        <div class="match-info">
            <p><strong>Fecha:</strong> 20 de Enero 2025</p>
            <p><strong>Hora:</strong> 18:00</p>
            <button>Haz tu predicción</button>
        </div>
    </div>
""", unsafe_allow_html=True)

# Botón para predicción
if st.button("Haz tu predicción"):
    st.success("¡Tu predicción ha sido registrada!")



