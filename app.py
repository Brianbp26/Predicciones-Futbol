import streamlit as st
from datetime import datetime
import pandas as pd
import requests
# Configuración de la página
st.set_page_config(
    page_title="Predicciones Fútbol",
    page_icon="⚽",
    layout="wide"
)

st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
    }
    .match-container {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .team-logo {
        text-align: center;
    }
    .team-logo img {
        width: 100px;
        height: 100px;
    }
    .team-name {
        font-weight: bold;
        margin-top: 0.5rem;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)
# Sidebar para selección de liga
st.sidebar.title("⚽ Predicciones Fútbol")
liga_seleccionada = st.sidebar.selectbox(
    "Selecciona una liga",
    ["LaLiga", "Premier League", "Serie A", "Bundesliga", "Ligue 1"]
)

# Diccionario de logos por liga (ejemplo con LaLiga, agrega más si es necesario)
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


# API Key de Football-Data
API_KEY = "d21df9a683e74915bdb6dac39270a985"
API_URL = "https://api.football-data.org/v4/competitions/{}/matches"

# Diccionario de ID de ligas (usando el código interno de Football-Data)
liga_ids = {
    "LaLiga": "PD",  # LaLiga tiene el código "PD" en Football-Data
    "Premier League": "PL",
    "Serie A": "IT1",
    "Bundesliga": "BL1",
    "Ligue 1": "FR1"
}

# Función para obtener partidos de la API de Football-Data
def obtener_partidos(liga):
    url = API_URL.format(liga_ids[liga])
    headers = {
        "X-Auth-Token": API_KEY
    }
    
    # Realizamos la solicitud HTTP
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        matches = data.get("matches", [])
        
        # Crear un DataFrame de los partidos
        partidos = []
        for match in matches:
            home_team = match["homeTeam"]["name"]
            away_team = match["awayTeam"]["name"]
            score = match["score"]
            partidos.append({
                "Local": home_team,
                "Visitante": away_team,
                "Resultado": f"{score['fullTime']['homeTeam']} - {score['fullTime']['awayTeam']}",
                "Fecha": match["utcDate"]
            })
        
        return pd.DataFrame(partidos)
    else:
        st.error("Error al obtener los datos de los partidos.")
        return pd.DataFrame()

# Función para mostrar los partidos con los logos
def mostrar_partidos(partidos, logos):
    for partido in partidos:
        home_team = partido['teams']['home']['name']
        away_team = partido['teams']['away']['name']
        home_score = partido['scores']['home']['ft']
        away_score = partido['scores']['away']['ft']
        
        # Mostrar los partidos en tarjetas
        st.markdown(f"### {home_team} vs {away_team}")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            logo_home = logos.get(home_team.lower(), '')
            if logo_home:
                st.image(logo_home, width=100)
            st.markdown(f"**{home_team}**")
        
        with col2:
            st.markdown(f"**{home_score} - {away_score}**")
        
        with col3:
            logo_away = logos.get(away_team.lower(), '')
            if logo_away:
                st.image(logo_away, width=100)
            st.markdown(f"**{away_team}**")
        
        st.markdown("---")

# Selección de temporada
temporada = st.sidebar.selectbox("Selecciona una temporada", ["2022", "2023"])



# Obtener los partidos de la liga seleccionada y temporada
liga_id = liga_map[liga_seleccionada]
partidos = obtener_partidos(liga_ids)

# Mostrar partidos con los logos correspondientes
if liga_seleccionada == "LaLiga":
    logos = URL_LOGOS_LALIGA
elif liga_seleccionada == "Premier League":
    logos = URL_LOGOS_PREMIER
elif liga_seleccionada == "Serie A":
    logos = URL_LOGOS_SERIE_A
elif liga_seleccionada == "Ligue 1":
    logos = URL_LOGOS_LIGUE_1
elif liga_seleccionada == "Bundesliga":
    logos = URL_LOGOS_BUNDESLIGA
else:
    logos = {}

if partidos:
    mostrar_partidos(partidos, logos)
else:
    st.write("No se encontraron partidos para esta liga y temporada.")

# Métricas adicionales en el sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Estadísticas del Modelo")
st.sidebar.metric("Precisión Global", "73%")
st.sidebar.metric("Partidos Predichos", "152")


