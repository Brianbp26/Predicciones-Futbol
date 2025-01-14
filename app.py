import streamlit as st
import requests
from datetime import datetime

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

# Diccionario de logos de equipos (de acuerdo a las ligas)
logos = {
    "LaLiga": {
    "athleticclub": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/athletic.png",
    "clubatléticodemadrid": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/atleticomadrid.png",
    "fcbarcelona": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/barcelona.png",
    "deportivoalavés": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/alaves.png",
    "realbetisbalompié": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/betis.png",
    "rcceltadevigo": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/celta.png",
    "rcdespanyoldebarcelona": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/espanyol.png",
    "getafecf": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/getafe.png",
    "gironafc": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/girona.png",
    "udlaspalmas": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/laspalmas.png",
    "cdleganés": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/leganes.png",
    "rcdmallorca": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/mallorca.png",
    "caosasuna": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/osasuna.png",
    "rayovallecanodemadrid": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/rayovallecano.png",
    "realmadridcf": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/realmadrid.png",
    "realsociedaddefútbol": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/realsociedad.png",
    "sevillafc": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/sevilla.png",
    "valenciacf": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/valencia.png",
    "valladolid": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/valladolid.png",
    "villarrealcf": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/villarreal.png"
    },
    "Premier League": {
        "newcastleunitedfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/newcastle.png",
        "afcbournemouth": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/bournemouth.png",
        "arsenalfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/arsenal.png",
        "astonvillafc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/astonvilla.png",
        "brentfordfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/brentford.png",
        "brighton&hovealbionfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/brighton.png",
        "chelseafc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/chelsea.png",
        "crystalpalacefc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/crystalpalace.png",
        "evertonfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/everton.png",
        "ipswichtownfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/ipswich.png",
        "nottinghamforestfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/nottinghamforest.png",
        "fulhamfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/fulham.png",
        "leicestercityfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/leicester.png",
        "liverpoolfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/liverpool.png",
        "manchesterunitedfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/manunited.png",
        "manchestercityfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/mancity.png",
        "southamptonfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/southampton.png",
        "tottenhamhotspurfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/tottenham.png",
        "westhamunitedfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/westham.png",
        "wolverhamptonwanderersfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/wolves.png"
        },
    "Serie A": {
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
        },
    "Bundesliga": {
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
        },
    "Ligue 1": {
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
}

# Función para obtener partidos de la API
def obtener_partidos(liga):
    url = f'https://api.football-data.org/v4/competitions/{liga}/matches'
    headers = {
        'X-Auth-Token': 'd21df9a683e74915bdb6dac39270a985'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data['matches']
    else:
        st.error("No se pudieron obtener los partidos.")
        return []

# Función para mostrar los partidos
def mostrar_partidos(partidos, liga):
    for partido in partidos:
        local = partido['homeTeam']['name']
        visitante = partido['awayTeam']['name']
        fecha = datetime.strptime(partido['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
        fecha = fecha.strftime('%d/%m/%Y %H:%M')

        logo_local = logos[liga].get(local.lower().replace(" ", ""), "")
        logo_visitante = logos[liga].get(visitante.lower().replace(" ", ""), "")

        st.markdown(f"""
            <div class="match-container">
                <div class="team-logo">
                    <img src="{logo_local}" alt="{local}">
                    <div class="team-name">{local}</div>
                </div>
                <div class="team-logo">
                    <img src="{logo_visitante}" alt="{visitante}">
                    <div class="team-name">{visitante}</div>
                </div>
                <div class="match-time">
                    <strong>{fecha}</strong>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Obtener partidos según la liga seleccionada
if liga_seleccionada == "Premier League":
    liga_id = "PL"
elif liga_seleccionada == "LaLiga":
    liga_id = "PD"
elif liga_seleccionada == "Serie A":
    liga_id = "SA"
elif liga_seleccionada == "Bundesliga":
    liga_id = "BL1"
elif liga_seleccionada == "Ligue 1":
    liga_id = "FL1"

partidos = obtener_partidos(liga_id)
mostrar_partidos(partidos, liga_seleccionada)


