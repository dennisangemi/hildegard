#!/usr/bin/env python3

# importing libraries
import pandas as pd
import re

# functions
def prima_pulizia_colonna(df, column):
    # rimuovi il ritorno a capo e il trattino
    df[column] = df[column].str.replace(r'(\w+)-\n', r'\1')
    # se nella colonna testo vi è una parola maiuscola con una sola lettera e poi il rigo successivo comincia con una parola minuscola, allora rimuovi carattere newline e attacca la maiuscola al resto della parola minuscola
    df[column] = df[column].str.replace(r'([A-Z])\n([a-z])', r'\1\2')
    # rimuovi tutti i ritorni a capo di una cella e sostituiscili con uno spazio
    df[column] = df[column].str.replace(r'\n', ' ')
    # rimuovi spazi superflui
    df[column] = df[column].str.replace(r'\s+', ' ')

"""
def prima_pulizia_v2(testo):
    nuovo_testo = testo.replace(r'(\w+)-\n', r'\1')
    nuovo_testo = nuovo_testo.replace(r'([A-Z])\n([a-z])', r'\1\2')
    # rimuovi tutti i ritorni a capo di una cella e sostituiscili con uno spazio
    nuovo_testo = nuovo_testo.replace(r'\n', ' ')
    # rimuovi spazi superflui
    nuovo_testo = nuovo_testo.replace(r'\s+', ' ')
    return nuovo_testo
"""

def riposiziona_maiuscole(testo):
    parole = testo.split()
    prima_parola = parole[0]
    ultima_parola = parole[-1]
    # Controlla se l'ultima parola è un solo carattere maiuscolo
    if len(ultima_parola) == 1 and ultima_parola.isupper():
        # Se la prima parola inizia con un carattere minuscolo
        if prima_parola[0].islower():
            # Rimuovi la lettera dalla fine e concatenala con la prima parola
            nuovo_testo = ' '.join(parole[:-1])
            resto_testo = ' '.join(nuovo_testo.split()[1:])
            return ultima_parola + prima_parola + ' ' + resto_testo
        # Se la prima parola inizia con un carattere maiuscolo
        elif prima_parola[0].isupper():
            # Trova l'ultima occorrenza di punto seguito da spazio e una parola che inizia con una lettera minuscola
            match = re.search(r'\.\s+[a-z]', testo)
            if match:
                # Inserisci la lettera maiuscola dopo il punto e lo spazio
                start, end = match.span()
                resto_parola_successiva = testo[end - 1:]
                nuovo_testo = testo[:end - 1] + ultima_parola + resto_parola_successiva
                # Rimuovi la lettera maiuscola dalla fine
                nuovo_testo = nuovo_testo.rsplit(' ', 1)[0]
                return nuovo_testo
    return testo

# constants
INPUT_FILE = 'liturgie/lezionari/raw_lezionario_anno_c.csv'
OUTPUT_FILE = 'liturgie/lezionari/lezionario_anno_c.csv'

# leggi il file csv
df = pd.read_csv(INPUT_FILE)

# pulisci la colonna testo
prima_pulizia_colonna(df, 'testo')
#df['testo'] = df['testo'].apply(prima_pulizia_v2)

# Applica la funzione a ogni cella della colonna 'testo'
df['testo'] = df['testo'].apply(riposiziona_maiuscole)

# salva il file csv
df.to_csv(OUTPUT_FILE, index=False)

# to do 
# transofrm prima_pulizia_colonna come riposiziona_maiuscole