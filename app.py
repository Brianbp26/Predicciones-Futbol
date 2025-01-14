import streamlit as st
from datetime import datetime
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Predicciones Fútbol",
    page_icon="⚽",
    layout="wide"
)

# URLs de los logos
URL_LOGOS = {
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
    "leganes": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/leganes.png",
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


# Diccionario para mapear nombres de equipos a nombres de archivo
NOMBRES_EQUIPOS = {
    'RCD Espanyol': 'espanyol',
    'Valladolid': 'valladolid',
    'Osasuna': 'osasuna',
    'Rayo Vallecano': 'rayovallecano',
    'Leganés': 'leganes',
    'Atlético Madrid': 'atleticomadrid',
    'Celta de Vigo': 'celta',
    'Athletic': 'athletic',
    'Getafe': 'getafe',
    'Barcelona': 'barcelona',
    'Betis': 'betis',
    'Alavés': 'alaves',
    'Real Madrid': 'realmadrid',
    'U. D. Las Palmas': 'laspalmas',
    'Valencia C. F.': 'valencia',
    'Real Sociedad': 'realsociedad',
    'Girona': 'girona',
    'Sevilla': 'sevilla',
    'Villarreal': 'villarreal',
    'R.C.D. Mallorca': 'mallorca'
}

# Función para cargar logos
def cargar_logo(equipo):
    nombre_archivo = NOMBRES_EQUIPOS.get(equipo, equipo.lower().replace(' ', ''))
    return URL_LOGOS.get(nombre_archivo, None)

# Datos de ejemplo con los partidos de la jornada 20
partidos_ejemplo = pd.DataFrame({
    'local': ['RCD Espanyol', 'Osasuna', 'Leganés', 'Celta de Vigo', 
              'Getafe', 'Betis', 'Real Madrid', 'Valencia C. F.', 
              'Girona', 'Villarreal'],
    'visitante': ['Valladolid', 'Rayo Vallecano', 'Atlético Madrid', 'Athletic',
                  'Barcelona', 'Alavés', 'U. D. Las Palmas', 'Real Sociedad',
                  'Sevilla', 'R.C.D. Mallorca'],
    'fecha': ['2024-01-17', '2024-01-18', '2024-01-18', '2024-01-18',
              '2024-01-18', '2024-01-19', '2024-01-19', '2024-01-19',
              '2024-01-19', '2024-01-20'],
    'hora': ['21:00', '14:00', '16:15', '18:30',
             '21:00', '14:00', '16:15', '18:30',
             '21:00', '21:00'],
    'prob_local': [0.35, 0.40, 0.30, 0.35,
                   0.25, 0.45, 0.60, 0.40,
                   0.45, 0.50],
    'prob_empate': [0.30, 0.30, 0.35, 0.30,
                    0.25, 0.30, 0.25, 0.30,
                    0.30, 0.30],
    'prob_visitante': [0.35, 0.30, 0.35, 0.35,
                       0.50, 0.25, 0.15, 0.30,
                       0.25, 0.20],
    'pred_goles_local': [1, 2, 1, 1,
                         1, 2, 3, 2,
                         2, 2],
    'pred_goles_visitante': [1, 1, 2, 1,
                            2, 0, 0, 1,
                            1, 0]
})

# Header principal
st.title("⚽ Predicciones Fútbol")
st.markdown("---")
st.subheader("Jornada 20 de 38 - Próximos partidos")

# Mostrar los partidos
for idx, partido in partidos_ejemplo.iterrows():
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
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

# Métricas adicionales en el sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Estadísticas del Modelo")
st.sidebar.metric("Precisión Global", "73%")
st.sidebar.metric("Partidos Predichos", "152")
