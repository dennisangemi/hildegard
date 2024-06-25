#!/usr/bin/env python3
import fitz  # PyMuPDF
import subprocess

def crop_pdf(input_pdf_path, output_pdf_path, top_margin, bottom_margin):
    # Apri il file PDF
    pdf_document = fitz.open(input_pdf_path)
    
    # Itera attraverso le pagine del PDF
    for page_num in range(len(pdf_document)):
        print(f"Elaborazione pagina {page_num + 1}...")
        # Estrai la pagina
        page = pdf_document.load_page(page_num)
        
        # Ottieni le dimensioni della pagina
        rect = page.rect
        width = rect.width
        height = rect.height
        
        # Calcola il rettangolo ritagliato escludendo i margini
        cropped_rect = fitz.Rect(0, top_margin, width, height - bottom_margin)
        
        # Applica il ritaglio alla pagina
        page.set_cropbox(cropped_rect)
    
    # Salva il PDF ritagliato
    pdf_document.save(output_pdf_path)
    pdf_document.close()

def convert_pdf_to_text(input_pdf_path, output_txt_path):
    # Usa pdftotext per convertire il PDF in testo
    subprocess.run(['pdftotext', input_pdf_path, output_txt_path], check=True)

# Specifica i percorsi del file PDF di input, del PDF ritagliato e del file TXT di output
input_pdf_path = 'liturgie/lezionari/pdf/lezionario_domenicale_festivo_anno_b.pdf'
cropped_pdf_path = 'liturgie/lezionari/pdf/lezionario_domenicale_festivo_anno_b_cropped.pdf'
output_txt_path = 'liturgie/lezionari/pdf/lezionario_domenicale_festivo_anno_b_converted.txt'

# Imposta i margini da escludere (in punti PDF; 1 punto = 1/72 pollice)
top_margin = 130  # margine superiore da escludere
bottom_margin = 39.5  # margine inferiore da escludere

# Ritaglia le pagine del PDF
crop_pdf(input_pdf_path, cropped_pdf_path, top_margin, bottom_margin)
print("PDF ritagliato salvato in:", cropped_pdf_path)

# Converti il PDF ritagliato in testo
convert_pdf_to_text(cropped_pdf_path, output_txt_path)
print("Testo estratto salvato in:", output_txt_path)
