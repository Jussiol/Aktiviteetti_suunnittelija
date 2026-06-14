import tkinter as tk
from tkinter import ttk

def tee_arvo_tab(alue, manageri):
    print("Arvonta tehty cli mutta gui puuttuu")
    
def tee_lisays_tab(alue, manageri):

    ilmoitusalue = ttk.Label(alue)
    ilmoitusalue.grid(row=0, column=0, sticky="ew")
    
    lisaysalue = ttk.Frame(alue)
    lisaysalue.grid(row=1, column=0, sticky="ew")

    taulukkoalue = ttk.Frame(alue)
    taulukkoalue.grid(row=2, column=0, sticky="nsew")
   
    alue.columnconfigure(0, weight=1)
    alue.columnconfigure(1, weight=1)
    alue.rowconfigure(2, weight=1)

    lisaysalue.columnconfigure(0, weight=1)
    taulukkoalue.columnconfigure(0, weight=1)
    taulukkoalue.columnconfigure(1, weight=1)
    taulukkoalue.columnconfigure(2, weight=1)

    ## LISÄYSALUE

    ttk.Label(lisaysalue, text="Lisää aktiviteetti").grid(row=0, column=0, sticky="ew", padx=10, pady=10)
    
    aktiviteetti_entry = ttk.Entry(lisaysalue)
    aktiviteetti_entry.grid(row=1, column=0, sticky= "ew")

    radiobutton_frame = ttk.Frame(lisaysalue)
    
    kesto = tk.IntVar(value=1)
    ttk.Radiobutton(
        radiobutton_frame,
        text="Hetki",
        variable=kesto,
        value=1
    ).pack(side="left")
    ttk.Radiobutton(
        radiobutton_frame,
        text="Päivä",
        variable=kesto,
        value=2
    ).pack(side="left")
    ttk.Radiobutton(
        radiobutton_frame,
        text="Viikonloppu",
        variable=kesto,
        value=3
    ).pack(side="left")

    radiobutton_frame.grid(row=3, column=0)
    
    ttk.Button(
        lisaysalue,
        text="Tallenna",
        command=lambda: manageri.lisaa_aktiviteetti(aktiviteetti_entry.get(), kesto.get())
    ).grid(row=4, column=0)

    ## AKTIVITEETTIALUE TAULUKOT

    sarake = "Aktiviteetti"
    taulukko_hetki = ttk.Treeview(taulukkoalue, columns=sarake, show="headings")
    taulukko_paiva = ttk.Treeview(taulukkoalue, columns=sarake, show="headings")
    taulukko_vloppu = ttk.Treeview(taulukkoalue, columns=sarake, show="headings")

    taulukko_hetki.heading(sarake, text="Hetki")
    taulukko_paiva.heading(sarake, text="Päivä")
    taulukko_vloppu.heading(sarake, text="Viikonloppu")

    taulukko_hetki.column("Aktiviteetti", width=200, stretch=True)
    taulukko_hetki.column("Aktiviteetti", width=200, stretch=True)
    taulukko_hetki.column("Aktiviteetti", width=200, stretch=True)

    ## Taulukoiden arvojen muokkaus
    taulukko_hetki.bind("<Double-1>", lambda e: avaa_muokkaa_akt(alue, taulukko_hetki, onDoubleClick(taulukko_hetki), manageri))
    taulukko_paiva.bind("<Double-1>", lambda e: avaa_muokkaa_akt(alue, taulukko_paiva, onDoubleClick(taulukko_paiva), manageri))
    taulukko_vloppu.bind("<Double-1>", lambda e: avaa_muokkaa_akt(alue, taulukko_vloppu, onDoubleClick(taulukko_vloppu), manageri))

    ttk.Label(taulukkoalue, text="Aktiviteetit").grid(row=0, columnspan=3, sticky="ew")
   
    taulukko_hetki.grid(row=1, column=0)
    taulukko_paiva.grid(row=1, column=1)
    taulukko_vloppu.grid(row=1, column=2)

    taulukko_hetki.grid(row=1, column=0, sticky="nsew")
    taulukko_paiva.grid(row=1, column=1, sticky="nsew")
    taulukko_vloppu.grid(row=1, column=2, sticky="nsew")

    taulukot = [taulukko_hetki, taulukko_paiva, taulukko_vloppu]
    tayta_taulukko(taulukot, manageri)

    ttk.Label(taulukkoalue, text= f"\nTallennus: {manageri.data_polku}").grid(row=2, columnspan=3, sticky="ew")

    return taulukot, ilmoitusalue


def avaa_muokkaa_akt(root, tree, id, manageri):
    ikkuna = tk.Toplevel(root)
    ikkuna.title("Muokkaa aktiviteettia")
    
    ttk.Label(ikkuna, text="Kuvaus").grid(row=0, column=0)
    kuvaus_entry = ttk.Entry(ikkuna)
    kuvaus_entry.grid(row=0, column=1)
    
    for akt in manageri.data:
         if akt.id == int(id):
              kuvaus_entry.insert(0, akt.kuvaus)
              kesto = akt.kesto
              break


    #radiobuttonit
    #ttk.Label(ikkuna, text="Summa").grid(row=1, column=0)
    #summa_entry = ttk.Entry(ikkuna)
    #summa_entry.grid(row=1, column=1)

    #poistonappi
    #ttk.Label(ikkuna, text="Kategoria").grid(row=2, column=0)
    #kategoria_entry = ttk.Entry(ikkuna)
    #kategoria_entry.grid(row=2, column=1)

    
    def muokkaa():
        manageri.muokkaa_aktiviteettia(int(id), kuvaus_entry.get())

    ttk.Button(
        ikkuna,
        text="Muokkaa",
        command=muokkaa
    ).grid(row=3, columnspan=2, pady=10)
    
def onDoubleClick(taulukko):
    item = taulukko.selection()[0]
    return item

def tayta_taulukko(taulukot, manageri):
    manageri.lue_json()
    for taulukko in taulukot:
        for rivi in taulukko.get_children():
            taulukko.delete(rivi)

    for akt in manageri.data:
        if akt.kesto == 1: #hetki
                taulukot[0].insert("", "end", values=(
                akt.kuvaus,), iid = akt.id
                )
        elif akt.kesto == 2: #päivä
                taulukot[1].insert("", "end", values=(
                akt.kuvaus,), iid = akt.id
                )
        else:   #viikonloppu
            taulukot[2].insert("", "end", values=(
                akt.kuvaus,), iid = akt.id
                )
    return taulukot
                

if __name__ == "__main__":
    print("Ei suoritettava tiedosto")