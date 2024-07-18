#!/bin/bash

# usa questo script per costuire anagrafica delle liturgie.
# il file di output sarà sporco e verrà pulito manualmente.

# import constants
source <(grep = scripts/config.ini)

# Funzione per estrarre i numeri dei salmi da un file liturgia in txt

extract_numbers() {
   # input: file liturgia in txt

   # output: id_liturgia,salmo_n_eb,salmo_n_gl 

   # note:
   # - id_liturgia è il nome del file senza estensione
   # - salmo_n_eb è il numero del Salmo secondo la tradizione ebraica
   # - salmo_n_gl è il numero del Salmo secondo la tradizione greca e latina

   local file="$1"
   local filename_without_ext=$(basename "$file" .txt)
   
   # Unisci tutto il testo in una sola riga rimuovendo i ritorni a capo
   local one_line=$(tr -d '\n' < "$file")

   # Usa una regex per trovare il numero del Salmo e il numero tra parentesi
   if [[ $one_line =~ SALMO\ RESPONSORIALE.*Dal\ Salmo\ ([0-9]+)\ \(([0-9]+)\) ]]; then
      local number1=${BASH_REMATCH[1]}
      local number2=${BASH_REMATCH[2]}
      echo "$filename_without_ext,$number1,$number2"
   else
      echo "$filename_without_ext,NA,NA"
   fi
}

# crea header file csv con id_liturgia, salmo_n_eb, salmo_n_gl (cioè numero salmo ebraico e greco-latino)
output_file=$PATH_ANAGRAFICA_SALMI
echo "id_liturgia,salmo_n_eb,salmo_n_gl" > "$output_file"

# Itera su ogni file .txt nella cartella liturgie
for file in $PATH_LITURGIE/*.txt; do
   extract_numbers "$file" >> "$output_file"
done

echo "Estrazione completata. I risultati sono salvati in $output_file."
