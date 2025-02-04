#!/usr/bin/env python3

# questo script serve per pulire il file vector_similarities.csv dalle antifone non esistenti. 
# le uniche due cose che servono sono i path al file con le liturgie (in cui ci sono le letture splitted) e al 
# file con le similarità dei vettori.
# l'output sarà un file csv nella stessa posizione del file con le similarità dei vettori, ma con _cleaned nel nome.
# questo script è utile perchè get_vector_similarities.py ha un bug e include il punteggio di similarità anche per le antifone non esistenti.

# costanti
PATH_LITURGIE = 'risorse/lezionari/liturgie.csv'
PATH_VECTOR_SIMILARITIES = 'data/vector_similarities.csv'

# librairies
import pandas as pd

liturgie=pd.read_csv(PATH_LITURGIE)
vector_similarities=pd.read_csv(PATH_VECTOR_SIMILARITIES)
print("Dati caricati correttamente")

print("Dimensione iniziale di vector_similarities:")
print(vector_similarities.shape)

# ottieni la lista delle liturgie in cui le antifone esistono
liturgie_con_antifona_ingresso=liturgie[liturgie['antifona_ingresso'].notnull()]['id_liturgia']
# print(liturgie_con_antifona_ingresso.head())
liturgie_con_antifona_comunione=liturgie[liturgie['antifona_comunione'].notnull()]['id_liturgia']
# print(liturgie_con_antifona_comunione.head())

# filtra vector_similarities per avere solo le righe con antifona ingresso realmente esistenti
antifone_ingresso = vector_similarities[
   (vector_similarities['id_liturgia'].isin(liturgie_con_antifona_ingresso)) &
   (vector_similarities['riferimento'] == 'antifona_ingresso')
]
# print(antifone_ingresso.head())
# print(antifone_ingresso.shape)

# filtra vector_similarities per avere solo le righe con antifona comunione realmente esistenti
antifone_comunione = vector_similarities[
   (vector_similarities['id_liturgia'].isin(liturgie_con_antifona_ingresso)) &
   (vector_similarities['riferimento'] == 'antifona_comunione')
]
# print(antifone_comunione.head())
# print(antifone_comunione.shape)

# rimuovi da vector_similarities tutte le righe in cui `riferimento` è 'antifona_ingresso' oppure 'antifona_comunione'
vector_similarities = vector_similarities[
   (vector_similarities['riferimento'] != 'antifona_ingresso') &
   (vector_similarities['riferimento'] != 'antifona_comunione')
]
# print(vector_similarities.head())
# print("Ho rimosso tutte le antifone")

# aggiungi le righe di antifone_ingresso e antifone_comunione a vector_similarities
vector_similarities = pd.concat([vector_similarities, antifone_ingresso, antifone_comunione])
# print(vector_similarities.head())
# print("Ho aggiunto le antifone corrette")

# dimensione di vector_similarities
print("Dimensione finale di vector_similarities:")
print(vector_similarities.shape)

# L'output deve avere lo stesso path di PATH_VECTOR_SIMILARITIES ma con _cleaned nel nome file csv
vector_similarities.to_csv(PATH_VECTOR_SIMILARITIES.replace('.csv', '_cleaned.csv'), index=False)
