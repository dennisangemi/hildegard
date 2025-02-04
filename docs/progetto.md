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
Hildegard (se preferite, Ildegarda di Bingen[^1]) fu una monaca benedettina che, tra le numerose attività, fu anche compositrice di musica sacra. Diamo a questo strumento il suo nome non solo per celebrare l'incanto della sua opera musicale[^2], ma anche per omaggiare i contributi (spesso dimenticati) delle donne alla musica.

[Scopri di più :material-arrow-right:](https://it.wikipedia.org/wiki/Ildegarda_di_Bingen){ .md-button }

## Come funziona
Ogni settimana, l'algoritmo su cui si basa questo strumento confronta (stupidamente) la liturgia con i testi di circa 1500 canti raccolti online in [librettocanti.it](http://librettocanti.it/). Proprio perchè la procedura è automatizzata e non validata, è possibile che produca output irrilevanti e sbagliati. Ecco perchè consigliamo comunque di leggere la liturgia quando si utilizza Hildegard.

??? example "Scopri i dettagli"
    ## Introduzione

    Questa sezione descrive il funzionamento dello script Python [`suggeritore_v3.py`](https://github.com/dennisangemi/hildegard/blob/main/scripts/suggeritore_v3.py) progettato per suggerire canti liturgici basati sulla similarità con i testi della liturgia. Verranno indicati i criteri di selezione dei canti, le formule matematiche utilizzate per il calcolo della similarità e delle deviazioni, e le fonti dati impiegate.

    ## I Dati

    Il suggeritore sfrutta diversi set di dati

    1. **Anagrafica Canti**: Un dataset che contiene informazioni dettagliate sui canti, inclusi gli ID, i titoli, gli autori e le raccolte.
        - path: [`data/anagrafica_canti.csv`](https://github.com/dennisangemi/hildegard/blob/main/data/anagrafica_canti.csv)
        - script: [`scrips/get_anagrafica`](https://github.com/dennisangemi/hildegard/blob/main/scripts/get_anagrafica)
        - fonte: [librettocanti.it](http://librettocanti.it/)
    2. **Calendario Liturgico**: Un calendario che associa le date delle celebrazioni ai corrispondenti ID delle liturgie.
        - path: [`data/calendari_liturgici/calendario_2019-2050.csv`](https://github.com/dennisangemi/hildegard/blob/main/data/calendari_liturgici/calendario_2019-2050.csv)
        - script: [`scripts/get_calendario_liturgico`](https://github.com/dennisangemi/hildegard/blob/main/scripts/get_calendario_liturgico)
        - fonte: API del [Calcolatore del calendario liturgico cattolico italiano](https://www.favrin.net/misc/calendario_liturgico/) sviluppato e rilasciato in CC-BY da Gabriele Favrin (grazie!).
    3. **Media delle Similarità**: Un insieme di dati che contiene le similarità medie storiche tra i testi della liturgia e i testi dei canti.
        - path: [`data/mean_similarities.csv`](https://github.com/dennisangemi/hildegard/blob/main/data/mean_similarities.csv)
        - script: [`scripts/get_mean_text_similarities.py`](https://github.com/dennisangemi/hildegard/blob/main/scripts/get_mean_text_similarities.py)
    4. **Pesi**: Un documento che specifica i pesi delle diverse metriche utilizzate per il calcolo del punteggio finale.
        - path: [`data/score_weights.csv`](https://github.com/dennisangemi/hildegard/blob/main/data/score_weights.csv)
    5. **Canti Selezionati Manualmente**: Un elenco di canti selezionati manualmente per specifiche liturgie.
        - path: [`data/manually_selected.csv`](https://github.com/dennisangemi/hildegard/blob/main/data/manually_selected.csv)
        - script: [`scripts/get_manually_selected`](https://github.com/dennisangemi/hildegard/blob/main/scripts/get_manually_selected)

    ## Calcolo della Similarità

    La similarità tra il testo della liturgia e i testi dei canti viene calcolata utilizzando la tecnica del TF-IDF (Term Frequency-Inverse Document Frequency) e la similarità coseno. Di seguito, si descrivono i passaggi dettagliati per il calcolo della similarità:

    1. **Caricamento dei Testi dei Canti**: I testi dei canti vengono caricati una volta sola e memorizzati in una variabile globale.
      
    2. **Unione dei Testi**: Il testo della liturgia viene combinato con i testi dei canti in una singola lista.

    3. **Vettorizzazione con TF-IDF**: Un vettorizzatore TF-IDF viene inizializzato e applicato a tutti i testi combinati per trasformarli in vettori numerici. 

    4. **Calcolo della Similarità Coseno**: La similarità coseno viene calcolata tra il vettore del testo della liturgia (riga di riferimento) e i vettori dei testi dei canti. Questo produce una lista di valori di similarità.

    5. **Creazione del Dizionario di Similarità**: I valori di similarità vengono associati agli ID dei canti per creare un dizionario che mappa ogni canto con il suo rispettivo valore di similarità.

    La formula per il calcolo della similarità coseno è la seguente:

    \[ \text{similarity}(A, B) = \frac{A \cdot B}{||A|| \cdot ||B||} \]

    dove \(A\) e \(B\) sono i vettori TF-IDF dei testi, \(A \cdot B\) è il prodotto scalare dei due vettori e \(||A||\) e \(||B||\) sono le norme (lunghezze) dei vettori.

    ## Calcolo della Deviazione

    La deviazione tra la similarità calcolata e la media delle similarità storiche viene determinata. Questa deviazione permette di capire quanto un canto sia più o meno simile alla liturgia rispetto alla media storica.

    ## Calcolo del Punteggio

    I pesi delle metriche vengono definiti per le diverse componenti del punteggio:

    {{ read_csv('data/score_weights.csv') }}

    ### Punteggio di Similarità

    Calcolato come combinazione ponderata della percentuale di similarità e della percentuale massima di similarità. La formula utilizzata è:

    \[ \text{score_similarity} = 0.6 \left( \frac{\text{similarity} \times w_s}{100} \right) + 0.4 \left( \frac{\text{similarity} \times w_s}{\max(\text{similarity})} \right) \]

    dove:

    - \( \text{similarity} \) è la similarità calcolata tra il testo della liturgia e il testo del canto.
    - \( w_s \) è il peso assegnato alla similarità.

    ### Punteggio di Deviazione

    Calcolato tenendo conto della deviazione massima e minima. La formula è:

    \[ \text{score_deviation} = \frac{\text{deviation} \times w_d}{\max(\text{deviation})} \]

    e

    \[ \text{score_deviation} = \frac{\text{deviation} \times w_d}{|\min(\text{deviation})|} \]

    a seconda che la deviazione sia positiva o negativa, dove:

    - \( \text{deviation} \) è la deviazione della similarità rispetto alla media storica.
    - \( w_d \) è il peso assegnato alla deviazione.

    ### Punteggio di Selezione Manuale

    Se un canto è stato selezionato manualmente, viene aggiunto un ulteriore punteggio basato su un peso specifico:

    \[ \text{score_selection} = \text{manually_selected} \times \frac{w_m}{100} \]

    dove:

    - \( \text{manually_selected} \) indica se il canto è stato selezionato manualmente.
    - \( w_m \) è il peso assegnato alla selezione manuale.

    ### Punteggio Totale

    Il punteggio totale viene calcolato come:

    \[ \text{score} = \text{score_similarity} + \text{score_deviation} \]

    Se un canto è stato selezionato manualmente, il punteggio totale viene ricalcolato come:

    \[ \text{score} = \text{score_similarity} + |\text{score_deviation}| + \text{score_selection} \]

    ## Filtraggio e Ordinamento dei Risultati

    I canti vengono ordinati in base al punteggio finale. Vengono esclusi i canti non pertinenti ai momenti liturgici specifici come l'atto penitenziale e il Gloria.

Sei una sviluppatrice? Sei uno sviluppatore? Il codice è su [GitHub](https://github.com/dennisangemi/hildegard) e se vuoi, puoi contribuire!

[Contribuisci :material-arrow-right:](https://github.com/dennisangemi/hildegard){ .md-button }

## Ringraziamenti
Senza il lavoro straordinario di Michele Mammini, che ha sviluppato [librettocanti.it](https://www.librettocanti.it/), "Hildegard: il suggeritore di canti liturgici" non esisterebbe. A lui il nostro più sincero grazie per la disponibilità e le autorizzazioni necessarie.

[Apri librettocanti.it :material-arrow-right:](https://www.librettocanti.it/){ .md-button }

## Contatti e segnalazioni
Se trovi degli errori o ti vuoi mettere in contatto con chi ha sviluppato questo strumento, scrivi una mail a Dennis Angemi usando questo indirizzo: [dennisangemi@gmail.com](mailto:dennisangemi@gmail.com)

[^1]: [Questa](https://it.wikipedia.org/wiki/Ildegarda_di_Bingen) è la sua pagina Wikipedia 
[^2]: [Qui](https://www.youtube.com/watch?v=HYzPR0nwcmY) un esempio
