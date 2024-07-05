#!/usr/bin/env python3

# questo script calcola la similarità tra tutte le liturgie e tutti i testi dei canti

# librairies
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import sys

# importing costants
import config

# costants (input)
# config.PATH_ANAGRAFICA_CANTI = 'data/anagrafica_canti.csv'
# config.PATH_CANTI = 'risorse/canti'
# config.PATH_LITURGIE = 'risorse/lezionari/liturgie'
# 
# # costants (output)
# config.PATH_SIMILARITIES = 'data/similarities.csv'



# functions

# ottieni il testo da un file
def get_text_from_file(file):
      with open(file, 'r') as f:
         return f.read()

# ottieni la lista di file da una directory
def get_files_from_dir(directory):
      return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# ottieni un dizionario con id_canti e similarity tra il testo di riferimento e i testi dei canti
def get_similarities(text_to_compare, filename_canti):
    # input
    # liturgia:       testo della liturgia o testo di riferimento
    # filename_canti: lista di nomi dei file contenenti i testi dei canti (generato con get_files_from_dir())

    # output
    # data:           dizionario con id_canti e similarity

    # carica i canti (una volta sola, e quindi solo se la variabile `canti` non esiste già)
    if 'canti' not in globals():
        print("🎵 Carico i testi dei canti...")
        global canti
        canti = []
        for canto in file_canti:
            canti.append(re.sub(r'\n', ' ', get_text_from_file(os.path.join(config.PATH_CANTI, canto))))

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

    # output of the function
    return data



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
print("📊 Calcolo la media normalizzata e la deviazione della similarità per ogni canto...")

# add mean and deviation
max_similarity = df['similarity'].max()

# normalize similarity
df['similarity'] = df['similarity'] / max_similarity

# turn similarity into a percentage with no decimal
df['similarity'] = (df['similarity'] * 100).round(2)

# Calcolo della media della colonna 'similarity' per ogni 'id_canti' e associazione del risultato a ogni riga
df['mean_similarity'] = df.groupby('id_canti')['similarity'].transform('mean')

# crea un nuovo df con la colonna univoca id_canti e mean_similarity
# mean_similarity = df.groupby('id_canti')['similarity'].mean().reset_index()
# 
# # preview mean_similarity
# print(mean_similarity.head())
# 
# #shape of mean_similarity
# print(mean_similarity.shape)
# 
# # wait for user input
# input("Press Enter to continue...")

# add deviation from the mean
df['deviation'] = df['similarity'] - df['mean_similarity']

# ruound mean and deviation to 2 decimal places
df['mean_similarity'] = df['mean_similarity'].round(2)
df['deviation'] = df['deviation'].round(2)

# sort df by id_liturgia and by deviation
df = df.sort_values(by=['id_liturgia', 'deviation'], ascending=[True, False])

# export to csv
df.to_csv(config.PATH_SIMILARITIES, index=False)
print(f"📄 Esportato il file {config.PATH_SIMILARITIES} con successo.")
print("✅ Tutte similiarità con deviazioni sono state calcolate!")

# qui posso fare eventualmente il merging con l'anagrafica per una preview dei risultati ma non serve
# import anagrafica_canti.csv
# anagrafica = pd.read_csv(config.PATH_ANAGRAFICA_CANTI)

# questo script continua con similarities_analyzer.py