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
    "leicester": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/leicester.png",
    "liverpool": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/liverpool.png",
    "manunited": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/manunited.png",
    "mancity": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/mancity.png",
    "southampton": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/southampton.png",
    "tottenham": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/tottenham.png",
    "westham": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/westham.png",
    "wolverhampton": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/wolverhampton.png"
}


URL_LOGOS = {
    "LaLiga": URL_LOGOS_LALIGA,
    "Premier League": URL_LOGOS_PREMIER,
    # Agrega más ligas aquí
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

PARTIDOS = {
    "LaLiga": PARTIDOS_LALIGA,
    "Premier League": PARTIDOS_PREMIER,
    # Agrega más ligas aquí
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

