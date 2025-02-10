#!/usr/bin/env python3



"""
Questo script suggerisce i canti liturgici più adatti per una determinata liturgia.

Il calcolo dell'accuratezza dipende da 4 score: text_similarity, deviation, selection e history
- Similarity: calcolato con cosine text_similarity tra la liturgia e i testi dei canti;
- Deviation (dalla media della similarità): calcolato come la differenza tra text_similarity e mean_text_similarity;
- Selection: accuratezza scelta manualmente;
- History: accuratezza basata sulla frequenza di suonata dei canti in passato grazie a librettocanti.it/canticristiani.it;
"""



# librairies
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import sys
import numpy as np
# import matplotlib.pyplot as plt


# importing costants
import config


# functions
from functions.hd_py_functions import get_text_from_file
from functions.hd_py_functions import get_files_from_dir
from functions.hd_py_functions import get_text_similarities


# constants of the script
N_MAX_SUGGESTIONS = 20
N_PEAKS = 10


# main
# get variable from command line
if len(sys.argv) > 1:
    data_liturgia = sys.argv[1]
else:
    print("Nessun valore passato come argomento. Inserisci la data della liturgia nel formato 'YYYY-MM-DD'")
    sys.exit()


# importing tables
anagrafica = pd.read_csv(config.PATH_ANAGRAFICA_CANTI)
calendario = pd.read_csv(config.PATH_CALENDARIO_LITURGICO)
mean_text_similarities = pd.read_csv(config.PATH_MEAN_TEXT_SIMILARITIES)
weights = pd.read_csv(config.PATH_WEIGHTS)
manually_selected = pd.read_csv(config.PATH_MANUALLY_SELECTED)
storico_suonati = pd.read_csv(config.PATH_STORICO_SUONATI)
mean_suonati = pd.read_csv(config.PATH_MEAN_SUONATI)
vector_similarities = pd.read_csv(config.PATH_VECTOR_SIMILARITIES)


# cerca data_liturgia in calendario (colonna date) e estrai colonna id_liturgia
id_liturgia = calendario[calendario['date'] == data_liturgia]['id_liturgia'].values[0]
print("📖 La liturgia corrispondente alla data", data_liturgia, "è", id_liturgia)
print("")


# --------------------------------- score_vector_similarity --------------------------------- #
print("🔍 Canti consigliati secondo vicinanza embeddings:")
vector_similarities = vector_similarities[vector_similarities['id_liturgia'] == id_liturgia]
print(vector_similarities)

vector_similarities = vector_similarities.rename(columns={'vector_similarity': 'score_vector_similarity'})

# se ci sono canti duplicati mantieni solo quelli con lo score più alto
vector_similarities = vector_similarities.sort_values(by='score_vector_similarity', ascending=False)
vector_similarities = vector_similarities.drop_duplicates(subset='id_canti', keep='first')

vector_similarities = vector_similarities[['id_canti', 'score_vector_similarity']]


# --------------------------------- score_selection --------------------------------- #
print("🔍 Canti consigliati manualmente:")
manually_selected = manually_selected[manually_selected['id_liturgia'] == id_liturgia]
print(manually_selected)
manually_selected = manually_selected.rename(columns={'accuratezza': 'score_selection'})
manually_selected = manually_selected[['id_canti', 'score_selection']]
manually_selected['score_selection'] = (manually_selected['score_selection'] / 100).round(2)
print("")
print("✅ Score (manual) selection determinato")

# debug
# print(manually_selected.head(10)) 
# input("Premi invio per continuare...")



# --------------------------------- score_history --------------------------------- #
# filter storico_suonati per id_liturgia
storico_suonati = storico_suonati[storico_suonati['id_liturgia'] == id_liturgia]

# rimuovi la colonna titolo da mean_suonati (non serve perchè è già in storico_suonati e poi ci sarà merging)
mean_suonati = mean_suonati.drop(columns=['titolo'])

# add to storico_suonati the mean of the played songs from mean_suonati
storico_suonati = pd.merge(storico_suonati, mean_suonati, on='id_canti')

# add column cnt/max
storico_suonati['cnt/max'] = (storico_suonati['cnt'] / storico_suonati['max']).round(2)

# add column normalized deviation from mean
storico_suonati['norm_dev'] = ((storico_suonati['cnt'] - storico_suonati['mean']) / storico_suonati['cnt']).round(2)

# add cnt/max(cnt)
storico_suonati['cnt/max(cnt)'] = (storico_suonati['cnt'] / storico_suonati['cnt'].max()).round(2)

# compute the final score for suonati 
storico_suonati['score_history'] = ((0.275*storico_suonati['cnt/max'] + 0.275*storico_suonati['norm_dev'] + 0.45*storico_suonati['cnt/max(cnt)'])).round(2)

# normalize score_history
storico_suonati['score_history'] = ((storico_suonati['score_history'] / storico_suonati['score_history'].max())).round(2)

# keep only canti with score_history > 0
storico_suonati = storico_suonati[storico_suonati['score_history'] >= 0]

# order by score_history and print the table
storico_suonati = storico_suonati.sort_values(by='score_history', ascending=False)
print("")
print("🔍 Storico dei canti suonati per la liturgia:")
print(storico_suonati)
print("")
print("✅ Score history determinato")
print("")

# select only id_canti e score_history
storico_suonati = storico_suonati[['id_canti', 'score_history']]

# debug
# print(storico_suonati.head(10))
# input("Premi invio per continuare...")



# --------------------------------- score_text_similarity --------------------------------- #
# calcola similarità tra liturgia e canti
liturgia = get_text_from_file(os.path.join(config.PATH_LITURGIE, id_liturgia + '.txt'))
file_canti = get_files_from_dir(config.PATH_CANTI)

df = get_text_similarities(liturgia, file_canti)
print("🔎 Calcolo la similarità tra la liturgia e i testi dei canti...")
df = pd.DataFrame(df)

# change column names: similarity -> text_similarity
df = df.rename(columns={'similarity': 'text_similarity'})

print("min text_similarity:", df['text_similarity'].min())
print("max text_similarity:", df['text_similarity'].max())
print("")
# input("Premi invio per continuare...")

# sort by text_similarity
df = df.sort_values(by='text_similarity', ascending=False)

# join df with mean_text_similarities on id_canti
df['id_canti'] = df['id_canti'].astype(int)
mean_text_similarities['id_canti'] = mean_text_similarities['id_canti'].astype(int)
df = pd.merge(df, mean_text_similarities, on='id_canti')

print("min mean_text_similarity:", df['mean_text_similarity'].min())
print("max mean_text_similarity:", df['mean_text_similarity'].max())
print("")
#input("Premi invio per continuare...")

# old (anche se interessante, forse ma sbagliato)
# compute score_text_similarity (forse con questi passaggi rendo invalido il confronto con deviation)
df['score_text_similarity_c1'] = (df['text_similarity'] / df['max_text_similarity'].max()).round(2)
df['score_text_similarity_c2'] = (df['text_similarity'] / df['max_text_similarity']).round(2)
df['score_text_similarity'] = (0.65*df['score_text_similarity_c1'] + 0.35*df['score_text_similarity_c2']).round(2)

# new compute score_text_similarity
# df['score_text_similarity'] = (df['text_similarity'] / df['max_text_similarity']).round(2)
# alla fine quello di prima pensavo fosse sbagliato perchè pensavo venisse utilizzato lo score text sim per calcolare dev invece no.

# debug
# print id, text_similarity, max_text_similarity, score_text_similarity
# print(df[['id_canti', 'text_similarity', 'max_text_similarity', 'score_text_similarity']].head(20))
# input("Premi invio per continuare...")

print(df[['id_canti', 'text_similarity', 'max_text_similarity', 'score_text_similarity']].head(20))
print("✅ Score text_similarity determinato")
print("")


# --------------------------------- score_deviation --------------------------------- #
# crea in df una colonna score_deviation che sia la deviation
df['deviation'] = df['text_similarity'] - df['mean_text_similarity']
df = df.sort_values(by='deviation', ascending=False)

print("max deviation:", df['deviation'].max())
print("min deviation:", df['deviation'].min())

# calcolo score_deviation normalizzando deviation con max_deviation
# df['score_deviation'] = df['deviation'] / df['max_deviation']

# anzi, calcola score_deviation così come fatto per score_text_similarity
df['score_deviation_c1'] = df['deviation'] / df['max_deviation'].max()
df['score_deviation_c2'] = df['deviation'] / df['max_deviation']
df['score_deviation'] = (0.65*df['score_deviation_c1'] + 0.35*df['score_deviation_c2']).round(2)
# altrimenti ottengo risultati troppo alti

# debug
# print id, max_text_similarity, text_similarity, deviation, max_deviation, score_deviation
# print(df[['id_canti', 'text_similarity', 'mean_text_similarity', 'deviation', 'max_deviation', 'score_deviation']].head(20))
# input("Premi invio per continuare...")

print("max score_deviation:", df['score_deviation'].max())
print("min score_deviation:", df['score_deviation'].min())

print(df[['id_canti', 'text_similarity', 'mean_text_similarity', 'deviation', 'max_deviation', 'score_deviation']].head(20))
print("✅ Score deviation determinato")
print("")



# --------------------------------- total score --------------------------------- #
# from df maintain only id_canti, score_text_similarity, score_deviation
df = df[['id_canti', 'score_text_similarity', 'score_deviation']]

# debug
# print(df.head(10))
# input("Premi invio per continuare...")

# join with manually_selected if manually_selected is not empty
if not manually_selected.empty:
    df = pd.merge(df, manually_selected, on='id_canti', how='left')
    print("Manually selected joined")

# join with storico_suonati if storico_suonati is not empty
if not storico_suonati.empty:
    df = pd.merge(df, storico_suonati, on='id_canti', how='left')
    print("Storico suonati joined")

# join with vector_similarities if vector_similarities is not empty
if not vector_similarities.empty:
    df = pd.merge(df, vector_similarities, on='id_canti', how='left')
    print("Vector similarities joined")

# debug 
# print("max score_history:", df['score_history'].max())
# print("min score_history:", df['score_history'].min())
# print(df.head(10))
# input("Premi invio per continuare...")

# join with anagrafica
anagrafica['id_canti'] = anagrafica['id_canti'].astype(int)
df = pd.merge(df, anagrafica, on='id_canti')

# remove rows with momento column = 22 (atto penitenziale), momento column = 23 (gloria), momento = 71 (agnello di dio)
df = df[df['momento'] != '22']
df = df[df['momento'] != '22,11']
df = df[df['momento'] != '22,10,11']
df = df[df['momento'] != '23']
df = df[df['momento'] != '71']
df = df[df['momento'] != '71,18']
print("✂️  Signore pietà, Gloria e Agnello di Dio rimossi")

# remove rows con alcuni canti che non vogliono siano suggeriti
df = df[df['id_canti'] != 2624]
df = df[df['id_canti'] != 1969]
print("✂️  Canti 'inutili' rimossi")
print("")

"""
print("")
print(df[['id_canti','titolo', 'score_text_similarity','score_deviation', 'score_selection', 'score_history']])
input("Premi invio per continuare...")
"""

# defining weights
weight_text_similarity = weights[weights['metric'] == 'text_similarity']['weight'].values[0]
weight_vector_similarity = weights[weights['metric'] == 'vector_similarity']['weight'].values[0]
weight_deviation  = weights[weights['metric'] == 'deviation']['weight'].values[0]
weight_history    = weights[weights['metric'] == 'history']['weight'].values[0]
weight_selection  = weights[weights['metric'] == 'selection']['weight'].values[0]
print("⚖️  Pesi caricati")
print("   text_similarity   :", weight_text_similarity)
print("   vector_similarity :", weight_vector_similarity)
print("   sim deviation:", weight_deviation)
print("   selection    :", weight_selection)
print("   history      :", weight_history)
print("")

# score calculation
# fai media pesata di score_text_similarity,score_deviation,score_selection,score_history
# df['score'] = (weight_text_similarity*df['score_text_similarity'] + weight_deviation*df['score_deviation'] + weight_selection*df['score_selection'] + weight_history*df['score_history']) / (weight_text_similarity + weight_deviation + weight_selection + weight_history)

# if score_selection non fa parte del df, aggiungila e mettila NaN
if 'score_selection' not in df.columns:
    df['score_selection'] = np.nan

# stessa cosa per score_vector_similarity
if 'score_vector_similarity' not in df.columns:
    df['score_vector_similarity'] = np.nan

df['score'] = ((
    df['score_text_similarity'].fillna(0) * weight_text_similarity +
    df['score_vector_similarity'].fillna(0) * weight_vector_similarity +
    df['score_deviation'].fillna(0) * weight_deviation +
    df['score_selection'].fillna(0) * weight_selection +
    df['score_history'].fillna(0) * weight_history
) / (
    (df['score_text_similarity'].notna() * weight_text_similarity) +
    (df['score_vector_similarity'].notna() * weight_vector_similarity) +
    (df['score_deviation'].notna() * weight_deviation) +
    (df['score_selection'].notna() * weight_selection) +
    (df['score_history'].notna() * weight_history)
)).round(2)*100

# sort by score
df = df.sort_values(by='score', ascending=False)

print("")
print(df[['id_canti','titolo', 'score_text_similarity', 'score_vector_similarity', 'score_history', 'score']].head(20))
# input("Premi invio per continuare...")


# --------------------------------- adeguatezza (label) --------------------------------- #
print("")
print("📊 Sto calcolando l'adeguatezza dei canti...")

# Funzione per calcolare l'adeguatezza
def calcola_adeguatezza(row):
    if (row['score_selection'] >= 0.92 ) or ((row['score_history'] >= 0.9) and row['score'] >= 80) or (row['score'] >= 95):
        return ':material-check-all: Alta'
    elif (0.7 <= row['score_selection'] < 0.92):
        return ':material-check: Buona'
    else:
        return ':material-dots-horizontal: Mh'

# Applicazione della funzione
df['adeguatezza'] = df.apply(calcola_adeguatezza, axis=1)

print("")
print("Mostro solo canti > soglia")
# print(df[['id_canti','titolo', 'score_text_similarity','score_deviation', 'score_selection', 'score_history', 'score', 'adeguatezza']].head(20))
print(df[['id_canti','titolo', 'score_text_similarity', 'score_vector_similarity', 'score_deviation', 'score_selection', 'score_history', 'score', 'adeguatezza']][df['score'] >= config.THRESHOLD_MIN_SCORE])



# vorrei questo. Magari classificazione con PCA? non so
""""
id_canti                                          titolo  score_text_similarity  score_deviation  score_selection  score_history  score   adeguatezza
  217                                        Grandi cose              0.88            -0.06              1.0            1.0   78.0   ✅ Alta
 1649                 Accogli Signore i nostri doni (v2)              0.60             0.43              NaN            NaN   52.0   🧐 Mh
    6                      Accogli Signore i nostri doni              0.60             0.43              NaN            NaN   52.0   🧐 Mh
 1651                                         Talità Kum              0.23            -0.06              0.7            NaN   38.0   👌 Buona
  133                                      Come è grande              0.92            -0.29              NaN            NaN   38.0   👌 Buona
 1999                                     Cose stupende               0.87            -0.29              NaN            NaN   35.0   🧐 Mh
  195                                    Fissa gli occhi              0.94            -0.40              NaN            NaN   34.0   ✅ Alta
 1678                                Io credo in te Gesù              0.65            -0.09              NaN            NaN   32.0   🧐 Mh
 1975                            Tu sei qui (Medjugorje)              0.40             0.23              NaN            NaN   32.0   🧐 Mh
 1818                         Ciò che Dio ha fatto in me              0.67            -0.11              NaN            NaN   32.0   🧐 Mh
  423                                    Servo per amore              0.66            -0.12              NaN            NaN   31.0   🧐 Mh
 2111                                      Alleluia Gesù              0.71            -0.21              NaN            NaN   30.0   🧐 Mh
 2360                           Il Signore ci ha salvato              0.73            -0.27              NaN            NaN   29.0   🧐 Mh
  290                                 Lode e gloria a Te              0.55            -0.06              NaN            NaN   28.0   🧐 Mh
 1583                                 E' tempo di grazia              0.78            -0.35              NaN            NaN   28.0   🧐 Mh
 2523                                  Gesù (mi perdonò)              0.53            -0.04              NaN            NaN   28.0   🧐 Mh
 2393                           Io credo in te Gesù (v2)              0.61            -0.14              NaN            NaN   28.0   🧐 Mh
 2436                          Anche tu sei mio fratello              0.61            -0.13              NaN            NaN   28.0   🧐 Mh
 2522                            Gesù io desidero amarti              0.22             0.35              NaN            NaN   28.0   🧐 Mh
 1888  Inno della Divina Misericordia (Gesù, confido ...              0.70            -0.26              NaN            NaN   27.0   🧐 Mh

"""


# --------------------------------- export --------------------------------- #

### export to csv
# probabilmente sarebbe meglio non salvare con latest ma con la data della liturgia
# ragionare sul senso di tnere questo output completo in csv.
output_df_path = 'data/suggerimenti-latest.csv'
df[['id_canti','titolo', 'score_vector_similarity', 'score_text_similarity', 'score_deviation', 'score_selection', 'score_history', 'score','adeguatezza']].to_csv(output_df_path, index=False)

# mantieni solo score >= THRESHOLD_MIN_SCORE
dfc = df # creo copia di df
df = df[df['score'] >= config.THRESHOLD_MIN_SCORE]
df = df.reset_index(drop=True)

### export to md per hildegard.it
# crea una nuova colonna titolo_md che contenga il link al canto su librettocanti.it
df['titolo_md'] = df.apply(lambda row: row['titolo'] if pd.isnull(row['id_canti']) else '[' + row['titolo'] + '](https://www.librettocanti.it' + str(row['url']) + ')', axis=1)

# prima di esportare aggiungi data_liturgia a tutti quelli che saranno json (top20 e i 4 momenti)
df['data'] = data_liturgia

# score to int
df['score'] = df['score'].astype(int)

# exclude if momento columns is NaN
nonan=df.dropna(subset=['momento'])

# split momenti
suggested_ingresso = nonan[nonan['momento'].str.contains('21')].head(10).fillna('')
suggested_offertorio = nonan[nonan['momento'].str.contains('26')].head(10).fillna('')
suggested_comunione = nonan[nonan['momento'].str.contains('31')].head(10).fillna('')
suggested_congedo = nonan[nonan['momento'].str.contains('32')].head(10).fillna('')

# preview of the table md_res
# print(df.head(20).drop(columns=['titolo_md']).fillna(''))

### export to json for canticristiani
# forse michele usa data/suggeriti-top20-latest.json, capire
json_cols = ['id_canti', 'text_similarity', 'label', 'titolo', 'autore', 'raccolta', 'momento', 'link_youtube', 'data']

df.rename(columns={'score': 'text_similarity', 'adeguatezza': 'label'})[json_cols].fillna('').sort_values(by='text_similarity', ascending=False).head(20).to_json('data/suggeriti-top20-latest.json', orient='records')
suggested_ingresso.rename(columns={'score': 'text_similarity', 'adeguatezza': 'label'})[json_cols].fillna('').sort_values(by='text_similarity', ascending=False).to_json('data/suggeriti-ingresso-latest.json', orient='records')
suggested_offertorio.rename(columns={'score': 'text_similarity', 'adeguatezza': 'label'})[json_cols].fillna('').sort_values(by='text_similarity', ascending=False).to_json('data/suggeriti-offertorio-latest.json', orient='records')
suggested_comunione.rename(columns={'score': 'text_similarity', 'adeguatezza': 'label'})[json_cols].fillna('').sort_values(by='text_similarity', ascending=False).to_json('data/suggeriti-comunione-latest.json', orient='records')
suggested_congedo.rename(columns={'score': 'text_similarity', 'adeguatezza': 'label'})[json_cols].fillna('').sort_values(by='text_similarity', ascending=False).to_json('data/suggeriti-congedo-latest.json', orient='records')

print("")
print("✅ I suggerimenti formattati per librettocanti sono stati scritti nei file json")
print("📄 File prodotti:")
print("   data/suggeriti-top20-latest.json")
print("   data/suggeriti-ingresso-latest.json")
print("   data/suggeriti-offertorio-latest.json")
print("   data/suggeriti-comunione-latest.json")
print("   data/suggeriti-congedo-latest.json")

### formatting data for hildegard website
# capires se si può stare in alto. Mi piacerebbe mantenere una sezione per export per hidlegard e un export per canticristiani
# mapping columns
md_cols = ['titolo_md', 'adeguatezza', 'score', 'autore', 'raccolta']
md_cols_renamed = ['Titolo', 'Adeguatezza', '%' , 'Autore', 'Raccolta']

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

# save extra file for hildegard with 20 not selected songs
dfc = dfc[dfc['score'] < config.THRESHOLD_MIN_SCORE]
dfc = dfc.reset_index(drop=True)

# sort by score 
dfc = dfc.sort_values(by='score', ascending=False)

# select only first 20
dfc = dfc.head(20)

# creo colonna titolo_md
dfc['titolo_md'] = dfc.apply(lambda row: row['titolo'] if pd.isnull(row['id_canti']) else '[' + row['titolo'] + '](https://www.librettocanti.it' + str(row['url']) + ')', axis=1)

# score to int
df['score'] = df['score'].astype(int)


# transform data_liturgia from YYYY-MM-DD to YYYYMMDD
data_liturgia = data_liturgia.replace('-', '')

# save csv named notselected-${data_liturgia}.csv
dfc[md_cols].fillna('').rename(columns=dict(zip(md_cols, md_cols_renamed))).to_csv(f'data/not-selected-{data_liturgia}.csv', index=False)

print ("")
print("✅ I canti non selezionati sono stati esportati")
