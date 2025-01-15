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

def calcular_posicion_tabla(df, equipo):
    """
    Calcula la posición en la tabla de un equipo para la temporada actual
    """
    ultima_temporada = df['Temporada'].max()
    partidos_temporada = df[df['Temporada'] == ultima_temporada]
    
    if partidos_temporada.empty:
        return 10  # Posición media por defecto
    
    equipos_stats = partidos_temporada.groupby('HomeTeam').agg({
        'FTHG': 'sum', 'FTAG': 'sum'
    }).rename(columns={'FTHG': 'gf', 'FTAG': 'gc'}).add(
        partidos_temporada.groupby('AwayTeam').agg({
            'FTAG': 'sum', 'FTHG': 'sum'
        }).rename(columns={'FTAG': 'gf', 'FTHG': 'gc'}), fill_value=0
    )
    
    equipos_stats['puntos'] = partidos_temporada.apply(lambda x: 3 if x['FTR'] == 'H' else (3 if x['FTR'] == 'A' else 1), axis=1).groupby(partidos_temporada[['HomeTeam', 'AwayTeam']].stack()).sum(level=0).reindex(equipos_stats.index, fill_value=0)
    
    tabla = equipos_stats.sort_values(by=['puntos', 'gf', 'gc'], ascending=[False, False, True]).reset_index()
    
    return tabla.index[tabla['index'] == equipo][0] + 1 if equipo in tabla['index'].values else 10

def prepare_data_for_model(df, home_team, away_team):
    """
    Prepara los datos para el modelo usando todas las temporadas con ponderación
    """
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date']).sort_values('Date')
    
    temporadas = sorted(df['Temporada'].unique())
    num_temporadas = len(temporadas)
    pesos_temporadas = {temp: 1 - (0.8 * (num_temporadas - i - 1) / (num_temporadas - 1)) for i, temp in enumerate(temporadas)}
    
    stats = {
        'home_wins': 0, 'home_draws': 0, 'home_losses': 0,
        'away_wins': 0, 'away_draws': 0, 'away_losses': 0,
        'home_goals_scored': 0, 'home_goals_conceded': 0,
        'away_goals_scored': 0, 'away_goals_conceded': 0,
        'h2h_matches': 0, 'h2h_home_wins': 0, 'h2h_away_wins': 0, 'h2h_draws': 0
    }
    
    for temporada in temporadas:
        peso = pesos_temporadas[temporada]
        df_temp = df[df['Temporada'] == temporada]
        
        home_local = df_temp[df_temp['HomeTeam'] == home_team]
        stats['home_wins'] += peso * sum(home_local['FTR'] == 'H')
        stats['home_draws'] += peso * sum(home_local['FTR'] == 'D')
        stats['home_losses'] += peso * sum(home_local['FTR'] == 'A')
        stats['home_goals_scored'] += peso * home_local['FTHG'].mean() if len(home_local) > 0 else 0
        stats['home_goals_conceded'] += peso * home_local['FTAG'].mean() if len(home_local) > 0 else 0
        
        away_visit = df_temp[df_temp['AwayTeam'] == away_team]
        stats['away_wins'] += peso * sum(away_visit['FTR'] == 'A')
        stats['away_draws'] += peso * sum(away_visit['FTR'] == 'D')
        stats['away_losses'] += peso * sum(away_visit['FTR'] == 'H')
        stats['away_goals_scored'] += peso * away_visit['FTAG'].mean() if len(away_visit) > 0 else 0
        stats['away_goals_conceded'] += peso * away_visit['FTHG'].mean() if len(away_visit) > 0 else 0
        
        h2h_matches = df_temp[((df_temp['HomeTeam'] == home_team) & (df_temp['AwayTeam'] == away_team)) | ((df_temp['HomeTeam'] == away_team) & (df_temp['AwayTeam'] == home_team))]
        if len(h2h_matches) > 0:
            stats['h2h_matches'] += peso * len(h2h_matches)
            stats['h2h_home_wins'] += peso * sum((h2h_matches['HomeTeam'] == home_team) & (h2h_matches['FTR'] == 'H'))
            stats['h2h_away_wins'] += peso * sum((h2h_matches['HomeTeam'] == away_team) & (h2h_matches['FTR'] == 'H'))
            stats['h2h_draws'] += peso * sum(h2h_matches['FTR'] == 'D')
    
    ultimos_partidos_home = df[(df['HomeTeam'] == home_team) | (df['AwayTeam'] == home_team)].tail(5)
    ultimos_partidos_away = df[(df['HomeTeam'] == away_team) | (df['AwayTeam'] == away_team)].tail(5)
    
    features = {
        'home_position': calcular_posicion_tabla(df, home_team),
        'away_position': calcular_posicion_tabla(df, away_team),
        'home_historical_wins_weighted': stats['home_wins'],
        'home_historical_draws_weighted': stats['home_draws'],
        'home_historical_losses_weighted': stats['home_losses'],
        'away_historical_wins_weighted': stats['away_wins'],
        'away_historical_draws_weighted': stats['away_draws'],
        'away_historical_losses_weighted': stats['away_losses'],
        'home_historical_goals_scored_weighted': stats['home_goals_scored'],
        'home_historical_goals_conceded_weighted': stats['home_goals_conceded'],
        'away_historical_goals_scored_weighted': stats['away_goals_scored'],
        'away_historical_goals_conceded_weighted': stats['away_goals_conceded'],
        'h2h_home_wins_weighted': stats['h2h_home_wins'],
        'h2h_away_wins_weighted': stats['h2h_away_wins'],
        'h2h_draws_weighted': stats['h2h_draws'],
        'h2h_total_matches': stats['h2h_matches'],
        'home_last5_wins': sum((ultimos_partidos_home['HomeTeam'] == home_team) & (ultimos_partidos_home['FTR'] == 'H') | (ultimos_partidos_home['AwayTeam'] == home_team) & (ultimos_partidos_home['FTR'] == 'A')),
        'home_last5_draws': sum(ultimos_partidos_home['FTR'] == 'D'),
        'away_last5_wins': sum((ultimos_partidos_away['HomeTeam'] == away_team) & (ultimos_partidos_away['FTR'] == 'H') | (ultimos_partidos_away['AwayTeam'] == away_team) & (ultimos_partidos_away['FTR'] == 'A')),
        'away_last5_draws': sum(ultimos_partidos_away['FTR'] == 'D')
    }
    
    features['home_last5_losses'] = 5 - (features['home_last5_wins'] + features['home_last5_draws'])
    features['away_last5_losses'] = 5 - (features['away_last5_wins'] + features['away_last5_draws'])
    
    return pd.DataFrame([features])

def train_model(df, home_team, away_team):
    features_list = []
    results = []

    temporadas = sorted(df['Temporada'].unique())
    df_equipos = df[((df['HomeTeam'] == home_team) | (df['AwayTeam'] == home_team) | (df['HomeTeam'] == away_team) | (df['AwayTeam'] == away_team))]
    
    for idx, partido in df_equipos[df_equipos['Temporada'] != temporadas[0]].iterrows():
        temporada_actual = partido['Temporada']
        temporadas_anteriores = [t for t in temporadas if t < temporada_actual]
        if not temporadas_anteriores:
            continue
        df_hasta_temporada = df_equipos[df_equipos['Temporada'].isin(temporadas_anteriores)]
        
        try:
            features = prepare_data_for_model(df_hasta_temporada, partido['HomeTeam'], partido['AwayTeam'])
            if features is not None and not features.empty:
                features_list.append(features)
                result = 0 if partido['FTR'] == 'A' else (1 if partido['FTR'] == 'D' else 2)
                results.append(result)
        except Exception as e:
            print(f"Error procesando partido de temporada {temporada_actual}: {e}")
            continue
    
    if not features_list:
        raise ValueError("No se pudieron generar suficientes datos para entrenar el modelo")
    
    X = pd.concat(features_list, ignore_index=True)
    y = np.array(results)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = RandomForestClassifier(n_estimators=300, max_depth=20, min_samples_split=8, min_samples_leaf=4, class_weight='balanced', random_state=42, n_jobs=-1)
    model.fit(X_train_scaled, y_train)
    
    train_score = model.score(X_train_scaled, y_train)
    test_score = model.score(X_test_scaled, y_test)
    
    feature_importance = pd.DataFrame({'feature': X.columns, 'importance': model.feature_importances_}).sort_values('importance', ascending=False)
    
    return model, scaler, train_score, test_score

def prepare_new_match_data(df, home_team, away_team, match_date):
    """
    Prepara los datos para un nuevo partido
    """
    if isinstance(match_date, str):
        match_date = pd.to_datetime(match_date)
        
    new_match = pd.DataFrame({'Date': [match_date], 'HomeTeam': [home_team], 'AwayTeam': [away_team], 'Temporada': [str(match_date.year)], 'FTR': ['H']})
    df_with_new = pd.concat([df, new_match], ignore_index=True)
    
    X, _ = prepare_data_for_model(df_with_new)
    return X[-1:] if len(X) > 0 else None

def predict_match(df, home_team, away_team):
    """
    Entrena el modelo para los equipos específicos y predice el resultado del partido.
    """
    try:
        model, scaler, train_score, test_score = train_model(df, home_team, away_team)
        current_features = prepare_data_for_model(df, home_team, away_team)
        
        if current_features is None:
            raise ValueError("No se pudieron preparar las características del partido")
        
        features_scaled = scaler.transform(current_features)
        probabilities = model.predict_proba(features_scaled)[0]
        
        resultado_idx = probabilities.argmax()
        resultados = ['Victoria Visitante', 'Empate', 'Victoria Local']
        resultado_probable = resultados[resultado_idx]
        
        prediccion = {
            'probabilidades': {
                'victoria_local': f"{probabilities[2]*100:.1f}%",
                'empate': f"{probabilities[1]*100:.1f}%",
                'victoria_visitante': f"{probabilities[0]*100:.1f}%"
            },
            'resultado_mas_probable': resultado_probable,
            'confianza_prediccion': f"{probabilities[resultado_idx]*100:.1f}%",
            'metricas_modelo': {
                'score_entrenamiento': f"{train_score:.3f}",
                'score_test': f"{test_score:.3f}"
            }
        }
        
        print(f"\nPredicción para {home_team} vs {away_team}:")
        print(f"Victoria {home_team}: {prediccion['probabilidades']['victoria_local']}")
        print(f"Empate: {prediccion['probabilidades']['empate']}")
        print(f"Victoria {away_team}: {prediccion['probabilidades']['victoria_visitante']}")
        
        return prediccion
        
    except Exception as e:
        print(f"Error al realizar la predicción: {e}")
        return None
    
