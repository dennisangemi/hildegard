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


# costants
# OUTPUT_FILE = 'suggerimenti.md'
# config.PATH_CANTI = 'risorse/canti'
# config.PATH_LITURGIA = 'risorse/lezionari/liturgia-latest.txt'
# config.PATH_ANAGRAFICA_CANTI = 'data/anagrafica_canti.csv'
# config.PATH_LITURGIE = 'risorse/lezionari/liturgie'
# config.PATH_TEXT_SIMILARITIES = 'data/all_similarities.csv'
# config.PATH_CALENDARIO_LITURGICO = 'data/calendari_liturgici/calendario_2019-2050.csv'
MIN_THRESHOLD_DEVIATION = 5



# functions

# ottieni il testo da un file
def get_text_from_file(file):
      with open(file, 'r') as f:
         return f.read()

# ottieni la lista di file da una directory
def get_files_from_dir(directory):
      return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# ottieni un dizionario con id_canti e similarity tra il testo di riferimento e i testi dei canti
def get_text_similarities(text_to_compare, filename_canti, canti):
    # INPUT
    # liturgia:       testo della liturgia o testo di riferimento
    # filename_canti: lista di nomi dei file contenenti i testi dei canti (generato con get_files_from_dir())
    # canti:          lista di testi dei canti
    # OUTPUT
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
    # percentage
    similarities = similarities.round(2)*100
    similarities = similarities.astype(int)
    # Trova l'indice del testo con la massima similarità
    most_similar_index = similarities.argmax()
    # remove the .txt extension from the file names
    filename_canti = [file[:-4] for file in filename_canti]
    # Create a dictionary with the file names and similarity values
    data = {'id_canti': filename_canti, 'similarity': similarities}
    return data

# funzione utile per ottenere le parti della liturgia 
def get_text_between_strings(text, start, end):
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    if start in text and end in text:
        return re.search(start + '(.*?)' + end, text, re.DOTALL).group(1)
    else:
        return ""



# main
print("🔎 Calcolo la similarità tra la liturgia e i testi dei canti...")

# get variable from command line
if len(sys.argv) > 1:
    data_liturgia = sys.argv[1]
    print(f"La data della liturgia prossima liturgia che includo nei json è: {data_liturgia}")
else:
    print("Nessun valore passato come argomento.")


# importing tables
anagrafica = pd.read_csv(config.PATH_ANAGRAFICA_CANTI)
calendario = pd.read_csv(config.PATH_CALENDARIO_LITURGICO)
similarities = pd.read_csv(config.PATH_TEXT_SIMILARITIES)

# cerca data_liturgia in calendario (colonna date) e estrai colonna id_liturgia
data_liturgia = "2024-06-30" # to comment
id_liturgia = calendario[calendario['date'] == data_liturgia]['id_liturgia'].values[0]
print(id_liturgia)

# filtra similarities per id_liturgia
similarities = similarities[similarities['id_liturgia'] == id_liturgia]

# remove titolo column
# similarities = similarities.drop(columns=['titolo'])
# non c'è bisogno di rimuoverlo perché non è presente nella nuova versione

# join con anagrafica by id_canti
similarities = pd.merge(similarities, anagrafica, on='id_canti')

# remove rows with momento column = 22 (atto penitenziale) and remove momento column = 23 (gloria)
similarities = similarities[similarities['momento'] != '22']
similarities = similarities[similarities['momento'] != '23']

# seleziona solo le righe con deviazione >= MIN_THRESHOLD_DEVIATION
similarities = similarities[similarities['deviation'] >= MIN_THRESHOLD_DEVIATION]

# sort by deviation
similarities = similarities.sort_values(by='deviation', ascending=False)

# preview
print(" ⏯ I testi più devianti sono:")
print(similarities.head())
print(similarities.shape)



# --------------------------------- SALMO E ANTIFONE --------------------------------- #

# test salmo e antifone
liturgia = get_text_from_file(os.path.join(config.PATH_LITURGIE, id_liturgia + '.txt'))
print(liturgia)

# genera lista di filename contenuti in directory config.PATH_CANTI
file_canti = get_files_from_dir(config.PATH_CANTI)

# per ogni elemento di file_canti estrai il testo e salvalo in un vettore concatenato
# `canti` è una list contenente i testi dei canti
canti = []
for canto in file_canti:
    canti.append(re.sub(r'\n', ' ', get_text_from_file(os.path.join(config.PATH_CANTI, canto))))

# estrai salmo
salmo = get_text_between_strings(liturgia, 'SALMO RESPONSORIALE', 'SECONDA LETTURA')

# se salmo non è vuoto, calcola la similarità tra salmo e i testi dei canti
if salmo:
    data_salmo = get_text_similarities(salmo, file_canti, canti)
    df_salmo = pd.DataFrame(data_salmo)
    df_salmo['id_canti'] = df_salmo['id_canti'].astype(int)
    df_salmo = df_salmo.sort_values(by='similarity', ascending=False)
    print(df_salmo.head())



###################################### wip ######################################

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

