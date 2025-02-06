# Funzioni di hildegard.it
Attualmente è disponibile la documentazioni di solo 3 funzioni utilizzate per la creazione di blog post automatici.

## Generazione di blog post powered by AI
Questa cartella contiene tre funzioni Bash utilizzate per generare suggerimenti di canti liturgici e creare un post per il blog basato su un modello predefinito. Le funzioni sono:

- `build_hai_suggestions_blog_post`
- `get_hai_suggestions_prompt`
- `build_hai_suggestions_attachment`

Di seguito vengono fornite le descrizioni dettagliate delle funzioni, le loro dipendenze e le istruzioni su come invocarle correttamente.

### 1. build_hai_suggestions_blog_post

##### Descrizione
Questa funzione genera un blog post basato su suggerimenti di canti per una determinata celebrazione liturgica. Si basa su un modello predefinito e utilizza un LLM (Large Language Model) per generare il contenuto.

##### Parametri
```bash
build_hai_suggestions_blog_post <date> <liturgical_calendar_csv> <liturgical_texts_folder> <all_csv_md> <ingresso_csv_md> <offertorio_csv_md> <comunione_csv_md> <congedo_csv_md> <hai_suggestions_blog_post_template> <lyrics_folder> <suggested_raw_csv> <threshold> <attachment_file> <llm_model> <system_prompt_file>
```

| Parametro | Descrizione |
|-----------|-------------|
| `<date>` | Data della celebrazione (YYYY-MM-DD) |
| `<liturgical_calendar_csv>` | Percorso del file CSV con il calendario liturgico |
| `<liturgical_texts_folder>` | Cartella contenente i testi delle liturgie |
| `<all_csv_md>` | CSV con tutti i canti suggeriti |
| `<ingresso_csv_md>` | CSV con i canti per l’ingresso |
| `<offertorio_csv_md>` | CSV con i canti per l’offertorio |
| `<comunione_csv_md>` | CSV con i canti per la comunione |
| `<congedo_csv_md>` | CSV con i canti per il congedo |
| `<hai_suggestions_blog_post_template>` | Modello del blog post |
| `<lyrics_folder>` | Cartella con i testi dei canti |
| `<suggested_raw_csv>` | CSV con i suggerimenti elaborati per la data specificata |
| `<threshold>` | Soglia di punteggio minimo per considerare un canto |
| `<attachment_file>` | Nome del file di output dell’allegato |
| `<llm_model>` | Modello LLM da utilizzare |
| `<system_prompt_file>` | File con il prompt di sistema |

#### Dipendenze
- `get_hai_suggestions_prompt`
- `build_hai_suggestions_attachment`
- `llm` (eseguibile per interagire con il modello LLM)

#### Invocazione
```bash
build_hai_suggestions_blog_post 2025-02-09 data/calendari_liturgici/calendario_2019-2050.csv risorse/lezionari/liturgie data/suggeriti-top20-latest.csv data/suggeriti-ingresso-latest.csv data/suggeriti-offertorio-latest.csv data/suggeriti-comunione-latest.csv data/suggeriti-congedo-latest.csv useful-files/template-blog-post-hai.md risorse/canti data/suggerimenti-20250209.csv 40 test_hai_attachment.md gemini-2.0-flash-exp useful-files/hai-suggestions-system-prompt.txt
```

### 2. get_hai_suggestions_prompt

#### Descrizione
Questa funzione crea il prompt per l’LLM basandosi sui dati liturgici e sui canti suggeriti.

#### Parametri
```bash
get_hai_suggestions_prompt <date> <liturgical_calendar_csv> <liturgical_texts_folder> <all_csv> <ingresso_csv> <offertorio_csv> <comunione_csv> <congedo_csv>
```

| Parametro | Descrizione |
|-----------|-------------|
| `<date>` | Data della celebrazione |
| `<liturgical_calendar_csv>` | File CSV con il calendario liturgico |
| `<liturgical_texts_folder>` | Cartella con i testi delle liturgie |
| `<all_csv>` | CSV con tutti i canti suggeriti |
| `<ingresso_csv>` | CSV con i canti per l’ingresso |
| `<offertorio_csv>` | CSV con i canti per l’offertorio |
| `<comunione_csv>` | CSV con i canti per la comunione |
| `<congedo_csv>` | CSV con i canti per il congedo |

#### Dipendenze
- `get_raw_liturgia` (funzione per estrarre i testi liturgici dal calendario e dai file delle liturgie)

#### Invocazione
```bash
get_hai_suggestions_prompt 2025-02-09 data/calendari_liturgici/calendario_2019-2050.csv risorse/lezionari/liturgie data/suggeriti-top20-latest.csv data/suggeriti-ingresso-latest.csv data/suggeriti-offertorio-latest.csv data/suggeriti-comunione-latest.csv data/suggeriti-congedo-latest.csv
```

### 3. build_hai_suggestions_attachment

#### Descrizione
Questa funzione genera un allegato con i testi dei canti selezionati in base a una soglia minima di punteggio.

#### Parametri
```bash
build_hai_suggestions_attachment <path_to_template> <path_to_lyrics_folder> <path_to_suggested_songs_csv> <threshold> <output_file>
```

| Parametro | Descrizione |
|-----------|-------------|
| `<path_to_template>` | Modello del blog post |
| `<path_to_lyrics_folder>` | Cartella con i testi dei canti |
| `<path_to_suggested_songs_csv>` | CSV con i canti suggeriti |
| `<threshold>` | Soglia minima per includere un canto |
| `<output_file>` | Nome del file di output |

#### Dipendenze
- `get_local_text_by_id_canti` (funzione per ottenere il testo di un canto dato il suo ID)
- `mlr` (Miller, per la manipolazione dei file CSV)

#### Invocazione
```bash
build_hai_suggestions_attachment useful-files/template-blog-post-hai.md risorse/canti data/suggerimenti-20250209.csv 40 test_hai_attachment.md
```

### Dipendenze Generali
Tutte le funzioni dipendono da:
- **Script esterni**: Le funzioni utilizzano `source` per includere altri script in `./scripts/functions/`
- **Esecuzione di comandi esterni**:
  - `llm` per la generazione del blog post
  - `mlr` per la gestione dei CSV
  - `grep`, `cat`, `touch`, `rm` per manipolare file di testo

Se qualche dipendenza non è disponibile, lo script restituirà un errore.


