#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <file>"
    exit 1
fi

file=$1

# Definire le frasi come variabili
frase_inizio="Antifona alla Comunione"
frase_fine="Dopo la Comunione"

# Estrarre il testo tra "Antifona alla Comunione" e "Dopo la Comunione"
awk -v inizio="$frase_inizio" -v fine="$frase_fine" \
    '$0 ~ inizio {flag=1; next} $0 ~ fine {flag=0} flag' "$file" |
# Rimuovere le espressioni specificate e gli asterischi
sed -e 's/—(antica)—//g' -e 's/—(oppure)—//g' -e 's/\*//g'
