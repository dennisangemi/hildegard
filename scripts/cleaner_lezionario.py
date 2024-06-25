#!/usr/bin/env python3

# importing libraries
import pandas as pd
import re

# functions
# Funzione per elaborare il testo delle celle
def fix_capital(text):
    lines = text.splitlines()  # Dividi il testo in righe
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Verifica se la riga contiene esattamente una singola lettera maiuscola
        if len(line.strip()) == 1 and line.isupper():
            found_concatenation = False
            
            # Cerca la prima parola disponibile nelle righe successive
            j = i + 1
            while j < len(lines):
                next_line = lines[j].strip()
                if next_line:
                    words = next_line.split()
                    if words:
                        # Concatena la lettera maiuscola con la prima parola trovata
                        concatenated_word = line + words[0]
                        rest_of_text = ' '.join(words[1:])
                        if rest_of_text:
                            lines[i] = concatenated_word + ' ' + rest_of_text
                        else:
                            lines[i] = concatenated_word
                        lines.pop(j)  # Rimuovi la riga dalla quale hai preso la parola
                        found_concatenation = True
                        break
                j += 1
            
            # Se non trovi parole nelle righe successive, passa alla riga successiva
            if not found_concatenation:
                i += 1
                continue
        
        i += 1
    
    # Ricostruisci il testo modificato mantenendo i caratteri di nuova riga tra le parti
    modified_text = '\n'.join(lines)
    return modified_text

# Funzione per rimuovere le righe contenenti solo numeri
def remove_rows_with_only_numbers(text):
    lines = text.splitlines()  # Dividi il testo in righe
    
    # Filtra le righe che contengono solo numeri
    filtered_lines = [line for line in lines if re.match(r'^\d+$', line.strip()) is None]
    
    # Ricostruisci il testo senza le righe che contengono solo numeri
    modified_text = '\n'.join(filtered_lines)
    return modified_text


# Funzione per rimuovere le righe vuote iniziali e le righe vuote extra
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

# Funzione per rimuovere le righe contenenti "ANNO A", "ANNO B" o "ANNO C" tutto in maiuscolo
def remove_rows_with_annos(text):
    lines = text.splitlines()  # Dividi il testo in righe
    
    # Lista delle stringhe da cercare e rimuovere
    strings_to_remove = ["ANNO A", "ANNO B", "ANNO C"]
    
    # Filtra le righe che contengono una delle stringhe da rimuovere tutto in maiuscolo
    filtered_lines = [line for line in lines if not any(s.upper() in line.upper() for s in strings_to_remove)]
    
    # Ricostruisci il testo senza le righe contenenti "ANNO A", "ANNO B" o "ANNO C"
    modified_text = '\n'.join(filtered_lines)
    return modified_text

# Funzione per sostituire "9-10-2007" con una stringa vuota ""
def replace_date(text):
    return text.replace("9-10-2007", "")

# applica il cleaning ai tre lezionari
INPUT_FILES = ['risorse/lezionari/lezionario_anno_a.csv', 'risorse/lezionari/lezionario_anno_b.csv', 'risorse/lezionari/lezionario_anno_c.csv']

for INPUT_FILE in INPUT_FILES:
    # leggi il file csv
    print(INPUT_FILE)
    df = pd.read_csv(INPUT_FILE)

    # Applica le funzione alla colonna 'testo' per effettuare cleaning
    df['testo'] = df['testo'].apply(replace_date)
    df['testo'] = df['testo'].apply(remove_rows_with_annos)
    df['testo'] = df['testo'].apply(fix_capital)
    df['testo'] = df['testo'].apply(remove_rows_with_only_numbers)
    df['testo'] = df['testo'].apply(remove_empty_lines)

    # ordina il csv colonna pagina numerica
    df = df.sort_values(by=['pagina'])

    # salva il file csv
    df.to_csv(INPUT_FILE, index=False)
    print("File salvato correttamente!")

# continuare questo script lanciano build_liturgie.py
