#!/usr/bin/env python3

# this script will transform the lezionario in a structured set of liturgie using anagrafica liturgie.

# importing libraries
import pandas as pd
import os

# constants
PATH_ANAGRAFICA_LITURGIE = 'risorse/lezionari/anagrafica_liturgie_cei.csv'
PATH_LEZIONARIO = 'risorse/lezionari/lezionario_anno_'
PATH_LITURGIE = 'risorse/lezionari/liturgie_anno_'
cicli_domenicali = ['A', 'B', 'C']

# funzione build_liturgie
def build_liturgie(lezionario, ciclo_domenicale, path_anagrafica_liturgie):
    anagrafica = pd.read_csv(path_anagrafica_liturgie)
    anagrafica = anagrafica[['id_liturgia', 'ciclo_domenicale', 'pagina_pdf']]
    anagrafica = anagrafica[anagrafica['ciclo_domenicale'] == ciclo_domenicale]
    anagrafica = anagrafica.drop(columns=['ciclo_domenicale'])
    anagrafica = anagrafica.rename(columns={'pagina_pdf': 'start_page'})
    anagrafica['end_page'] = anagrafica['start_page'].shift(-1) - 1
    anagrafica['end_page'] = anagrafica['end_page'].fillna(0).astype(int)
    # l'ultimo end_page deve essere l'ultimo valore della colonna pagina di lezionario
    anagrafica['end_page'].iloc[-1] = lezionario['pagina'].iloc[-1]
    rows = []
    for i in range(len(anagrafica)):
        start_page = anagrafica['start_page'].iloc[i]
        end_page = anagrafica['end_page'].iloc[i]
        liturgia_i = lezionario[lezionario['pagina'].between(start_page, end_page)]
        if not liturgia_i.empty:
            testo_liturgia_i = liturgia_i['testo'].str.cat(sep=' ')
            rows.append({'testo_liturgia': testo_liturgia_i, 'start_page': start_page})
    liturgie = pd.DataFrame(rows)
    anagrafica = anagrafica.drop(columns=['end_page'])
    liturgie = liturgie.merge(anagrafica, on='start_page')
    liturgie = liturgie.drop(columns=['start_page'])
    return liturgie

# Funzione per sostituire "9-10-2007" con una stringa vuota ""
def replace_date(text):
    return text.replace("9-10-2007", "")

# funzione per rimuovere le righe vuote iniziali e le righe vuote extra
def remove_empty_lines(text):
    lines = text.splitlines()  # Dividi il testo in righe

    # Trova l'indice della prima riga non vuota
    start_index = 0
    while start_index < len(lines) and lines[start_index].strip() == '':
        start_index += 1

    # Trova l'indice dell'ultima riga non vuota
    end_index = len(lines) - 1
    while end_index >= 0 and lines[end_index].strip() == '':
        end_index -= 1

    # Estrai le righe non vuote comprese tra start_index e end_index inclusi
    filtered_lines = lines[start_index:end_index + 1]

    # Ricostruisci il testo senza le righe vuote iniziali e le righe vuote extra
    modified_text = '\n'.join(filtered_lines)
    return modified_text

# main
for ciclo_domenicale in cicli_domenicali:
    path_lezionario = PATH_LEZIONARIO + ciclo_domenicale.lower() + '.csv'
    path_liturgie = PATH_LITURGIE + ciclo_domenicale.lower() + '.csv'
    lezionario = pd.read_csv(path_lezionario)
    liturgie = build_liturgie(lezionario, ciclo_domenicale, PATH_ANAGRAFICA_LITURGIE)
    liturgie.to_csv(path_liturgie, index=False)

# join le tre liturgie in un unico file
liturgie = pd.concat([pd.read_csv(PATH_LITURGIE + ciclo_domenicale.lower() + '.csv') for ciclo_domenicale in cicli_domenicali])

# cleaning
liturgie['testo_liturgia'] = liturgie['testo_liturgia'].apply(replace_date)
# liturgie['testo_liturgia'] = liturgie['testo_liturgia'].apply(remove_empty_lines)

liturgie['testo_liturgia'] = liturgie['testo_liturgia'].str.strip()

liturgie.to_csv('risorse/lezionari/liturgie.csv', index=False)

# rm le tre liturgie
for ciclo_domenicale in cicli_domenicali:
    path_liturgie = PATH_LITURGIE + ciclo_domenicale.lower() + '.csv'
    os.remove(path_liturgie)

# crea cartella liturgie in risorse
if not os.path.exists('risorse/lezionari/liturgie'):
    os.makedirs('risorse/lezionari/liturgie')

# split liturgie in files singoli aventi per filename l'id_liturgia
for index, row in liturgie.iterrows():
    id_liturgia = row['id_liturgia']
    testo_liturgia = row['testo_liturgia']
    with open('risorse/lezionari/liturgie/' + str(id_liturgia) + '.txt', 'w') as file:
        file.write(testo_liturgia)

print('Liturgie create con successo!')
