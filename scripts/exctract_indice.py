#!/usr/bin/env python3

import pandas as pd
import re
import io

# constant
INPUT_FILE = 'liturgie/lezionari/raw_lezionario_anno_b.csv'
OUTPUT_FILE = 'liturgie/lezionari/indice_anno_b.csv'

# import input file
df = pd.read_csv(INPUT_FILE)

# seleziona solo righe con colonna pagina uguale a 565 oppure 566 o 567
df = df[df['pagina'].isin([553, 554, 555])]

# rimuovi la colonna pagina e salva la colonna testo come unica variabile stringa
testo = ' '.join(df['testo'].tolist())

# rimuovi tutti i punti da testo
testo = testo.replace('.', '')

# alla fine di ogni riga c'è un numero. Aggiungi una sola virgola prima di ogni numero
testo = re.sub(r'(\d+)', r',\1', testo)

print(testo)

# esporta il testo in un file csv
with io.open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(testo)

