---
date:
  created: 2024-07-08
  updated: 2024-07-09
authors:
  - dennis
categories:
  - Novità
---

# Abbiamo migliorato l'accuratezza di Hildegard

Sfruttando diverse fonti dati e un nuovo algoritmo di calcolo, adesso [Hildegard](../../index.md) è in grado di fornire risultati più accurati. Non si tratta della versione definiva: presto arriveranno altri aggiornamenti!
<!-- more -->

La prima versione di [hildegard.it](https://hildegard.it) risale ormai a circa **2 mesi fa**. In questo periodo abbiamo tenuto traccia dei canti suggeriti e abbiamo monitorato l'**accuratezza** (estremamente bassa) dei risultati. Mentre prima l'**algoritmo** di selezione si basava solo ed esclusivamente sulla *similarità* tra i testi dei canti e il testo della liturgia, adesso abbiamo introdotto due nuove metriche che contribuiscono a migliorare l'accuratezza dei suggerimenti: la *deviazione dalla similarità media storica* (per evitare di suggerire canti che vengono erroneamente selezionati ogni domenica a causa della loro - piccola - somiglianza a praticamente tutte le liturgie) e un'*accuratezza manualmente indicata*.

Dall'incrocio di questi nuovi contributi, contiamo di aver migliorato l'accuratezza dell'output e speriamo di aver reso più adeguati e aderenti i canti selezionati per la liturgia. Tutti i dettagli relativi alla nuova versione dell'algoritmo del suggeritore sono visualizzabili qui nella sezione [Progetto](https://hildegard.it/progetto/#come-funziona).

Ti ricordiamo che questo progetto è open-source: se vuoi contribuire, sei benvenutə!

- Se sei una sviluppatrice o uno sviluppatore puoi dare un'occhiata al [repository GitHub di Hildegard](https://github.com/dennisangemi/hildegard);
- se sei un animatore liturgico senza skill di sviluppo, puoi sempre aiutarci a migliorare i risultati indicandoci i canti che secondo te sono adatti per una determinata liturgia. Li stiamo raccogliendo in [questo Google Sheet](https://docs.google.com/spreadsheets/d/1cS9Bf4iBtzkJqROZ6DxxNxJNj6-YqoGFdtIdiM5tpQs/edit?gid=0#gid=0). Fai click su `Solo commenti` e poi `Richiedi accesso in modifica` per aggiungere un suggerimento ;)