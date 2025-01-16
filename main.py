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
    # Obtener la temporada más reciente
    ultima_temporada = df['Temporada'].max()
    
    # Filtrar solo los partidos de la temporada actual
    partidos_temporada = df[df['Temporada'] == ultima_temporada]
    
    if len(partidos_temporada) == 0:
        return 10  # Posición media por defecto
        
    equipos_stats = {}
    
    # Inicializar estadísticas para todos los equipos
    equipos = set(partidos_temporada['HomeTeam'].unique()) | set(partidos_temporada['AwayTeam'].unique())
    for eq in equipos:
        equipos_stats[eq] = {'puntos': 0, 'gf': 0, 'gc': 0}
    
    # Calcular estadísticas
    for _, partido in partidos_temporada.iterrows():
        # Actualizar goles
        equipos_stats[partido['HomeTeam']]['gf'] += partido['FTHG']
        equipos_stats[partido['HomeTeam']]['gc'] += partido['FTAG']
        equipos_stats[partido['AwayTeam']]['gf'] += partido['FTAG']
        equipos_stats[partido['AwayTeam']]['gc'] += partido['FTHG']
        
        # Actualizar puntos
        if partido['FTR'] == 'H':
            equipos_stats[partido['HomeTeam']]['puntos'] += 3
        elif partido['FTR'] == 'A':
            equipos_stats[partido['AwayTeam']]['puntos'] += 3
        else:
            equipos_stats[partido['HomeTeam']]['puntos'] += 1
            equipos_stats[partido['AwayTeam']]['puntos'] += 1
    
    # Ordenar equipos por puntos y diferencia de goles
    tabla = sorted(equipos_stats.items(), 
                  key=lambda x: (x[1]['puntos'], x[1]['gf'] - x[1]['gc'], x[1]['gf']), 
                  reverse=True)
    
    # Encontrar posición del equipo
    for pos, (team, _) in enumerate(tabla, 1):
        if team == equipo:
            return pos
    
    return 10  # Posición media por defecto si no se encuentra

def prepare_data_for_model(df, home_team, away_team):
    """
    Prepara los datos para el modelo usando todas las temporadas con ponderación.
    Da mayor peso a la forma actual y posición en la tabla.
    """
    # Convertir fechas
    date_formats = ["%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d"]
    for fmt in date_formats:
        try:
            df.loc[:, 'Date'] = pd.to_datetime(df['Date'], format=fmt, errors='coerce')
            break
        except ValueError:
            continue
    else:
        df.loc[:, 'Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')

    df = df.dropna(subset=['Date']).copy()
    df = df.sort_values('Date').copy()

    # Obtener temporadas ordenadas
    temporadas = sorted(df['Temporada'].unique())
    num_temporadas = len(temporadas)

    # Reducir el peso de temporadas antiguas (0.6 en lugar de 0.8 para dar más peso a datos recientes)
    pesos_temporadas = {temp: 1 - (0.6 * (num_temporadas - i - 1) / (num_temporadas - 1)) 
                        for i, temp in enumerate(temporadas)}

    # Inicializar estadísticas
    stats = {
        'home_wins': 0,
        'home_draws': 0,
        'home_losses': 0,
        'away_wins': 0,
        'away_draws': 0,
        'away_losses': 0,
        'home_goals_scored': 0,
        'home_goals_conceded': 0,
        'away_goals_scored': 0,
        'away_goals_conceded': 0,
        'h2h_matches': 0,
        'h2h_home_wins': 0,
        'h2h_away_wins': 0,
        'h2h_draws': 0
    }

    # Calcular estadísticas ponderadas por temporada
    for temporada in temporadas:
        peso = pesos_temporadas[temporada]
        df_temp = df[df['Temporada'] == temporada].copy()

        try:
            # Partidos como local del equipo local
            home_local = df_temp[df_temp['HomeTeam'] == home_team].copy()
            stats['home_wins'] += peso * sum(home_local['FTR'] == 'H')
            stats['home_draws'] += peso * sum(home_local['FTR'] == 'D')
            stats['home_losses'] += peso * sum(home_local['FTR'] == 'A')
            stats['home_goals_scored'] += peso * home_local['FTHG'].mean() if len(home_local) > 0 else 0
            stats['home_goals_conceded'] += peso * home_local['FTAG'].mean() if len(home_local) > 0 else 0

            # Partidos como visitante del equipo visitante
            away_visit = df_temp[df_temp['AwayTeam'] == away_team].copy()
            stats['away_wins'] += peso * sum(away_visit['FTR'] == 'A')
            stats['away_draws'] += peso * sum(away_visit['FTR'] == 'D')
            stats['away_losses'] += peso * sum(away_visit['FTR'] == 'H')
            stats['away_goals_scored'] += peso * away_visit['FTAG'].mean() if len(away_visit) > 0 else 0
            stats['away_goals_conceded'] += peso * away_visit['FTHG'].mean() if len(away_visit) > 0 else 0

            # Enfrentamientos directos
            h2h_matches = df_temp[
                ((df_temp['HomeTeam'] == home_team) & (df_temp['AwayTeam'] == away_team)) |
                ((df_temp['HomeTeam'] == away_team) & (df_temp['AwayTeam'] == home_team))
            ].copy()

            if len(h2h_matches) > 0:
                stats['h2h_matches'] += peso * len(h2h_matches)
                stats['h2h_home_wins'] += peso * sum((h2h_matches['HomeTeam'] == home_team) & (h2h_matches['FTR'] == 'H'))
                stats['h2h_away_wins'] += peso * sum((h2h_matches['HomeTeam'] == away_team) & (h2h_matches['FTR'] == 'H'))
                stats['h2h_draws'] += peso * sum(h2h_matches['FTR'] == 'D')

        except ZeroDivisionError:
            continue

    # Obtener y ponderar últimos 5 partidos con más peso (2.0)
    FORM_WEIGHT = 2.0
    ultimos_partidos_home = df[
        (df['HomeTeam'] == home_team) | 
        (df['AwayTeam'] == home_team)
    ].tail(5).copy()

    ultimos_partidos_away = df[
        (df['HomeTeam'] == away_team) | 
        (df['AwayTeam'] == away_team)
    ].tail(5).copy()

    # Calcular posiciones con mayor peso (1.5)
    POSITION_WEIGHT = 1.5
    home_pos = calcular_posicion_tabla(df, home_team)
    away_pos = calcular_posicion_tabla(df, away_team)

    # Normalizar posiciones (invertidas para que mejor posición = mayor valor)
    max_pos = 20  # número máximo de equipos
    home_pos_normalized = (max_pos - home_pos) / max_pos
    away_pos_normalized = (max_pos - away_pos) / max_pos

    # Preparar features finales con pesos ajustados
    features = {
        # Posiciones en la tabla con mayor peso
        'home_position': home_pos_normalized * POSITION_WEIGHT,
        'away_position': away_pos_normalized * POSITION_WEIGHT,
        
        # Estadísticas históricas ponderadas (peso normal)
        'home_historical_wins_weighted': stats['home_wins'],
        'home_historical_draws_weighted': stats['home_draws'],
        'home_historical_losses_weighted': stats['home_losses'],
        'away_historical_wins_weighted': stats['away_wins'],
        'away_historical_draws_weighted': stats['away_draws'],
        'away_historical_losses_weighted': stats['away_losses'],
        
        # Promedios de goles históricos ponderados (peso normal)
        'home_historical_goals_scored_weighted': stats['home_goals_scored'],
        'home_historical_goals_conceded_weighted': stats['home_goals_conceded'],
        'away_historical_goals_scored_weighted': stats['away_goals_scored'],
        'away_historical_goals_conceded_weighted': stats['away_goals_conceded'],
        
        # Historial directo ponderado (peso normal)
        'h2h_home_wins_weighted': stats['h2h_home_wins'],
        'h2h_away_wins_weighted': stats['h2h_away_wins'],
        'h2h_draws_weighted': stats['h2h_draws'],
        'h2h_total_matches': stats['h2h_matches'],
        
        # Forma reciente con mayor peso
        'home_last5_wins': FORM_WEIGHT * sum(
            (ultimos_partidos_home['HomeTeam'] == home_team) & (ultimos_partidos_home['FTR'] == 'H') |
            (ultimos_partidos_home['AwayTeam'] == home_team) & (ultimos_partidos_home['FTR'] == 'A')
        ),
        'home_last5_draws': FORM_WEIGHT * sum(ultimos_partidos_home['FTR'] == 'D'),
        'away_last5_wins': FORM_WEIGHT * sum(
            (ultimos_partidos_away['HomeTeam'] == away_team) & (ultimos_partidos_away['FTR'] == 'H') |
            (ultimos_partidos_away['AwayTeam'] == away_team) & (ultimos_partidos_away['FTR'] == 'A')
        ),
        'away_last5_draws': FORM_WEIGHT * sum(ultimos_partidos_away['FTR'] == 'D')
    }

    # Añadir losses de últimos 5 partidos (también con mayor peso)
    features['home_last5_losses'] = FORM_WEIGHT * (5 - (features['home_last5_wins'] + features['home_last5_draws']) / FORM_WEIGHT)
    features['away_last5_losses'] = FORM_WEIGHT * (5 - (features['away_last5_wins'] + features['away_last5_draws']) / FORM_WEIGHT)

    return pd.DataFrame([features])

def train_model(df, home_team, away_team):
    """
    Entrena el modelo usando solo los partidos del equipo local y visitante especificados.
    
    Args:
        df: DataFrame con los datos históricos
        home_team: Equipo local
        away_team: Equipo visitante
    """
    # Crear listas para almacenar features y resultados
    features_list = []
    results = []
    
    # Ordenar temporadas
    temporadas = sorted(df['Temporada'].unique())
    
    # Filtrar partidos relevantes
    df_equipos = df[
        ((df['HomeTeam'] == home_team) | (df['AwayTeam'] == home_team) |
         (df['HomeTeam'] == away_team) | (df['AwayTeam'] == away_team))
    ]
    
    # Generar datos de entrenamiento
    for idx, partido in df_equipos[df_equipos['Temporada'] != temporadas[0]].iterrows():
        temporada_actual = partido['Temporada']
        temporadas_anteriores = [t for t in temporadas if t < temporada_actual]
        
        if not temporadas_anteriores:
            continue
            
        df_hasta_temporada = df_equipos[df_equipos['Temporada'].isin(temporadas_anteriores)]
        
        try:
            features = prepare_data_for_model(
                df_hasta_temporada,
                partido['HomeTeam'],
                partido['AwayTeam']
            )
            
            if features is not None and not features.empty:
                features_list.append(features)
                result = 0 if partido['FTR'] == 'A' else (1 if partido['FTR'] == 'D' else 2)
                results.append(result)
                
        except Exception as e:
            print(f"Error procesando partido de temporada {temporada_actual}: {e}")
            continue
    
    if not features_list:
        raise ValueError("Datos insuficientes para entrenar el modelo")
    
    # Preparar datos
    X = pd.concat(features_list, ignore_index=True)
    y = np.array(results)
    
    print(f"\nEntrenando modelo con {len(X)} partidos")
    
    # Escalar características
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Definir parámetros para búsqueda
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [3, 4, 5],
        'learning_rate': [0.01, 0.1],
        'subsample': [0.8, 0.9, 1.0],
        'colsample_bytree': [0.8, 0.9, 1.0],
        'min_child_weight': [1, 3, 5]
    }
    
    # Inicializar modelo base
    base_model = XGBClassifier(
        objective='multi:softproba',
        num_class=3,
        random_state=42,
        use_label_encoder=False,
        eval_metric='mlogloss'
    )
    
    # Realizar búsqueda de hiperparámetros con validación cruzada
    grid_search = GridSearchCV(
        estimator=base_model,
        param_grid=param_grid,
        cv=5,
        scoring='accuracy',
        n_jobs=-1,
        verbose=1
    )
    
    grid_search.fit(X_scaled, y)
    
    # Obtener y entrenar modelo final con mejores parámetros
    best_model = XGBClassifier(**grid_search.best_params_,
                              objective='multi:softproba',
                              num_class=3,
                              random_state=42,
                              use_label_encoder=False,
                              eval_metric='mlogloss')
    
    # Realizar validación cruzada con el mejor modelo
    cv_scores = cross_val_score(best_model, X_scaled, y, cv=5)
    
    # Entrenar modelo final con todos los datos
    best_model.fit(X_scaled, y)
    
    # Calcular importancia de características
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nMejores hiperparámetros encontrados:")
    print(grid_search.best_params_)
    print(f"\nScore medio de validación cruzada: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
    print("\nCaracterísticas más importantes:")
    print(feature_importance.head(10))
    
    return best_model, scaler, cv_scores.mean(), cv_scores.std()

def predict_match(df, home_team, away_team):
    """
    Entrena el modelo para los equipos específicos y predice el resultado del partido.
    
    Args:
        df: DataFrame con los datos históricos
        home_team: Equipo local
        away_team: Equipo visitante
        
    Returns:
        dict: Probabilidades y resultado más probable
    """
    try:
        # Entrenar el modelo específico para estos equipos
        model, scaler, train_score, test_score = train_model(df, home_team, away_team)
        
        # Obtener las características para el partido actual
        current_features = prepare_data_for_model(df, home_team, away_team)
        
        if current_features is None:
            raise ValueError("No se pudieron preparar las características del partido")
        
        # Escalar las características
        features_scaled = scaler.transform(current_features)
        
        # Obtener probabilidades
        probabilities = model.predict_proba(features_scaled)[0]
        
        # Encontrar el resultado más probable
        resultado_idx = probabilities.argmax()
        resultados = ['Victoria Visitante', 'Empate', 'Victoria Local']
        resultado_probable = resultados[resultado_idx]
        
        # Crear diccionario con los resultados
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
        
        return prediccion
        
    except Exception as e:
        print(f"Error al realizar la predicción: {e}")
        return None

def predict_match_score(df, home_team, away_team):
    """
    Predice el resultado y marcador del partido usando modelo entrenado y estadísticas.
    
    Args:
        df: DataFrame con histórico de partidos
        home_team: Equipo local
        away_team: Equipo visitante
    
    Returns:
        tuple: (goles_local, goles_visitante)
    """
    try:
        # Entrenar el modelo para predecir el resultado
        model, scaler, train_score, test_score = train_model(df, home_team, away_team)
        
        # Obtener características para el partido actual
        current_features = prepare_data_for_model(df, home_team, away_team)
        
        if current_features is None:
            raise ValueError("No se pudieron preparar las características del partido")
        
        # Escalar características
        features_scaled = scaler.transform(current_features)
        
        # Obtener probabilidades del modelo
        probabilities = model.predict_proba(features_scaled)[0]
        
        # Obtener resultado más probable
        resultado_idx = probabilities.argmax()
        resultados = ['Victoria Visitante', 'Empate', 'Victoria Local']
        resultado_probable = resultados[resultado_idx]
        
        # Calcular goles esperados usando estadísticas recientes
        recent_matches = df.tail(10*20)
        
        # Estadísticas equipo local
        home_recent = recent_matches[recent_matches['HomeTeam'] == home_team]['FTHG'].mean()
        home_historical = df[df['HomeTeam'] == home_team]['FTHG'].mean()
        
        # Estadísticas equipo visitante
        away_recent = recent_matches[recent_matches['AwayTeam'] == away_team]['FTAG'].mean()
        away_historical = df[df['AwayTeam'] == away_team]['FTAG'].mean()
        
        # Manejar NaN
        home_recent = home_recent if not pd.isna(home_recent) else home_historical
        away_recent = away_recent if not pd.isna(away_recent) else away_historical
        
        # Calcular goles esperados (70% forma reciente, 30% histórico)
        home_expected = (0.7 * home_recent + 0.3 * home_historical)
        away_expected = (0.7 * away_recent + 0.3 * away_historical)
        
        # Predecir marcador según resultado predicho por el modelo
        if resultado_probable == 'Victoria Local':
            home_score = round(max(home_expected, away_expected + 1))
            away_score = round(min(away_expected, home_score - 1))
        elif resultado_probable == 'Victoria Visitante':
            away_score = round(max(away_expected, home_expected + 1))
            home_score = round(min(home_expected, away_score - 1))
        else:  # Empate
            avg_goals = (home_expected + away_expected) / 2
            home_score = away_score = max(1, round(avg_goals))
            if home_score > 3:
                home_score = away_score = 2
        
        # Ajustar resultados poco probables
        if abs(home_score - away_score) > 3:
            if home_score > away_score:
                home_score = away_score + 2
            else:
                away_score = home_score + 2
        
        return home_score, away_score
        
    except Exception as e:
        print(f"Error al realizar la predicción: {e}")
        return None, None

    

    


    

    
