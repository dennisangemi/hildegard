#!/usr/bin/env python3

import fitz  # PyMuPDF
import pandas as pd

# Imposta i margini da escludere (in punti PDF; 1 punto = 1/72 pollice)
top_margin = 78.1  # margine superiore da escludere
bottom_margin = 39.5  # margine inferiore da escludere

def extract_text_from_pdf(pdf_path):
    # Apri il documento PDF
    document = fitz.open(pdf_path)
    data = []

    # Itera attraverso le pagine
    for page_number in range(len(document)):
        page = document[page_number]
        page_height = page.rect.height
        
        # Definisci il rettangolo di estrazione, escludendo i margini
        clip_rect = fitz.Rect(0, top_margin, page.rect.width, page_height - bottom_margin)
        
        # Estrai il testo dalla pagina ritagliata
        text = page.get_text("text", clip=clip_rect)
        
        # Aggiungi il testo e il numero di pagina alla lista
        if text.strip():  # Aggiungi solo se c'è testo
            data.append([text.strip(), page_number + 1])  # +1 per numerazione delle pagine umana

    return data

def extract_text_from_pdf_v2(pdf_path):
    # Apri il documento PDF
    document = fitz.open(pdf_path)
    data = []

    # Itera attraverso le pagine
    for page_number in range(len(document)):
        page = document[page_number]
        page_height = page.rect.height
        
        # Definisci il rettangolo di estrazione, escludendo i margini
        clip_rect = fitz.Rect(0, top_margin, page.rect.width, page_height - bottom_margin)
        
        # Estrai i blocchi di testo dalla pagina ritagliata
        blocks = page.get_text("dict", clip=clip_rect)["blocks"]
        
        # Ordina i blocchi per la loro posizione y per mantenere l'ordine di lettura
        blocks.sort(key=lambda b: b['bbox'][1])
        
        # Concatenare i blocchi di testo in ordine di lettura
        text = "\n".join(block["lines"][0]["spans"][0]["text"] for block in blocks if block["type"] == 0)
        
        # Aggiungi il testo e il numero di pagina alla lista
        if text.strip():  # Aggiungi solo se c'è testo
            data.append([text.strip(), page_number + 1])  # +1 per numerazione delle pagine umana

    return data

def save_to_csv(data, output_csv_path):
    # Crea un DataFrame con due colonne: "testo" e "pagina"
    df = pd.DataFrame(data, columns=["testo", "pagina"])
    
    # Salva il DataFrame in un file CSV
    df.to_csv(output_csv_path, index=False)

# Percorso al file PDF di input e al file CSV di output
input_pdf = "liturgie/lezionari/lezionario_domenicale_festivo_anno_c.pdf"
output_csv = "liturgie/lezionari/raw_nr_lezionario_anno_c.csv"

# Estrai il testo dal PDF e salva nel CSV
text_data = extract_text_from_pdf(input_pdf)
save_to_csv(text_data, output_csv)

print(f"Conversione completata. File CSV salvato come {output_csv}.")
