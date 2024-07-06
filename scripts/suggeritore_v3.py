#!/usr/bin/env python3


# questo script calcola la similarità tra il testo della liturgia e i testi dei canti


# librairies
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import sys
# import matplotlib.pyplot as plt
import numpy as np

# importing costants
import config



# functions
from functions.hd_py_functions import get_text_from_file
from functions.hd_py_functions import get_files_from_dir
from functions.hd_py_functions import get_similarities



# main


# get variable from command line
if len(sys.argv) > 1:
    data_liturgia = sys.argv[1]
    # print(f"La data della liturgia prossima liturgia che includo nei json è: {data_liturgia}")
else:
    print("Nessun valore passato come argomento.")
    sys.exit()


# importing tables
anagrafica = pd.read_csv(config.PATH_ANAGRAFICA_CANTI)
calendario = pd.read_csv(config.PATH_CALENDARIO_LITURGICO)
mean_similarities = pd.read_csv(config.PATH_MEAN_SIMILARITIES)
weights = pd.read_csv(config.PATH_WEIGHTS)
manually_selected = pd.read_csv(config.PATH_MANUALLY_SELECTED)

# cerca data_liturgia in calendario (colonna date) e estrai colonna id_liturgia
# data_liturgia = "2024-06-30" # to comment
id_liturgia = calendario[calendario['date'] == data_liturgia]['id_liturgia'].values[0]
# print(id_liturgia)
print("📖 La liturgia corrispondente alla data", data_liturgia, "è", id_liturgia)

# filter manually_selected per id_liturgia
manually_selected = manually_selected[manually_selected['id_liturgia'] == id_liturgia]

# calcola similarità tra liturgia e canti
liturgia = get_text_from_file(os.path.join(config.PATH_LITURGIE, id_liturgia + '.txt'))
file_canti = get_files_from_dir(config.PATH_CANTI)

print("🔎 Calcolo la similarità tra la liturgia e i testi dei canti...")
df = get_similarities(liturgia, file_canti)
df = pd.DataFrame(df)

# make similarity a percentage
df['similarity'] = (df['similarity']*100).round(2)

# make id_canti column an integer in order to join
df['id_canti'] = df['id_canti'].astype(int)
mean_similarities['id_canti'] = mean_similarities['id_canti'].astype(int)
anagrafica['id_canti'] = anagrafica['id_canti'].astype(int)

# join df with mean_similarities on id_canti
df = pd.merge(df, mean_similarities, on='id_canti')

# compute deviation
df['deviation'] = df['similarity'] - df['mean_similarity']

# order by similarity
df = df.sort_values(by='similarity', ascending=False)

# join with manually_selected if manually_selected is not empty
if not manually_selected.empty:
    df = pd.merge(df, manually_selected, on='id_canti', how='left')

# join with anagrafica
df = pd.merge(df, anagrafica, on='id_canti')

# remove rows with momento column = 22 (atto penitenziale) and remove momento column = 23 (gloria)
df = df[df['momento'] != '22']
df = df[df['momento'] != '23']

# defining weights
weight_similarity = weights[weights['metric'] == 'similarity']['weight'].values[0]
weight_deviation = weights[weights['metric'] == 'deviation']['weight'].values[0]
weight_history = weights[weights['metric'] == 'history']['weight'].values[0]
weight_selection = weights[weights['metric'] == 'selection']['weight'].values[0]


# score calculation

# crea in df una colonna score_similarity
# df['score_similarity'] = df['similarity'] * weight_similarity / 100
# df['score_similarity'] = df['similarity'] * weight_similarity / df['similarity'].max()
# siccome sono indeciso sul metodo di calcolo, faccio una media pesata
df['score_similarity'] = 0.6*(df['similarity'] * weight_similarity / 100) + 0.4*(df['similarity'] * weight_similarity / df['similarity'].max())

# crea in df una colonna score_deviation che sia la deviation moltiplicata per il peso/max deviation. Anzi compresa tra -weight_deviation e +weight_deviation
df['score_deviation'] = df['deviation'] * weight_deviation / df['deviation'].max()
df['score_deviation'] = np.where(df['score_deviation'] >= 0, df['score_deviation'], df['deviation'] * weight_deviation / abs(df['deviation'].min()))

# crea in df una colonna score che sia la somma di score_similarity e score_deviation
df['score'] = df['score_similarity'] + df['score_deviation']

# se esiste la colonna `accuratezza`, rinominala in `manually_selected` (cioè se ci sono canti selezionati manualmente per questa determinata liturgia)
if 'accuratezza' in df.columns:
    # rinomina accuratezza in manually_selected
    df = df.rename(columns={'accuratezza': 'manually_selected'})
    # crea una colonna score_selection che sia la manually_selected moltiplicata per il peso weight_selection/100
    df['score_selection'] = df['manually_selected'] * weight_selection / 100
    # per ogni riga, se la colonna `manually_selected` non è NaN, allora score è score_similarity + abs(score_deviation) + score_selection
    df['score'] = df.apply(lambda row: row['score_similarity'] + abs(row['score_deviation']) + row['score_selection']  if pd.notnull(row['manually_selected']) else row['score'], axis=1)

# normalize score dividing by sum of the weights
# df['score'] = ((df['score'] / (weight_similarity + weight_deviation + weight_selection))*100).round(2)

# sort df by score
df = df.sort_values(by='score', ascending=False)

print("")
print(" ⏯ I testi più simili sono:")

if 'score_selection' in df.columns:
    print(df[['id_canti','titolo', 'similarity', 'mean_similarity', 'deviation', 'score_similarity','score_deviation', 'score_selection', 'score']].head())
else:
    print(df[['id_canti','titolo', 'similarity', 'mean_similarity', 'deviation', 'score_similarity','score_deviation', 'score']].head())

# plot histogram of score with plt
# plt.hist(df['score'], bins=20)
# plt.show()

# basic stats
print("")
print("📊 Statistiche sui punteggi:")
print("score_similarity = [", df['score_similarity'].min(), ",", df['score_similarity'].max(), "]")
print("score_deviation  = [", df['score_deviation'].min(), ",", df['score_deviation'].max(), "]")

if 'score_selection' in df.columns:
    print("score_selection = [", df['score_selection'].min(), ",", df['score_selection'].max(), "]")

print("score = [", df['score'].min(), ",", df['score'].max(), "]")

# export to csv
output_df_path = 'data/suggerimenti-latest.csv'
df.to_csv(output_df_path, index=False)

# mantieni in df solo  le righe con score > 0
df = df[df['score'] > 0]

# crea una nuova colonna titolo_md che contenga il link al canto su librettocanti.it
df['titolo_md'] = df.apply(lambda row: row['titolo'] if pd.isnull(row['id_canti']) else '[' + row['titolo'] + '](https://www.librettocanti.it/mod_canti_gestione#!canto/vedi/' + str(row['id_canti']) + ')', axis=1)

# prima di esportare aggiungi data_liturgia a tutti quelli che saranno json (top20 e i 4 momenti)
df['data'] = data_liturgia

# round score to 2 decimal
df['score'] = df['score'].round(2)

# exclude if momento columns is NaN
nonan=df.dropna(subset=['momento'])

# split momenti
suggested_ingresso = nonan[nonan['momento'].str.contains('21')].head(10).fillna('')
suggested_offertorio = nonan[nonan['momento'].str.contains('26')].head(10).fillna('')
suggested_comunione = nonan[nonan['momento'].str.contains('31')].head(10).fillna('')
suggested_congedo = nonan[nonan['momento'].str.contains('32')].head(10).fillna('')

# preview of the table md_res
# print(df.head(20).drop(columns=['titolo_md']).fillna(''))

# export data to json for canticristiani
json_cols = ['id_canti', 'similarity', 'titolo', 'autore', 'raccolta', 'momento', 'link_youtube', 'data']

df.drop(columns=['similarity']).rename(columns={'score': 'similarity'})[json_cols].fillna('').sort_values(by='similarity', ascending=False).head(20).to_json('data/suggeriti-top20-latest.json', orient='records')
suggested_ingresso.drop(columns=['similarity']).rename(columns={'score': 'similarity'})[json_cols].fillna('').sort_values(by='similarity', ascending=False).to_json('data/suggeriti-ingresso-latest.json', orient='records')
suggested_offertorio.drop(columns=['similarity']).rename(columns={'score': 'similarity'})[json_cols].fillna('').sort_values(by='similarity', ascending=False).to_json('data/suggeriti-offertorio-latest.json', orient='records')
suggested_comunione.drop(columns=['similarity']).rename(columns={'score': 'similarity'})[json_cols].fillna('').sort_values(by='similarity', ascending=False).to_json('data/suggeriti-comunione-latest.json', orient='records')
suggested_congedo.drop(columns=['similarity']).rename(columns={'score': 'similarity'})[json_cols].fillna('').sort_values(by='similarity', ascending=False).to_json('data/suggeriti-congedo-latest.json', orient='records')

print("")
print("✅ I suggerimenti formattati per librettocanti sono stati scritti nei file json")
print("📄 File prodotti:")
print("   data/suggeriti-top20-latest.json")
print("   data/suggeriti-ingresso-latest.json")
print("   data/suggeriti-offertorio-latest.json")
print("   data/suggeriti-comunione-latest.json")
print("   data/suggeriti-congedo-latest.json")

# formatting data for hildegard website

# mapping columns
md_cols = ['titolo_md', 'score', 'autore', 'raccolta']
md_cols_renamed = ['Titolo', 'Adeguatezza (0-10)', 'Autore', 'Raccolta']

# export
df[md_cols].head(20).fillna('').rename(columns=dict(zip(md_cols, md_cols_renamed))).to_csv('data/suggeriti-top20-latest.csv', index=False)
suggested_ingresso[md_cols].fillna('').rename(columns=dict(zip(md_cols, md_cols_renamed))).head(10).to_csv('data/suggeriti-ingresso-latest.csv', index=False)
suggested_offertorio[md_cols].fillna('').rename(columns=dict(zip(md_cols, md_cols_renamed))).head(10).to_csv('data/suggeriti-offertorio-latest.csv', index=False)
suggested_comunione[md_cols].fillna('').rename(columns=dict(zip(md_cols, md_cols_renamed))).head(10).to_csv('data/suggeriti-comunione-latest.csv', index=False)
suggested_congedo[md_cols].fillna('').rename(columns=dict(zip(md_cols, md_cols_renamed))).head(10).to_csv('data/suggeriti-congedo-latest.csv', index=False)

# end
print("")
print("✅ I suggerimenti formattati per hildegard sono stati esportati")   
print("📄 File prodotti:")
print("   data/suggeriti-top20-latest.csv")
print("   data/suggeriti-ingresso-latest.csv")
print("   data/suggeriti-offertorio-latest.csv")
print("   data/suggeriti-comunione-latest.csv")
print("   data/suggeriti-congedo-latest.csv")
