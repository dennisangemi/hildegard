---
title: Suggerimenti di animazione liturgica
description: I canti suggeriti per la liturgia di Domenica 6 aprile 2025
hide:
    - toc
    - navigation
template: home.html
---

<div class="grid md:grid-cols-2 gap-8 mb-12">
  <div class="bg-white rounded-lg shadow p-6 border-l-4 border-accent-500">
    <h2 class="text-2xl font-extrabold text-primary-800 mb-3" style="font-weight: 800 !important;">Cos'è Hildegard?</h2>
    <p class="text-gray-700">Un suggeritore automatico che ti aiuta a selezionare i canti più adatti per la liturgia domenicale, basandosi sul confronto dei testi con le letture del giorno.</p>
  </div>
  
  <div class="bg-white rounded-lg shadow p-6 border-l-4 border-primary-500">
    <h2 class="text-2xl font-extrabold text-primary-800 mb-3" style="font-weight: 800 !important;">Come funziona?</h2>
    <p class="text-gray-700">L'algoritmo analizza le letture della domenica e confronta il testo con una vasta raccolta di canti liturgici per suggerirti quelli più pertinenti.</p>
  </div>
</div>

<br>

{% import 'macros.html' as macros %}
{% set canti = load_json('data/suggeriti-top20-latest.json') %}

## <span id="canti-suggeriti" class="text-primary-700 font-bold"> :material-music-note-plus: Canti suggeriti per Domenica 13 aprile 2025</span>

??? quote "Leggi la liturgia"

    {% include-markdown "../risorse/lezionari/liturgia-latest.txt" %}

    ---

    [Apri la liturgia della CEI :material-arrow-right:](https://www.chiesacattolica.it/liturgia-del-giorno/?data-liturgia=20250413){ .md-button }

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
    | [Nostalgia d’una sorgente](https://www.librettocanti.it/canto/nostalgia-d-una-sorgente-327) | :material-dots-horizontal: Mh | 49 | Giosy Cento |  |
    | [Sai fischiare?](https://www.librettocanti.it/canto/sai-fischiare-2099) | :material-dots-horizontal: Mh | 49 | Verdi Note dell'Antoniano | Estate Ragazzi con Le Verdi Note dell'Antoniano |
    | [Madre io vorrei](https://www.librettocanti.it/canto/madre-io-vorrei-295) | :material-dots-horizontal: Mh | 49 | Pierangelo Sequeri | E mi sorprende |
    | [Cosa renderti](https://www.librettocanti.it/canto/cosa-renderti-2233) | :material-dots-horizontal: Mh | 49 |  |  |
    | [Cantico delle creature](https://www.librettocanti.it/canto/cantico-delle-creature-2203) | :material-dots-horizontal: Mh | 48 | Marco Frisina | Tu sei bellezza |
    | [Il Signore della danza](https://www.librettocanti.it/canto/il-signore-della-danza-1555) | :material-dots-horizontal: Mh | 48 |  |  |
    | [E correremo insieme](https://www.librettocanti.it/canto/e-correremo-insieme-169) | :material-dots-horizontal: Mh | 48 | Giosy Cento |  |
    | [Io non sono degno](https://www.librettocanti.it/canto/io-non-sono-degno-253) | :material-dots-horizontal: Mh | 48 | Claudio Chieffo | È bella la strada |
    | [Gesù gridò Mashalem](https://www.librettocanti.it/canto/ges-grid-mashalem-1597) | :material-dots-horizontal: Mh | 47 | Cantàmmo a Gesù |  |
    | [Non più due (Buttazzo)](https://www.librettocanti.it/canto/non-pi-due-buttazzo-1467) | :material-dots-horizontal: Mh | 47 | Buttazzo |  |
    | [Non mi abbandonare](https://www.librettocanti.it/canto/non-mi-abbandonare-1775) | :material-dots-horizontal: Mh | 47 | L. Scaglianti |  |
    | [Tu sei qui (Way maker)](https://www.librettocanti.it/canto/tu-sei-qui-way-maker-2575) | :material-dots-horizontal: Mh | 47 | Leeland |  |
    | [Disse un giorno il Padre](https://www.librettocanti.it/canto/disse-un-giorno-il-padre-2728) | :material-dots-horizontal: Mh | 47 | G.Stefani - M.Giombini  |  |
    | [Nascerà](https://www.librettocanti.it/canto/nascer-2550) | :material-dots-horizontal: Mh | 46 | Gen Rosso |  |
    | [La trasfigurazione](https://www.librettocanti.it/canto/la-trasfigurazione-2269) | :material-dots-horizontal: Mh | 46 | Marco Frisina | Non di solo pane |
    | [Il Figliol Prodigo (Abbracciami Gesù)](https://www.librettocanti.it/canto/il-figliol-prodigo-abbracciami-ges-1596) | :material-dots-horizontal: Mh | 46 | Figli del Divino Amore |  |
    | [Il figliol prodigo](https://www.librettocanti.it/canto/il-figliol-prodigo-227) | :material-dots-horizontal: Mh | 46 | Vittorio Nadalin |  |
    | [Grazie Gesù](https://www.librettocanti.it/canto/grazie-ges-2453) | :material-dots-horizontal: Mh | 45 | Giulia e Tommaso Fasano | Festa di prima Comunione |
    | [Ciò che Dio ha fatto in me](https://www.librettocanti.it/canto/ci-che-dio-ha-fatto-in-me-1818) | :material-dots-horizontal: Mh | 45 | Morning Star |  |
    | [Luce per noi](https://www.librettocanti.it/canto/luce-per-noi-2104) | :material-dots-horizontal: Mh | 45 | Oratorio Salesiano di Arese |  |
## Note
!!! warning "Attenzione"
    I canti sono selezionati automaticamente da un algoritmo che confronta i testi. La selezione potrebbe non essere accurata; pertanto ti consigliamo comunque di leggere la liturgia per verificare personalmente l'adeguatezza dei suggerimenti!<br>Per maggiori informazioni sull'algoritmo di selezione puoi leggere la [pagina del progetto](https://hildegard.it/progetto/).

!!! info "Testi"
    I testi dei canti sono stati tratti da [librettocanti.it](https://www.librettocanti.it/). Si ringrazia Michele Mammini per la disponibilità <3


