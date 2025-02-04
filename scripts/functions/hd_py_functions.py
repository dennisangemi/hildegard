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



# ottieni un dizionario con id_canti e text_similarity tra il testo di riferimento e i testi dei canti
def get_text_similarities(text_to_compare, filename_canti):
    # input
    # liturgia:       testo della liturgia o testo di riferimento
    # filename_canti: lista di nomi dei file contenenti i testi dei canti (generato con get_files_from_dir())

    # output
    # data:           dizionario con id_canti e text_similarity

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

    # Create a dictionary with the file names and text_similarity values
    data = {'id_canti': filename_canti, 'text_similarity': similarities}

    # output of the function
    return data



# converti liturgia da txt a md
def text_formatter(input_file, output_file):
   # input:
   # input_file:  percorso del file txt da convertire

   # output:
   # output_file: percorso del file md convertito

   with open(input_file, 'r', encoding='utf-8') as f:
      lines = f.readlines()

   markdown_lines = []
   n_lines = enumerate(lines)

   for i, line in n_lines:
      line = line.strip()

      # Prima riga come titolo di secondo livello
      if i == 0:
         markdown_lines.append(f"## {line}")

      # se la linea contiene "PRIMA LETTURA" oppure "SECONDA LETTURA" oppure "VANGELO", trasformo in titolo di terzo livello 
      elif re.search(r'PRIMA LETTURA|SECONDA LETTURA|VANGELO', line):
         # if line not contain "CANTO AL VANGELO"
         if not re.search(r'CANTO AL VANGELO', line):
            markdown_lines.append(f"### {line}")

            # trasformo in corsivo la riga successiva
            next_line = next(n_lines)
            markdown_lines.append(f"*{next_line[1].strip()}*")

            # trasforma  la riga successivo in niente
            next_line = next(n_lines)
            markdown_lines.append(f"{next_line[1].strip()}")

            # trasforma la riga successiva concantenando ":material-book-open-outline:" con la riga
            next_line = next(n_lines)
            markdown_lines.append(f":material-book-open-outline: {next_line[1].strip()}")

            # trasforma la riga successiva in niente
            next_line = next(n_lines)
            markdown_lines.append(f"{next_line[1].strip()}")

            # trasforma la riga successiva in niente
            next_line = next(n_lines)
            markdown_lines.append(f"{next_line[1].strip()}")
         else:
            # formatto il canto al vangelo
            markdown_lines.append(f"### {line}")
            next_line = next(n_lines)
            markdown_lines.append(f":material-book-open-outline: {next_line[1].strip()}")
            next_line = next(n_lines)
            markdown_lines.append(f"{next_line[1].strip()}")
      
      # formatto salmo responsoriale
      elif re.search(r'SALMO', line):
         markdown_lines.append(f"### {line}")

         # riferimento dalmo
         next_line = next(n_lines)
         markdown_lines.append(f":material-book-open-outline: {next_line[1].strip()}")

         # riga vuota
         next_line = next(n_lines)
         markdown_lines.append(f"{next_line[1].strip()}")

         # ritornello
         next_line = next(n_lines)
         markdown_lines.append(f">**{next_line[1].strip()}**")

         # riga vuota
         next_line = next(n_lines)
         markdown_lines.append(f"{next_line[1].strip()}")

      elif line.isupper():
         # Titoli di terzo livello
         markdown_lines.append(f"### {line}")
      else:
         markdown_lines.append(f"> {line}")

   with open(output_file, 'w', encoding='utf-8') as f:
      f.write('\n'.join(markdown_lines))

