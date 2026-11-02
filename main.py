# tridici algoritmy: bubble sort, quick sort, merge sort, selection sort,
# insertion sort a heap sort
#
# soubor ma dve casti:
# 1. tridici algoritmy - sest funkci, u kazde je popsany princip
# 2. jednoduche okno - zadas cisla, vyberes algoritmus a seradis je,
#    nebo porovnas, ktery algoritmus je nejrychlejsi
#
# spusteni: python main.py

import random
import sys
import time
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# quick sort a merge sort volaji sami sebe, tak povolime vic volani v sobe
sys.setrecursionlimit(100000)


# ======================================================================
# 1. TRIDICI ALGORITMY
# ======================================================================
# kazdy algoritmus dostane seznam "data" a seradi ho primo (zmeni ho),
# nic nevraci - stejne jako list.sort() v pythonu


def swap(data, a, b):
    # prohodi dva prvky v seznamu
    data[a], data[b] = data[b], data[a]


# ---------- bubble sort (bublinkove trideni) ----------
#
# princip:
# - prochazime seznam zleva doprava a porovnavame vzdy dva SOUSEDNI prvky
# - kdyz je levy vetsi nez pravy, jsou ve spatnem poradi a prohodime je
# - nejvetsi prvek se tak pri kazdem porovnani posune o kus doprava,
#   az "probubla" na konec seznamu (jako bublina, ktera stoupa nahoru)
# - po 1. pruchodu je na konci nejvetsi prvek, po 2. pruchodu druhy nejvetsi atd.,
#   proto muze byt kazdy dalsi pruchod o jeden prvek kratsi
# - kdyz behem celeho pruchodu nic neprohodime, seznam uz je serazeny a koncime
#
# priklad: [5, 1, 4, 2]
#   1. pruchod: 5>1 vymena, 5>4 vymena, 5>2 vymena -> [1, 4, 2, 5]  (5 je na miste)
#   2. pruchod: 1<4 nic,    4>2 vymena            -> [1, 2, 4, 5]  (4 je na miste)
#   3. pruchod: 1<2 nic -> zadna vymena, hotovo
#
# slozitost: O(n^2) porovnani, kdyz uz je seznam serazeny tak jen O(n) (jeden pruchod)
# stabilni (stejne prvky si nevymeni poradi), nepotrebuje pomocnou pamet

def bubble_sort(data):
    n = len(data)
    # kazdy pruchod da na konec jeden prvek, takze staci n - 1 pruchodu
    for i in range(n - 1):
        swapped = False
        # poslednich i prvku uz je serazenych, ty neporovnavame
        for j in range(n - 1 - i):
            # levy soused je vetsi -> spatne poradi, prohodime je
            if data[j] > data[j + 1]:
                swap(data, j, j + 1)
                swapped = True
        # kdyz jsme za cely pruchod nic neprohodili, je hotovo
        if not swapped:
            break


# ---------- selection sort (trideni vyberem) ----------
#
# princip:
# - seznam si rozdelime na dve casti: vlevo SERAZENA (na zacatku prazdna)
#   a vpravo NESERAZENA (na zacatku cely seznam)
# - v neserazene casti najdeme nejmensi prvek - musime ji projit celou
# - ten prohodime s prvnim prvkem neserazene casti
#   -> nejmensi prvek je na svem konecnem miste a serazena cast se zvetsi o 1
# - opakujeme, dokud v neserazene casti nezbude jen jeden prvek
#   (ten uz je nutne nejvetsi, takze je taky na miste)
#
# priklad: [5, 1, 4, 2]
#   nejmensi z [5, 1, 4, 2] je 1 -> prohodime s 5 -> [1 | 5, 4, 2]
#   nejmensi z [5, 4, 2]    je 2 -> prohodime s 5 -> [1, 2 | 4, 5]
#   nejmensi z [4, 5]       je 4 -> uz je na miste -> [1, 2, 4 | 5]  hotovo
#
# slozitost: vzdy O(n^2) porovnani (i kdyz je seznam uz serazeny),
# ale nejvys n - 1 vymen
# nestabilni (vymena na dlouhou vzdalenost muze preskocit stejny prvek),
# nepotrebuje pomocnou pamet

def selection_sort(data):
    n = len(data)
    # i = prvni pozice neserazene casti, vse pred ni uz je serazene
    for i in range(n - 1):
        # najdeme nejmensi prvek ve zbytku seznamu (od i do konce)
        # zatim predpokladame, ze nejmensi je hned ten prvni
        smallest = i
        for j in range(i + 1, n):
            if data[j] < data[smallest]:
                smallest = j
        # a dame ho na pozici i - tim se serazena cast prodlouzi o jeden prvek
        swap(data, i, smallest)


# ---------- insertion sort (trideni vkladanim) ----------
#
# princip (jako kdyz si radime karty v ruce):
# - seznam si rozdelime na dve casti: vlevo SERAZENA (na zacatku jen prvni prvek,
#   jeden prvek je serazeny sam od sebe) a vpravo NESERAZENA
# - vezmeme prvni prvek neserazene casti ("do ruky", promenna current)
# - serazenou cast prochazime zprava doleva a kazdy prvek, ktery je VETSI
#   nez current, posuneme o jedno misto doprava - tim se uvolni misto
# - jakmile narazime na prvek mensi nebo stejny (nebo na zacatek seznamu),
#   vlozime current na uvolnene misto
# - serazena cast se tak zvetsi o 1; opakujeme, dokud neni serazeny cely seznam
# - rozdil oproti selection sortu: prvky v serazene casti jeste NEJSOU na svem
#   konecnem miste, dalsi vkladany prvek je muze posunout doprava
#
# priklad: [5, 1, 4, 2]
#   [5 | 1, 4, 2]  vezmi 1: 5 > 1 posun         -> vloz na zacatek -> [1, 5 | 4, 2]
#   [1, 5 | 4, 2]  vezmi 4: 5 > 4 posun, 1 < 4   -> vloz za 1       -> [1, 4, 5 | 2]
#   [1, 4, 5 | 2]  vezmi 2: 5 a 4 posun, 1 < 2  -> vloz za 1       -> [1, 2, 4, 5]
#
# slozitost: O(n^2) porovnani (obracene serazeny seznam - kazdy prvek jde az
# na zacatek), kdyz uz je seznam serazeny tak jen O(n) - nic se neposouva
# stabilni (posouvame jen ostre vetsi prvky, stejny prvek nepreskocime),
# nepotrebuje pomocnou pamet

def insertion_sort(data):
    # prvni prvek je serazeny sam od sebe, zaciname od druheho
    for i in range(1, len(data)):
        # prvek, ktery zarazujeme - vezmeme si ho "do ruky"
        current = data[i]
        # j jde serazenou casti zprava doleva
        j = i - 1
        # vetsi prvky posouvame o jedno doprava, tim se misto pro current
        # posouva doleva (current mezitim prepiseme, ale mame ho v promenne)
        while j >= 0 and data[j] > current:
            data[j + 1] = data[j]
            j -= 1
        # data[j] je mensi nebo stejny (nebo uz jsme pred zacatkem seznamu),
        # takze current patri hned za nej
        data[j + 1] = current


# ---------- merge sort (trideni slevanim) ----------
#
# princip "rozdel a panuj":
# 1. ROZDEL: seznam rozdelime na dve poloviny
# 2. VYRES:  kazdou polovinu seradime - uplne stejnym zpusobem, tedy funkce
#            zavola sama sebe (rekurze). deleni konci, kdyz ma cast jen 1 prvek,
#            protoze jeden prvek je serazeny sam od sebe
# 3. SPOJ:   dve serazene poloviny slijeme (merge) do jedne serazene:
#            divame se na prvni prvek obou polovin (je to jejich nejmensi prvek),
#            mensi z nich vezmeme do vysledku a v jeho polovine se posuneme dal;
#            opakujeme, dokud nevezmeme vsechny prvky
#
# priklad: [5, 1, 4, 2]
#   deleni:   [5, 1, 4, 2] -> [5, 1] a [4, 2] -> [5] [1] [4] [2]
#   slevani:  [5]+[1] -> [1, 5]      [4]+[2] -> [2, 4]
#   slevani:  [1, 5]+[2, 4]: 1<2 vezmi 1, 2<5 vezmi 2, 4<5 vezmi 4, zbyva 5
#             -> [1, 2, 4, 5]
#
# slozitost: vzdy O(n log n) - pulenim vznikne log n urovni
# a na kazde urovni se dohromady slije n prvku
# stabilni (pri shode bereme prvek z leve poloviny),
# ale potrebuje pomocnou pamet O(n) na kopie polovin

def merge_sort(data, start=0, end=None):
    # tridime cast seznamu od "start" do "end" (end uz tam nepatri)
    if end is None:
        end = len(data)
    # cast s jednim (nebo zadnym) prvkem je uz serazena - tady rekurze konci
    if end - start <= 1:
        return

    # 1. a 2. krok: rozdelime na dve poloviny a kazdou seradime zvlast
    mid = (start + end) // 2
    merge_sort(data, start, mid)
    merge_sort(data, mid, end)

    # 3. krok: slijeme dve serazene poloviny dohromady
    # udelame si jejich kopie, protoze do "data" budeme prepisovat vysledek
    left = data[start:mid]
    right = data[mid:end]
    i = 0        # kde jsme v leve polovine
    j = 0        # kde jsme v prave polovine
    k = start    # kam v "data" zapiseme dalsi prvek
    while i < len(left) or j < len(right):
        # bereme mensi z obou polovin (nebo co zbyva, kdyz je jedna uz prazdna)
        # "<=" znamena, ze pri shode bereme z leve - proto je trideni stabilni
        if j >= len(right) or (i < len(left) and left[i] <= right[j]):
            data[k] = left[i]
            i += 1
        else:
            data[k] = right[j]
            j += 1
        k += 1


# ---------- quick sort (rychle trideni) ----------
#
# princip taky "rozdel a panuj", ale hlavni prace se dela pri DELENI
# (u merge sortu az pri spojovani):
# 1. vybereme jeden prvek = PIVOT (tady prostredni prvek)
# 2. ROZDELENI (partition): prvky mensi nez pivot presuneme doleva,
#    ostatni zustanou vpravo a pivot dame presne mezi ne
#    -> pivot je ted na sve konecne pozici a uz se nikdy nepohne
# 3. stejnym zpusobem seradime levou cast a pravou cast (rekurze);
#    cast s 0 nebo 1 prvkem je hotova. spojovat nic nemusime, vsechno uz
#    je na spravnych mistech
#
# jak presne funguje rozdeleni (Lomutovo schema):
# - pivot si odlozime na konec, aby nam neprekazel
# - "boundary" (hranice) ukazuje, kam patri dalsi prvek mensi nez pivot
# - projdeme vsechny prvky; kdyz je prvek mensi nez pivot,
#   prohodime ho na hranici a hranici posuneme o 1 doprava
# - nakonec prohodime pivot z konce na hranici
#
# priklad: [5, 1, 4, 2, 3], pivot = 4 (prostredni)
#   rozdeleni: mensi nez 4 jsou 1, 2, 3 -> [1, 3, 2] 4 [5]
#   leva cast [1, 3, 2] stejne: pivot 3 -> [1, 2] 3 []  ...  -> [1, 2, 3]
#   prava cast [5] ma jeden prvek -> hotovo
#   vysledek: [1, 2, 3, 4, 5]
#
# slozitost: prumerne O(n log n), nejhorsi O(n^2) - kdyz je pivot porad
# nejmensi nebo nejvetsi prvek, deleni je pak uplne nerovnomerne.
# prostredni pivot funguje dobre i na uz serazenych datech
# nestabilni, nepotrebuje pomocnou pamet (jen zasobnik na rekurzi)

def quick_sort(data, start=0, end=None):
    # tridime cast seznamu od "start" do "end" (tady end uz patri)
    if end is None:
        end = len(data) - 1
    # cast s jednim (nebo zadnym) prvkem je uz serazena - tady rekurze konci
    if start >= end:
        return

    # pivot vezmeme z prostredka a dame ho na konec
    mid = (start + end) // 2
    swap(data, mid, end)
    pivot = data[end]

    # vsechno mensi nez pivot presuneme doleva
    # vlevo od "boundary" jsou jen prvky mensi nez pivot
    boundary = start
    for i in range(start, end):
        if data[i] < pivot:
            swap(data, i, boundary)
            boundary += 1

    # pivot dame mezi mensi a vetsi - tim je na svem konecnem miste
    swap(data, boundary, end)

    # to same udelame pro levou a pravou cast (pivot uz nepocitame)
    quick_sort(data, start, boundary - 1)
    quick_sort(data, boundary + 1, end)


# ---------- heap sort (trideni haldou) ----------
#
# HALDA (heap) je binarni strom, kde je kazdy rodic VETSI nebo stejny nez oba
# jeho potomci -> nejvetsi prvek celeho stromu je vzdy nahore v koreni
#
# strom nemusime nikde stavet, ulozime ho primo do seznamu:
# - koren je na indexu 0
# - potomci prvku na indexu i jsou na indexech 2*i + 1 (levy) a 2*i + 2 (pravy)
# - strom se tak plni po patrech zleva doprava
#
#   seznam [5, 3, 4, 2, 1] jako strom:        5          index 0
#                                           /   \
#                                          3     4       indexy 1, 2
#                                         / \
#                                        2   1           indexy 3, 4
#
# PROSETI (heapify): kdyz je nejaky rodic mensi nez jeho potomek, prohodime ho
# s VETSIM z potomku a pokracujeme o patro niz, dokud neni vetsi nez oba potomci
# (nebo uz zadne potomky nema) - prvek tak "propadne" na sve misto
#
# princip heap sortu ma dve faze:
# 1. STAVBA HALDY: proseveme vsechny prvky, ktere maji potomky, odspodu nahoru
#    (od indexu n // 2 - 1 k indexu 0); listy dole jsou haldou samy o sobe
# 2. VYBIRANI: nejvetsi prvek je v koreni, tak ho prohodime s poslednim prvkem
#    haldy -> nejvetsi je na konci seznamu na svem konecnem miste a halda se
#    zmensi o 1. novy koren muze byt maly, proto ho proseveme dolu.
#    opakujeme, dokud v halde nezbude jeden prvek
#    (podobne jako selection sort, jen nejvetsi prvek nehledame pruchodem celym
#    seznamem, ale mame ho hned v koreni)
#
# priklad: [5, 1, 4, 2, 3]
#   stavba:  proseti indexu 1 (hodnota 1): vetsi potomek je 3 -> [5, 3, 4, 2, 1]
#            proseti indexu 0 (hodnota 5): je vetsi nez 3 i 4 -> halda hotova
#   vybirani: 5 <-> 1, proseti 1 -> [4, 3, 1, 2 | 5]
#             4 <-> 2, proseti 2 -> [3, 2, 1 | 4, 5]
#             3 <-> 1, proseti 1 -> [2, 1 | 3, 4, 5]
#             2 <-> 1            -> [1 | 2, 3, 4, 5]  hotovo
#
# slozitost: vzdy O(n log n) - halda ma log n pater, takze jedno proseti
# udela nejvys log n vymen, a prosevame n krat
# nestabilni (vymeny na dlouhou vzdalenost), nepotrebuje pomocnou pamet

def heapify(data, root, end):
    # proseje prvek na indexu "root" dolu haldou
    # halda jsou prvky od 0 do "end" (end uz tam nepatri, to je serazena cast)
    while True:
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2
        # najdeme nejvetsi z trojice rodic, levy potomek, pravy potomek
        # (potomek s indexem >= end neexistuje nebo uz do haldy nepatri)
        if left < end and data[left] > data[largest]:
            largest = left
        if right < end and data[right] > data[largest]:
            largest = right
        # rodic je vetsi nez oba potomci -> prvek je na svem miste, konec
        if largest == root:
            return
        # jinak rodice prohodime s vetsim potomkem a pokracujeme o patro niz
        swap(data, root, largest)
        root = largest


def heap_sort(data):
    n = len(data)
    # 1. faze: stavba haldy - prvky s potomky proseveme odspodu nahoru,
    # takze kdyz prosevame rodice, jeho podstromy uz jsou haldy
    for i in range(n // 2 - 1, -1, -1):
        heapify(data, i, n)
    # 2. faze: "end" je posledni prvek haldy, za nim je serazena cast
    for end in range(n - 1, 0, -1):
        # nejvetsi prvek haldy (koren) dame na konec - tam uz zustane
        swap(data, 0, end)
        # halda je ted o 1 mensi (konci pred "end"), novy koren proseveme
        heapify(data, 0, end)


# algoritmy, ze kterych se vybira v okne: nazev -> funkce
ALGORITHMS = {
    "Bubble sort": bubble_sort,
    "Quick sort": quick_sort,
    "Merge sort": merge_sort,
    "Selection sort": selection_sort,
    "Insertion sort": insertion_sort,
    "Heap sort": heap_sort,
}


# ======================================================================
# 2. OKNO APLIKACE
# ======================================================================

# vic cisel nedovolime - bubble sort by na nich trval moc dlouho
MAX_COUNT = 5000
# kolik cisel z vysledku vypiseme, zbytek se jen spocita
MAX_SHOWN = 30


def load_numbers_from_file(file_path):
    # nacte cela cisla z textoveho souboru (.txt)
    # cisla mohou byt na radcich, oddelena mezerami nebo carkami
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    numbers = []
    # rozdelime text podle bilych znaku (mezery, nove radky) i carek
    for part in content.replace(",", " ").split():
        # zadani vyzaduje cela cisla, takze prevadime pomoci int()
        numbers.append(int(part))
    return numbers


def parse_numbers(text):
    # cisla jsou oddelena mezerami nebo carkami, desetinna cisla pisou s teckou
    # kdyz neco neni cislo, float() vyhodi ValueError
    numbers = []
    for part in text.replace(",", " ").split():
        try:
            numbers.append(int(part))
        except ValueError:
            numbers.append(float(part))
    return numbers


def format_numbers(numbers):
    # vypise prvnich MAX_SHOWN cisel, u delsiho seznamu napise, kolik jich je celkem
    text = " ".join(str(n) for n in numbers[:MAX_SHOWN])
    if len(numbers) > MAX_SHOWN:
        text += f" … (celkem {len(numbers)} čísel)"
    return text


def compare_speed(numbers):
    # kazdy algoritmus seradi svoji kopii stejnych cisel a zmerime, jak dlouho to trvalo
    times = []
    for name, func in ALGORITHMS.items():
        copy = numbers.copy()
        t_start = time.perf_counter()
        func(copy)
        t_end = time.perf_counter()
        times.append(((t_end - t_start) * 1000, name))  # cas v milisekundach a nazev
    # dvojice (cas, nazev) seradime nasim merge sortem - porovnavaji se podle casu,
    # takze nejrychlejsi algoritmus bude prvni
    merge_sort(times)
    return times


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("SortApp")

        frame = ttk.Frame(root, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="SortApp", font=("", 18, "bold")).grid(row=0, column=0, columnspan=2, sticky="w")

        # radek s cisly
        ttk.Label(frame, text="Čísla:").grid(row=1, column=0, sticky="w", pady=(10, 0))
        self.numbers_entry = ttk.Entry(frame, width=45)
        self.numbers_entry.insert(0, "5 1 4 2 3")
        self.numbers_entry.grid(row=1, column=1, sticky="we", padx=5, pady=(10, 0))

        # radek s nahodnymi cisly: kolik jich vygenerovat a tlacitko
        ttk.Label(frame, text="Počet:").grid(row=2, column=0, sticky="w", pady=(5, 0))
        row = ttk.Frame(frame)
        row.grid(row=2, column=1, sticky="w", padx=5, pady=(5, 0))
        self.count_box = ttk.Spinbox(row, from_=1, to=MAX_COUNT, width=7)
        self.count_box.set(1000)
        self.count_box.pack(side="left")
        ttk.Button(row, text="Náhodná", command=self.random_numbers).pack(side="left", padx=5)
        ttk.Button(row, text="Načíst ze souboru", command=self.load_from_file).pack(side="left", padx=5)

        # vyber algoritmu - prepinace ve dvou sloupcich
        self.algorithm = tk.StringVar(value="Bubble sort")
        choices = ttk.Frame(frame)
        choices.grid(row=3, column=0, columnspan=2, sticky="w", pady=10)
        for i, name in enumerate(ALGORITHMS):
            ttk.Radiobutton(choices, text=name, value=name, variable=self.algorithm).grid(
                row=i // 2, column=i % 2, sticky="w", padx=(0, 40))

        # tlacitka
        row = ttk.Frame(frame)
        row.grid(row=4, column=0, columnspan=2, sticky="w")
        ttk.Button(row, text="Seřadit", command=self.sort).pack(side="left")
        ttk.Button(row, text="Porovnat rychlost", command=self.compare).pack(side="left", padx=5)

        # vysledek razeni a porovnani rychlosti
        self.result = ttk.Label(frame, text="Výsledek:", wraplength=500)
        self.result.grid(row=5, column=0, columnspan=2, sticky="w", pady=(10, 0))
        self.speed = ttk.Label(frame, text="", justify="left")
        self.speed.grid(row=6, column=0, columnspan=2, sticky="w", pady=(10, 0))

    def random_numbers(self):
        # vygeneruje zadany pocet nahodnych celych cisel od 0 do 99 999
        try:
            count = int(self.count_box.get())
        except ValueError:
            count = 0
        if not 1 <= count <= MAX_COUNT:
            messagebox.showerror("Chyba", f"Počet musí být celé číslo od 1 do {MAX_COUNT}.")
            return
        numbers = [random.randint(0, 99999) for _ in range(count)]
        self.numbers_entry.delete(0, "end")
        self.numbers_entry.insert(0, " ".join(str(n) for n in numbers))

    def load_from_file(self):
        # otevre dialog pro vyber souboru (.txt)
        file_path = filedialog.askopenfilename(
            title="Vyberte textový soubor s čísly",
            filetypes=[("Textové soubory", "*.txt"), ("Všechny soubory", "*.*")],
        )
        # kdyz uzivatel klikne na Storno, nic nedelame
        if not file_path:
            return

        try:
            numbers = load_numbers_from_file(file_path)
        except ValueError:
            messagebox.showerror("Chyba", "Soubor obsahuje neplatná data (musí obsahovat pouze celá čísla).")
            return
        except Exception as e:
            messagebox.showerror("Chyba", f"Nepodařilo se načíst soubor:\n{e}")
            return

        if not numbers:
            messagebox.showerror("Chyba", "Soubor je prázdný nebo neobsahuje žádná čísla.")
            return

        if len(numbers) > MAX_COUNT:
            messagebox.showerror("Chyba", f"V souboru je {len(numbers)} čísel. Maximum je {MAX_COUNT}.")
            return

        # nactena cisla vlozime do policka v okne
        self.numbers_entry.delete(0, "end")
        self.numbers_entry.insert(0, " ".join(str(n) for n in numbers))

    def read_numbers(self):
        # precte cisla z policka; kdyz jsou spatne, ukaze chybu a vrati None
        try:
            numbers = parse_numbers(self.numbers_entry.get())
        except ValueError:
            messagebox.showerror("Chyba", "Zadejte čísla oddělená mezerou (desetinná čísla s tečkou).")
            return None
        if not numbers:
            messagebox.showerror("Chyba", "Zadejte aspoň jedno číslo.")
            return None
        if len(numbers) > MAX_COUNT:
            messagebox.showerror("Chyba", f"Zadejte nejvýš {MAX_COUNT} čísel.")
            return None
        return numbers

    def sort(self):
        numbers = self.read_numbers()
        if numbers is None:
            return
        # vybrany algoritmus seradi seznam primo, takze ho pak jen vypiseme
        ALGORITHMS[self.algorithm.get()](numbers)
        self.result.config(text="Výsledek: " + format_numbers(numbers))

    def compare(self):
        numbers = self.read_numbers()
        if numbers is None:
            return
        # u vetsiho mnozstvi cisel to chvili trva, tak to napiseme do okna
        self.speed.config(text="Měřím…")
        self.root.update()

        times = compare_speed(numbers)
        lines = [f"Porovnání rychlosti ({len(numbers)} čísel), od nejrychlejšího:"]
        for rank, (ms, name) in enumerate(times, start=1):
            ms_text = f"{ms:.3f}".replace(".", ",")  # desetinna carka jako v cestine
            lines.append(f"{rank}. {name} – {ms_text} ms")
        lines.append(f"Nejrychlejší je {times[0][1]}.")
        self.speed.config(text="\n".join(lines))


# spusteni aplikace (jen kdyz se soubor spusti, ne kdyz se importuje)
if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
