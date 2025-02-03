#!/bin/bash

# Questo script Bash ottiene un token di accesso utilizzando le credenziali fornite e lo utilizza per ottenere una risposta da API per verificarne il funzionamento.

# Parametri:
# $1 - USERNAME: Il nome utente per l'autenticazione
# $2 - PASSWORD: La password per l'autenticazione

# Utilizzo:
# ./test_token_cc.sh <USERNAME> <PASSWORD>
# Esempio:
# ./test_token_cc.sh mio_username mia_password

# Variabili:
# USERNAME - Il nome utente passato come primo argomento
# PASSWORD - La password passata come secondo argomento
# token - Il token di accesso ottenuto dall'API

# Ottiene il token di accesso utilizzando le credenziali fornite
# e lo estrae dalla risposta JSON utilizzando jq

# Stampa il nome utente, la password e il token di accesso

# Esegue una richiesta all'API per validare la lista di canti utilizzando il token di accesso
# e stampa il primo elemento dei dati restituiti

USERNAME=$1
PASSWORD=$2

# get access token
token=$(curl -s https://www.librettocanti.it/api/get_access_token/$USERNAME/$PASSWORD | jq -r ".access_token")

echo "Username: $USERNAME"
echo "Password: $PASSWORD"
echo "Access token: $token"
echo ""

# testo valida canti
curl -skL "https://www.librettocanti.it/api/valida_canti/?act=lista&access_token=$token" | jq ".data[0]"