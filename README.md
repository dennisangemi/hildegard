# Suggeritore di canti liturgici

Ti interessano i canti consigliati e più adatti per la liturgia della prossima domenica? [Fai click qui!](suggerimenti.md)

## Actions
1. scarica l'anagrafica dei canti con `get_anagrafica`
1. scarica i canti con `db_downloader`
1. scarica la liturgia con `get_liturgia YYYYMMDD` (per scaricare la liturgia della prossima domenica si può usare ad esempio `./get_liturgia $(./get_next_sunday)`)
1. effettua il calcolo della similatirà con `suggeritore.py`

# To do
1. documentare
1. automatizzare tutto una volta alla settimana e produrre report interattivo cliccabile
1. calcolare similarità per parti (letture, salmi, vangelo, completo) e restituire i primi 10/20 risultati per ogni parte

# Note e ringraziamenti
I testi dei canti provengono da http://librettocanti.it/ sviluppato da Michele Mammini. A lui il nostro più sincero ringraziamento.