#!/usr/bin/env python3

import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import config

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
        for canto in filename_canti:
            # WARNING: attenzione alla dipendenza da config.PATH_CANTI
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