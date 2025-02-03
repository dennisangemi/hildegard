#!/usr/bin/env python3

"""
Script Name: page_mapping.py
Description:
    Questo script utilizza la libreria PyMuPDF (fitz) per mappare le pagine di un file PDF.
    Estrae i numeri di pagina stampati dal margine inferiore di ogni pagina del PDF e li associa
    ai numeri di pagina effettivi del PDF.

Usage:
    python page_mapping.py <file_path>

Dependencies:
    - PyMuPDF (fitz)
    - pandas
    - re

Functions:
    - map_pdf_pages(file_path): Mappa le pagine di un file PDF e restituisce una lista di numeri di pagina stampati e numeri di pagina del PDF.
    - extract_printed_page_number(text): Estrae il numero di pagina stampato dal testo fornito.

Example:
    python page_mapping.py example.pdf
"""

import fitz  # PyMuPDF
import pandas as pd
import re

def map_pdf_pages(file_path):
    # Apri il file PDF
    pdf_document = fitz.open(file_path)
    num_pages = pdf_document.page_count
    
    # Inizializza le liste per i numeri di pagina
    printed_pages = []
    pdf_pages = []
    
    # Itera attraverso tutte le pagine del PDF
    for i in range(num_pages):
        page = pdf_document[i]
        # Definisci l'area del margine inferiore
        page_height = page.rect.height
        lower_margin = fitz.Rect(0, page_height - 39.5, page.rect.width, page_height)
        
        # Estrai il testo dal margine inferiore
        text = page.get_text("text", clip=lower_margin)
        printed_page_number = extract_printed_page_number(text)
        
        printed_pages.append(printed_page_number)
        pdf_pages.append(i + 1)
    
    # Crea un DataFrame con la mappa delle pagine
    page_mapping_df = pd.DataFrame({
        'pagina_printed': printed_pages,
        'pagina_pdf': pdf_pages
    })
    
    return page_mapping_df

def extract_printed_page_number(text):
    # Funzione per estrarre il numero di pagina stampata dal testo
    match = re.search(r'\b\d+\b', text)
    if match:
        return int(match.group(0))
    else:
        return None

def write_to_csv(page_mapping_df, output_csv):
    # Filtra le righe con 'None' in 'pagina_printed'
    filtered_df = page_mapping_df.dropna(subset=['pagina_printed'])
    
    # set pagina_stapata as int
    filtered_df['pagina_printed'] = filtered_df['pagina_printed'].astype(int)

    # Scrivi i dati nel file CSV
    filtered_df.to_csv(output_csv, index=False)

# Esempio di utilizzo
file_path = 'liturgie/lezionari/pdf/lezionario_domenicale_festivo_anno_c.pdf'
output_csv = 'liturgie/lezionari/page_mapping_c.csv'
page_mapping_df = map_pdf_pages(file_path)
write_to_csv(page_mapping_df, output_csv)

print(f'La mappa delle pagine è stata scritta in {output_csv}')
