import streamlit as st
from datetime import datetime
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Predicciones Fútbol",
    page_icon="⚽",
    layout="wide"
)

st.markdown("""
    <style>
    .main {
        padding: 0rem 2rem;
        background-color: #f4f5f7;
    }
    .stButton>button {
        width: 100%;
        background-color: #006400;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 15px;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #004d00;
    }
    .sidebar .sidebar-content {
        background-color: #1a1a1a;
        color: white;
        padding: 2rem;
    }
    .sidebar .sidebar-content h1 {
        font-size: 2rem;
        font-family: 'Arial', sans-serif;
    }
    .match-container {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
    }
    .team-logo {
        width: 60px;
        height: 60px;
        border-radius: 8px;
        box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
        margin-right: 10px;
    }
    .match-info {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 1rem;
    }
    .match-info h3 {
        font-size: 1.5rem;
        color: #333;
    }
    .match-info .score {
        font-size: 1.2rem;
        color: #ff4500;
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


URL_LOGOS = {
    "LaLiga": URL_LOGOS_LALIGA,
    "Premier League": URL_LOGOS_PREMIER,
    "Serie A": URL_LOGOS_SERIE_A,
    "Ligue 1": URL_LOGOS_LIGUE_1,
    "Bundesliga": URL_LOGOS_BUNDESLIGA
}

# Partidos de ejemplo por liga
PARTIDOS_LALIGA = pd.DataFrame({
    'local': ['Espanyol', 'Osasuna', 'Leganes', 'Celta', 'Getafe'],
    'visitante': ['Valladolid', 'Rayo Vallecano', 'Atletico Madrid', 'Athletic', 'Barcelona'],
    'fecha': ['2024-01-17', '2024-01-18', '2024-01-18', '2024-01-18', '2024-01-18'],
    'hora': ['21:00', '14:00', '16:15', '18:30', '21:00'],
    'prob_local': [0.35, 0.40, 0.30, 0.35, 0.25],
    'prob_empate': [0.30, 0.30, 0.35, 0.30, 0.25],
    'prob_visitante': [0.35, 0.30, 0.35, 0.35, 0.50],
    'pred_goles_local': [1, 2, 1, 1, 1],
    'pred_goles_visitante': [1, 1, 2, 1, 2]
})

PARTIDOS_PREMIER = pd.DataFrame({
    'local': ['Arsenal', 'Chelsea', 'Liverpool', 'Man City', 'Man United'],
    'visitante': ['Tottenham', 'Everton', 'Brighton', 'Newcastle', 'Ipswich'],
    'fecha': ['2024-01-17', '2024-01-18', '2024-01-18', '2024-01-18', '2024-01-18'],
    'hora': ['21:00', '14:00', '16:15', '18:30', '21:00'],
    'prob_local': [0.45, 0.50, 0.60, 0.65, 0.55],
    'prob_empate': [0.30, 0.25, 0.20, 0.20, 0.30],
    'prob_visitante': [0.25, 0.25, 0.20, 0.15, 0.15],
    'pred_goles_local': [2, 1, 3, 3, 2],
    'pred_goles_visitante': [1, 1, 0, 0, 1]
})

PARTIDOS_SERIE_A = pd.DataFrame({
    'local': ['Atalanta', 'Inter', 'Roma', 'Lazio', 'Bolonia'],
    'visitante': ['Juventus', 'Milan', 'Napoles', 'Fiorentina', 'Udinese'],
    'fecha': ['2024-01-17', '2024-01-17', '2024-01-18', '2024-01-18', '2024-01-19'],
    'hora': ['18:00', '20:45', '15:00', '18:00', '12:30'],
    'prob_local': [0.45, 0.50, 0.40, 0.55, 0.35],
    'prob_empate': [0.30, 0.25, 0.35, 0.30, 0.30],
    'prob_visitante': [0.25, 0.25, 0.25, 0.15, 0.35],
    'pred_goles_local': [2, 3, 1, 2, 1],
    'pred_goles_visitante': [1, 1, 1, 0, 1]
})

PARTIDOS_LIGUE_1 = pd.DataFrame({
    'local': ['Psg', 'Niza', 'Marsella', 'Angers', 'Lille'],
    'visitante': ['Monaco', 'Lyon', 'Nantes', 'Lens', 'Havre'],
    'fecha': ['2024-01-17', '2024-01-17', '2024-01-18', '2024-01-18', '2024-01-19'],
    'hora': ['18:00', '20:45', '15:00', '18:00', '12:30'],
    'prob_local': [0.45, 0.50, 0.40, 0.55, 0.35],
    'prob_empate': [0.30, 0.25, 0.35, 0.30, 0.30],
    'prob_visitante': [0.25, 0.25, 0.25, 0.15, 0.35],
    'pred_goles_local': [2, 3, 1, 2, 1],
    'pred_goles_visitante': [1, 1, 1, 0, 1]
})

PARTIDOS_BUNDESLIGA = pd.DataFrame({
    'local': ['Bayern Munich', 'Bochum', 'Union Berlin', 'Friburgo', 'Augsburgo'],
    'visitante': ['Borussia Dortmund', 'Mainz', 'RB Leipzig', 'Wolfsburgo', 'Bayer Leverkusen'],
    'fecha': ['2024-01-17', '2024-01-17', '2024-01-18', '2024-01-18', '2024-01-19'],
    'hora': ['18:00', '20:45', '15:00', '18:00', '12:30'],
    'prob_local': [0.45, 0.50, 0.40, 0.55, 0.35],
    'prob_empate': [0.30, 0.25, 0.35, 0.30, 0.30],
    'prob_visitante': [0.25, 0.25, 0.25, 0.15, 0.35],
    'pred_goles_local': [2, 3, 1, 2, 1],
    'pred_goles_visitante': [1, 1, 1, 0, 1]
})


PARTIDOS = {
    "LaLiga": PARTIDOS_LALIGA,
    "Premier League": PARTIDOS_PREMIER,
    "Serie A": PARTIDOS_SERIE_A,
    "Ligue 1": PARTIDOS_LIGUE_1,
    "Bundesliga": PARTIDOS_BUNDESLIGA
}

# Obtener partidos y logos de la liga seleccionada
partidos = PARTIDOS.get(liga_seleccionada, pd.DataFrame())
logos = URL_LOGOS.get(liga_seleccionada, {})

# Función para cargar logo
def cargar_logo(equipo):
    nombre_archivo = equipo.lower().replace(" ", "").replace(".", "").replace("'", "")
    return logos.get(nombre_archivo, None)

# Header principal
st.title(f"Predicciones {liga_seleccionada}")
st.markdown("---")
st.subheader(f"Jornada 20 de 38 - Próximos partidos ({liga_seleccionada})")

# Mostrar los partidos
for idx, partido in partidos.iterrows():
    col1, col2, col3 = st.columns([2, 3, 2])

    with col1:
        logo_local = cargar_logo(partido['local'])
        if logo_local:
            st.image(logo_local, width=100)
        else:
            st.warning(f"Logo no encontrado para: {partido['local']}")

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f"<h2 style='text-align: center;'>{partido['pred_goles_local']} - {partido['pred_goles_visitante']}</h2>",
            unsafe_allow_html=True,
        )
        # Mostrar probabilidades
        col_prob1, col_prob2, col_prob3 = st.columns(3)
        with col_prob1:
            st.metric("Victoria Local", f"{int(partido['prob_local'] * 100)}%")
        with col_prob2:
            st.metric("Empate", f"{int(partido['prob_empate'] * 100)}%")
        with col_prob3:
            st.metric("Victoria Visitante", f"{int(partido['prob_visitante'] * 100)}%")

    with col3:
        logo_visitante = cargar_logo(partido['visitante'])
        if logo_visitante:
            st.image(logo_visitante, width=100)
        else:
            st.warning(f"Logo no encontrado para: {partido['visitante']}")

# Métricas adicionales en el sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Estadísticas del Modelo")
st.sidebar.metric("Precisión Global", "73%")
st.sidebar.metric("Partidos Predichos", "152")

