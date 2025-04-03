{% set canti = load_json('data/suggeriti-top20-20250406.json') %}

## <span id="canti-suggeriti" class="text-primary-700 font-bold"> :material-music-note-plus: Canti suggeriti per Domenica 6 aprile 2025</span>

??? quote "Leggi la liturgia"

    {% include-markdown "https://raw.githubusercontent.com/dennisangemi/hildegard/refs/heads/main/risorse/lezionari/liturgia-latest.txt" %}

    ---

    [Apri la liturgia della CEI :material-arrow-right:](https://www.chiesacattolica.it/liturgia-del-giorno/?data-liturgia=20250406){ .md-button }

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
    | [Gesù che sta passando](https://www.librettocanti.it/canto/ges-che-sta-passando-2337) | :material-dots-horizontal: Mh | 48 | Figli del Divino Amore |  |
    | [Il Signore della danza](https://www.librettocanti.it/canto/il-signore-della-danza-1555) | :material-dots-horizontal: Mh | 47 |  |  |
    | [Io credo in te Gesù](https://www.librettocanti.it/canto/io-credo-in-te-ges-1678) | :material-dots-horizontal: Mh | 47 | RnS - Reuben Morgan | Io credo |
    | [Canzone della speranza](https://www.librettocanti.it/canto/canzone-della-speranza-1616) | :material-dots-horizontal: Mh | 46 | Paolo Iotti |  |
    | [Nostra gloria è la Croce](https://www.librettocanti.it/canto/nostra-gloria-la-croce-2798) | :material-dots-horizontal: Mh | 46 | Dargenio |  |
    | [Cristo è risorto veramente](https://www.librettocanti.it/canto/cristo-risorto-veramente-145) | :material-dots-horizontal: Mh | 46 | RnS | Venti dello Spirito |
    | [Canto di contrizione](https://www.librettocanti.it/canto/canto-di-contrizione-2115) | :material-dots-horizontal: Mh | 46 | Valmaggi |  |
    | [Io credo in te Gesù (v2)](https://www.librettocanti.it/canto/io-credo-in-te-ges-v2-2393) | :material-dots-horizontal: Mh | 46 | RnS - Reuben Morgan | Io credo |
    | [E la strada si apre](https://www.librettocanti.it/canto/e-la-strada-si-apre-1880) | :material-dots-horizontal: Mh | 46 | Gen Arcobaleno |  |
    | [Dio della storia](https://www.librettocanti.it/canto/dio-della-storia-2921) | :material-dots-horizontal: Mh | 45 | RnS | Mi ami tu? |
    | [Ora che sei qui (Now That You're Near)](https://www.librettocanti.it/canto/ora-che-sei-qui-now-that-you-re-near-2553) | :material-dots-horizontal: Mh | 45 | Hillsong  |  |
    | [Laudato sii, o mi Signore](https://www.librettocanti.it/canto/laudato-sii-o-mi-signore-278) | :material-dots-horizontal: Mh | 45 | --- |  |
    | [Alla mensa del Signore](https://www.librettocanti.it/canto/alla-mensa-del-signore-13) | :material-dots-horizontal: Mh | 45 | Francesco Buttazzo |  |
    | [E pace intima](https://www.librettocanti.it/canto/e-pace-intima-177) | :material-dots-horizontal: Mh | 45 | Gen Rosso | Se siamo uniti |
    | [Il Figliol Prodigo (Abbracciami Gesù)](https://www.librettocanti.it/canto/il-figliol-prodigo-abbracciami-ges-1596) | :material-dots-horizontal: Mh | 43 | Figli del Divino Amore |  |
    | [Chi ha sete](https://www.librettocanti.it/canto/chi-ha-sete-1757) | :material-dots-horizontal: Mh | 43 | Charles Christmas |  |
    | [I Tuoi passi](https://www.librettocanti.it/canto/i-tuoi-passi-222) | :material-dots-horizontal: Mh | 43 | padre daniele  |  |
    | [Luce per noi](https://www.librettocanti.it/canto/luce-per-noi-2104) | :material-dots-horizontal: Mh | 43 | Oratorio Salesiano di Arese |  |
    | [E lo credemmo abbandonato da DIo](https://www.librettocanti.it/canto/e-lo-credemmo-abbandonato-da-dio-2301) | :material-dots-horizontal: Mh | 43 | Pierangelo Sequeri |  |
    | [Dio aprirà una via](https://www.librettocanti.it/canto/dio-aprir-una-via-1686) | :material-dots-horizontal: Mh | 43 | Don Moen |  |
## Note
!!! warning "Attenzione"
    I canti sono selezionati automaticamente da un algoritmo che confronta i testi. La selezione potrebbe non essere accurata; pertanto ti consigliamo comunque di leggere la liturgia per verificare personalmente l'adeguatezza dei suggerimenti!<br>Per maggiori informazioni sull'algoritmo di selezione puoi leggere la [pagina del progetto](https://hildegard.it/progetto/).

!!! info "Testi"
    I testi dei canti sono stati tratti da [librettocanti.it](https://www.librettocanti.it/). Si ringrazia Michele Mammini per la disponibilità <3


