#!/usr/bin/env python3
import os
import csv

"""

Istruzioni per l'uso:
Eseguire da terminale con:

```bash
python split_liturgie_in_letture.py input_folder output.csv
```

dove input_folder è la cartella contenente i file .txt e output.csv è il nome del file CSV da generare.

Attualmente questo script ha prodotto risorse/lezionari/liturgie.csv

"""

# Mappatura delle keyword alle colonne del CSV
KEYWORD_TO_COLUMN = {
    'ANTIFONA D\'INGRESSO': 'antifona_ingresso',
    'PRIMA LETTURA': 'prima_lettura',
    'SALMO RESPONSORIALE': 'salmo',
    'SECONDA LETTURA': 'seconda_lettura',
    'CANTO AL VANGELO': 'versetto',
    'VANGELO': 'vangelo',
    'ANTIFONA ALLA COMUNIONE': 'antifona_comunione'
}

COLUMN_ORDER = [
    'id_liturgia',
    'antifona_ingresso',
    'prima_lettura',
    'salmo',
    'seconda_lettura',
    'versetto',
    'vangelo',
    'antifona_comunione'
]

def process_file(file_path):
    """Elabora un singolo file estraendo le sezioni rilevanti"""
    file_name = os.path.basename(file_path)
    id_liturgia = os.path.splitext(file_name)[0]
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    result = {col: '' for col in COLUMN_ORDER}
    result['id_liturgia'] = id_liturgia
    
    current_section = None
    content = []

    for line in lines:
        stripped_line = line.strip()
        
        if stripped_line in KEYWORD_TO_COLUMN:
            if current_section:
                # Salva il contenuto accumulato
                result[current_section] = ''.join(content).strip()
            current_section = KEYWORD_TO_COLUMN[stripped_line]
            content = []
        else:
            if current_section:
                content.append(line)

    # Aggiungi l'ultima sezione elaborata
    if current_section and content:
        result[current_section] = ''.join(content).strip()

    return result

def process_folder(input_folder, output_csv):
    """Elabora tutti i file .txt in una cartella e genera il CSV"""
    files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
    all_data = []

    for file in files:
        file_path = os.path.join(input_folder, file)
        file_data = process_file(file_path)
        all_data.append(file_data)

    with open(output_csv, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=COLUMN_ORDER)
        writer.writeheader()
        writer.writerows(all_data)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Estrai sezioni liturgiche da file txt')
    parser.add_argument('input_folder', help='Cartella contenente i file .txt')
    parser.add_argument('output_csv', help='Percorso del file CSV da generare')
    
    args = parser.parse_args()
    
    process_folder(args.input_folder, args.output_csv)
