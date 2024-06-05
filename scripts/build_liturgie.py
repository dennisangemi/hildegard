#!/usr/bin/env python3

# this script will transform the lezionario in a structured set of liturgie using anagrafica liturgie.

# importing libraries
import pandas as pd
import os

# constants
PATH_ANAGRAFICA_LITURGIE = 'liturgie/lezionari/anagrafica_liturgie_cei.csv'
PATH_LEZIONARIO = 'liturgie/lezionari/lezionario_anno_'
PATH_LITURGIE = 'liturgie/lezionari/liturgie_anno_'
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

# main
for ciclo_domenicale in cicli_domenicali:
    path_lezionario = PATH_LEZIONARIO + ciclo_domenicale.lower() + '.csv'
    path_liturgie = PATH_LITURGIE + ciclo_domenicale.lower() + '.csv'
    lezionario = pd.read_csv(path_lezionario)
    liturgie = build_liturgie(lezionario, ciclo_domenicale, PATH_ANAGRAFICA_LITURGIE)
    liturgie.to_csv(path_liturgie, index=False)

# join le tre liturgie in un unico file
liturgie = pd.concat([pd.read_csv(PATH_LITURGIE + ciclo_domenicale.lower() + '.csv') for ciclo_domenicale in cicli_domenicali])
liturgie.to_csv('liturgie/lezionari/liturgie.csv', index=False)

# rm le tre liturgie
for ciclo_domenicale in cicli_domenicali:
    path_liturgie = PATH_LITURGIE + ciclo_domenicale.lower() + '.csv'
    os.remove(path_liturgie)

