# load libreries
library(rvest)
library(dplyr)

# constants
# URL <- "https://www.chiesacattolica.it/liturgia-del-giorno/?data-liturgia=20240519"
URL <- "https://www.chiesacattolica.it/liturgia-del-giorno/?data-liturgia=20240505"
OUTPUT_FILE <- "liturgia.txt"
LITURGIA_SELECTOR <- "p"
# ANTIFONA_SELECTOR <- ".cci-multiple-liturgie+ .cci-fontsize-dynamic p"
# COLLETTA_SELECTOR <- ".cci-fontsize-dynamic+ .cci-fontsize-dynamic .cci-liturgia-giorno-section-title+ .cci-liturgia-giorno-section-content p:nth-child(2)"
# # PRIMA_LETTURA_SELECTOR <- ".cci-fontsize-dynamic:nth-child(4) p:nth-child(3)"
# PRIMA_LETTURA_SELECTOR <- ".cci-fontsize-dynamic:nth-child(4) p"
# SALMO_SELECTOR <- ".cci-liturgia-giorno-section-versetto+ .cci-liturgia-giorno-section-content p , strong"
# SECONDA_LETTURA_SELECTOR <- ".cci-fontsize-dynamic:nth-child(6) p:nth-child(3)"
# VANGELO_SELECTOR <- ".cci-fontsize-dynamic:nth-child(8) p:nth-child(3)"
# ANTIFONA_COMUNIONE_SELECTOR <- ".cci-fontsize-dynamic:nth-child(10) p:nth-child(2)"
# 
# # scrape the page
# page <- read_html(URL)
# antifona <- page %>% html_nodes(ANTIFONA_SELECTOR) %>% html_text() %>% paste(., collapse = " ")
# colletta <- page %>% html_nodes(COLLETTA_SELECTOR) %>% html_text() %>% paste(., collapse = " ")
# prima_lettura <- page %>% html_nodes(PRIMA_LETTURA_SELECTOR) %>% html_text() %>% paste(., collapse = " ")
# salmo <- page %>% html_nodes(SALMO_SELECTOR) %>% html_text() %>% paste(., collapse = " ")
# seconda_lettura <- page %>% html_nodes(SECONDA_LETTURA_SELECTOR) %>% html_text() %>% paste(., collapse = " ")
# vangelo <- page %>% html_nodes(VANGELO_SELECTOR) %>% html_text() %>% paste(., collapse = " ")
# antifona_comunione <- page %>% html_nodes(ANTIFONA_COMUNIONE_SELECTOR) %>% html_text() %>% paste(., collapse = " ")
# 
# # merge the results in a single string
# liturgia <- paste(antifona, colletta, prima_lettura, salmo, seconda_lettura, vangelo, antifona_comunione,  collapse = " ")

page <- read_html(URL)
liturgia <- page %>% html_nodes(LITURGIA_SELECTOR) %>% html_text() %>% paste(., collapse = " ")

# write the result to a file
write(liturgia, file = OUTPUT_FILE)





