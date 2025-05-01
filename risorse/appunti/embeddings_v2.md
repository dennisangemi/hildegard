# Note sugli embeddings

Ho usato `llm` cli di datasette con plugin `llm-sentence-transformers`. vd https://llm.datasette.io/en/stable/embeddings/cli.html e https://github.com/simonw/llm-sentence-transformers

Il modello per gli embeddings (compatibile con la lingua italiana) usato è `paraphrase-multilingual-MiniLM-L12-v2` vd https://www.sbert.net/docs/sentence_transformer/pretrained_models.html e https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

## Pipeline

### Installazione plugin in llm
```sh
llm install llm-sentence-transformers
```

### Scelta del modello di embedding
La lista dei modelli è questa https://www.sbert.net/docs/sentence_transformer/pretrained_models.html. Su huggingface si capisce se è adatto anche per l'italiano o meno. Io ho selezionato `paraphrase-multilingual-MiniLM-L12-v2` di circa 500 MB.

### Download del modello selezionato
```sh
llm sentence-transformers register paraphrase-multilingual-MiniLM-L12-v2
```

Per visualizzare i modelli disponibili sulla macchina che stai usando puoi usare
```sh
llm embed-models
```

Per configurare di default il tuo modello preferito puoi usare
```sh
llm embed-models default sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

### Generazione del dataset da embeddare
Ho preparato `data/canti.json` con `id, titolo, content`. Il modello lo userà per generare un embedding per ogni elemento del json.

### Generazione embeddings
```sh
llm embed-multi canti data/canti.json -d risorse/embeddings.db --store
```

Il comando creerà un embedding per ogni elemento del file `data/canti.json` e li salverà insieme al contenuto originale nel database `risorse/embeddings.db`.

`--store` è opzionale, semplicemente salva nel db anche il testo, una cosa simile.

### Ricerca semantica
Per una frase/parola inserita da terminale
```sh
llm similar canti -c 'spirito' -d risorse/embeddings.db
```

L'output è un json di questo tipo
```json
{
  "id": "247",
  "score": 0.7840886898345113,
  "content": "Invocazione allo Spirito --- Vieni Santo Spirito  manda dal cielo la Tua luce diffondi (...)",
  "metadata": null
},
{
  "id": "1696",
  "score": 0.7367683913717257,
  "content": "Spirito di santità A. Gouzes Spirito di santità Spirito di luce Spirito di fuoco, scendi su di noi.  Spirito del Pa(...)",
  "metadata": null
}
{
  "id": "3011",
  "score": 0.7330843477565376,
  "content": "Lo Spirito di Cristo Basadonna Meregalli Lo Spirito di Cristo fa fiorire il deserto, torna la vita,(...)",
  "metadata": null
}
{
  "id": "2470",
  "score": 0.7266774970070493,
  "content": "Spirito Santo cuore dell'umanità RnS - F. Marranzino Spirito Santo scendi su di noi, Con la tu(...)",
  "metadata": null
}
{
  "id": "282",
  "score": 0.7236594711054561,
  "content": "Lo Spirito del Signore Marco Frisina Lo Spirito del Signore è su di me, Lo Spirito del Signore mi ha consacrato, Lo Spiri(...)",
  "metadata": null
}
{
  "id": "1976",
  "score": 0.7107899186964762,
  "content": "Come brezza  Daniele Ricci Spirito di luce pura che parli nell'anima spirito di gioia e vita che (...)",
  "metadata": null
}

(...)
```

Oppure da un file
```sh
cat risorse/lezionari/liturgie/C13-C.txt | llm similar canti -d risorse/embeddings.db -i -
```

Essendo stato generato il csv con le letture disaggregate delle liturgie si può fare pure 
```sh
< liturgie_splitted.csv mlr --csv --headerless-csv-output filter '$id_liturgia=="C40-C"' | llm similar canti -d risorse/embeddings.db -i - 
```

Oppure selezionare una specifica lettura di una specifica liturgia con 
```sh
< liturgie_splitted.csv mlr --csv --headerless-csv-output filter '$id_liturgia=="C40-C"' then cut -f salmo | llm similar canti -d risorse/embeddings.db -i - 
```

Per il versetto alleluiatico potrebbe essere opportuno nascondere la parola "alleluia"
```sh
< liturgie_splitted.csv mlr --csv --headerless-csv-output filter '$id_liturgia=="C40-C"' then cut -f versetto | sed 's/Alleluia//g; s/alleluia//g'
```

## Generazione del dataset delle vector similarities
Così come esiste `similarities.csv` e `mean_similarities.csv` (che vale la pena rinominare in `text_similarities`), creo `vector_similarities.csv` che avrà questa struttura

| id_liturgia | riferimento | id_canti | vector_similarity | 
| --- | --- | --- | --- |
| C1-A | liturgia | 252 | 0.8 |
| C1-A | liturgia | 652 | 0.5 |
| C1-A | prima_lettura | 252 | 0.8 |
| C1-A | seconda_lettura | 652 | 0.5 |
| ... | ... | ... | ... |

è generato tramite l'anagrafica dei canti: si estrae la colonna degli id_canti, si fa un ciclo per ogni canto e si usano i comandi di prima con liturgie_splitted.csv, mlr e llm similar 

## Cose da capire
1. come impostare metadata dinamici per embed-multi
3. come pubblicare/elaborare per non far girare il modello su macchina github


