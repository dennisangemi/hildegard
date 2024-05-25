#!/usr/bin/env python3
#shebang per python


# confronta il testo del file liturgia.txt con il testo di ogni file in canti/*.txt e dammi un indice di somiglianza
# per ogni canto

import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def get_text_from_file(file):
      with open(file, 'r') as f:
         return f.read()


def get_files_from_dir(directory):
      return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


# apri liturgia.txt
liturgia = get_text_from_file(os.path.join('liturgie', 'liturgia-latest.txt'))

# apri un canto
file_canti = get_files_from_dir('canti')

# per ogni elemento di file_canti estrai il testo e salvalo in un vettore concatenato
canti = []
for canto in file_canti:
    canti.append(re.sub(r'\n', ' ', get_text_from_file(os.path.join('canti', canto))))

# calcola la similarità tra liturgia e canti
# reference_text = liturgia
# texts = canti

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



# stampa il nome del file e il valore di similarità
# for i in range(len(file_canti)):
#     print(f"{file_canti[i]}: {similarities[i]:.2f}")

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

# Stampa il risultato
print(f"Il testo più simile è: ' {result.titolo[most_similar_index]} ' con una similarità di {similarities[most_similar_index]:.2f}")
print("")

# sort the DataFrame by similarity
result = result.sort_values(by='similarity', ascending=False)

# Print only titolo and similarity columns primi 20
print(result[['titolo', 'id_canti', 'similarity']].head(20))