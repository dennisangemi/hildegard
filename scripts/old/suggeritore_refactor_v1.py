#!/usr/bin/env python3

"""
Script per suggerire canti liturgici basati su similarità testuale, deviazione, selezione manuale e storico.
Funziona ma dà risultati leggermenti diversi del suggeritore_v8
"""

import sys
import os
from typing import Tuple, Dict
import pandas as pd
import numpy as np
import config
from functions.hd_py_functions import (
    get_text_from_file,
    get_files_from_dir,
    get_text_similarities
)

# Costanti
N_MAX_SUGGESTIONS = 20
N_PEAKS = 10
MOMENTI_ESCLUSI = {'22', '22,11', '22,10,11', '23', '71', '71,18'}
CANTI_ESCLUSI = {2624, 1969}


def parse_arguments() -> Tuple[str, str]:
    """Gestisce gli argomenti da riga di comando"""
    if len(sys.argv) < 2:
        print("Inserisci la data della liturgia nel formato 'YYYY-MM-DD'")
        sys.exit(1)
    
    date = sys.argv[1]
    return date, date.replace('-', '')


def load_datasets() -> Dict[str, pd.DataFrame]:
    """Carica tutti i dataset necessari"""
    return {
        'anagrafica': pd.read_csv(config.PATH_ANAGRAFICA_CANTI),
        'calendario': pd.read_csv(config.PATH_CALENDARIO_LITURGICO),
        'mean_text': pd.read_csv(config.PATH_MEAN_TEXT_SIMILARITIES),
        'weights': pd.read_csv(config.PATH_WEIGHTS),
        'manuali': pd.read_csv(config.PATH_MANUALLY_SELECTED),
        'storico': pd.read_csv(config.PATH_STORICO_SUONATI),
        'media_suonati': pd.read_csv(config.PATH_MEAN_SUONATI),
        'vector_sim': pd.read_csv(config.PATH_VECTOR_SIMILARITIES)
    }


def get_liturgy_id(calendario_df: pd.DataFrame, data: str) -> str:
    """Recupera l'ID liturgia dalla data"""
    liturgy = calendario_df[calendario_df['date'] == data]
    if liturgy.empty:
        raise ValueError(f"Liturgia non trovata per la data {data}")
    return liturgy['id_liturgia'].iloc[0]


def process_vector_scores(vector_df: pd.DataFrame, liturgy_id: str) -> pd.DataFrame:
    """Elabora i punteggi di similarità vettoriale"""
    df = vector_df[vector_df['id_liturgia'] == liturgy_id].copy()
    if df.empty:
        return pd.DataFrame()
    
    df = df.rename(columns={'vector_similarity': 'score_vector_similarity'})
    return df.sort_values('score_vector_similarity', ascending=False)\
             .drop_duplicates('id_canti', keep='first')\
             [['id_canti', 'score_vector_similarity']]


def process_manual_scores(manual_df: pd.DataFrame, liturgy_id: str) -> pd.DataFrame:
    """Elabora i punteggi manuali"""
    df = manual_df[manual_df['id_liturgia'] == liturgy_id].copy()
    if df.empty:
        return pd.DataFrame()
    
    df = df.rename(columns={'accuratezza': 'score_selection'})
    df['score_selection'] = (df['score_selection'] / 100).round(2)
    return df[['id_canti', 'score_selection']]


def process_history_scores(storico_df: pd.DataFrame, media_df: pd.DataFrame, liturgy_id: str) -> pd.DataFrame:
    """Calcola i punteggi storici"""
    df = storico_df[storico_df['id_liturgia'] == liturgy_id].copy()
    if df.empty:
        return pd.DataFrame()
    
    df = pd.merge(df, media_df.drop(columns=['titolo'], errors='ignore'), on='id_canti')
    
    # Calcoli intermedi
    df['cnt/max'] = (df['cnt'] / df['max']).round(2)
    df['norm_dev'] = ((df['cnt'] - df['mean']) / df['cnt']).round(2)
    df['cnt/max(cnt)'] = (df['cnt'] / df['cnt'].max()).round(2)
    
    # Punteggio finale
    df['score_history'] = (0.275 * df['cnt/max'] + 0.275 * df['norm_dev'] + 0.45 * df['cnt/max(cnt)'])
    df['score_history'] = (df['score_history'] / df['score_history'].max()).round(2)
    return df[df['score_history'] >= 0][['id_canti', 'score_history']]


def process_text_scores(liturgy_id: str, liturgy_path: str, canti_path: str, mean_text_df: pd.DataFrame) -> pd.DataFrame:
    """Calcola i punteggi di similarità testuale"""
    liturgy_text = get_text_from_file(os.path.join(liturgy_path, f"{liturgy_id}.txt"))
    canti_files = get_files_from_dir(canti_path)
    
    sim_df = pd.DataFrame(get_text_similarities(liturgy_text, canti_files))
    sim_df = sim_df.rename(columns={'similarity': 'text_similarity'})
    sim_df['id_canti'] = sim_df['id_canti'].astype(int)
    
    merged = pd.merge(sim_df, mean_text_df.astype({'id_canti': int}), on='id_canti')
    
    # Calcolo punteggi
    merged['score_text_similarity'] = (
        0.65 * (merged['text_similarity'] / merged['max_text_similarity'].max()) +
        0.35 * (merged['text_similarity'] / merged['max_text_similarity'])
    ).round(2)
    
    merged['score_deviation'] = (
        0.65 * ((merged['text_similarity'] - merged['mean_text_similarity']) / merged['max_deviation'].max()) +
        0.35 * ((merged['text_similarity'] - merged['mean_text_similarity']) / merged['max_deviation'])
    ).round(2)
    
    return merged[['id_canti', 'score_text_similarity', 'score_deviation']]


def calculate_final_score(merged_df: pd.DataFrame, weights_df: pd.DataFrame) -> pd.DataFrame:
    """Calcola il punteggio finale complessivo"""
    # Define weights
    weight_text_similarity = weights_df[weights_df['metric'] == 'text_similarity']['weight'].values[0]
    weight_vector_similarity = weights_df[weights_df['metric'] == 'vector_similarity']['weight'].values[0]
    weight_deviation = weights_df[weights_df['metric'] == 'deviation']['weight'].values[0]
    weight_selection = weights_df[weights_df['metric'] == 'selection']['weight'].values[0]
    weight_history = weights_df[weights_df['metric'] == 'history']['weight'].values[0]

    # Print weights for verification
    print("⚖️  Pesi caricati")
    print("   text_similarity   :", weight_text_similarity)
    print("   vector_similarity :", weight_vector_similarity)
    print("   sim deviation     :", weight_deviation)
    print("   selection        :", weight_selection)
    print("   history          :", weight_history)
    print("")

    # Ensure all score columns exist
    for col in ['score_text_similarity', 'score_vector_similarity', 'score_deviation', 
                'score_selection', 'score_history']:
        if col not in merged_df:
            merged_df[col] = np.nan
    
    # Calculate weighted sum for numerator and denominator
    numerator = (
        merged_df['score_text_similarity'].fillna(0) * weight_text_similarity +
        merged_df['score_vector_similarity'].fillna(0) * weight_vector_similarity +
        merged_df['score_deviation'].fillna(0) * weight_deviation +
        merged_df['score_selection'].fillna(0) * weight_selection +
        merged_df['score_history'].fillna(0) * weight_history
    )
    
    denominator = (
        merged_df['score_text_similarity'].notna().astype(int) * weight_text_similarity +
        merged_df['score_vector_similarity'].notna().astype(int) * weight_vector_similarity +
        merged_df['score_deviation'].notna().astype(int) * weight_deviation +
        merged_df['score_selection'].notna().astype(int) * weight_selection +
        merged_df['score_history'].notna().astype(int) * weight_history
    )
    
    # Calculate final score
    merged_df['score'] = (numerator / denominator).fillna(0).round(2) * 100
    return merged_df.astype({'score': int})


def apply_adequacy_label(row: pd.Series) -> str:
    """Assegna etichetta di adeguatezza"""
    if (row.get('score_selection', 0) >= 0.92 or
        (row.get('score_history', 0) >= 0.9 and row['score'] >= 80) or
        row['score'] >= 95):
        return ':material-check-all: Alta'
    elif 0.7 <= row.get('score_selection', 0) < 0.92:
        return ':material-check: Buona'
    return ':material-dots-horizontal: Mh'


def export_results(main_df: pd.DataFrame, data_str: str, date_suffix: str):
    """Gestisce l'esportazione dei risultati"""
    # Esportazione CSV principale
    main_df.to_csv('data/suggerimenti-latest.csv', index=False)
    
    # Preparazione dati per esportazioni
    main_df['data'] = data_str
    main_df['titolo_md'] = main_df.apply(
        lambda r: f"[{r['titolo']}](https://www.librettocanti.it{r['url']})" if not pd.isnull(r['id_canti']) else r['titolo'], 
        axis=1
    )
    
    # Define column mappings
    md_cols = ['titolo_md', 'adeguatezza', 'score', 'autore', 'raccolta']
    md_cols_renamed = ['Titolo', 'Adeguatezza', '%', 'Autore', 'Raccolta']
    col_mapping = dict(zip(md_cols, md_cols_renamed))
    
    # Main export
    main_df[md_cols].head(20).fillna('').rename(columns=col_mapping)\
        .to_csv('data/suggeriti-top20-latest.csv', index=False)
    
    # Esportazione JSON
    json_cols = ['id_canti', 'text_similarity', 'label', 'titolo', 'autore', 'raccolta', 'momento', 'link_youtube', 'data']
    main_df.rename(columns={'score': 'text_similarity', 'adeguatezza': 'label'})[json_cols]\
        .fillna('').sort_values(by='text_similarity', ascending=False)\
        .head(20).to_json('data/suggeriti-top20-latest.json', orient='records')
    
    # Filter for valid momenti
    valid_df = main_df.dropna(subset=['momento'])
    
    # Esportazione per momenti liturgici
    momenti = {
        'ingresso': '21',
        'offertorio': '26',
        'comunione': '31',
        'congedo': '32'
    }
    
    for nome, codice in momenti.items():
        filtered = valid_df[valid_df['momento'].str.contains(codice)].head(10)
        filtered[md_cols].fillna('').rename(columns=col_mapping)\
            .to_csv(f'data/suggeriti-{nome}-latest.csv', index=False)


def main():
    """Funzione principale"""
    data_liturgia, data_yyyymmdd = parse_arguments()
    datasets = load_datasets()
    
    try:
        liturgy_id = get_liturgy_id(datasets['calendario'], data_liturgia)
    except ValueError as e:
        print(e)
        sys.exit(1)
    
    print(f"📖 Liturgia del {data_liturgia}: {liturgy_id}\n")
    
    # Elaborazione punteggi
    vector_scores = process_vector_scores(datasets['vector_sim'], liturgy_id)
    manual_scores = process_manual_scores(datasets['manuali'], liturgy_id)
    history_scores = process_history_scores(datasets['storico'], datasets['media_suonati'], liturgy_id)
    text_scores = process_text_scores(
        liturgy_id, config.PATH_LITURGIE, config.PATH_CANTI, datasets['mean_text']
    )
    
    # Unione dataset
    merged = pd.merge(text_scores, datasets['anagrafica'], on='id_canti')
    for df in [vector_scores, manual_scores, history_scores]:
        if not df.empty:
            merged = pd.merge(merged, df, on='id_canti', how='left')
    
    # Filtri
    merged = merged[~merged['momento'].isin(MOMENTI_ESCLUSI)]
    merged = merged[~merged['id_canti'].isin(CANTI_ESCLUSI)]
    
    # Calcolo finale
    final_df = calculate_final_score(merged, datasets['weights'])
    final_df['adeguatezza'] = final_df.apply(apply_adequacy_label, axis=1)
    
    # Suddivisione risultati
    threshold = config.THRESHOLD_MIN_SCORE
    suggested = final_df[final_df['score'] >= threshold].sort_values('score', ascending=False)
    excluded = final_df[final_df['score'] < threshold].sort_values('score', ascending=False).head(20)
    
    # Prepare excluded data with correct columns
    excluded['titolo_md'] = excluded.apply(
        lambda r: f"[{r['titolo']}](https://www.librettocanti.it{r['url']})" if not pd.isnull(r['id_canti']) else r['titolo'], 
        axis=1
    )
    md_cols = ['titolo_md', 'adeguatezza', 'score', 'autore', 'raccolta']
    md_cols_renamed = ['Titolo', 'Adeguatezza', '%', 'Autore', 'Raccolta']
    
    # Esportazione
    export_results(suggested, data_liturgia, data_yyyymmdd)
    excluded[md_cols].fillna('').rename(columns=dict(zip(md_cols, md_cols_renamed)))\
        .to_csv(f'data/not-selected-{data_yyyymmdd}.csv', index=False)
    
    print("\n✅ Esportazione completata")


if __name__ == '__main__':
    main()
