#!/usr/bin/env python3

# questo script calcola la similarità tra tutte le liturgie e tutti i testi dei canti

# librairies
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import sys



# costants
CANTI_DIR = 'risorse/canti'
PATH_ANAGRAFICA_CANTI = 'data/anagrafica_canti.csv'
PATH_LITURGIE = 'risorse/lezionari/liturgie'
OUTPUT_FILE = 'data/all_similarities.csv'



# functions

# ottieni il testo da un file
def get_text_from_file(file):
      with open(file, 'r') as f:
         return f.read()

# ottieni la lista di file da una directory
def get_files_from_dir(directory):
      return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# ottieni un dizionario con id_canti e similarity tra il testo di riferimento e i testi dei canti
def get_similarities(text_to_compare, filename_canti, canti):
    # input
    # liturgia:       testo della liturgia o testo di riferimento
    # filename_canti: lista di nomi dei file contenenti i testi dei canti (generato con get_files_from_dir())
    # canti:          lista di testi dei canti

    # output
    # data:           dizionario con id_canti e similarity

    # Unisci il testo di riferimento con gli altri testi
    all_texts = [text_to_compare] + canti

    # Inizializza il vettorizzatore TF-IDF
    vectorizer = TfidfVectorizer()

    # Calcola i vettori TF-IDF per tutti i testi
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # La prima riga del tfidf_matrix è il nostro testo di riferimento
    reference_vector = tfidf_matrix[0]

    # Calcola la similarità coseno tra il testo di riferimento e tutti gli altri testi
    similarities = cosine_similarity(reference_vector, tfidf_matrix[1:])

    # Estrai i valori di similarità come una lista
    similarities = similarities.flatten()

    # Trova l'indice del testo con la massima similarità
    most_similar_index = similarities.argmax()

    # remove the .txt extension from the file names
    filename_canti = [file[:-4] for file in filename_canti]

    # Create a dictionary with the file names and similarity values
    data = {'id_canti': filename_canti, 'similarity': similarities}

    return data



# main
print("🔎 Calcolo la similarità tra la liturgia e i testi dei canti...")

# genera lista di filename contenuti in directory CANTI_DIR
file_canti = get_files_from_dir(CANTI_DIR)

# per ogni elemento di file_canti estrai il testo e salvalo in un vettore concatenato
# `canti` è una list contenente i testi dei canti
canti = []
for canto in file_canti:
    canti.append(re.sub(r'\n', ' ', get_text_from_file(os.path.join(CANTI_DIR, canto))))

# import anagrafica_canti.csv
anagrafica = pd.read_csv(PATH_ANAGRAFICA_CANTI)

# fai tutto quello che c'è sopra (cioè calcola la similarità con tutti i testi canti) per ogni liturgia testo file presente in risorse/lezionari/liturgia
# ottieni la lista di file di testo della liturgia
liturgia_files = get_files_from_dir(PATH_LITURGIE)

# lista di DataFrame
df_list = []

# per ogni file di testo della liturgia
for liturgia_file in liturgia_files:
    # ottieni il testo della liturgia
    liturgia_text = get_text_from_file(os.path.join(PATH_LITURGIE, liturgia_file))
    # calcola la similarità con i testi dei canti
    data = get_similarities(liturgia_text, file_canti, canti)
    # Create a DataFrame from the dictionary
    df = pd.DataFrame(data)
    # make id column an integer
    df['id_canti'] = df['id_canti'].astype(int)
    # merge df and anagrafica on id_canti column
    df = pd.merge(df, anagrafica, on='id_canti')
    # select only columns id_canti similatiry titolo
    df = df[['id_canti', 'similarity', 'titolo']]
    # make similarity a percentage
    df.similarity = df.similarity.round(2)*100
    df.similarity = df.similarity.astype(int)
    # sort the DataFrame by similarity
    df = df.sort_values(by='similarity', ascending=False)
    # add to df the liturgia_file column withouth the .txt extension
    df['id_liturgia'] = liturgia_file[:-4]
    # append the result to a df_list
    df_list.append(df)
    # display the size of the list df
    print(f"La lista df_list ha {len(df_list)} elementi.")
    # preview dell'ultimo elemento della lista
    # print(" ⏯ I testi più simili sono:")
    # print(df_list[-1].head())
    # input("Press Enter to continue...")

# concatena tutti i DataFrame in df_list
df = pd.concat(df_list)

# export to csv
df.to_csv(OUTPUT_FILE, index=False)
print(f"Esportato il file {OUTPUT_FILE} con successo.")
print("Fine del programma.")

# questo script continua con similarities_analyzer.py