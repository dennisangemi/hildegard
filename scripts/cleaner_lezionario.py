#!/usr/bin/env python3

import pandas as pd
import re

INPUT_FILE = 'liturgie/lezionari/raw_nr_lezionario_anno_c.csv'
OUTPUT_FILE = 'liturgie/lezionari/nr_lezionario_anno_c.csv'



def clean_text_column(df, column):
    # rimuovi il ritorno a capo e il trattino
    df[column] = df[column].str.replace(r'(\w+)-\n', r'\1')
    # se nella colonna testo vi è una parola maiuscola con una sola lettera e poi il rigo successivo comincia con una parola minuscola, allora rimuovi carattere newline e attacca la maiuscola al resto della parola minuscola
    df[column] = df[column].str.replace(r'([A-Z])\n([a-z])', r'\1\2')
    # rimuovi tutti i ritorni a capo di una cella e sostituiscili con uno spazio
    df[column] = df[column].str.replace(r'\n', ' ')
    # rimuovi spazi superflui
    df[column] = df[column].str.replace(r'\s+', ' ')



# Funzione per modificare il testo come richiesto
def modifica_testo_v1(testo):
    # Cerca una parola di una sola lettera maiuscola alla fine
    match = re.search(r' (\b\w\b)$', testo)
    if match:
        lettera = match.group(1).strip()
        # Rimuovi la lettera dalla fine e concatenala con la prima parola
        nuovo_testo = testo[:match.start(1)].strip()
        prima_parola = nuovo_testo.split()[0]
        resto_testo = ' '.join(nuovo_testo.split()[1:])
        return lettera + prima_parola + ' ' + resto_testo
    else:
        return testo

def modifica_testo_v2(testo):
    # Controlla se il primo carattere della prima parola è minuscolo
    prima_parola = testo.split()[0]
    if prima_parola[0].islower():
        # Cerca una parola di una sola lettera alla fine
        match = re.search(r' (\b\w\b)$', testo)
        if match:
            lettera = match.group(1).strip()
            # Rimuovi la lettera dalla fine e concatenala con la prima parola
            nuovo_testo = testo[:match.start(1)].strip()
            resto_testo = ' '.join(nuovo_testo.split()[1:])
            return lettera + prima_parola + ' ' + resto_testo
    return testo


def modifica_testo(testo):
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
            pos_punto = [(m.start(), m.end()) for m in re.finditer(r'\.\s+[a-z]', testo)]
            if pos_punto:
                # Usa l'ultima occorrenza trovata
                start, end = pos_punto[-1]
                nuovo_testo = testo[:end] + ultima_parola + testo[end:].strip()
                return nuovo_testo[:-2]  # Rimuovi la lettera maiuscola dalla fine
    return testo



# leggi il file csv
df = pd.read_csv(INPUT_FILE)

# pulisci la colonna testo
clean_text_column(df, 'testo')

# Applica la funzione a ogni cella della colonna 'testo'
df['testo'] = df['testo'].apply(modifica_testo)

df['testo'][8]

# salva il file csv
df.to_csv(OUTPUT_FILE, index=False)