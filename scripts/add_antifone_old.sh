#!/bin/bash

source ./scripts/extract_antifona_ingresso
source ./scripts/extract_antifona_comunione

PATH_CALENDARIO_LITURGICO="./data/calendari_liturgici/calendario_2019-2050.csv"

df_date=$(mlr --csv --headerless-csv-output cut -f date $PATH_CALENDARIO_LITURGICO)
df_id_liturgie=$(mlr --csv --headerless-csv-output cut -f id_liturgia $PATH_CALENDARIO_LITURGICO)
n_lines=$(echo "$df_date" | wc -l)

for i in $(seq 1 $n_lines); do
   date=$(echo "$df_date" | sed -n "${i}p")
   id_liturgia=$(echo "$df_id_liturgie" | sed -n "${i}p")
   file="./risorse/lezionari/liturgie/$id_liturgia.txt"

   echo "Processing $file"

   # check if file contains "ANTIFONA ALLA COMUNIONE"
   if ! grep -q "ANTIFONA ALLA COMUNIONE" $file; then
      echo "File $file does not contain ANTIFONA ALLA COMUNIONE"
      continue
   fi
   echo ciaoooooo
   read -n 1 -p Continue?

   echo "ANTIFONA D'INGRESSO" >> $file
   extract_antifona_ingresso $date >> $file
   echo "ANTIFONA ALLA COMUNIONE" >> $file
   echo "" >> $file
   echo "DOPO LA COMUNIONE" >> $file
   extract_antifona_comunione $date >> $file
   echo "" >> $file

   # pause until user input
   read -n 1 -p Continue?

done