#!/usr/bin/env python3

# questo script analizza la similiarità tra i testi dei canti e i testi delle liturgie
# si basa sui risultati di all_similarities.csv ottentuti con get_all_similarities.py

# to do 
# - generare delle label basate su deviazione normalizzata per classifficare l'adeguatezza dei canti per una liturgia (alta, buona, bassa)

# constants
INPUT_FILE = 'data/all_similarities.csv'

# libraries
import pandas as pd
import matplotlib.pyplot as plt

# load data
df = pd.read_csv(INPUT_FILE)

# preview
print(df.head())

# max and min similarity
print('Max similarity:', df['similarity'].max())
print('Min similarity:', df['similarity'].min())

max_similarity = df['similarity'].max()

# normalize similarity
df['similarity'] = df['similarity'] / max_similarity

# turn similarity into a percentage with no decimal
df['similarity'] = (df['similarity'] * 100).astype(int)

# plot hist of similarity
# plt.hist(df['similarity'], bins=30)
# plt.xlabel('Similarity')
# plt.ylabel('Frequency')
# plt.show()

# Calcolo della media della colonna 'similarity' per ogni 'id_canti' e associazione del risultato a ogni riga
df['mean_similarity'] = df.groupby('id_canti')['similarity'].transform('mean')

# add deviation from the mean
df['deviation'] = df['similarity'] - df['mean_similarity']
devs = df[['id_canti','similarity','mean_deviation','deviation','id_liturgia']]
devs = devs.drop_duplicates()

# print size of the dataset
print(devs.shape)

# fammi vedere i primi 10 più devianti
print(devs.sort_values(by='deviation', ascending=False).head(10))

# plot hist of deviation
plt.hist(devs['deviation'], bins=30)
plt.xlabel('Deviation')
plt.ylabel('Frequency')
plt.show()

# direi di escludere tutti i canti che hanno deviazione < 10
devs = devs[devs['deviation'] > 10]

# print size of the dataset
print(devs.shape)

print(devs.head())

# fammi vedere i primi 10 meno devianti
print(devs.sort_values(by='deviation', ascending=True).head(10))

# controlla se id canto 1879 è in devs e ordina per deviation (preconio pasquale)
print(devs[devs['id_canti'] == 1879].sort_values(by='deviation', ascending=False))
# il preconio pasquale ha il massimo di dev pari a 23.27 per la notte di pasqua C23
# il preconio pasquale, dopo il 23 a 16 per natale (wtf)
# forse quindi conviene manentere solo i cantici con deviazione > 20 o di 15 o di 17?

# controllare ad esempio io ti amo signore mia forza tu sei 2432 con liturgia C65-A perchè mi pare che non va

# plot hist of deviation
plt.hist(devs['deviation'], bins=30)
plt.xlabel('Deviation')
plt.ylabel('Frequency')
plt.show()

# già questo secondo me è un buon risultato


# ----------- mean similarity per canto ------------ #

# select only id_canti similarity and mean_similarity columns
df = df[['id_canti', 'titolo','mean_similarity']]

# delete duplicates
df = df.drop_duplicates()

# size of the dataset
print(df.shape)

# Stampa delle prime righe per verificare il risultato
print(df.head())

# plot distribution of mean similarity
plt.hist(df['mean_similarity'], bins=30)
plt.xlabel('Mean similarity')
plt.ylabel('Frequency')
plt.show()

# max and min similarity
print('Max mean similarity:', df['mean_similarity'].max())
print('Min mean similarity:', df['mean_similarity'].min())

# fammi vedere i canti con la similarità più alta
print(df.sort_values(by='mean_similarity', ascending=False).head())