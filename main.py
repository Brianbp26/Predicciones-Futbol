pip install scikit-learn
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os
import glob
def load_data(ruta):
    """
    Carga los datos desde archivos CSV de La Liga
    """
    archivos = glob.glob(ruta)
    
    if not archivos:
        raise ValueError(f"No se encontraron archivos en la ruta: {ruta}")
    
    print(f"Archivos encontrados: {archivos}")
    
    dataframes = []
    for f in archivos:
        try:
            temp = pd.read_csv(f, usecols=range(22))
            años = os.path.basename(f).split('_')[1]
            temp['Temporada'] = '20' + años
            dataframes.append(temp)
        except Exception as e:
            print(f"Error al procesar archivo {f}: {str(e)}")
    
    if not dataframes:
        raise ValueError("No se pudo cargar ningún archivo correctamente")
    
    return pd.concat(dataframes, ignore_index=True)

def prepare_data_for_model(df):
    """
    Prepara los datos para el modelo incluyendo todas las variables relevantes
    """
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    
    match_features = []
    results = []
    
    for index, match in df.iterrows():
        # Datos históricos hasta la fecha del partido
        historical_data = df[df['Date'] < match['Date']]
        
        if len(historical_data) < 10:  # Necesitamos suficientes datos históricos
            continue
            
        home_team = match['HomeTeam']
        away_team = match['AwayTeam']
        
        # 1. FORMA RECIENTE (últimos 5 partidos)
        home_last5 = historical_data[
            (historical_data['HomeTeam'] == home_team) | 
            (historical_data['AwayTeam'] == home_team)
        ].tail(5)
        
        away_last5 = historical_data[
            (historical_data['HomeTeam'] == away_team) | 
            (historical_data['AwayTeam'] == away_team)
        ].tail(5)
        
        # 2. HISTORIAL DE LA TEMPORADA
        current_season = historical_data[historical_data['Temporada'] == match['Temporada']]
        home_season = current_season[
            (current_season['HomeTeam'] == home_team) | 
            (current_season['AwayTeam'] == home_team)
        ]
        away_season = current_season[
            (current_season['HomeTeam'] == away_team) | 
            (current_season['AwayTeam'] == away_team)
        ]
        
        # 3. ENFRENTAMIENTOS DIRECTOS (últimos 3 años)
        h2h_matches = historical_data[
            ((historical_data['HomeTeam'] == home_team) & (historical_data['AwayTeam'] == away_team)) |
            ((historical_data['HomeTeam'] == away_team) & (historical_data['AwayTeam'] == home_team))
        ].tail(6)  # Últimos 6 enfrentamientos

        # Calcular victorias y empates primero
        home_last5_wins = sum((home_last5['HomeTeam'] == home_team) & (home_last5['FTR'] == 'H') |
                             (home_last5['AwayTeam'] == home_team) & (home_last5['FTR'] == 'A'))
        home_last5_draws = sum(home_last5['FTR'] == 'D')
        away_last5_wins = sum((away_last5['HomeTeam'] == away_team) & (away_last5['FTR'] == 'H') |
                             (away_last5['AwayTeam'] == away_team) & (away_last5['FTR'] == 'A'))
        away_last5_draws = sum(away_last5['FTR'] == 'D')
        
        features = {
            # FORMA RECIENTE (últimos 5 partidos)
            'home_last5_wins': home_last5_wins,
            'home_last5_draws': home_last5_draws,
            'home_last5_losses': 5 - (home_last5_wins + home_last5_draws),
            
            'home_last5_goals_scored': sum(
                (home_last5['HomeTeam'] == home_team) * home_last5['FTHG'] +
                (home_last5['AwayTeam'] == home_team) * home_last5['FTAG']
            ) / len(home_last5) if len(home_last5) > 0 else 0,
            
            'home_last5_goals_conceded': sum(
                (home_last5['HomeTeam'] == home_team) * home_last5['FTAG'] +
                (home_last5['AwayTeam'] == home_team) * home_last5['FTHG']
            ) / len(home_last5) if len(home_last5) > 0 else 0,
            
            # Lo mismo para el equipo visitante
            'away_last5_wins': away_last5_wins,
            'away_last5_draws': away_last5_draws,
            'away_last5_losses': 5 - (away_last5_wins + away_last5_draws),
            
            # ESTADÍSTICAS DE LA TEMPORADA
            'home_season_wins': sum((home_season['HomeTeam'] == home_team) & (home_season['FTR'] == 'H') |
                                  (home_season['AwayTeam'] == home_team) & (home_season['FTR'] == 'A')),
            
            'home_season_goals_per_game': sum(
                (home_season['HomeTeam'] == home_team) * home_season['FTHG'] +
                (home_season['AwayTeam'] == home_team) * home_season['FTAG']
            ) / len(home_season) if len(home_season) > 0 else 0,
            
            # ENFRENTAMIENTOS DIRECTOS
            'h2h_home_wins': sum((h2h_matches['HomeTeam'] == home_team) & (h2h_matches['FTR'] == 'H')),
            'h2h_away_wins': sum((h2h_matches['HomeTeam'] == away_team) & (h2h_matches['FTR'] == 'H')),
            'h2h_draws': sum(h2h_matches['FTR'] == 'D'),
            
            # ESTADÍSTICAS DE TIROS Y CORNERS
            'home_season_shots_avg': sum(
                (home_season['HomeTeam'] == home_team) * home_season['HS'] +
                (home_season['AwayTeam'] == home_team) * home_season['AS']
            ) / len(home_season) if len(home_season) > 0 else 0,
            
            'home_season_corners_avg': sum(
                (home_season['HomeTeam'] == home_team) * home_season['HC'] +
                (home_season['AwayTeam'] == home_team) * home_season['AC']
            ) / len(home_season) if len(home_season) > 0 else 0,
            
            # ESTADÍSTICAS DEFENSIVAS
            'home_season_conceded_avg': sum(
                (home_season['HomeTeam'] == home_team) * home_season['FTAG'] +
                (home_season['AwayTeam'] == home_team) * home_season['FTHG']
            ) / len(home_season) if len(home_season) > 0 else 0,
            
            # FACTOR LOCAL/VISITANTE
            'home_home_wins': sum((home_season['HomeTeam'] == home_team) & (home_season['FTR'] == 'H')),
            'away_away_wins': sum((away_season['AwayTeam'] == away_team) & (away_season['FTR'] == 'A')),
        }
        
        match_features.append(features)
        # Convertir resultado (0: Away, 1: Draw, 2: Home)
        result = 0 if match['FTR'] == 'A' else (1 if match['FTR'] == 'D' else 2)
        results.append(result)
    
    return pd.DataFrame(match_features), np.array(results)

def train_model(df):
    """
    Prepara los datos y entrena el modelo
    """
    X, y = prepare_data_for_model(df)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        random_state=42
    )
    
    model.fit(X_train_scaled, y_train)
    
    train_score = model.score(X_train_scaled, y_train)
    test_score = model.score(X_test_scaled, y_test)
    
    return model, scaler, train_score, test_score

def prepare_new_match_data(df, home_team, away_team, match_date):
    """
    Prepara los datos para un nuevo partido
    """
    # Convertir fecha a datetime si es string
    if isinstance(match_date, str):
        match_date = pd.to_datetime(match_date)
        
    # Crear un DataFrame con un solo partido
    new_match = pd.DataFrame({
        'Date': [match_date],
        'HomeTeam': [home_team],
        'AwayTeam': [away_team],
        'Temporada': [str(match_date.year)],
        'FTR': ['H']  # Valor temporal, no afecta la predicción
    })
    
    # Concatenar con datos históricos
    df_with_new = pd.concat([df, new_match], ignore_index=True)
    
    # Preparar datos
    X, _ = prepare_data_for_model(df_with_new)
    
    # Devolver solo la última fila (el nuevo partido)
    return X[-1:] if len(X) > 0 else None

def predict_match(model, scaler, features):
    """
    Hace la predicción para un partido
    """
    if features is None:
        raise ValueError("No se pudieron preparar las características del partido")
        
    # Escalar características
    features_scaled = scaler.transform(features)
    
    # Obtener probabilidades
    probabilities = model.predict_proba(features_scaled)[0]
    
    return {
        'away_win': probabilities[0],
        'draw': probabilities[1],
        'home_win': probabilities[2]
    }
    
