from pathlib import Path
import json
from dataclasses import dataclass, asdict
from random import choice

@dataclass
class Aktiviteetti():
    id: int
    kuvaus: str
    kesto: int

def normalisoi_vertailuun(teksti):
    return teksti.strip().casefold()

class Aktiviteetti_Manager:
    def __init__(self):
        self.viimeisin_mtime = None
        self.data = []
        self.viesti = ""
        self.uusi_viesti = False
        self.data_polku = self.hae_data_polku() #Määritetään tiedostopolut ja tehdään tarvittaessa tiedostot      
        self.arpoja = FIFOarpoja()

    def hae_data_polku(self):
        OHJELMAKANSIO = Path(__file__).parent
        config_polku = OHJELMAKANSIO / "config.json"

        if not config_polku.exists():
            with open(config_polku, "w", encoding="utf-8") as f:
                json.dump(
                    {"data_polku": "data.json"},
                    f,
                    ensure_ascii=False,
                    indent=4
                )

        with open(config_polku, "r", encoding="utf-8") as f:
            config = json.load(f)

        data_polku = Path(config["data_polku"])

        if not data_polku.exists():
            data_polku.parent.mkdir(parents=True, exist_ok=True)

            with open(data_polku, "w", encoding="utf-8") as f:
                json.dump(
                {
                    "aktiviteetit": [],
                    "arvonta": {
                        "vaihtoehdot": [],
                        "estetyt": []
                    }
                },
                f,
                    ensure_ascii=False,
                    indent=4
                )
        return data_polku
    
    def lue_json(self) -> None:
        if self.data_polku.exists():
            with open(self.data_polku, "r", encoding = "utf-8") as f:
                raakadata = json.load(f)

            self.data = [Aktiviteetti(**rivi) for rivi in raakadata["aktiviteetit"]]
            arvonta = raakadata.get("arvonta", {})
            self.arpoja = FIFOarpoja(
                arvonta.get("vaihtoehdot", []),
                arvonta.get("estetyt", [])
                )        
        else:
            raise FileNotFoundError(
                f"Tiedostoa ei löytynyt: {self.data_polku}"
                )

    def kirjoita_json(self):
        tallennettava = {
            "aktiviteetit": [
                asdict(aktiviteetti)
                for aktiviteetti in self.data
            ],        
            "arvonta": {
                "vaihtoehdot": self.arpoja.vaihtoehdot,
                "estetyt": self.arpoja.estetyt
            }
            }
        with open(self.data_polku, "w", encoding = "utf-8") as j:
            json.dump(tallennettava, j, ensure_ascii=False, indent=4)
        

    def lisaa_aktiviteetti(self, lisa_kuvaus, lisa_kesto):
        if not lisa_kuvaus.strip():
            self.lisaa_viesti("Anna aktiviteetti!")
            return
        self.lue_json()
        # Päivitetään ensin olemassaoleva aktiviteetti jos löytyy
        for aktiviteetti in self.data:
            if normalisoi_vertailuun(aktiviteetti.kuvaus) == normalisoi_vertailuun(lisa_kuvaus):
                if lisa_kesto is not None:
                    aktiviteetti.kesto = lisa_kesto
                self.kirjoita_json()
                self.lisaa_viesti("Päivitetty!")
                return
         
        # lisätään uusi aktiviteetti jos ei ollut ennestään
        uusi_id = max([aktiviteetti.id for aktiviteetti in self.data], default=0) + 1
        uusi_meno = Aktiviteetti(uusi_id, lisa_kuvaus, lisa_kesto)
        self.data.append(uusi_meno)

        self.kirjoita_json()
        self.lisaa_viesti("Tallennettu!")
        return 
    
    def muokkaa_aktiviteettia(self, id, kuvaus=None, kesto=None):
        for akt in self.data:
            if akt.id == id:
                if kuvaus is not None:

                    akt.kuvaus = kuvaus
                if kesto is not None:
                    akt.kesto = kesto
                self.kirjoita_json()
                return

    def tarkista_data_muutos(self):
        nykyinen_mtime = self.data_polku.stat().st_mtime
        if nykyinen_mtime != self.viimeisin_mtime:
            self.viimeisin_mtime = nykyinen_mtime
            return True
        return False
    
    def lisaa_viesti(self, viesti):
        self.uusi_viesti = True
        self.viesti = viesti

    def listaa_keston_mukaan(self, kayt_aika: int) -> list:
        self.lue_json()
        valitut = []
        jaljella = kayt_aika
        
        while jaljella > 0:
            sopivat = [
                akt for akt in self.data if akt.kesto <= jaljella
            ]
            sopivat_idt = [akt.id for akt in sopivat]

            if not sopivat_idt:
                break

            valittu = self.arpoja.valitse(sopivat_idt)
            for akt in self.data:
                if akt.id == valittu:
                    jaljella -= akt.kesto
                    valitut.append(akt.kuvaus)
                    break
        self.kirjoita_json()
        return valitut


class FIFOarpoja:
    def __init__(self, vaihtoehdot=None, estetyt=None):
        self.vaihtoehdot = vaihtoehdot or []
        self.estetyt = estetyt or []
    
    def laske_eston_pituus(self, maara):
        
        if maara <= 1:
            return 0
        if maara <= 3:
            return 1
        if maara <= 6:
            return 2
        return 3 
    
    def valitse(self, kaikki):
        
        #siivotaan listat siltä varalta, että "kaikki"-listaa on muutettu
        self.vaihtoehdot = [x for x in self.vaihtoehdot if x in kaikki]
        self.estetyt = [x for x in self.estetyt if x in kaikki]
            
        estopituus = self.laske_eston_pituus(len(kaikki))
        if not self.vaihtoehdot:
            self.vaihtoehdot = list(kaikki)
        aktiviteetti = choice(self.vaihtoehdot)
        self.estetyt.append(aktiviteetti)
        self.vaihtoehdot.remove(aktiviteetti)
        
        if len(self.estetyt) > estopituus:
            self.vaihtoehdot.append(self.estetyt.pop(0))

        return aktiviteetti

        
if __name__ == "__main__":
    print("Ei suoritettava tiedosto")
    testimanageri = Aktiviteetti_Manager()
    print()
    print("0 lopettaa")
    print()
    while True:

        kesto = int(input("Anna kesto 1-3 "))
        
        try:
            arvotut = testimanageri.listaa_keston_mukaan(kesto)
            print("Ehdotukset:")
            for arvottu in arvotut:
                print(f"  - {arvottu}")
            print()
        except :
            print("Numero 1-3 kiitos")
            continue