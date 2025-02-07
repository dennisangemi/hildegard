#!/usr/bin/env python3

"""
Questo script suggerisce i canti liturgici più adatti per una determinata liturgia.

Il calcolo dell'accuratezza dipende da 4 score: text_similarity, deviation, selection e history
- Similarity: calcolato con cosine text_similarity tra la liturgia e i testi dei canti;
- Deviation (dalla media della similarità): calcolato come la differenza tra text_similarity e mean_text_similarity;
- Selection: accuratezza scelta manualmente;
- History: accuratezza basata sulla frequenza di suonata dei canti in passato grazie a librettocanti.it/canticristiani.it;

Refactor con classi: tutto il codice e la logica rimangono invariati, ma suddivisi in metodi.
"""

import os
import re
import sys
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# import constants
import config

# import functions
from functions.hd_py_functions import get_text_from_file
from functions.hd_py_functions import get_files_from_dir
from functions.hd_py_functions import get_text_similarities

# constants
N_MAX_SUGGESTIONS = 20
N_PEAKS = 10


class SuggeritoreRefactor:
    def __init__(self, data_liturgia):
        self.data_liturgia = data_liturgia
        self.id_liturgia = None

        # DataFrames
        self.anagrafica = None
        self.calendario = None
        self.mean_text_similarities = None
        self.weights = None
        self.manually_selected = None
        self.storico_suonati = None
        self.mean_suonati = None
        self.vector_similarities = None

        self.df = None

    def load_data(self):
        """Caricamento tabelle dal filesystem e inizializzazione variabili."""
        self.anagrafica = pd.read_csv(config.PATH_ANAGRAFICA_CANTI)
        self.calendario = pd.read_csv(config.PATH_CALENDARIO_LITURGICO)
        self.mean_text_similarities = pd.read_csv(config.PATH_MEAN_TEXT_SIMILARITIES)
        self.weights = pd.read_csv(config.PATH_WEIGHTS)
        self.manually_selected = pd.read_csv(config.PATH_MANUALLY_SELECTED)
        self.storico_suonati = pd.read_csv(config.PATH_STORICO_SUONATI)
        self.mean_suonati = pd.read_csv(config.PATH_MEAN_SUONATI)
        self.vector_similarities = pd.read_csv(config.PATH_VECTOR_SIMILARITIES)

    def get_liturgia_id(self):
        """Estrae id_liturgia dal calendario utilizzando la data passata come argomento."""
        self.id_liturgia = self.calendario[self.calendario['date'] == self.data_liturgia]['id_liturgia'].values[0]
        print("📖 La liturgia corrispondente alla data", self.data_liturgia, "è", self.id_liturgia)
        print("")

    def compute_vector_similarities(self):
        """Seleziona e rinomina la colonna vector_similarity in score_vector_similarity."""
        print("🔍 Canti consigliati secondo vicinanza embeddings:")
        self.vector_similarities = self.vector_similarities[self.vector_similarities['id_liturgia'] == self.id_liturgia]
        print(self.vector_similarities)

        self.vector_similarities = self.vector_similarities.rename(columns={'vector_similarity': 'score_vector_similarity'})
        self.vector_similarities = self.vector_similarities.sort_values(by='score_vector_similarity', ascending=False)
        self.vector_similarities = self.vector_similarities.drop_duplicates(subset='id_canti', keep='first')
        self.vector_similarities = self.vector_similarities[['id_canti', 'score_vector_similarity']]

    def compute_manually_selected(self):
        """Seleziona e normalizza lo score_selection (manual)."""
        print("🔍 Canti consigliati manualmente:")
        self.manually_selected = self.manually_selected[self.manually_selected['id_liturgia'] == self.id_liturgia]
        print(self.manually_selected)
        self.manually_selected = self.manually_selected.rename(columns={'accuratezza': 'score_selection'})
        self.manually_selected = self.manually_selected[['id_canti', 'score_selection']]
        self.manually_selected['score_selection'] = (self.manually_selected['score_selection'] / 100).round(2)
        print("")
        print("✅ Score (manual) selection determinato")

    def compute_storico_suonati(self):
        """Calcola lo score_history dei canti suonati in passato."""
        # filter storico_suonati
        self.storico_suonati = self.storico_suonati[self.storico_suonati['id_liturgia'] == self.id_liturgia]

        # drop colonna titolo da mean_suonati
        self.mean_suonati = self.mean_suonati.drop(columns=['titolo'])

        # merge
        self.storico_suonati = pd.merge(self.storico_suonati, self.mean_suonati, on='id_canti')

        self.storico_suonati['cnt/max'] = (self.storico_suonati['cnt'] / self.storico_suonati['max']).round(2)
        self.storico_suonati['norm_dev'] = ((self.storico_suonati['cnt'] - self.storico_suonati['mean']) / self.storico_suonati['cnt']).round(2)
        self.storico_suonati['cnt/max(cnt)'] = (self.storico_suonati['cnt'] / self.storico_suonati['cnt'].max()).round(2)

        self.storico_suonati['score_history'] = (
            (0.275 * self.storico_suonati['cnt/max']) +
            (0.275 * self.storico_suonati['norm_dev']) +
            (0.45 * self.storico_suonati['cnt/max(cnt)'])
        ).round(2)

        # normalizza score_history
        self.storico_suonati['score_history'] = (self.storico_suonati['score_history'] / self.storico_suonati['score_history'].max()).round(2)

        # keep only canti con score_history >= 0
        self.storico_suonati = self.storico_suonati[self.storico_suonati['score_history'] >= 0]

        # order by score_history
        self.storico_suonati = self.storico_suonati.sort_values(by='score_history', ascending=False)
        print("")
        print("🔍 Storico dei canti suonati per la liturgia:")
        print(self.storico_suonati)
        print("")
        print("✅ Score history determinato")
        print("")

        self.storico_suonati = self.storico_suonati[['id_canti', 'score_history']]

    def compute_text_similarity(self):
        """Calcola la similarità di testo tra liturgia e canti, e prepara df con score_text_similarity."""
        liturgia = get_text_from_file(os.path.join(config.PATH_LITURGIE, self.id_liturgia + '.txt'))
        file_canti = get_files_from_dir(config.PATH_CANTI)

        df_local = get_text_similarities(liturgia, file_canti)
        print("🔎 Calcolo la similarità tra la liturgia e i testi dei canti...")
        df_local = pd.DataFrame(df_local)

        df_local = df_local.rename(columns={'similarity': 'text_similarity'})

        print("min text_similarity:", df_local['text_similarity'].min())
        print("max text_similarity:", df_local['text_similarity'].max())
        print("")

        # sort
        df_local = df_local.sort_values(by='text_similarity', ascending=False)

        # join con mean_text_similarities
        df_local['id_canti'] = df_local['id_canti'].astype(int)
        self.mean_text_similarities['id_canti'] = self.mean_text_similarities['id_canti'].astype(int)
        df_local = pd.merge(df_local, self.mean_text_similarities, on='id_canti')

        print("min mean_text_similarity:", df_local['mean_text_similarity'].min())
        print("max mean_text_similarity:", df_local['mean_text_similarity'].max())
        print("")

        df_local['score_text_similarity_c1'] = (df_local['text_similarity'] / df_local['text_similarity'].max()).round(2)
        df_local['score_text_similarity_c2'] = (df_local['text_similarity'] / df_local['max_text_similarity']).round(2)
        df_local['score_text_similarity'] = (0.65 * df_local['score_text_similarity_c1'] + 0.35 * df_local['mean_text_similarity']).round(2)
        print(df_local)
        print("✅ Score text_similarity determinato")
        print("")

        # deviation
        df_local['deviation'] = df_local['text_similarity'] - df_local['mean_text_similarity']
        df_local = df_local.sort_values(by='deviation', ascending=False)

        print("max deviation:", df_local['deviation'].max())
        print("min deviation:", df_local['deviation'].min())

        df_local['max_deviation'] = df_local['max_text_similarity'] - df_local['text_similarity']
        df_local['score_deviation'] = df_local['deviation'] / df_local['max_deviation']

        print("max score_deviation:", df_local['score_deviation'].max())
        print("min score_deviation:", df_local['score_deviation'].min())
        print("✅ Score deviation determinato")
        print("")

        # keep only needed columns
        df_local = df_local[['id_canti', 'score_text_similarity', 'score_deviation']]
        self.df = df_local

    def compute_total_score(self):
        """Riunisce tutti gli score e calcola lo score totale."""
        # join with manually_selected
        if not self.manually_selected.empty:
            self.df = pd.merge(self.df, self.manually_selected, on='id_canti', how='left')
            print("Manually selected joined")

        # join with storico_suonati
        if not self.storico_suonati.empty:
            self.df = pd.merge(self.df, self.storico_suonati, on='id_canti', how='left')
            print("Storico suonati joined")

        # join with vector_similarities
        if not self.vector_similarities.empty:
            self.df = pd.merge(self.df, self.vector_similarities, on='id_canti', how='left')
            print("Vector similarities joined")

        # join with anagrafica
        self.anagrafica['id_canti'] = self.anagrafica['id_canti'].astype(int)
        self.df = pd.merge(self.df, self.anagrafica, on='id_canti')

        # rimuove i canti con momento non desiderato
        self.df = self.df[self.df['momento'] != '22']
        self.df = self.df[self.df['momento'] != '22,11']
        self.df = self.df[self.df['momento'] != '22,10,11']
        self.df = self.df[self.df['momento'] != '23']
        self.df = self.df[self.df['momento'] != '71']
        self.df = self.df[self.df['momento'] != '71,18']
        print("✂️  Signore pietà, Gloria e Agnello di Dio rimossi")

        # rimuove canti 'inutili'
        self.df = self.df[self.df['id_canti'] != 2624]
        self.df = self.df[self.df['id_canti'] != 1969]
        print("✂️  Canti 'inutili' rimossi")
        print("")

        # extracting weights
        weight_text_similarity = self.weights[self.weights['metric'] == 'text_similarity']['weight'].values[0]
        weight_vector_similarity = self.weights[self.weights['metric'] == 'vector_similarity']['weight'].values[0]
        weight_deviation = self.weights[self.weights['metric'] == 'deviation']['weight'].values[0]
        weight_history = self.weights[self.weights['metric'] == 'history']['weight'].values[0]
        weight_selection = self.weights[self.weights['metric'] == 'selection']['weight'].values[0]

        print("⚖️  Pesi caricati")
        print("   text_similarity   :", weight_text_similarity)
        print("   vector_similarity :", weight_vector_similarity)
        print("   sim deviation:", weight_deviation)
        print("   selection    :", weight_selection)
        print("   history      :", weight_history)
        print("")

        if 'score_selection' not in self.df.columns:
            self.df['score_selection'] = np.nan
        if 'score_vector_similarity' not in self.df.columns:
            self.df['score_vector_similarity'] = np.nan

        self.df['score'] = ((
            self.df['score_text_similarity'].fillna(0) * weight_text_similarity +
            self.df['score_vector_similarity'].fillna(0) * weight_vector_similarity +
            self.df['score_deviation'].fillna(0) * weight_deviation +
            self.df['score_selection'].fillna(0) * weight_selection +
            self.df['score_history'].fillna(0) * weight_history
        ) / (
            (self.df['score_text_similarity'].notna() * weight_text_similarity) +
            (self.df['score_vector_similarity'].notna() * weight_vector_similarity) +
            (self.df['score_deviation'].notna() * weight_deviation) +
            (self.df['score_selection'].notna() * weight_selection) +
            (self.df['score_history'].notna() * weight_history)
        )).round(2) * 100

        self.df = self.df.sort_values(by='score', ascending=False)

        print("")
        print(self.df[['id_canti', 'titolo', 'score_text_similarity', 'score_vector_similarity', 'score_history', 'score']].head(20))

    def compute_adeguatezza(self):
        """Calcola l'adeguatezza dei canti e filtra quelli sopra la soglia."""
        print("")
        print("📊 Sto calcolando l'adeguatezza dei canti...")

        def calcola_adeguatezza(row):
            if (row.get('score_selection', 0) >= 0.92) or ((row.get('score_history', 0) >= 0.9) and row['score'] >= 80) or (row['score'] >= 95):
                return ':material-check-all: Alta'
            elif 0.7 <= row.get('score_selection', 0) < 0.92:
                return ':material-check: Buona'
            else:
                return ':material-dots-horizontal: Mh'

        self.df['adeguatezza'] = self.df.apply(calcola_adeguatezza, axis=1)

        print("")
        print("Mostro solo canti > soglia")
        mask_soglia = self.df['score'] >= config.THRESHOLD_MIN_SCORE
        print(self.df[['id_canti', 'titolo', 'score_text_similarity', 'score_vector_similarity', 'score_deviation',
                       'score_selection', 'score_history', 'score', 'adeguatezza']][mask_soglia])

    def export_data(self):
        """Esporta i dati in CSV e JSON come da codice originale."""
        # export to csv
        output_df_path = 'data/suggerimenti-latest.csv'
        self.df[['id_canti', 'titolo', 'score_vector_similarity', 'score_text_similarity',
                 'score_deviation', 'score_selection', 'score_history', 'score',
                 'adeguatezza']].to_csv(output_df_path, index=False)

        # filtra sotto soglia
        filtered_df = self.df[self.df['score'] >= config.THRESHOLD_MIN_SCORE].copy()
        filtered_df = filtered_df.reset_index(drop=True)

        # crea colonna con link
        filtered_df['titolo_md'] = filtered_df.apply(lambda row: row['titolo'] if pd.isnull(row['id_canti'])
                                                     else '[' + row['titolo'] + '](https://www.librettocanti.it' +
                                                     str(row['url']) + ')', axis=1)
        filtered_df['data'] = self.data_liturgia
        filtered_df['score'] = filtered_df['score'].astype(int)

        # split momenti
        nonan = filtered_df.dropna(subset=['momento'])
        suggested_ingresso = nonan[nonan['momento'].str.contains('21')].head(10).fillna('')
        suggested_offertorio = nonan[nonan['momento'].str.contains('26')].head(10).fillna('')
        suggested_comunione = nonan[nonan['momento'].str.contains('31')].head(10).fillna('')
        suggested_congedo = nonan[nonan['momento'].str.contains('32')].head(10).fillna('')

        # export to json
        json_cols = ['id_canti', 'text_similarity', 'label', 'titolo', 'autore', 'raccolta', 'momento', 'link_youtube', 'data']
        top20 = filtered_df.rename(columns={'score': 'text_similarity', 'adeguatezza': 'label'})
        top20[json_cols].fillna('').sort_values(by='text_similarity', ascending=False).head(20).to_json('data/suggeriti-top20-latest.json', orient='records')

        ing_json = suggested_ingresso.rename(columns={'score': 'text_similarity', 'adeguatezza': 'label'})
        ing_json[json_cols].fillna('').sort_values(by='text_similarity', ascending=False).to_json('data/suggeriti-ingresso-latest.json', orient='records')

        off_json = suggested_offertorio.rename(columns={'score': 'text_similarity', 'adeguatezza': 'label'})
        off_json[json_cols].fillna('').sort_values(by='text_similarity', ascending=False).to_json('data/suggeriti-offertorio-latest.json', orient='records')

        com_json = suggested_comunione.rename(columns={'score': 'text_similarity', 'adeguatezza': 'label'})
        com_json[json_cols].fillna('').sort_values(by='text_similarity', ascending=False).to_json('data/suggeriti-comunione-latest.json', orient='records')

        cong_json = suggested_congedo.rename(columns={'score': 'text_similarity', 'adeguatezza': 'label'})
        cong_json[json_cols].fillna('').sort_values(by='text_similarity', ascending=False).to_json('data/suggeriti-congedo-latest.json', orient='records')

        print("")
        print("✅ I suggerimenti formattati per librettocanti sono stati scritti nei file json")
        print("📄 File prodotti:")
        print("   data/suggeriti-top20-latest.json")
        print("   data/suggeriti-ingresso-latest.json")
        print("   data/suggeriti-offertorio-latest.json")
        print("   data/suggeriti-comunione-latest.json")
        print("   data/suggeriti-congedo-latest.json")

        # export csv for hildegard
        md_cols = ['titolo_md', 'adeguatezza', 'score', 'autore', 'raccolta']
        md_cols_renamed = ['Titolo', 'Adeguatezza', '%', 'Autore', 'Raccolta']

        filtered_df[md_cols].head(20).fillna('').rename(columns=dict(zip(md_cols, md_cols_renamed))).to_csv('data/suggeriti-top20-latest.csv', index=False)
        suggested_ingresso[md_cols].fillna('').rename(columns=dict(zip(md_cols, md_cols_renamed))).head(10).to_csv('data/suggeriti-ingresso-latest.csv', index=False)
        suggested_offertorio[md_cols].fillna('').rename(columns=dict(zip(md_cols, md_cols_renamed))).head(10).to_csv('data/suggeriti-offertorio-latest.csv', index=False)
        suggested_comunione[md_cols].fillna('').rename(columns=dict(zip(md_cols, md_cols_renamed))).head(10).to_csv('data/suggeriti-comunione-latest.csv', index=False)
        suggested_congedo[md_cols].fillna('').rename(columns=dict(zip(md_cols, md_cols_renamed))).head(10).to_csv('data/suggeriti-congedo-latest.csv', index=False)

        print("")
        print("✅ I suggerimenti formattati per hildegard sono stati esportati")
        print("📄 File prodotti:")
        print("   data/suggeriti-top20-latest.csv")
        print("   data/suggeriti-ingresso-latest.csv")
        print("   data/suggeriti-offertorio-latest.csv")
        print("   data/suggeriti-comunione-latest.csv")
        print("   data/suggeriti-congedo-latest.csv")

    def run(self):
        """Esegue in sequenza tutti i passi necessari per generare i suggerimenti."""
        self.load_data()
        self.get_liturgia_id()
        self.compute_vector_similarities()
        self.compute_manually_selected()
        self.compute_storico_suonati()
        self.compute_text_similarity()
        self.compute_total_score()
        self.compute_adeguatezza()
        self.export_data()


def main():
    if len(sys.argv) > 1:
        data_liturgia = sys.argv[1]
    else:
        print("Nessun valore passato come argomento. Inserisci la data della liturgia nel formato 'YYYY-MM-DD'")
        sys.exit()

    suggeritore = SuggeritoreRefactor(data_liturgia)
    suggeritore.run()


if __name__ == "__main__":
    main()
