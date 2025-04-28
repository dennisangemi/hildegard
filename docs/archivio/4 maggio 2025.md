{% set canti = load_json('data/suggeriti-top20-20250504.json') %}

## <span id="canti-suggeriti" class="text-primary-700 font-bold"> :material-music-note-plus: Canti suggeriti per Domenica 4 maggio 2025</span>

??? quote "Leggi la liturgia"

    {% include-markdown "../../risorse/lezionari/liturgie/formatted/C26-C.md" %}

    ---

    [Apri la liturgia della CEI :material-arrow-right:](https://www.chiesacattolica.it/liturgia-del-giorno/?data-liturgia=20250504){ .md-button }

<div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
  {% for canto in canti %}
  <div class="bg-white rounded-lg shadow-md overflow-hidden border-t-4 border-accent-500 flex flex-col">
    <div class="p-5 flex-grow">
      <div class="flex justify-between items-start">
        <h4 class="text-lg font-bold text-gray-800 mb-2">{{ canto.titolo }}</h4>
        <span class="bg-accent-100 text-accent-800 text-sm font-semibold rounded-full px-3 py-1">{{ canto.text_similarity }}%</span>
      </div>
      <p class="text-sm text-gray-600 mb-1">{{ canto.autore }}</p>
      {% if canto.raccolta %}
      <p class="text-sm text-gray-500 italic mb-3">{{ canto.raccolta }}</p>
      {% else %}
      <div class="mb-3"></div>
      {% endif %}
    </div>
    <div class="bg-gray-50 p-3 border-t border-gray-100 flex justify-between items-center">
      <a href="https://www.librettocanti.it/canto/{{ canto.titolo | lower | replace(' ', '-') }}-{{ canto.id_canti }}" class="text-accent-600 hover:text-accent-800 text-sm font-medium" target="_blank">
        <span class="flex items-center"><i class="material-icons" style="font-size: 1rem; margin-right: 0.25rem;">description</i> Testo</span>
      </a>
      {% if canto.link_youtube %}
      <a href="https://www.youtube.com/watch?v={{ canto.link_youtube }}" class="text-red-600 hover:text-red-800 text-sm font-medium" target="_blank">
        <span class="flex items-center"><i class="material-icons" style="font-size: 1rem; margin-right: 0.25rem;">play_circle</i> Ascolta</span>
      </a>
      {% endif %}
    </div>
  </div>
  {% endfor %}
</div>


### Altro
Di seguito altri 20 canti che potrebbero essere adatti per la liturgia ma sono stati esclusi perchè il loro punteggio di adeguatezza non ha raggiunto la soglia minima.
??? question "Apri la lista"
    | Titolo | Adeguatezza | % | Autore | Raccolta |
    | --- | --- | --- | --- | --- |
    | [Trasformi in Gesù](https://www.librettocanti.it/canto/trasformi-in-ges-1715) | :material-dots-horizontal: Mh | 48 | Giosy Cento  |  |
    | [Nella Chiesa del Signore](https://www.librettocanti.it/canto/nella-chiesa-del-signore-1924) | :material-dots-horizontal: Mh | 46 | Michele Bonfitto | Sei grande nell'amore |
    | [Corpo di Gesù](https://www.librettocanti.it/canto/corpo-di-ges-1685) | :material-dots-horizontal: Mh | 43 | M. Penhard |  |
    | [Benedetto sei o Padre](https://www.librettocanti.it/canto/benedetto-sei-o-padre-2166) | :material-dots-horizontal: Mh | 43 | Francesco Buttazzo |  |
    | [La trasfigurazione](https://www.librettocanti.it/canto/la-trasfigurazione-2269) | :material-dots-horizontal: Mh | 43 | Marco Frisina | Non di solo pane |
    | [Alleluia Gesù](https://www.librettocanti.it/canto/alleluia-ges-2111) | :material-dots-horizontal: Mh | 42 | Daniele Ricci | Amati da Te |
    | [Gesù dolce musica](https://www.librettocanti.it/canto/ges-dolce-musica-1687) | :material-dots-horizontal: Mh | 42 | RnS | Davanti al Re |
    | [Io sono il pane della vita](https://www.librettocanti.it/canto/io-sono-il-pane-della-vita-2354) | :material-dots-horizontal: Mh | 41 | Lucio Maria Zappatore | Il Signore è vita |
    | [Insieme a Te](https://www.librettocanti.it/canto/insieme-a-te-245) | :material-dots-horizontal: Mh | 41 | Francesco Buttazzo | Alla tua festa |
    | [Inno a San Giovanni ](https://www.librettocanti.it/canto/inno-a-san-giovanni-2127) | :material-dots-horizontal: Mh | 41 |  |  |
    | [Amar come Gesù amò (per avere la felicità)](https://www.librettocanti.it/canto/amar-come-ges-am-per-avere-la-felicit-46) | :material-dots-horizontal: Mh | 40 | --- |  |
    | [Come fuoco vivo](https://www.librettocanti.it/canto/come-fuoco-vivo-134) | :material-dots-horizontal: Mh | 40 | Gen Rosso / Gen Verde | Come fuoco vivo |
    | [Sia lode all'Agnello](https://www.librettocanti.it/canto/sia-lode-all-agnello-2387) | :material-dots-horizontal: Mh | 39 | RnS  | Risplendi Gerusalemme |
    | [Giorno di Pentecoste](https://www.librettocanti.it/canto/giorno-di-pentecoste-1627) | :material-dots-horizontal: Mh | 38 | Giosy Cento | Attendi in linea... ti passo Dio |
    | [Lasciate che i bambini vengano a me](https://www.librettocanti.it/canto/lasciate-che-i-bambini-vengano-a-me-2600) | :material-dots-horizontal: Mh | 38 | Daniele Esposito |  |
    | [Vocazione (v2)](https://www.librettocanti.it/canto/vocazione-v2-493) | :material-dots-horizontal: Mh | 37 | Pierangelo Sequeri | In cerca d'autore |
    | [Vocazione](https://www.librettocanti.it/canto/vocazione-1780) | :material-dots-horizontal: Mh | 37 | Pierangelo Sequeri | In cerca d'autore |
    | [Fermarono i cieli](https://www.librettocanti.it/canto/fermarono-i-cieli-194) | :material-dots-horizontal: Mh | 36 | S. Alfonso |  |
    | [Spirito Santo, dolce presenza](https://www.librettocanti.it/canto/spirito-santo-dolce-presenza-2098) | :material-dots-horizontal: Mh | 36 | RnS |  |
    | [Fonti di Nazareth](https://www.librettocanti.it/canto/fonti-di-nazareth-196) | :material-dots-horizontal: Mh | 36 | Chiara Bizzetti |  |
## Note
!!! warning "Attenzione"
    I canti sono selezionati automaticamente da un algoritmo che confronta i testi. La selezione potrebbe non essere accurata; pertanto ti consigliamo comunque di leggere la liturgia per verificare personalmente l'adeguatezza dei suggerimenti!<br>Per maggiori informazioni sull'algoritmo di selezione puoi leggere la [pagina del progetto](https://hildegard.it/progetto/).

!!! info "Testi"
    I testi dei canti sono stati tratti da [librettocanti.it](https://www.librettocanti.it/). Si ringrazia Michele Mammini per la disponibilità <3


