# Hildegard

### Il suggeritore di canti liturgici

Ti interessano i canti consigliati e più adatti per la liturgia della prossima domenica? [Fai click qui!](https://dennisangemi.github.io/hildegard/)

## Set up
Clone/download this repo

### Requirements
- utility [`scrape`](https://github.com/aborruso/scrape-cli)
    ```sh
    sudo cp ./bin/scrape /usr/bin
    sudo chmod +x /usr/bin/scrape
    ```
- utility [`mlr`](https://miller.readthedocs.io/en/6.12.0/)
    ```sh
    sudo cp ./bin/mlr /usr/bin
    sudo chmod +x /usr/bin/mlr
    ```
- python packages: yq, scikit-learn, pandas, tabulate
  ```sh
  pip install yq scikit-learn pandas tabulate
  ```

### How to build
Check requirements and then run (from the root)
```sh
chmod +x ./build
./build
```

## Note e ringraziamenti
I testi dei canti provengono da http://librettocanti.it/ sviluppato da Michele Mammini. A lui il nostro più sincero ringraziamento.
