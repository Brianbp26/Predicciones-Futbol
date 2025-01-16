import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
from datos import obtener_clasificacion, mostrar_clasificacion, obtener_partidos, mostrar_partidos
from main import predict_match, load_data, predict_match_score
st.set_page_config(
    page_title="Predicciones Fútbol",
    page_icon="⚽",
    layout="wide"
)

st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #000000;  /* Set the background color to black */
    }
    .main {
        background-color: #000000;  /* Set the background color to black */
        color: #ffffff;
    }
    .css-18e3th9 {
        background-color: #000000;  /* Set the background color to black */
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
    
# Diccionario de logos de ligas
logos_ligas = {
    "LaLiga": "https://raw.githubusercontent.com/Brianbp26/Logos/d6015e93917a71eee579fca028b9e03c5cfe0067/laliga.png",
    "Premier League": "https://raw.githubusercontent.com/Brianbp26/Logos/038dae8a150d6cd90da2c99b08c461f3887b6095/premier.png",
    "Serie A": "https://raw.githubusercontent.com/Brianbp26/Logos/d6015e93917a71eee579fca028b9e03c5cfe0067/serie a.png",
    "Bundesliga": "https://raw.githubusercontent.com/Brianbp26/Logos/d6015e93917a71eee579fca028b9e03c5cfe0067/bundesliga.png",
    "Ligue 1": "https://raw.githubusercontent.com/Brianbp26/Logos/59347f45da1c564258e4e9084414772207443bbd/ligue 1.png",
}

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
    "realvalladolidcf": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/valladolid.png",
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
       "atalantabc": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/atalanta.png",
        "bolognafc1909": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/bolonia.png",
        "cagliaricalcio": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/cagliari.png",
        "empolifc": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/empoli.png",
        "acffiorentina": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/fiorentina.png",
        "hellasveronafc": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/hellasverona.png",
        "genoacfc": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/genoa.png",
        "fcinternazionalemilano": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/inter.png",
        "juventusfc": "https://raw.githubusercontent.com/Brianbp26/Logos/287c42548bfa091d3763008fa5060db5485242fb/juventus.png",
        "sslazio": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/lazio.png",
        "uslecce": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/lecce.png",
        "acmilan": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/milan.png",
        "acmonza": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/monza.png",
        "sscnapoli": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/napoles.png",
        "asroma": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/roma.png",
        "parmacalcio1913": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/parma.png",
        "como1907": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/como.png",
        "torinofc": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/torino.png",
        "udinesecalcio": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/udinese.png",
        "veneziafc": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/venezia.png"
        },
    "Bundesliga": {
        "fcaugsburg": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/augsburgo.png",
        "bayer04leverkusen": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/bayerleverkusen.png",
        "fcbayernmünchen": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/bayernmunich.png",
        "vflbochum1848": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/bochum.png",
        "borussiadortmund": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/borussiadortmund.png",
        "borussiamönchengladbach": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/borussiamgladbach.png",
        "eintrachtfrankfurt": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/eintrachtfrankfurt.png",
        "scfreiburg": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/friburgo.png",
        "1.fcheidenheim1846": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/heidenheim.png",
        "tsg1899hoffenheim": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/hoffenheim.png",
        "holsteinkiel": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/holsteinkiel.png",
        "1.fsvmainz05": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/mainz.png",
        "rbleipzig": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/rbleipzig.png",
        "fcst.pauli1910": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/st_pauli.png",
        "vfbstuttgart": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/stuttgart.png",
        "1.fcunionberlin": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/unionberlin.png",
        "svwerderbremen": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/werderbremen.png",
        "vflwolfsburg": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/wolfsburgo.png"
        },
    "Ligue 1": {
        "angerssco": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/angers.png",
        "ajauxerre": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/auxerre.png",
        "rcstrasbourgalsace": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/estrasburgo.png",
        "lehavreac": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/havre.png",
        "racingclubdelens": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/lens.png",
        "lilleosc": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/lille.png",
        "olympiquelyonnais": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/lyon.png",
        "olympiquedemarseille": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/marsella.png",
        "asmonacofc": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/monaco.png",
        "montpellierhsc": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/montpellier.png",
        "fcnantes": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/nantes.png",
        "ogcnice": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/niza.png",
        "parissaint-germainfc": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/psg.png",
        "assaint-étienne": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/saintetienne.png",
        "stadebrestois29": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/stadebretois.png",
        "stadedereims": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/stadereims.png",
        "staderennaisfc1901": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/staderennais.png",
        "toulousefc": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/toulouse.png"
        }
}

liga_ids = {
    "LaLiga": "PD",  # Primera División Española
    "Premier League": "PL",  # Premier League
    "Serie A": "SA",  # Serie A
    "Bundesliga": "BL1",  # Bundesliga
    "Ligue 1": "FL1"  # Ligue 1
}
liga_archivos = {
    "LaLiga": "España/LaLigaEASPORTS",  # Primera División Española
    "Premier League": "Inglaterra/PremierLeague",  # Premier League
    "Serie A": "Italia/SerieA",  # Serie A
    "Bundesliga": "Alemania/Bundesliga",  # Bundesliga
    "Ligue 1": "Francia/Ligue1"  # Ligue 1
}
# Header principal con logo de la liga
st.markdown(f"""
<div style="display: flex; align-items: center; gap: 1rem;">
    <h1 style="margin: 0;">Predicciones {liga_seleccionada}</h1>
    <img src="{logos_ligas[liga_seleccionada]}" alt="{liga_seleccionada}" style="width: 50px; height: 50px;">
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# Diccionario de mapeo de nombres de equipos
mapeo_equipos = {
    "newcastleunitedfc": "Newcastle",
    "afcbournemouth": "Bournemouth",
    "arsenalfc": "Arsenal",
    "astonvillafc": "Aston Villa",
    "brentfordfc": "Brentford",
    "brighton&hovealbionfc": "Brighton",
    "chelseafc": "Chelsea",
    "crystalpalacefc": "Crystal Palace",
    "evertonfc": "Everton",
    "ipswichtownfc": "Ipswich",
    "nottinghamforestfc": "Nott'm Forest",
    "fulhamfc": "Fulham",
    "leicestercityfc": "Leicester",
    "liverpoolfc": "Liverpool",
    "manchesterunitedfc": "Man United",
    "manchestercityfc": "Man City",
    "southamptonfc": "Southampton",
    "tottenhamhotspurfc": "Tottenham",
    "westhamunitedfc": "West Ham",
    "wolverhamptonwanderersfc": "Wolves",
    "athleticclub": "Ath Bilbao",
    "clubatléticodemadrid": "Ath Madrid",
    "fcbarcelona": "Barcelona",
    "deportivoalavés": "Alaves",
    "realbetisbalompié": "Betis",
    "rcceltadevigo": "Celta",
    "rcdespanyoldebarcelona": "Espanol",
    "getafecf": "Getafe",
    "gironafc": "Girona",
    "udlaspalmas": "Las Palmas",
    "cdleganés": "Leganes",
    "rcdmallorca": "Mallorca",
    "caosasuna": "Osasuna",
    "rayovallecanodemadrid": "Vallecano",
    "realmadridcf": "Real Madrid",
    "realsociedaddefútbol": "Sociedad",
    "sevillafc": "Sevilla",
    "valenciacf": "Valencia",
    "realvalladolidcf": "Valladolid",
    "villarrealcf": "Villarreal",
    "atalantabc": "Atalanta",
    "bolognafc1909": "Bologna",
    "cagliaricalcio": "Cagliari",
    "empolifc": "Empoli",
    "acffiorentina": "Fiorentina",
    "hellasveronafc": "Verona",
    "genoacfc": "Genoa",
    "fcinternazionalemilano": "Inter",
    "juventusfc": "Juventus",
    "sslazio": "Lazio",
    "uslecce": "Lecce",
    "acmilan": "Milan",
    "acmonza": "Monza",
    "sscnapoli": "Napoli",
    "asroma": "Roma",
    "parmacalcio1913": "Parma",
    "como1907": "Como",
    "torinofc": "Torino",
    "udinesecalcio": "Udinese",
    "veneziafc": "Venezia",
    "fcaugsburg": "Augsburg",
    "bayer04leverkusen": "Leverkusen",
    "fcbayernmünchen": "Bayern Munich",
    "vflbochum1848": "Bochum",
    "borussiadortmund": "Dortmund",
    "borussiamönchengladbach": "M'gladbach",
    "eintrachtfrankfurt": "Ein Frankfurt",
    "scfreiburg": "Freiburg",
    "1.fcheidenheim1846": "Heidenheim",
    "tsg1899hoffenheim": "Hoffenheim",
    "holsteinkiel": "Holstein Kiel",
    "1.fsvmainz05": "Mainz",
    "rbleipzig": "RB Leipzig",
    "fcst.pauli1910": "St Pauli",
    "vfbstuttgart": "Stuttgart",
    "1.fcunionberlin": "Union Berlin",
    "svwerderbremen": "Werder Bremen",
    "vflwolfsburg": "Wolfsburg",
    "angerssco": "Angers",
    "ajauxerre": "Auxerre",
    "rcstrasbourgalsace": "Strasbourg",
    "lehavreac": "Le Havre",
    "racingclubdelens": "Lens",
    "lilleosc": "Lille",
    "olympiquelyonnais": "Lyon",
    "olympiquedemarseille": "Marseille",
    "asmonacofc": "Monaco",
    "montpellierhsc": "Montpellier",
    "fcnantes": "Nantes",
    "ogcnice": "Nice",
    "parissaint-germainfc": "Paris SG",
    "assaint-étienne": "St Etienne",
    "stadebrestois29": "Brest",
    "stadedereims": "Reims",
    "staderennaisfc1901": "Rennes",
    "toulousefc": "Toulouse" }

def estandarizar_nombre_equipo(nombre_equipo):
    equipo = nombre_equipo.lower().replace(" ", "")
    return mapeo_equipos.get(equipo)

# Función para cargar datos históricos según la liga seleccionada
@st.cache_resource
def cargar_datos_historicos(liga_seleccionada):
    base_path = liga_archivos.get(liga_seleccionada, "")
    datos_historicos_ruta = f"archivos/{base_path}_*_*.csv"
    print(f"Buscando archivos en la ruta: {datos_historicos_ruta}")
    return load_data(datos_historicos_ruta)

if liga_seleccionada:
    liga_id = liga_ids.get(liga_seleccionada)
    if liga_id:
        clasificacion = obtener_clasificacion(liga_id)
        mostrar_clasificacion(clasificacion, liga_seleccionada, logos)

        df_historico = cargar_datos_historicos(liga_seleccionada)

        # Obtener los partidos y hacer predicciones
        partidos = obtener_partidos(liga_id)
        st.markdown("## 🎲 Predicciones próximos partidos")

        for partido in partidos:
            home_team = estandarizar_nombre_equipo(partido['homeTeam']['name'])
            away_team = estandarizar_nombre_equipo(partido['awayTeam']['name'])
            
            # Mostrar los partidos de la jornada
            mostrar_partidos([partido], liga_seleccionada, logos)
            
            try:
                home_score, away_score = predict_match_score(df_historico, home_team, away_team)
                prediccion = predict_match(df_historico, home_team, away_team)
                if prediccion:
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.markdown(f"""
                        <div style='background-color: #1e272e; padding: 20px; border-radius: 10px; margin: 10px 0; color: white;'>
                            <h3 style='text-align: center;'>{partido['homeTeam']['name']} vs {partido['awayTeam']['name']}</h3>
                            <div style='display: flex; justify-content: space-between; margin: 20px 0;'>
                                <div style='text-align: center; width: 30%;'>
                                    <p>Victoria Local</p>
                                    <h2>{prediccion['probabilidades']['victoria_local']}</h2>
                                </div>
                                <div style='text-align: center; width: 30%;'>
                                    <p>Empate</p>
                                    <h2>{prediccion['probabilidades']['empate']}</h2>
                                </div>
                                <div style='text-align: center; width: 30%;'>
                                    <p>Victoria Visitante</p>
                                    <h2>{prediccion['probabilidades']['victoria_visitante']}</h2>
                                </div>
                            </div>
                            <div style='text-align: center; margin-top: 20px;'>
                                <p>Marcador Predicho</p>
                                <h2>{home_score} - {away_score}</h2>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning(f"No se pudo generar predicción para {partido['homeTeam']['name']} vs {partido['awayTeam']['name']}")
            except Exception as e:
                st.error(f"Error al procesar predicción: {str(e)}")



        







        




        




        







        








        







        








        







        




        




        







        








        







        






        







        




        




        







        








        







        




