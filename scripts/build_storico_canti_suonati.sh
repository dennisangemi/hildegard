#!/bin/bash

# questo script usa get_canti_suonati per costruire il file con lo storico dei canti suonati

# enviroment secrets
# USERNAME="***"
# PASSWORD="***"

# constants for temporary files
TEMP_CALENDARIO_PER_STORICO="data/calendario_temp.csv"

# import constants
source <(grep = scripts/config.ini)

# constants
IDS_FILE="data/id_canti.txt"

# importa funzioni
source ./scripts/get_canti_suonati

# seleziono date da calendario liturgico maggiore a quella di oggi
today_date=$(date +"%Y-%m-%d")
#<$PATH_CALENDARIO_LITURGICO mlr --csv filter -S "\$date >= \"$today_date\"" | vd -f csv

# for every unique id_liturgia, select the min date
duckdb -c "COPY (SELECT MIN(date) AS date, id_liturgia FROM read_csv_auto('$PATH_CALENDARIO_LITURGICO') WHERE date >= '$today_date' GROUP BY id_liturgia ORDER BY MIN(date)) TO '$TEMP_CALENDARIO_PER_STORICO' (HEADER, DELIMITER ',');"

echo "📅 Salvate le date selezionate in $TEMP_CALENDARIO_PER_STORICO"

# extract date column from TEMP_CALENDARIO_PER_STORICO
# dates_list=$(<$TEMP_CALENDARIO_PER_STORICO mlr --csv --headerless-csv-output cut -f date | head -n 3)
dates_list=$(<$TEMP_CALENDARIO_PER_STORICO mlr --csv --headerless-csv-output cut -f date)
n_dates=$(echo $dates_list | wc -w)
echo "📅 Trovate $n_dates date"

# get access token
echo "🔑 Ottengo l'access token..."
url="https://www.librettocanti.it/api/get_access_token/$USERNAME/$PASSWORD"
token=$(curl -s "$url" | jq -r ".access_token")

# check token
if [ -z "$token" ] || [ "$token" == "null" ]; then
   echo "❌ Errore: access token non ottenuto"
   exit 1
else
   echo "✅ Access token ottenuto"
fi

# per ogni data, ottengo i canti suonati
echo "🎵 Ottengo i canti suonati..."
i=1
for date in $dates_list; do
   echo "📅 [$i/$n_dates] Liturgia del $date"
   get_canti_suonati $date $token data/suonati_$date.csv

   # wait 10 seconds
   sleep 10
   
   # pause key press
   # read -p "Premi un tasto per continuare..."
   
   i=$((i + 1))
done

# merge all suonati files
echo "🔀 Unisco tutti i file..."
mlr --csv cat data/suonati_*.csv > data/temp_suonati.csv

# merge suonati.csv with TEMP_CALENDARIO_PER_STORICO per aggiungere la colonna id_liturgia a suonati.csv
echo "🔀 Aggiungo id_liturgia a temp_suonati.csv (usando $TEMP_CALENDARIO_PER_STORICO)..."
mlr --csv join --ul -j date -f data/temp_suonati.csv then cut -x -f date $TEMP_CALENDARIO_PER_STORICO | mlr --csv cut -o -f id_liturgia,id_canti,titolo,cnt > $PATH_STORICO_SUONATI

# build mean_suonati.csv
echo "📊 Costruisco $PATH_MEAN_SUONATI..."
duckdb -c "COPY (SELECT id_canti, titolo, MAX(cnt) AS max, ROUND(MEAN(cnt),2) AS mean FROM read_csv_auto('$PATH_STORICO_SUONATI') GROUP BY id_canti, titolo ORDER BY max desc) TO '$PATH_MEAN_SUONATI' (HEADER, DELIMITER ',');"

# remove temporary files
# rm $TEMP_CALENDARIO_PER_STORICO
rm data/temp_suonati.csv
rm data/suonati_*.csv

# stampa finito con tick
echo "✅ Finito!"