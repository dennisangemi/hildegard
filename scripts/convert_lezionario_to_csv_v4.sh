#!/bin/bash

input_pdf="risorse/lezionari/pdf/lezionario_domenicale_festivo_anno_c.pdf"
output_dir="risorse/lezionari/lezionario_c"
output_csv="risorse/lezionari/lezionario_anno_c_v2.csv"

# Creazione della directory per i file di testo
mkdir -p "$output_dir"

# Funzione per rimuovere le righe indesiderate utilizzando grep -v con regex
remove_unwanted_lines() {
    local input_file="$1"
    local output_file="$2"
    
    # Filtra le righe indesiderate usando grep -v con regex
    # grep -Ev '(Lezionar io|8:51|8:52|8:53|10-10-2007)' "$input_file" > "$output_file"
    grep -Ev '(Lezionar io|10-10-2007|11-10-2007|\bPagina [0-9]+\b|[0-9]{1,2}:[0-9]{2})' "$input_file" > "$output_file"


}

# Estrazione del testo per ogni pagina e rimozione delle righe indesiderate
num_pages=$(pdfinfo "$input_pdf" | grep "Pages" | awk '{print $2}')

echo "Progress:"
for ((i=1; i<=num_pages; i++))
do
    echo "$i/$num_pages"
    pdftotext -f $i -l $i "$input_pdf" "$output_dir/pagina_$i.txt"
    remove_unwanted_lines "$output_dir/pagina_$i.txt" "$output_dir/pagina_$i-clean.txt"
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

echo "Conversione completata. File CSV creato: $output_csv"

# usa mlr per pulire il file
# mlr --csv clean-whitespace "$output_csv" > "$output_csv.tmp" && mv "$output_csv.tmp" "$output_csv"
# questo metodo rimuove tutti i ritorni a capo che possono tornare utili
# vabbè poi la pulizia la facciamo in python