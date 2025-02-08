#!/usr/bin/env python3

# questo script calcola la similarità tra tutte le liturgie e tutti i testi dei canti e genera il file data/mean_similarities.csv che contiene una riga per ogni canti e la sua similarità media

# librairies
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import sys

# importing costants
import config



# functions

from functions.hd_py_functions import get_text_from_file
from functions.hd_py_functions import get_files_from_dir
from functions.hd_py_functions import get_text_similarities


# main
print("🔎 Calcolo la similarità tra la liturgia e i testi dei canti...")

# ottieni lista di filename contenuti in directory config.PATH_CANTI
file_canti = get_files_from_dir(config.PATH_CANTI)

# ottieni la lista di file di testo della liturgia
liturgia_files = get_files_from_dir(config.PATH_LITURGIE)

# crea lista di DataFrame vuota
df_list = []

# per ogni file di testo della liturgia
for liturgia_file in liturgia_files:

    # ottieni il testo della liturgia
    liturgia_text = get_text_from_file(os.path.join(config.PATH_LITURGIE, liturgia_file))

    # calcola la similarità con i testi dei canti
    data = get_text_similarities(liturgia_text, file_canti)

    # Create a DataFrame from the dictionary
    df = pd.DataFrame(data)

    # add to df the liturgia_file column without the .txt extension
    df['id_liturgia'] = liturgia_file[:-4]

    # append the result to a df_list
    df_list.append(df)

    # display the size of the list df
    print(f"🔄 Processate {len(df_list)} liturgie...")

# concatena tutti i DataFrame in df_list
df = pd.concat(df_list)



# print 
# print("📊 Calcolo la media normalizzata per ogni canto...")

# add mean and deviation
# max_text_similarity = df['text_similarity'].max()

# normalize text_similarity
# df['text_similarity'] = df['text_similarity'] / max_text_similarity

# Calcolo della media e del massimo della colonna 'text_similarity' per ogni 'id_canti'
dfg = df.groupby('id_canti')['text_similarity'].agg(['mean', 'max']).reset_index()

# Arrotonda la media e il massimo a 2 cifre decimali
dfg['mean'] = dfg['mean'] #.round(2)
dfg['max'] = dfg['max'] #.round(2)

# tieni solo righe con max_text_similarity > 0
dfg = dfg[dfg['max'] > 0]

# Rinominare le colonne per chiarezza
dfg = dfg.rename(columns={'mean': 'mean_text_similarity', 'max': 'max_text_similarity'})

# sort by mean_text_similarity
dfg = dfg.sort_values(by='mean_text_similarity', ascending=False)

print(dfg)

# turn mean_text_similarity into a percentage with no decimal
# df['mean_text_similarity'] = (df['mean_text_similarity'] * 100).round(2)

# export to csv (old)
# dfg.to_csv(config.PATH_MEAN_TEXT_SIMILARITIES, index=False)
# print(f"📄 Esportato il file {config.PATH_MEAN_TEXT_SIMILARITIES} con successo.")
# print("✅ Tutte similiarità medie sono state calcolate!")

# provo a calcolare il massimo delle deviazioni per ogni canto

# add the mean column of the dfg to the df merging on id_canti
df = pd.merge(df, dfg, on='id_canti')

# adesso il df contiene le colonne: id_canti, id_liturgia text_similarity, max_text_similarity, mean_text_similarity

# calcolo tutte le deviazioni dalla media possibili
df['deviation'] = df['text_similarity'] - df['mean_text_similarity']

# calcolo la deviazione massima per ogni canto, gruppo by id_canti
dfg_deviation = df.groupby('id_canti')['deviation'].agg('max').reset_index()

# rinomino la colonna in max_deviation
dfg_deviation = dfg_deviation.rename(columns={'deviation': 'max_deviation'})

# seleziono solo colonne id_canti e max_deviation
dfg_deviation = dfg_deviation[['id_canti', 'max_deviation']]

# merge dfg_deviation con dfg
dfg = pd.merge(dfg, dfg_deviation, on='id_canti')

# seleziona solo colonne id_canti, mean_text_similarity, max_text_similarity, max_deviation
dfg = dfg[['id_canti', 'mean_text_similarity', 'max_text_similarity', 'max_deviation']]

# export to csv
dfg.to_csv(config.PATH_MEAN_TEXT_SIMILARITIES, index=False)
print(f"📄 Esportato il file {config.PATH_MEAN_TEXT_SIMILARITIES} con successo.")
print("✅ Tutte similiarità medie sono state calcolate (insieme ai relativi massimi e deviazioni massime)!")

# domanda stupida: ma per calcolare la deviazione massima non era sufficiente sottrarre max_text_similarity a mean_text_similarity?
# non lo so, c'è da ragionarci
# mi sa di si. quindi era più semplice il calcolo.
