#!/bin/bash

# Script per mappare la numerazione delle pagine del lezionario con la numerazione delle pagine del PDF

ANNO=$1

# check che anno sia una lettera tra a,b,c e che sia minuscola
if [[ ! $ANNO =~ ^[a-c]$ ]]; then
    echo "Errore: l'anno deve essere una lettera tra a,b,c"
    exit 1
fi

ANAGRAFICA="liturgie/lezionari/processing/anagrafica_anno_'$ANNO'_v1.csv"
MAPPING="liturgie/lezionari/processing/page_mapping_$ANNO.csv"
OUTPUT="liturgie/lezionari/anagrafica_anno_'$ANNO'_v2.csv"

mlr --csv join --ul -j pagina_printed -f $ANAGRAFICA then unsparsify $MAPPING \
| mlr --csv reorder -f evento,pagina_printed > $

# to do: trasformare in funzione. Così fa un po' schifo