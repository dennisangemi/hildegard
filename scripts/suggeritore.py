#!/usr/bin/env python3

# confronta il testo del file liturgia.txt con il testo di ogni file in canti/*.txt e dammi un indice di somiglianza
# per ogni canto

# librairies
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# costants
OUTPUT_FILE = 'suggerimenti.md'

# functions
def get_text_from_file(file):
      with open(file, 'r') as f:
         return f.read()

def get_files_from_dir(directory):
      return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# main
print("🔎 Calcolo la similarità tra la liturgia e i testi dei canti...")

# apri liturgia.txt
liturgia = get_text_from_file(os.path.join('liturgie', 'liturgia-latest.txt'))

# apri un canto
file_canti = get_files_from_dir('canti')

# per ogni elemento di file_canti estrai il testo e salvalo in un vettore concatenato
canti = []
for canto in file_canti:
    canti.append(re.sub(r'\n', ' ', get_text_from_file(os.path.join('canti', canto))))

# Unisci il testo di riferimento con gli altri testi
all_texts = [liturgia] + canti

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
file_canti = [file[:-4] for file in file_canti]

# Create a dictionary with the file names and similarity values
data = {'id_canti': file_canti, 'similarity': similarities}

# Create a DataFrame from the dictionary
df = pd.DataFrame(data)

# make id column an integer
df['id_canti'] = df['id_canti'].astype(int)

# import anagrafica_canti.csv
anagrafica = pd.read_csv('data/anagrafica_canti.csv')

# merge df and anagrafica on id_canti column
result = pd.merge(df, anagrafica, on='id_canti')
result.similarity = result.similarity.round(2)*100

# Stampa il risultato
print(f"⏯  Il testo più simile è: ' {result.titolo[most_similar_index]} ' con una similarità di {similarities[most_similar_index]:.2f}")
# print("")

# sort the DataFrame by similarity
result = result.sort_values(by='similarity', ascending=False)

# export to csv
result.to_csv('data/suggeriti-latest.csv', index=False)

# crea una nuova colonna titolo_md che contenga '[' + result.titolo + '](https://www.youtube.com/' + result.link_youtube  +')'
# se link_youtube è NaN, non mettere il link e lascia titolo, altrimenti '[' + result['titolo'] + '](https://www.youtube.com/' + result['link_youtube'] + ')'
result['titolo_md'] = result.apply(lambda row: row['titolo'] if pd.isnull(row['link_youtube']) else '[' + row['titolo'] + '](https://www.youtube.com/watch?v=' + row['link_youtube'] + ')', axis=1)

# exclude if momento columns is NaN
nonan=result.dropna(subset=['momento'])

# split momenti
suggested_ingresso = nonan[nonan['momento'].str.contains('21')].head(10)
suggested_offertorio = nonan[nonan['momento'].str.contains('26')].head(10)
suggested_comunione = nonan[nonan['momento'].str.contains('31')].head(10)
suggested_congedo = nonan[nonan['momento'].str.contains('32')].head(10)

# select only the columns we need
suggested_ingresso = suggested_ingresso[['titolo_md', 'similarity', 'autore', 'raccolta']].fillna('')
suggested_offertorio = suggested_offertorio[['titolo_md', 'similarity', 'autore', 'raccolta']].fillna('')
suggested_comunione = suggested_comunione[['titolo_md', 'similarity', 'autore', 'raccolta']].fillna('')
suggested_congedo = suggested_congedo[['titolo_md', 'similarity', 'autore', 'raccolta']].fillna('')

# rename columns
md_cols = ['Titolo', 'Similarità', 'Autore', 'Raccolta']
suggested_ingresso.columns = md_cols
suggested_offertorio.columns = md_cols
suggested_comunione.columns = md_cols
suggested_congedo.columns = md_cols

md_res = result[['titolo_md', 'similarity','autore', 'raccolta']].head(20).fillna('')
md_res.columns = md_cols

# crete a md file and write the result to it
with open(OUTPUT_FILE, 'w') as f:
      f.write('# Suggerimenti di animazione liturgica\n\n')
      f.write('## 📖 Liturgia\n')
      f.write('>' + liturgia)
      f.write('\n\n')
      f.write("# 🎵 Canti suggeriti\n\n")
      f.write("Ecco i 20 canti i cui testi sono più simili alla liturgia (indipendentemente dal momento liturgico)\n")
      f.write(md_res.to_markdown(index=False, ))
      f.write('\n\n')
      f.write("Di seguito i canti suggeriti per i vari momenti della liturgia\n\n")
      f.write('## Ingresso\n')
      f.write(suggested_ingresso.to_markdown(index=False))
      f.write('\n\n')
      f.write('## Offertorio\n')
      f.write(suggested_offertorio.to_markdown(index=False))
      f.write('\n\n')
      f.write('## Comunione\n')
      f.write(suggested_comunione.to_markdown(index=False))
      f.write('\n\n')
      f.write('## Congedo\n')
      f.write(suggested_congedo.to_markdown(index=False))


print("📄 I suggerimenti sono stati scritti nel file suggeriti.md e suggeriti-latest.csv")                         

# Print only titolo and similarity columns primi 20
# print(result[['titolo', 'id_canti', 'similarity']].head(20))

