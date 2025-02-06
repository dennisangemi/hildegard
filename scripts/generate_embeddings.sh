#!/bin/bash

# importa variabili
source <(grep = scripts/config.ini)

echo "$PATH_CANTI_DF"

# press key to continue
read -n 1 -s -r -p "Premi un tasto per continuare"

# generate risorse/canti.json tramite scripts/buidl_canti_df.py
./scripts/build_canti_df.py

# aspetta che l'esecuzione di build_canti_df.py sia completata
sleep 1

echo "Generato il file $PATH_CANTI_DF tramite build_canti_df.py"

read -n 1 -s -r -p "Premi un tasto per continuare"

echo "provo a mostrare head di path canti df"
< $PATH_CANTI_DF mlr --csv cat | head -n 2
read -n 1 -s -r -p "Premi un tasto per continuare"

# converti il csv in json tramite mlr
< $PATH_CANTI_DF mlr --csv rename id_canti,id then cut -x -f autore | mlr --c2j cat > $PATH_CANTI_JSON
echo "Generato il file $PATH_CANTI_JSON tramite mlr"

# imposta modello embeddings desiderato di default
llm embed-models default sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
echo "Impostato il modello di embeddings di default"

# usa il json per generare gli embeddings
llm embed-multi canti $PATH_CANTI_JSON -d $PATH_EMBEDDINGS --store
echo "Generati gli embeddings dei canti in $PATH_EMBEDDINGS"
