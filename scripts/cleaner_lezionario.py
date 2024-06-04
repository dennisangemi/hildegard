#!/usr/bin/env python3

import pandas as pd

INPUT_FILE = 'liturgie/lezionari/raw_lezionario_anno_b.csv'
OUTPUT_FILE = 'liturgie/lezionari/lezionario_anno_b.csv'

# leggi il file csv
df = pd.read_csv(INPUT_FILE)

def clean_text_column(df, column):
    # rimuovi il ritorno a capo e il trattino
    df[column] = df[column].str.replace(r'(\w+)-\n', r'\1')
    # se nella colonna testo vi è una parola maiuscola con una sola lettera e poi il rigo successivo comincia con una parola minuscola, allora rimuovi carattere newline e attacca la maiuscola al resto della parola minuscola
    df[column] = df[column].str.replace(r'([A-Z])\n([a-z])', r'\1\2')
    # rimuovi tutti i ritorni a capo di una cella e sostituiscili con uno spazio
    df[column] = df[column].str.replace(r'\n', ' ')
    # rimuovi spazi superflui
    df[column] = df[column].str.replace(r'\s+', ' ')

# pulisci la colonna testo
clean_text_column(df, 'testo')

# salva il file csv
df.to_csv(OUTPUT_FILE, index=False)