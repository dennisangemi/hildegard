#!/bin/bash

source ./scripts/extract_antifona_ingresso
source ./scripts/extract_antifona_comunione

PATH_CALENDARIO_LITURGICO="./data/calendari_liturgici/calendario_2019-2050.csv"

# Check if mlr is installed
if ! command -v mlr &> /dev/null; then
    echo "mlr (Miller) could not be found. Please install it first."
    exit 1
fi

# Use mlr to iterate over CSV rows
mlr --csv cut -f date,id_liturgia $PATH_CALENDARIO_LITURGICO | while IFS=, read -r date id_liturgia; do
   file="./risorse/lezionari/liturgie/$id_liturgia.txt"

   echo "Processing $file"

   # Check if file exists
   if [ ! -f "$file" ]; then
      echo "File $file does not exist"
      continue
   fi

   # Debug: print the first few lines of the file
   head -n 5 "$file"
   read -n 1 -p "Continue? "
   # Check if file contains "ANTIFONA ALLA COMUNIONE"
   if grep -q "ANTIFONA ALLA COMUNIONE" "$file"; then
      echo "File $file does not contain ANTIFONA ALLA COMUNIONE"
      return 1
   fi

   wait

   echo "ANTIFONA D'INGRESSO" >> "$file"
   extract_antifona_ingresso "$date" >> "$file"
   echo "ANTIFONA ALLA COMUNIONE" >> "$file"
   echo "" >> "$file"
   echo "DOPO LA COMUNIONE" >> "$file"
   extract_antifona_comunione "$date" >> "$file"
   echo "" >> "$file"

   # Pause until user input
   read -n 1 -p "Continue? "
done
