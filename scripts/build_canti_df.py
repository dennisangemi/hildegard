#!/usr/bin/env python3


# librairies
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import sys
import numpy as np
# import matplotlib.pyplot as plt


# importing costants
import config


# functions
from functions.hd_py_functions import get_text_from_file
from functions.hd_py_functions import get_files_from_dir
from functions.hd_py_functions import get_text_similarities


# ottieni un dizionario con id_canti e similarity tra il testo di riferimento e i testi dei canti
def get_all_text(filename_canti):
    # input
    # filename_canti: lista di nomi dei file contenenti i testi dei canti (generato con get_files_from_dir())

    # output
    # data:           dizionario con id_canti e testp del canto

    # carica i canti (una volta sola, e quindi solo se la variabile `canti` non esiste già)
    if 'canti' not in globals():
        print("🎵 Carico i testi dei canti...")
        global canti
        canti = []
        for canto in filename_canti:
            # WARNING: attenzione alla dipendenza da config.PATH_CANTI
            canti.append(re.sub(r'\n', ' ', get_text_from_file(os.path.join(config.PATH_CANTI, canto))))

    # remove the .txt extension from the file names
    filename_canti = [file[:-4] for file in filename_canti]

    # Create a dictionary with the file names and similarity values
    data = {'id_canti': filename_canti, 'content': canti}

    # output of the function
    return data


# importing tables
anagrafica = pd.read_csv(config.PATH_ANAGRAFICA_CANTI)


file_canti = get_files_from_dir(config.PATH_CANTI)
data = get_all_text(file_canti)
df = pd.DataFrame(data)
print(df.head())

# make id_canti int in order to merge with anagrafica
df['id_canti'] = df['id_canti'].astype(int)
anagrafica['id_canti'] = anagrafica['id_canti'].astype(int)

join = pd.merge(anagrafica, df, on='id_canti')
print(join.head())

# select columns id_canti, titolo, autore, content and export to csv
join = join[['id_canti', 'titolo', 'autore', 'content']]

# rename id_canti in id e remove autore column
# join = join.rename(columns={'id_canti': 'id'})
# join = join.drop(columns='autore')

join.to_csv(config.PATH_CANTI_DF, index=False)

