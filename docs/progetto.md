---
title: Progetto
description: Hildegard è un suggeritore di canti liturgici. Ogni settimana trovi i canti suggeriti per la liturgia domenicale.
hide:
  - navigation
  - toc
---

# Il progetto
Hildegard è un suggeritore di canti liturgici. Chiunque si sia occupatə di animazione liturgica conosce bene la fase preparatoria che consiste nalla lettura della liturgia e nella ricerca dei canti ad essa più adatti. Chiunque si sia occupato di animazione liturgica conosce benissimo anche quella fastidiosissima sensazione di sapere di conoscere il canto perfetto e non essere in grado di individuarlo tra i suoi ricordi. Questo strumento nasce per provare a rendere più semplice e meno estenuante questo processo.

[Gli ultimi suggerimenti :material-arrow-right:](index.md){ .md-button }

## Il nome
Hildegard von Bingen (se preferite, Ildegarda di Bingen[^1]) fu una monaca benedettina che, tra le numerose attività, fu anche compositrice di musica sacra. Diamo a questo strumento il suo nome non solo per celebrare l'incanto della sua opera musicale[^2], ma anche per omaggiare i contributi (spesso dimenticati) delle donne alla musica.

[Scopri di più :material-arrow-right:](https://it.wikipedia.org/wiki/Ildegarda_di_Bingen){ .md-button }

## Come funziona
Ogni settimana, l'algoritmo su cui si basa questo strumento confronta la liturgia con i testi di circa 1500 canti raccolti online in [librettocanti.it](http://librettocanti.it/). Proprio perchè la procedura è automatizzata e non validata, è possibile che produca output irrilevanti e sbagliati. Ecco perchè consigliamo comunque di leggere la liturgia quando si utilizza Hildegard.

??? example "Scopri i dettagli"    
    ## I Dati

    Il suggeritore sfrutta diversi set di dati:

    1. **Anagrafica Canti**: Informazioni dettagliate sui canti (ID, titoli, autori, raccolte)
        - path: `data/anagrafica_canti.csv`
        - fonte: [librettocanti.it](http://librettocanti.it/)
    
    2. **Calendario Liturgico**: Associazioni tra date e ID liturgie
        - path: `data/calendari_liturgici/calendario_2019-2050.csv`
        - fonte: API del [Calcolatore del calendario liturgico cattolico italiano](https://www.favrin.net/misc/calendario_liturgico/)
    
    3. **Similarità Medie**: Similarità medie storiche tra testi liturgici e canti
        - path: `data/mean_text_similarities.csv`
    
    4. **Similarità Vettoriali**: Similarità basate su embeddings dei testi
        - path: `data/vector_similarities.csv`
    
    5. **Pesi**: Definizione dei pesi per le diverse metriche
        - path: `data/score_weights.csv`
    
    6. **Selezioni Manuali**: Canti selezionati manualmente per specifiche liturgie
        - path: `data/manually_selected.csv`
    
    7. **Storico Esecuzioni**: Registro dei canti eseguiti storicamente
        - path: `data/storico_suonati.csv`
    
    8. **Medie Esecuzioni**: Statistiche sulle esecuzioni dei canti
        - path: `data/mean_suonati.csv`

    ## Calcolo del Punteggio
    Il punteggio finale è composto da cinque componenti, ciascuna progettata per catturare un aspetto diverso della rilevanza di un canto per una determinata liturgia.

    ### 1. Similarità Testuale (\(s_{ts}\))
    \[ s_{ts} = 0.65 \cdot \frac{\text{sim}(t_l, t_c)}{\max(\text{sim})} + 0.35 \cdot \frac{\text{sim}(t_l, t_c)}{\text{sim}_{\text{max}}} \]

    dove:

    - \(\text{sim}(t_l, t_c)\): similarità TF-IDF tra testo liturgico (\(t_l\)) e testo del canto (\(t_c\))
    - \(\max(\text{sim})\): massima similarità trovata nell'analisi corrente
    - \(\text{sim}_{\text{max}}\): massima similarità storica

    Questa formula combina:

    - Similarità relativa (65%): quanto il canto è simile rispetto agli altri canti analizzati
    - Similarità assoluta (35%): quanto il canto è simile rispetto al massimo storico
    
    Vantaggio: riduce l'impatto di falsi positivi dovuti a match occasionali.

    ### 2. Similarità Vettoriale (\(s_{vs}\))
    \[ s_{vs} = \cos(\vec{v_l}, \vec{v_c}) = \frac{\vec{v_l} \cdot \vec{v_c}}{||\vec{v_l}|| \cdot ||\vec{v_c}||} \]

    dove:

    - \(\vec{v_l}\): vettore di embedding del testo liturgico
    - \(\vec{v_c}\): vettore di embedding del testo del canto

    Questa metrica cattura similarità semantiche che potrebbero sfuggire al TF-IDF.
    
    Vantaggio: identifica relazioni semantiche anche quando i testi usano parole diverse.

    ### 3. Deviazione dalla Media (\(s_d\))
    \[ s_d = 0.65 \cdot \frac{\text{sim} - \mu}{\max(\Delta)} + 0.35 \cdot \frac{\text{sim} - \mu}{\Delta_{\text{max}}} \]

    dove:

    - \(\text{sim}\): similarità del canto
    - \(\mu\): media storica delle similarità
    - \(\Delta\): deviazione dalla media
    - \(\Delta_{\text{max}}\): massima deviazione storica

    Misura quanto un canto si discosta dalla sua performance media storica.
    
    Vantaggio: evidenzia canti che sono particolarmente rilevanti per questa liturgia specifica.

    ### 4. Punteggio Storico (\(s_h\))
    \[ s_h = 0.275 \cdot \frac{n}{\max(N)} + 0.275 \cdot \frac{n - \mu_n}{n} + 0.45 \cdot \frac{n}{\max(n)} \]

    dove:

    - \(n\): numero di esecuzioni del canto per questa liturgia
    - \(N\): totale esecuzioni di tutti i canti
    - \(\mu_n\): media delle esecuzioni
    - \(\max(n)\): massimo numero di esecuzioni per un singolo canto

    Combina tre fattori:

    - Popolarità globale (27.5%): quanto il canto è usato in generale
    - Deviazione dalla media (27.5%): quanto l'uso si discosta dalla media
    - Popolarità specifica (45%): quanto è usato per questa liturgia
    
    Vantaggio: bilancia tradizione e specificità liturgica.

    ### 5. Selezione Manuale (\(s_s\))
    \[ s_s = \frac{a}{100} \]

    dove \(a\) è l'accuratezza assegnata manualmente [0-100].

    Normalizza i punteggi di selezione manuale.
    
    Vantaggio: incorpora l'esperienza umana nel sistema automatico.

    ### Punteggio Finale
    \[ \text{score} = \frac{\sum_{i} w_i s_i}{\sum_{i} w_i h_i} \cdot 100 \]

    dove:

    - \(w_i\): pesi delle diverse componenti
    - \(s_i\): punteggi delle componenti
    - \(h_i\): indicatori di presenza (1 se il dato è disponibile, 0 altrimenti)

    Questa media pesata:

    1. Combina tutte le componenti secondo la loro importanza relativa
    2. Si adatta automaticamente ai dati disponibili
    3. Produce un punteggio finale in percentuale

    ### Pesi delle Metriche

    {{ read_csv('data/score_weights.csv') }}

    ### Componenti della Formula

    | Simbolo | Descrizione | Range |
    |---------|-------------|--------|
    | \(s_{ts}\) | Punteggio similarità testuale | [0-1] |
    | \(s_{vs}\) | Punteggio similarità vettoriale | [0-1] |
    | \(s_d\) | Punteggio deviazione | [-1,1] |
    | \(s_s\) | Punteggio selezione manuale | [0-1] |
    | \(s_h\) | Punteggio storico | [0-1] |
    | \(h_x\) | Indicatore presenza del dato | {0,1} |
    | \(w_x\) | Peso della metrica corrispondente | vedi tabella sopra |

    La formula calcola una media pesata dei vari punteggi, normalizzando per i pesi dei soli punteggi effettivamente disponibili. Questo permette di gestire casi in cui non tutti i dati sono presenti (es. canti mai eseguiti non avranno punteggio storico).

    ## Etichette di Adeguatezza

    Ogni canto riceve un'etichetta di adeguatezza:

    - **:material-check-all: Alta**: Per canti con selezione manuale ≥ 0.92, o storico ≥ 0.9 e score ≥ 80%, o score ≥ 95%
    - :material-check: **Buona**: Per canti con selezione manuale tra 0.7 e 0.92
    - :material-dots-horizontal: **Mh**: Per tutti gli altri casi

Sei una sviluppatrice? Sei uno sviluppatore? Il codice è su [GitHub](https://github.com/dennisangemi/hildegard) e se vuoi, puoi contribuire!

[Contribuisci :material-arrow-right:](https://github.com/dennisangemi/hildegard){ .md-button }

## Ringraziamenti
Senza il lavoro straordinario di Michele Mammini, che ha sviluppato [librettocanti.it](https://www.librettocanti.it/), "Hildegard: il suggeritore di canti liturgici" non esisterebbe. A lui il nostro più sincero grazie per la disponibilità e le autorizzazioni necessarie.

[Apri librettocanti.it :material-arrow-right:](https://www.librettocanti.it/){ .md-button }

A [hildegard.it](https://hildegard.it) hanno contribuito pure, in diversi modi, Rosanna Polillo e Maria Rita Messina. A loro va un altro grazie!

## Contatti e segnalazioni
Se trovi degli errori o ti vuoi mettere in contatto con chi ha sviluppato questo strumento, scrivi una mail a Dennis Angemi usando questo indirizzo: [dennisangemi@gmail.com](mailto:dennisangemi@gmail.com)

[^1]: [Consulta la pagina wikipedia dedicata Hildegard von Bingen ](https://it.wikipedia.org/wiki/Ildegarda_di_Bingen)
[^2]: [Ascolta uno dei brani che ha composto (De Spiritu Sancto)](https://www.youtube.com/watch?v=HYzPR0nwcmY)
