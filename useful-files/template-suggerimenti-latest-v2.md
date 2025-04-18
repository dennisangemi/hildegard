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

## <span id="canti-suggeriti" class="text-primary-700 font-bold"> :material-music-note-plus: Canti suggeriti per {{{DATA_LITURGIA}}}</span>

??? quote "Leggi la liturgia"

    {% include-markdown "../risorse/lezionari/liturgia-latest.txt" %}

    ---

    [Apri la liturgia della CEI :material-arrow-right:]({{{URL_LITURGIA_CEI}}}){ .md-button }

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


