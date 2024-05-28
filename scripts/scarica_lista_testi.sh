#!/bin/bash

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


