
# PyMetronome

Um simples metrônomo, feito em Python, para estudar música.


## Screenshots

![App Screenshot](tela.jpg)


## Instalação

O ideal é criar um ambiente virtual com o Python 3.12.

Instale PyMetronome com pip.

```bash
  git clone
  cd metronome
  pip install -r requirements.txt
```


Execute o código com:
```bash
  python metronome.py
```
    
## Criando executável

```bash
pyinstaller --onefile --windowed --add-data "click.wav;." --icon="metronome.ico" metronome.py
```

