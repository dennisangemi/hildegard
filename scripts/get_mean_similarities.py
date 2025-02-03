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
from functions.hd_py_functions import get_similarities


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
    data = get_similarities(liturgia_text, file_canti)

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
print("📊 Calcolo la media normalizzata per ogni canto...")

# add mean and deviation
max_similarity = df['similarity'].max()

# normalize similarity
df['similarity'] = df['similarity'] / max_similarity

# Calcolo della media e del massimo della colonna 'similarity' per ogni 'id_canti'
df = df.groupby('id_canti')['similarity'].agg(['mean', 'max']).reset_index()

# Arrotonda la media e il massimo a 2 cifre decimali
df['mean'] = df['mean'].round(2)
df['max'] = df['max'].round(2)

# tieni solo righe con max_similarity > 0
df = df[df['max'] > 0]

# Rinominare le colonne per chiarezza
df = df.rename(columns={'mean': 'mean_similarity', 'max': 'max_similarity'})

# sort by mean_similarity
df = df.sort_values(by='mean_similarity', ascending=False)

print(df)

# turn mean_similarity into a percentage with no decimal
# df['mean_similarity'] = (df['mean_similarity'] * 100).round(2)

# export to csv
df.to_csv(config.PATH_MEAN_SIMILARITIES, index=False)
print(f"📄 Esportato il file {config.PATH_MEAN_SIMILARITIES} con successo.")
print("✅ Tutte similiarità medie sono state calcolate!")
