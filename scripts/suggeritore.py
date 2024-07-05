#!/usr/bin/env python3

# questo script calcola la similarità tra il testo della liturgia e i testi dei canti

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

# get variable from command line
if len(sys.argv) > 1:
    data_liturgia = sys.argv[1]
    print(f"La data della liturgia prossima liturgia che includo nei json è: {data_liturgia}")
else:
    print("Nessun valore passato come argomento.")

# ottieni il testo della liturgia
liturgia = get_text_from_file(config.PATH_LITURGIA)

# testo di riferimento per testare il codice
# liturgia = "Popoli tutti battete le mani"

# genera lista di filename contenuti in directory config.PATH_CANTI
file_canti = get_files_from_dir(config.PATH_CANTI)

# per ogni elemento di file_canti estrai il testo e salvalo in un vettore concatenato
# `canti` è una list contenente i testi dei canti
canti = []
for canto in file_canti:
    canti.append(re.sub(r'\n', ' ', get_text_from_file(os.path.join(config.PATH_CANTI, canto))))

# calcolo similatirà
data = get_similarities(liturgia, file_canti, canti)

# Create a DataFrame from the dictionary
df = pd.DataFrame(data)

# make id column an integer
df['id_canti'] = df['id_canti'].astype(int)

# import anagrafica_canti.csv
anagrafica = pd.read_csv(config.PATH_ANAGRAFICA_CANTI)

# merge df and anagrafica on id_canti column
df = pd.merge(df, anagrafica, on='id_canti')

# make similarity a percentage
df.similarity = df.similarity.round(2)*100
df.similarity = df.similarity.astype(int)

# sort the DataFrame by similarity
df = df.sort_values(by='similarity', ascending=False)

# preview
print(" ⏯ I testi più simili sono:") 
print(df.head())

# pause until user input
# input("Press Enter to continue...")

# export to csv
output_df_path = 'data/suggerimenti-latest.csv'
df.to_csv(output_df_path, index=False)

# crea una nuova colonna titolo_md che contenga '[' + df.titolo + '](https://www.librettocanti.it/mod_canti_gestione#!canto/vedi/' + df.id_canti  +')'
# se link_youtube è NaN, non mettere il link e lascia titolo, altrimenti '[' + df['titolo'] + '](https://www.librettocanti.it/mod_canti_gestione#!canto/vedi/' + df['id_canti'] + ')'
df['titolo_md'] = df.apply(lambda row: row['titolo'] if pd.isnull(row['id_canti']) else '[' + row['titolo'] + '](https://www.librettocanti.it/mod_canti_gestione#!canto/vedi/' + str(row['id_canti']) + ')', axis=1)

# prima di esportare aggiungi data_liturgia a tutti quelli che saranno json (top20 e i 4 momenti)
df['data'] = data_liturgia

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
df.head(20).drop(columns=['titolo_md']).fillna('').to_json('data/suggeriti-top20-latest.json', orient='records')
suggested_ingresso.drop(columns=['titolo_md']).fillna('').to_json('data/suggeriti-ingresso-latest.json', orient='records')
suggested_offertorio.drop(columns=['titolo_md']).fillna('').to_json('data/suggeriti-offertorio-latest.json', orient='records')
suggested_comunione.drop(columns=['titolo_md']).fillna('').to_json('data/suggeriti-comunione-latest.json', orient='records')
suggested_congedo.drop(columns=['titolo_md']).fillna('').to_json('data/suggeriti-congedo-latest.json', orient='records')

# select only the columns we need
suggested_ingresso = suggested_ingresso[['titolo_md', 'similarity', 'autore', 'raccolta']].fillna('')
suggested_offertorio = suggested_offertorio[['titolo_md', 'similarity', 'autore', 'raccolta']].fillna('')
suggested_comunione = suggested_comunione[['titolo_md', 'similarity', 'autore', 'raccolta']].fillna('')
suggested_congedo = suggested_congedo[['titolo_md', 'similarity', 'autore', 'raccolta']].fillna('')

# rename columns
md_cols = ['Titolo', 'Similarità (%)', 'Autore', 'Raccolta']
suggested_ingresso.columns = md_cols
suggested_offertorio.columns = md_cols
suggested_comunione.columns = md_cols
suggested_congedo.columns = md_cols

md_res = df[['titolo_md', 'similarity','autore', 'raccolta']].head(20).fillna('')
md_res.columns = md_cols

# export data to csv
md_res.to_csv('data/suggeriti-top20-latest.csv', index=False)
suggested_ingresso.to_csv('data/suggeriti-ingresso-latest.csv', index=False)
suggested_offertorio.to_csv('data/suggeriti-offertorio-latest.csv', index=False)
suggested_comunione.to_csv('data/suggeriti-comunione-latest.csv', index=False)
suggested_congedo.to_csv('data/suggeriti-congedo-latest.csv', index=False)

# end
print("📄 I suggerimenti sono stati scritti nel file", output_df_path)                         

