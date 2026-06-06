import tkinter as tk
from tkinter import ttk
from aktiviteetti_funktiot import Aktiviteetti_Manager
from gui_funktiot import tee_lisays_tab, tayta_taulukko

def maingui():

    ikkuna = tk.Tk()
    ikkuna.title("Aktiviteettien suunnittelija")
    
    valilehdet = ttk.Notebook(ikkuna)
    valilehdet.pack(fill="both", expand=True)

    tab_arvo = ttk.Frame(valilehdet)
    tab_lisaa = ttk.Frame(valilehdet)
    manager = Aktiviteetti_Manager()

    akt_taulukot = tee_lisays_tab(tab_lisaa, manager)

    def tarkista_ja_paivita():
        if manager.tarkista_data_muutos():
            tayta_taulukko(akt_taulukot, manager)
        ikkuna.after(2000, tarkista_ja_paivita)

    tarkista_ja_paivita()

    valilehdet.add(tab_arvo, text="Aktiviteetin valinta")
    valilehdet.add(tab_lisaa, text="Aktiviteettien lisäys")
    
    ikkuna.mainloop()

if __name__ == "__main__":
    maingui()