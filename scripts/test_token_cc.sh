#!/bin/bash

# get access token
token=$(curl -s https://www.librettocanti.it/api/get_access_token/$USERNAME/$PASSWORD | jq -r ".access_token")

# testo valida canti
curl -s "https://www.librettocanti.it/api/valida_canti/?act=lista&access_token=$token" | jq ".data[0]"