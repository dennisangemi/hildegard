#!/bin/bash
# set -x
set -eo pipefail

# istruzioni
# Rendi eseguibile: chmod +x ./scripts/get_vector_similarities.sh
# Esegui: ./scripts/get_vector_similarities.sh

# importo variabili
source <(grep = scripts/config.ini)

# Configurazioni
ANAGRAFICA="risorse/lezionari/anagrafica_liturgie_cei.csv"
LITURGIE="risorse/lezionari/liturgie.csv"
OUTPUT="vector_similarities.csv"
TMP_DIR=$(mktemp -d)

# Pulizia eventuali file temporanei preesistenti
cleanup() {
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT

# crea il posto per il file di output
touch "$OUTPUT"

# aggiungi header
echo "id_liturgia,riferimento,id_canti,vector_similarity" > "$OUTPUT"

# Estrai lista di tutte le liturgie
echo "Estraggo lista liturgie..."
mlr --csv --headerless-csv-output cut -f id_liturgia "$ANAGRAFICA" | \
mlr --csv filter 'NR > 1' | \
while IFS= read -r id; do

    # Processa ogni riferimento per la liturgia corrente
    for riferimento in liturgia antifona_ingresso prima_lettura salmo seconda_lettura versetto vangelo antifona_comunione; do
        
        # File temporaneo per i risultati
        TMP_FILE="$TMP_DIR/${id}_${riferimento}.csv"
        
        # Caso liturgia completa
        if [[ "$riferimento" == "liturgia" ]]; then
            < $LITURGIE mlr --csv --headerless-csv-output filter "\$id_liturgia == \"$id\"" | \
            llm similar canti -d "$PATH_EMBEDDINGS" -i - | \
            jq --arg id "$id" --arg rif "$riferimento" '{id_liturgia: $id, riferimento: $rif, id_canti: .id, vector_similarity: .score}' | \
            mlr --j2c cat > "$TMP_FILE"
        
        # Caso singolo riferimento
        else
            # Estrai contenuto del riferimento
            < $LITURGIE mlr --csv --headerless-csv-output filter "\$id_liturgia == \"$id\"" then \
            cut -f "$riferimento" "$LITURGIE" | {
                read -r content
                
                # Salta se il contenuto è vuoto
                if [[ -z "$content" ]]; then
                    continue
                fi
                
                # Pulizia specifica per il versetto
                if [[ "$riferimento" == "versetto" ]]; then
                    content=$(echo "$content" | sed 's/Alleluia//g; s/alleluia//g')
                fi
                
                # Calcola similarità
                echo "$content" | \
                llm similar canti -d "$PATH_EMBEDDINGS" -i - | \
                jq --arg id "$id" --arg rif "$riferimento" \
                '{id_liturgia: $id, riferimento: $rif, id_canti: .id, vector_similarity: .score}' | \
                mlr --j2c cat > "$TMP_FILE"
            }
        fi
        
        # Aggiungi al risultato finale se il file non è vuoto
        if [[ -s "$TMP_FILE" ]]; then
            mlr --csv --headerless-csv-output cat "$TMP_FILE" >> "$OUTPUT"
        fi
    done
done

echo "Elaborazione completata. Risultato in: $OUTPUT"