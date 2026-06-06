import tkinter as tk
from tkinter import ttk

def tee_lisays_tab(alue, manageri):

    lisaysalue = ttk.Frame(alue)
    lisaysalue.grid(row=0, column=0, sticky="ew")

    taulukkoalue = ttk.Frame(alue)
    taulukkoalue.grid(row=1, column=0, sticky="nsew")
    
    alue.columnconfigure(0, weight=1)
    alue.rowconfigure(1, weight=1)

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
    
    viesti = ttk.Label(lisaysalue, text="")
    viesti.grid(row=5, column=0) 

    def tyhjenna_viesti():
        manageri.viesti = ""
        viesti.config(text="")

    viesti.config(text=manageri.viesti)
    viesti.after(2000,tyhjenna_viesti)

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

    return taulukot

def tayta_taulukko(taulukot, manageri):
    manageri.lue_json()
    for taulukko in taulukot:
        for rivi in taulukko.get_children():
            taulukko.delete(rivi)

    for akt in manageri.data:
        if akt.kesto == 1: #hetki
                taulukot[0].insert("", "end", values=(
                akt.kuvaus,
            ))
        elif akt.kesto == 2: #päivä
                taulukot[1].insert("", "end", values=(
                akt.kuvaus,
            ))
        else:   #viikonloppu
            taulukot[2].insert("", "end", values=(
                akt.kuvaus,
            ))
    return taulukot
                

if __name__ == "__main__":
    print("Ei suoritettava tiedosto")