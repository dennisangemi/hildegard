#!/bin/bash
set -eo pipefail

# Configurazioni
ANAGRAFICA="risorse/lezionari/anagrafica_liturgie_cei.csv"
LITURGIE="risorse/lezionari/liturgie.csv"
EMBEDDINGS_DB="risorse/embeddings.db"
OUTPUT="vector_similarities.csv"
TMP_DIR=$(mktemp -d)

# Pulizia eventuali file temporanei preesistenti
cleanup() {
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT

# Estrai lista di tutte le liturgie
echo "Estraggo lista liturgie..."
mlr --csv cut -f id_liturgia "$ANAGRAFICA" | \
mlr --csv filter 'NR > 1' | \
while IFS= read -r id; do

    # Processa ogni riferimento per la liturgia corrente
    for riferimento in liturgia antifona_ingresso prima_lettura salmo seconda_lettura versetto vangelo antifona_comunione; do
        
        # File temporaneo per i risultati
        TMP_FILE="$TMP_DIR/${id}_${riferimento}.csv"
        
        # Caso liturgia completa
        if [[ "$riferimento" == "liturgia" ]]; then
            mlr --csv --headerless-csv-output filter "\$id_liturgia == \"$id\"" then \
            cut -x -f id_liturgia then \
            put -S '$testo = gsub(joinv(" ", $*), " +", " ")' then \
            cut -f testo "$LITURGIE" | \
            llm similar canti -d "$EMBEDDINGS_DB" -i - | \
            jq --arg id "$id" --arg rif "$riferimento" \
            '{id_liturgia: $id, riferimento: $rif, id_canti: .id, vector_similarity: .score}' | \
            mlr --j2c cat > "$TMP_FILE"
        
        # Caso singolo riferimento
        else
            # Estrai contenuto del riferimento
            mlr --csv --headerless-csv-output filter "\$id_liturgia == \"$id\"" then \
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
                llm similar canti -d "$EMBEDDINGS_DB" -i - | \
                jq --arg id "$id" --arg rif "$riferimento" \
                '{id_liturgia: $id, riferimento: $rif, id_canti: .id, vector_similarity: .score}' | \
                mlr --j2c cat > "$TMP_FILE"
            }
        fi
        
        # Aggiungi al risultato finale se il file non è vuoto
        if [[ -s "$TMP_FILE" ]]; then
            cat "$TMP_FILE" >> "$OUTPUT"
        fi
    done
done

echo "Elaborazione completata. Risultato in: $OUTPUT"