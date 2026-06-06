# Aktiviteetti_suunnittelija

Yksinkertainen Python- ja Tkinter-pohjainen sovellus aktiviteettien ideointiin ja säilyttämiseen.

Aktiviteetit jaotellaan niiden keston mukaan kolmeen ryhmään:

* Hetki
* Päivä
* Viikonloppu

Tarkoituksena on lisätä myöhemmin aktiviteetin arvonta ensimmäiselle välilehdelle, jotta voi päättää mitä tekee kun ei ole oikein inspiraatiota löytynyt

## Ominaisuudet

* Aktiviteettien lisääminen graafisella käyttöliittymällä
* Aktiviteettien automaattinen tallennus JSON-tiedostoon
* Aktiviteettien päivittäminen, jos sama aktiviteetti lisätään uudelleen
* Aktiviteettien ryhmittely keston mukaan
* Taulukoiden automaattinen päivittyminen, jos data muuttuu
* Mahdollisuus käyttää yhteistä dataa esimerkiksi NAS-verkkoasemalla

## Käyttöönotto

Kloonaa projekti:

```bash
git clone https://github.com/Jussiol/Aktiviteetti_suunnittelija.git
cd Aktiviteetti_suunnittelija
```

Käynnistä ohjelma:

```bash
python main.py
```

Ensimmäisellä käynnistyksellä ohjelma luo automaattisesti tarvittavat tiedostot:

* `config.json`
* `data.json`

## Datan sijainti

Oletuksena aktiviteetit tallennetaan projektikansion `data.json`-tiedostoon.

Jos haluat käyttää yhteistä dataa esimerkiksi perheen NAS-palvelimella, muokkaa `config.json`-tiedostoa:

```json
{
    "data_polku": "\\\\PALVELIN\\Jaettu\\Aktiviteetti_suunnittelija\\data.json"
}
```

## Teknologiat

* Python 3
* Tkinter
* JSON
* Dataclasses
* pathlib

## Tulevaisuuden kehitysideoita

* Aktiviteetin arpominen ohjelman ensimmäisellä välilehdellä
* Aktiviteettien muokkaus ja poistaminen käyttöliittymästä

## Lisenssi

Tällä hetkellä projektille ei ole määritelty erillistä lisenssiä.
