#!/bin/bash

# questo script viene invocato da scripts/convert_lezionari_to_csv.sh

ciclo_domenicale=$1

# check if the input is one of this values: a, b, c in lower case
if [[ ! $ciclo_domenicale =~ ^[a-c]$ ]]; then
    echo "Errore: il ciclo domenicale deve essere uno dei seguenti valori: a, b, c"
    exit 1
fi

input_pdf="risorse/lezionari/pdf/lezionario_domenicale_festivo_anno_$ciclo_domenicale.pdf"
output_dir="risorse/lezionari/pagine_temp"
output_csv="risorse/lezionari/lezionario_anno_$ciclo_domenicale.csv"

# Creazione della directory temporanea per i file di testo
mkdir -p "$output_dir"

# Estrazione del testo per ogni pagina e rimozione delle righe indesiderate
num_pages=$(pdfinfo "$input_pdf" | grep "Pages" | awk '{print $2}')

echo "Progress:"
for ((i=1; i<=num_pages; i++))
do
    echo "$i/$num_pages"

    # estrai il testo dalla pagina
    pdftotext -f $i -l $i "$input_pdf" "$output_dir/pagina_$i.txt"
    
    # remove unwanted lines
    grep -Ev '(Lezionar io|\bPagina [0-9]+\b|[0-9]{1,2}:[0-9]{2}|[0-9]{2}-[0-9]{2}-[0-9]{4})' "$output_dir/pagina_$i.txt" > "$output_dir/pagina_$i-clean.txt"

    # rimuovi i file temporanei
    rm "$output_dir/pagina_$i.txt"
done

# Creazione del file CSV
echo "pagina,testo" > "$output_csv"

for file in "$output_dir"/*.txt
do
    page_number=$(basename "$file" | sed 's/pagina_\([0-9]\+\)-clean\.txt/\1/')
    content=$(cat "$file")
    echo "$page_number,\"$content\"" >> "$output_csv"
done

# Rimozione della directory temporanea se esiste
rm -r "$output_dir"

echo "Conversione completata. File CSV creato: $output_csv"

# ulteriore pulizia del file csv con python
# con la nuova versione di cleaner_lezionario.py