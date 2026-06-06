from pathlib import Path
import json
from dataclasses import dataclass, asdict

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
        self.data_polku = self.hae_data_polku() #Määritetään tiedostopolut ja tehdään tarvittaessa tiedostot      

    def hae_data_polku(self):
        config_polku = Path("config.json")

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
                    {"aktiviteetit": []},
                    f,
                    ensure_ascii=False,
                    indent=4
                )
        return data_polku
    
    def lue_json(self):
        if self.data_polku.exists():
            with open(self.data_polku, "r", encoding = "utf-8") as f:
                raakadata = json.load(f)

            self.data = [Aktiviteetti(**rivi) for rivi in raakadata["aktiviteetit"]]
        else:
            raise FileNotFoundError(
                f"Tiedostoa ei löytynyt: {self.data_polku}"
                )

    def kirjoita_json(self):
        tallennettava = {
            "aktiviteetit": [
                asdict(aktiviteetti)
                for aktiviteetti in self.data
            ]
            }
        with open(self.data_polku, "w", encoding = "utf-8") as j:
            json.dump(tallennettava, j, ensure_ascii=False, indent=4)
        

    def lisaa_aktiviteetti(self, lisa_kuvaus, lisa_kesto):
        if not lisa_kuvaus.strip():
            self.viesti =  "Anna aktiviteetti!"
            return
        self.lue_json()
        # Päivitetään ensin olemassaoleva aktiviteetti jos löytyy
        for aktiviteetti in self.data:
            if normalisoi_vertailuun(aktiviteetti.kuvaus) == normalisoi_vertailuun(lisa_kuvaus):
                if lisa_kesto is not None:
                    aktiviteetti.kesto = lisa_kesto
                self.kirjoita_json()
                self.viesti = "Päivitetty!"
                return
         
        # lisätään uusi aktiviteetti jos ei ollut ennestään
        uusi_id = max([aktiviteetti.id for aktiviteetti in self.data], default=0) + 1
        uusi_meno = Aktiviteetti(uusi_id, lisa_kuvaus, lisa_kesto)
        self.data.append(uusi_meno)

        self.kirjoita_json()
        self.viesti = "Tallennettu!"
        return 

    def tulosta_aktiviteetit(self):
        self.lue_json()
        return self.data
    
        
    def tarkista_data_muutos(self):
        nykyinen_mtime = self.data_polku.stat().st_mtime
        if nykyinen_mtime != self.viimeisin_mtime:
            self.viimeisin_mtime = nykyinen_mtime
            return True
        return False
        
if __name__ == "__main__":
    print("Ei suoritettava tiedosto")