#!/bin/bash

# Questo script scarica testi di canti utilizzando gli ID presenti in un file di input.
# È particolarmente utile per costruire un libretto di canti.

# Istruzioni per l'uso:
# 1. Assicurati che il file IDS_FILE contenga gli ID dei canti, uno per riga.
# 2. Assicurati che la funzione get_text_from_id sia definita e accessibile.
# 3. Esegui lo script con il comando: ./scarica_lista_testi.sh
# 4. I testi dei canti verranno salvati nella directory specificata da CANTI_DIR.

# Costanti:
# IDS_FILE: Nome del file che contiene gli ID dei canti.
# CANTI_DIR: Nome della directory dove verranno salvati i testi dei canti.

# Carica la funzione get_text_from_id da un file esterno.

# Crea la directory CANTI_DIR se non esiste.

# Per ogni riga del file IDS_FILE:
# - Legge l'ID del canto.
# - Scarica il testo del canto utilizzando la funzione get_text_from_id.
# - Salva il testo del canto in un file nella directory CANTI_DIR.

# attualmente questo script è inutilizzato

# contsants
IDS_FILE="cresime.txt"
CANTI_DIR="canti"

# load function from file
source get_text_from_id

# crea directory CANTI_DIR se non esiste
mkdir -p $CANTI_DIR

# per ogni riga del file IDS_FILE, poni id uguale alla riga corrente
while IFS= read -r id
do
    # scarica il testo del canto con id uguale alla riga corrente
    get_text_from_id $id > $CANTI_DIR/$id.txt
done < "$IDS_FILE"


