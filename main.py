import tkinter as tk
from tkinter import ttk
from aktiviteetti_funktiot import Aktiviteetti_Manager
from gui_funktiot import tee_arvo_tab, tee_lisays_tab, tayta_taulukko

def maingui():

    ikkuna = tk.Tk()
    ikkuna.title("Aktiviteettien suunnittelija")
    
    valilehdet = ttk.Notebook(ikkuna)
    valilehdet.pack(fill="both", expand=True)

    tab_arvo = ttk.Frame(valilehdet)
    tab_lisaa = ttk.Frame(valilehdet)
    manager = Aktiviteetti_Manager()

    tee_arvo_tab(tab_arvo, manager)

    akt_taulukot, ilmoitusalue = tee_lisays_tab(tab_lisaa, manager)

    def tarkista_ja_paivita():
        if manager.tarkista_data_muutos():
            tayta_taulukko(akt_taulukot, manager)
        ikkuna.after(2000, tarkista_ja_paivita)

    tarkista_ja_paivita()

    def uusi_viesti():
        if manager.uusi_viesti:
            ilmoitusalue.config(text=manager.viesti)
            manager.uusi_viesti = False
            def tyhjenna():
                ilmoitusalue.config(text="")
                manager.viesti = ""
            ilmoitusalue.after(2000, tyhjenna)
        ikkuna.after(500, uusi_viesti)
    
    uusi_viesti()

    valilehdet.add(tab_arvo, text="Aktiviteetin valinta")
    valilehdet.add(tab_lisaa, text="Aktiviteettien lisäys")
    
    ikkuna.mainloop()

if __name__ == "__main__":
    maingui()