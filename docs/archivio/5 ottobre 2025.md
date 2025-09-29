<!-- archivePageStartHere -->

{% import 'macros.html' as macros %}
{% set canti = load_json('data/suggeriti-top20-20251005.json') %}

## <span id="canti-suggeriti" class="text-primary-700 font-bold"> :material-music-note-plus: Canti suggeriti per Domenica 5 ottobre 2025</span>

??? quote "Leggi la liturgia"

    {% include-markdown "../../risorse/lezionari/liturgie/formatted/C62-C.md" %}

    ---

    [Apri la liturgia della CEI :material-arrow-right:](https://www.chiesacattolica.it/liturgia-del-giorno/?data-liturgia=20251005){ .md-button }

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

---

Conosci un canto adeguato che non è presente in questa pagina? Aggiungilo dal bottone qui sotto!

[:material-plus-circle: Aggiungi un canto](https://hildegard-form.streamlit.app){ .md-button }


### Altro
Di seguito altri 20 canti che potrebbero essere adatti per la liturgia ma sono stati esclusi perchè il loro punteggio di adeguatezza non ha raggiunto la soglia minima.

{% set canti_esclusi = load_json('data/not-selected-20251005.json') %}

??? question "Apri lista"

    <div class="w-full max-w-4xl mx-auto">
    {% for canto in canti_esclusi %}
    <div class="bg-gray-50 rounded border border-gray-200 p-3 mb-3 flex flex-col md:flex-row justify-between items-center text-center md:text-left shadow-sm hover:shadow-md transition-shadow">
      <div class="flex-grow mb-2 md:mb-0">
        <h5 class="text-base font-normal text-gray-700" style="text-transform: none !important; font-variant: normal !important;">{{ canto.titolo }}</h5>
      </div>
      <div class="flex items-center gap-4">
        <span class="text-xs bg-gray-200 text-gray-600 rounded px-2 py-1">{{ canto.score }}%</span>
        <a href="https://www.librettocanti.it/canto/{{ canto.titolo | lower | replace(' ', '-') }}-{{ canto.id_canti }}" class="text-primary-600 hover:text-primary-800 text-xs" target="_blank">
          <span class="flex items-center"><i class="material-icons" style="font-size: 0.8rem; margin-right: 0.25rem;">description</i> Testo</span>
        </a>
      </div>
    </div>
    {% endfor %}
    </div>


## Note
!!! warning "Attenzione"
    I canti sono selezionati automaticamente da un algoritmo che confronta i testi. La selezione potrebbe non essere accurata; pertanto ti consigliamo comunque di leggere la liturgia per verificare personalmente l'adeguatezza dei suggerimenti!<br>Per maggiori informazioni sull'algoritmo di selezione puoi leggere la [pagina del progetto](https://hildegard.it/progetto/).

!!! info "Testi"
    I testi dei canti sono stati tratti da [librettocanti.it](https://www.librettocanti.it/). Si ringrazia Michele Mammini per la disponibilità <3

