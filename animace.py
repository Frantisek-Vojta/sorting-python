# okno s animaci jednoho algoritmu
#
# jak to funguje:
# 1. algoritmus pustime hned na zacatku a on si zapise vsechny kroky do seznamu
# 2. kazdy krok je (seznam hodnot, aktivni pozice, popis)
# 3. animace pak jen kresli jeden krok za druhym

import tkinter as tk
from tkinter import ttk

# barvy
POZADI = "#13203a"
MODRA = "#60a5fa"
ORANZOVA = "#f59e0b"
ZELENA = "#22c55e"
TEXT = "#ffffff"

# rozmery sloupcu v pixelech
SIRKA_SLOUPCE = 60
MEZERA = 8
VYSKA_GRAFU = 380
VYSKA_POPISKU = 45


class OknoAnimace:
    def __init__(self, rodic, algoritmus, data):
        self.okno = tk.Toplevel(rodic)
        self.okno.title("Animace - " + algoritmus["nazev"])
        self.okno.geometry("1100x720")

        # spocitame vsechny kroky dopredu
        self.kroky = [(data.copy(), [], "Výchozí pořadí")]
        kopie = data.copy()
        algoritmus["funkce"](kopie, self.kroky)
        self.kroky.append((kopie.copy(), [], "Hotovo, seřazeno"))

        # vyska sloupce = poradi hodnoty mezi unikatnimi hodnotami
        # (takze to funguje i pro zaporna cisla a text)
        unikatni = sorted(set(data))
        self.poradi = {}
        for i, hodnota in enumerate(unikatni):
            self.poradi[hodnota] = i + 1
        self.pocet_unikatnich = len(unikatni)

        self.krok = 0         # ktery krok zrovna ukazujeme
        self.prehrava = False  # jestli bezi prehravani
        self.casovac = None    # id naplanovaneho dalsiho kroku

        self.vytvor_ovladani(algoritmus)
        self.nakresli()

        # kdyz se okno zavre krizkem, zastavime casovac
        self.okno.protocol("WM_DELETE_WINDOW", self.zavrit)

    def vytvor_ovladani(self, algoritmus):
        # nadpis a vysvetleni algoritmu
        ttk.Label(self.okno, text=algoritmus["nazev"], font=("", 20, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
        ttk.Label(self.okno, text=algoritmus["popis"], wraplength=1050).pack(anchor="w", padx=10, pady=5)
        ttk.Label(self.okno, text="Oranžová: aktivní prvky • Modrá: ostatní prvky • Zelená: hotovo").pack(anchor="w", padx=10)

        # platno na sloupce + posuvnik, kdyz se nevejdou
        ramecek = ttk.Frame(self.okno)
        ramecek.pack(fill="x", padx=10, pady=5)
        self.platno = tk.Canvas(ramecek, bg=POZADI, height=VYSKA_GRAFU + VYSKA_POPISKU, highlightthickness=0)
        self.platno.pack(fill="x")
        posuvnik = ttk.Scrollbar(ramecek, orient="horizontal", command=self.platno.xview)
        posuvnik.pack(fill="x")
        self.platno.config(xscrollcommand=posuvnik.set)
        # kdyz jedeme mysi nad sloupcem, ukazeme jeho hodnotu
        self.platno.bind("<Motion>", self.mys_nad_sloupcem)

        ttk.Label(self.okno, text="Výška sloupce = pořadí hodnoty mezi unikátními hodnotami; dole je její popisek.").pack(anchor="w", padx=10)
        self.popisek_pozice = ttk.Label(self.okno, text="Najeď myší na sloupec")
        self.popisek_pozice.pack(anchor="w", padx=10, pady=5)

        # tlacitka dole
        tlacitka = ttk.Frame(self.okno)
        tlacitka.pack(fill="x", padx=10, pady=10)
        self.tlacitko_prehrat = ttk.Button(tlacitka, text="Přehrát", command=self.prehrat_pauza)
        self.tlacitko_prehrat.pack(side="left", padx=3)
        ttk.Button(tlacitka, text="Jeden krok", command=self.jeden_krok).pack(side="left", padx=3)
        ttk.Button(tlacitka, text="Od začátku", command=self.od_zacatku).pack(side="left", padx=3)

        ttk.Label(tlacitka, text="Rychlost:").pack(side="left", padx=(20, 5))
        self.rychlost = tk.IntVar(value=5)
        ttk.Scale(tlacitka, from_=1, to=50, variable=self.rychlost, length=200,
                  command=self.zmena_rychlosti).pack(side="left")
        self.popisek_rychlosti = ttk.Label(tlacitka, text="5 kroků / s", width=12)
        self.popisek_rychlosti.pack(side="left", padx=5)

        ttk.Button(tlacitka, text="Zavřít", command=self.zavrit).pack(side="right")

        self.popisek_kroku = ttk.Label(self.okno, text="")
        self.popisek_kroku.pack(anchor="w", padx=10)

    def nakresli(self):
        # smazeme stare sloupce a nakreslime aktualni krok
        self.platno.delete("all")
        hodnoty, aktivni, popis = self.kroky[self.krok]
        posledni_krok = self.krok == len(self.kroky) - 1

        for i, hodnota in enumerate(hodnoty):
            # vybereme barvu
            if posledni_krok:
                barva = ZELENA
            elif i in aktivni:
                barva = ORANZOVA
            else:
                barva = MODRA

            # vyska podle poradi hodnoty
            vyska = self.poradi[hodnota] / self.pocet_unikatnich * (VYSKA_GRAFU - 20)
            x1 = i * (SIRKA_SLOUPCE + MEZERA) + MEZERA
            x2 = x1 + SIRKA_SLOUPCE
            y1 = VYSKA_GRAFU - vyska
            y2 = VYSKA_GRAFU
            self.platno.create_rectangle(x1, y1, x2, y2, fill=barva, outline="")

            # popisky pod sloupcem: hodnota a cislo pozice
            stred = (x1 + x2) / 2
            self.platno.create_text(stred, VYSKA_GRAFU + 15, text=str(hodnota), fill=TEXT)
            self.platno.create_text(stred, VYSKA_GRAFU + 32, text=str(i + 1), fill="#9ca3af", font=("", 8))

        # nastavime jak siroke je platno, aby fungoval posuvnik
        celkova_sirka = len(hodnoty) * (SIRKA_SLOUPCE + MEZERA) + MEZERA
        self.platno.config(scrollregion=(0, 0, celkova_sirka, VYSKA_GRAFU + VYSKA_POPISKU))

        # text pod grafem, co se zrovna deje
        text = f"Krok {self.krok + 1} / {len(self.kroky)} • {popis}"
        if aktivni:
            pozice = " a ".join(str(p + 1) for p in aktivni)
            text += f" (pozice {pozice})"
        self.popisek_kroku.config(text=text)

    def mys_nad_sloupcem(self, udalost):
        # prepocitame x mysi na cislo sloupce (canvasx pocita i s posunutim)
        x = self.platno.canvasx(udalost.x)
        i = int(x // (SIRKA_SLOUPCE + MEZERA))
        hodnoty = self.kroky[self.krok][0]
        if 0 <= i < len(hodnoty):
            self.popisek_pozice.config(text=f"Pozice {i + 1}: {hodnoty[i]}")

    def jeden_krok(self):
        # posuneme se o krok dal, pokud nejsme na konci
        if self.krok < len(self.kroky) - 1:
            self.krok += 1
            self.nakresli()

    def prehrat_pauza(self):
        if self.prehrava:
            self.zastav()
        else:
            # kdyz jsme na konci, zacneme znovu
            if self.krok == len(self.kroky) - 1:
                self.krok = 0
            self.prehrava = True
            self.tlacitko_prehrat.config(text="Pauza")
            self.dalsi_snimek()

    def dalsi_snimek(self):
        # udela jeden krok a naplanuje dalsi (tak vznikne animace)
        if not self.prehrava:
            return
        self.jeden_krok()
        if self.krok == len(self.kroky) - 1:
            self.zastav()
            return
        cekani = int(1000 / self.rychlost.get())
        self.casovac = self.okno.after(cekani, self.dalsi_snimek)

    def zastav(self):
        self.prehrava = False
        self.tlacitko_prehrat.config(text="Přehrát")
        if self.casovac is not None:
            self.okno.after_cancel(self.casovac)
            self.casovac = None

    def od_zacatku(self):
        self.zastav()
        self.krok = 0
        self.nakresli()

    def zmena_rychlosti(self, hodnota):
        # posuvnik vraci desetinne cislo, zaokrouhlime ho
        self.rychlost.set(round(float(hodnota)))
        self.popisek_rychlosti.config(text=f"{self.rychlost.get()} kroků / s")

    def zavrit(self):
        self.zastav()
        self.okno.destroy()
