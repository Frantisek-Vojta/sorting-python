# hlavni okno tridici aplikace
# spusteni: python main.py

import csv
import random
import statistics
import sys
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from algoritmy import ALGORITMY
from animace import OknoAnimace

# quick sort a merge sort volaji sami sebe, tak povolime vic volani v sobe
sys.setrecursionlimit(100000)

# pomale algoritmy O(n^2) pustime jen do tolika prvku
MAX_PRO_POMALE = 3000
# animace jen do tolika prvku
MAX_PRO_ANIMACI = 100

TYPY = ["Automaticky", "Celá čísla", "Desetinná čísla", "Text"]
PORADI = ["Náhodně", "Seřazeně", "Obráceně", "Skoro seřazeně"]


def generuj_data(pocet, seed, typ, poradi):
    # stejny seed = vzdycky stejna "nahodna" cisla
    nahoda = random.Random(seed)

    data = []
    for _ in range(pocet):
        if typ == "Desetinná čísla":
            data.append(round(nahoda.uniform(0, 1000), 2))
        elif typ == "Text":
            # nahodne slovo z 5 pismen
            slovo = ""
            for _ in range(5):
                slovo += nahoda.choice("abcdefghijklmnopqrstuvwxyz")
            data.append(slovo)
        else:
            data.append(nahoda.randint(0, 99999))

    # upravime poradi
    if poradi == "Seřazeně":
        data.sort()
    elif poradi == "Obráceně":
        data.sort(reverse=True)
    elif poradi == "Skoro seřazeně":
        data.sort()
        # prohodime par nahodnych dvojic
        for _ in range(max(1, pocet // 20)):
            a = nahoda.randrange(pocet)
            b = nahoda.randrange(pocet)
            data[a], data[b] = data[b], data[a]
    return data


def preved_text(text, typ):
    # carky a stredniky nahradime mezerou a rozdelime podle mezer a radku
    text = text.replace(",", " ").replace(";", " ")
    casti = text.split()

    if typ == "Celá čísla":
        return [int(c) for c in casti], typ
    if typ == "Desetinná čísla":
        return [float(c) for c in casti], typ
    if typ == "Text":
        return casti, typ

    # automaticky: zkusime cela cisla, pak desetinna, jinak text
    try:
        return [int(c) for c in casti], "Celá čísla"
    except ValueError:
        pass
    try:
        return [float(c) for c in casti], "Desetinná čísla"
    except ValueError:
        pass
    return casti, "Text"


class Aplikace:
    def __init__(self, okno):
        self.okno = okno
        self.okno.title("SortApp")
        self.okno.geometry("1050x800")

        self.data = []           # data, ktera budeme tridit
        self.vysledky = []       # vysledky posledniho porovnani
        self.zastavit = False    # nastavi tlacitko Zastavit

        ttk.Label(okno, text="SortApp", font=("", 20, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
        ttk.Label(okno, text="Stejná data. Čtyři algoritmy. Porovnání skutečné doby třídění.").pack(anchor="w", padx=10)

        self.vytvor_cast_data()
        self.vytvor_cast_algoritmy()
        self.vytvor_cast_vysledky()

        ttk.Label(okno, text=f"Pomalé metody O(n²): max. {MAX_PRO_POMALE} prvků. "
                             f"Animace: jeden algoritmus a max. {MAX_PRO_ANIMACI} hodnot.").pack(anchor="w", padx=10)
        self.stav = ttk.Label(okno, text="Připraveno.")
        self.stav.pack(anchor="w", padx=10, pady=(0, 10))

        # na zacatku rovnou vygenerujeme data
        self.generovat()

    # ---------- 1. cast: priprava dat ----------

    def vytvor_cast_data(self):
        ramecek = ttk.LabelFrame(self.okno, text="1  Připravte data")
        ramecek.pack(fill="x", padx=10, pady=5)

        # radek 1: typ hodnot a nacteni souboru
        radek = ttk.Frame(ramecek)
        radek.pack(fill="x", padx=5, pady=3)
        ttk.Label(radek, text="Typ hodnot").pack(side="left")
        self.typ = ttk.Combobox(radek, values=TYPY, state="readonly", width=18)
        self.typ.set("Automaticky")
        self.typ.pack(side="left", padx=5)
        ttk.Button(radek, text="Načíst TXT / CSV...", command=self.nacist_soubor).pack(side="right")

        # radek 2: generator
        radek = ttk.Frame(ramecek)
        radek.pack(fill="x", padx=5, pady=3)
        ttk.Label(radek, text="Počet").pack(side="left")
        self.pocet = ttk.Entry(radek, width=10)
        self.pocet.insert(0, "1000")
        self.pocet.pack(side="left", padx=5)
        ttk.Label(radek, text="Seed").pack(side="left", padx=(15, 0))
        self.seed = ttk.Entry(radek, width=10)
        self.seed.insert(0, "42")
        self.seed.pack(side="left", padx=5)
        self.poradi = ttk.Combobox(radek, values=PORADI, state="readonly", width=16)
        self.poradi.set("Náhodně")
        self.poradi.pack(side="left", padx=15)
        ttk.Button(radek, text="Generovat data", command=self.generovat).pack(side="left")

        # radek 3: rucni vstup
        ttk.Label(ramecek, text="Ruční vstup: mezery, nové řádky, čárky nebo středníky; desetinná čísla s tečkou.").pack(anchor="w", padx=5)
        radek = ttk.Frame(ramecek)
        radek.pack(fill="x", padx=5, pady=3)
        self.rucni = tk.Text(radek, height=2)
        self.rucni.insert("1.0", "12 -5 8 0 12 3")
        self.rucni.pack(side="left", fill="x", expand=True)
        ttk.Button(radek, text="Použít ruční vstup", command=self.pouzit_rucni).pack(side="left", padx=5)

        # informace o aktualnich datech
        self.info_data = ttk.Label(ramecek, text="")
        self.info_data.pack(anchor="w", padx=5, pady=3)

    def nastav_data(self, data, popis):
        # sem prijdou nova data odkudkoliv (generator, soubor, rucne)
        self.data = data
        self.info_data.config(text=f"{len(data)} hodnot • {popis}")
        self.ukaz_nahled()
        self.aktualizuj_animovat()

    def generovat(self):
        try:
            pocet = int(self.pocet.get())
            seed = int(self.seed.get())
        except ValueError:
            messagebox.showerror("Chyba", "Počet a seed musí být celá čísla.")
            return
        if pocet < 1:
            messagebox.showerror("Chyba", "Počet musí být aspoň 1.")
            return

        typ = self.typ.get()
        if typ == "Automaticky":
            typ = "Celá čísla"
        data = generuj_data(pocet, seed, typ, self.poradi.get())
        self.nastav_data(data, f"{typ} • Generátor, seed {seed}, {self.poradi.get()}")

    def pouzit_rucni(self):
        self.nacti_z_textu(self.rucni.get("1.0", "end"), "Ruční vstup")

    def nacist_soubor(self):
        cesta = filedialog.askopenfilename(filetypes=[("Text a CSV", "*.txt *.csv"), ("Všechny soubory", "*")])
        if not cesta:
            return
        with open(cesta, encoding="utf-8") as soubor:
            text = soubor.read()
        self.nacti_z_textu(text, "Soubor " + cesta)

    def nacti_z_textu(self, text, odkud):
        try:
            data, typ = preved_text(text, self.typ.get())
        except ValueError:
            messagebox.showerror("Chyba", f"Některé hodnoty nejsou typu: {self.typ.get()}")
            return
        if not data:
            messagebox.showerror("Chyba", "Nejsou tam žádné hodnoty.")
            return
        self.nastav_data(data, f"{typ} • {odkud}")

    # ---------- 2. cast: vyber algoritmu ----------

    def vytvor_cast_algoritmy(self):
        ramecek = ttk.LabelFrame(self.okno, text="2  Vyberte algoritmy")
        ramecek.pack(fill="x", padx=10, pady=5)

        # zaskrtavatka v mrizce 2 x 2
        mrizka = ttk.Frame(ramecek)
        mrizka.pack(fill="x", padx=5, pady=3)
        self.zaskrtnuto = []  # pro kazdy algoritmus jedna promenna True/False
        for i, alg in enumerate(ALGORITMY):
            promenna = tk.BooleanVar(value=False)
            self.zaskrtnuto.append(promenna)
            text = f"{alg['nazev']}  •  {alg['info']}"
            policko = ttk.Checkbutton(mrizka, text=text, variable=promenna, command=self.aktualizuj_animovat)
            # prvni 2 vlevo, dalsi 2 vpravo
            policko.grid(row=i % 2, column=i // 2, sticky="w", padx=(0, 60))

        # tlacitka
        radek = ttk.Frame(ramecek)
        radek.pack(fill="x", padx=5, pady=5)
        ttk.Button(radek, text="Vše", command=lambda: self.zaskrtni_vse(True)).pack(side="left")
        ttk.Button(radek, text="Nic", command=lambda: self.zaskrtni_vse(False)).pack(side="left", padx=5)
        ttk.Label(radek, text="Opakování (1–10):").pack(side="left", padx=(15, 5))
        self.opakovani = ttk.Spinbox(radek, from_=1, to=10, width=4)
        self.opakovani.set(3)
        self.opakovani.pack(side="left")
        self.tlacitko_porovnat = ttk.Button(radek, text="Porovnat algoritmy", command=self.porovnat)
        self.tlacitko_porovnat.pack(side="left", padx=(15, 5))
        ttk.Button(radek, text="Zastavit", command=self.zastav).pack(side="left", padx=5)
        self.tlacitko_animovat = ttk.Button(radek, text="Animovat", command=self.animovat)
        self.tlacitko_animovat.pack(side="left", padx=5)

    def vybrane_algoritmy(self):
        # vrati seznam algoritmu, ktere jsou zaskrtnute
        vybrane = []
        for i, alg in enumerate(ALGORITMY):
            if self.zaskrtnuto[i].get():
                vybrane.append(alg)
        return vybrane

    def zaskrtni_vse(self, hodnota):
        for promenna in self.zaskrtnuto:
            promenna.set(hodnota)
        self.aktualizuj_animovat()

    def aktualizuj_animovat(self):
        # animovat jde jen s jednim algoritmem a malo daty
        if len(self.vybrane_algoritmy()) == 1 and len(self.data) <= MAX_PRO_ANIMACI:
            self.tlacitko_animovat.config(state="normal")
        else:
            self.tlacitko_animovat.config(state="disabled")

    def animovat(self):
        algoritmus = self.vybrane_algoritmy()[0]
        OknoAnimace(self.okno, algoritmus, self.data)

    def zastav(self):
        self.zastavit = True

    def porovnat(self):
        vybrane = self.vybrane_algoritmy()
        if not vybrane:
            messagebox.showinfo("Porovnání", "Vyberte aspoň jeden algoritmus.")
            return
        try:
            opakovani = int(self.opakovani.get())
        except ValueError:
            opakovani = 1
        opakovani = max(1, min(10, opakovani))

        # spravny vysledek, podle nej kontrolujeme ostatni algoritmy
        spravne = sorted(self.data)

        self.zastavit = False
        self.tlacitko_porovnat.config(state="disabled")
        self.vysledky = []

        for alg in vybrane:
            # pomale algoritmy na moc datech preskocime
            if alg["pomaly"] and len(self.data) > MAX_PRO_POMALE:
                self.vysledky.append((alg["nazev"], None, None, None, "Přeskočeno (moc dat)"))
                continue

            casy = []
            for _ in range(opakovani):
                self.stav.config(text=f"Třídím: {alg['nazev']} ({len(casy) + 1}/{opakovani})...")
                # prekreslime okno, aby slo kliknout na Zastavit
                self.okno.update()
                if self.zastavit:
                    break

                # kazdy beh dostane kopii stejnych dat
                kopie = self.data.copy()
                start = time.perf_counter()
                alg["funkce"](kopie)
                konec = time.perf_counter()
                casy.append((konec - start) * 1000)  # v milisekundach

            if self.zastavit:
                break

            # zkontrolujeme, jestli algoritmus opravdu seradil spravne
            stav = "Ověřeno" if kopie == spravne else "CHYBA"
            self.vysledky.append((alg["nazev"], statistics.median(casy), min(casy), max(casy), stav))

        self.tlacitko_porovnat.config(state="normal")
        self.ukaz_vysledky()
        if self.zastavit:
            self.stav.config(text="Zastaveno. Zobrazeny jen dokončené algoritmy.")
        else:
            self.stav.config(text="Hotovo.")

    # ---------- 3. cast: vysledky ----------

    def vytvor_cast_vysledky(self):
        zalozky = ttk.Notebook(self.okno)
        zalozky.pack(fill="both", expand=True, padx=10, pady=5)

        # zalozka s tabulkou casu
        stranka = ttk.Frame(zalozky)
        zalozky.add(stranka, text="3  Porovnání časů")
        sloupce = ("algoritmus", "median", "minimum", "maximum", "stav")
        self.tabulka = ttk.Treeview(stranka, columns=sloupce, show="headings", height=8)
        nadpisy = ["Algoritmus", "Medián (ms)", "Minimum (ms)", "Maximum (ms)", "Stav"]
        for sloupec, nadpis in zip(sloupce, nadpisy):
            self.tabulka.heading(sloupec, text=nadpis)
            self.tabulka.column(sloupec, width=150, anchor="e")
        self.tabulka.column("algoritmus", anchor="w")
        self.tabulka.column("stav", anchor="w")
        self.tabulka.pack(fill="both", expand=True, padx=5, pady=5)

        self.nejrychlejsi = ttk.Label(stranka, text="")
        self.nejrychlejsi.pack(anchor="w", padx=5)
        ttk.Button(stranka, text="Export porovnání do CSV...", command=self.export_csv).pack(anchor="w", padx=5, pady=5)

        # zalozka s nahledem dat
        stranka = ttk.Frame(zalozky)
        zalozky.add(stranka, text="Náhled dat")
        self.nahled = tk.Text(stranka, height=8, wrap="word")
        self.nahled.pack(fill="both", expand=True, padx=5, pady=5)

    def ukaz_nahled(self):
        # ukazeme prvnich 500 hodnot, vic by bylo zbytecne
        self.nahled.delete("1.0", "end")
        text = " ".join(str(h) for h in self.data[:500])
        if len(self.data) > 500:
            text += f" ... (a dalších {len(self.data) - 500})"
        self.nahled.insert("1.0", text)

    def ukaz_vysledky(self):
        # smazeme starou tabulku
        for radek in self.tabulka.get_children():
            self.tabulka.delete(radek)

        # nejdriv ty s casem (od nejrychlejsiho), preskocene na konec
        s_casem = [v for v in self.vysledky if v[1] is not None]
        bez_casu = [v for v in self.vysledky if v[1] is None]
        s_casem.sort(key=lambda v: v[1])

        for nazev, median, minimum, maximum, stav in s_casem:
            self.tabulka.insert("", "end", values=(nazev, f"{median:.6f}", f"{minimum:.6f}", f"{maximum:.6f}", stav))
        for nazev, _, _, _, stav in bez_casu:
            self.tabulka.insert("", "end", values=(nazev, "-", "-", "-", stav))

        if s_casem:
            nazev, median = s_casem[0][0], s_casem[0][1]
            self.nejrychlejsi.config(text=f"Nejrychlejší v tomto měření: {nazev} — {median:.6f} ms (medián).")
        else:
            self.nejrychlejsi.config(text="")

    def export_csv(self):
        if not self.vysledky:
            messagebox.showinfo("Export", "Nejdřív spusťte porovnání.")
            return
        cesta = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not cesta:
            return
        with open(cesta, "w", newline="", encoding="utf-8") as soubor:
            zapisovac = csv.writer(soubor, delimiter=";")
            zapisovac.writerow(["Algoritmus", "Median (ms)", "Minimum (ms)", "Maximum (ms)", "Stav"])
            for radek in self.vysledky:
                zapisovac.writerow(radek)
        self.stav.config(text="Uloženo do " + cesta)


# spusteni aplikace
okno = tk.Tk()
Aplikace(okno)
okno.mainloop()
