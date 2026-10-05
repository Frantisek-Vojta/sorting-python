# tridici algoritmy: bubble sort, quick sort, merge sort a selection sort
#
# soubor ma dve casti:
# 1. tridici algoritmy - ctyri funkce, u kazde je popsany princip
# 2. jednoduche okno - zadas cisla, vyberes algoritmus a seradis je,
#    nebo porovnas, ktery algoritmus je nejrychlejsi
#
# spusteni: python main.py

import random
import sys
import time
import tkinter as tk
from tkinter import ttk, messagebox

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


# algoritmy, ze kterych se vybira v okne: nazev -> funkce
ALGORITHMS = {
    "Bubble sort": bubble_sort,
    "Quick sort": quick_sort,
    "Merge sort": merge_sort,
    "Selection sort": selection_sort,
}


# ======================================================================
# 2. OKNO APLIKACE
# ======================================================================

# vic cisel nedovolime - bubble sort by na nich trval moc dlouho
MAX_COUNT = 5000
# kolik cisel z vysledku vypiseme, zbytek se jen spocita
MAX_SHOWN = 30


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

        # vyber algoritmu - prepinace v mrizce 2 x 2
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
