# tady jsou vsechny tridici algoritmy
#
# kazdy algoritmus dostane seznam "data" a seradi ho primo (zmeni ho)
# navic muze dostat seznam "kroky" - do nej si zapisuje co zrovna dela,
# z toho se pak dela animace. kdyz kroky nedostane (je None), nic nezapisuje


def zapis(kroky, data, aktivni, popis):
    # kdyz nechceme animaci, tak nic nezapisujeme
    if kroky is not None:
        # ulozime kopii seznamu, jake prvky jsou zrovna aktivni a co se deje
        kroky.append((data.copy(), aktivni, popis))


def prohod(data, a, b):
    # prohodi dva prvky v seznamu
    data[a], data[b] = data[b], data[a]


def bubble_sort(data, kroky=None):
    n = len(data)
    for i in range(n - 1):
        prohozeno = False
        # porovnavame sousedy, nejvetsi prvek "probubla" na konec
        for j in range(n - 1 - i):
            zapis(kroky, data, [j, j + 1], "Porovnání sousedů")
            if data[j] > data[j + 1]:
                prohod(data, j, j + 1)
                prohozeno = True
                zapis(kroky, data, [j, j + 1], "Výměna")
        # kdyz jsme nic neprohodili, je hotovo
        if not prohozeno:
            break


def cocktail_sort(data, kroky=None):
    # jako bubble sort, ale chodi tam a zpatky
    zacatek = 0
    konec = len(data) - 1
    prohozeno = True
    while prohozeno:
        prohozeno = False
        # cesta doprava - nejvetsi jde na konec
        for j in range(zacatek, konec):
            zapis(kroky, data, [j, j + 1], "Porovnání (cesta doprava)")
            if data[j] > data[j + 1]:
                prohod(data, j, j + 1)
                prohozeno = True
                zapis(kroky, data, [j, j + 1], "Výměna")
        konec -= 1
        # cesta doleva - nejmensi jde na zacatek
        for j in range(konec, zacatek, -1):
            zapis(kroky, data, [j - 1, j], "Porovnání (cesta doleva)")
            if data[j - 1] > data[j]:
                prohod(data, j - 1, j)
                prohozeno = True
                zapis(kroky, data, [j - 1, j], "Výměna")
        zacatek += 1


def selection_sort(data, kroky=None):
    n = len(data)
    for i in range(n - 1):
        # najdeme nejmensi prvek ve zbytku seznamu
        nejmensi = i
        for j in range(i + 1, n):
            zapis(kroky, data, [nejmensi, j], "Hledání nejmenšího")
            if data[j] < data[nejmensi]:
                nejmensi = j
        # a dame ho na pozici i
        prohod(data, i, nejmensi)
        zapis(kroky, data, [i, nejmensi], "Nejmenší jde dopředu")


def insertion_sort(data, kroky=None):
    for i in range(1, len(data)):
        # prvek na pozici i posouvame doleva, dokud je mensi nez soused
        j = i
        while j > 0 and data[j - 1] > data[j]:
            prohod(data, j - 1, j)
            zapis(kroky, data, [j - 1, j], "Posun doleva")
            j -= 1


def gnome_sort(data, kroky=None):
    # "trpaslik" jde doprava, a kdyz najde spatnou dvojici, prohodi ji a vrati se
    i = 0
    while i < len(data):
        if i == 0 or data[i - 1] <= data[i]:
            i += 1
        else:
            prohod(data, i - 1, i)
            zapis(kroky, data, [i - 1, i], "Výměna a krok zpět")
            i -= 1


def shell_sort(data, kroky=None):
    # insertion sort, ale nejdriv porovnavame prvky daleko od sebe
    mezera = len(data) // 2
    while mezera > 0:
        for i in range(mezera, len(data)):
            j = i
            while j >= mezera and data[j - mezera] > data[j]:
                prohod(data, j - mezera, j)
                zapis(kroky, data, [j - mezera, j], f"Posun (mezera {mezera})")
                j -= mezera
        # mezeru pokazde zmensime na polovinu
        mezera //= 2


def comb_sort(data, kroky=None):
    # bubble sort, ale porovnava prvky s mezerou, ktera se zmensuje
    mezera = len(data)
    prohozeno = True
    while mezera > 1 or prohozeno:
        mezera = int(mezera / 1.3)
        if mezera < 1:
            mezera = 1
        prohozeno = False
        for j in range(len(data) - mezera):
            zapis(kroky, data, [j, j + mezera], f"Porovnání (mezera {mezera})")
            if data[j] > data[j + mezera]:
                prohod(data, j, j + mezera)
                prohozeno = True
                zapis(kroky, data, [j, j + mezera], "Výměna")


def merge_sort(data, kroky=None, zacatek=0, konec=None):
    # tridime cast seznamu od "zacatek" do "konec" (konec uz tam nepatri)
    if konec is None:
        konec = len(data)
    # jeden prvek je uz serazeny
    if konec - zacatek <= 1:
        return

    # rozdelime na dve poloviny a kazdou seradime zvlast
    stred = (zacatek + konec) // 2
    merge_sort(data, kroky, zacatek, stred)
    merge_sort(data, kroky, stred, konec)

    # slijeme dve serazene poloviny dohromady
    levy = data[zacatek:stred]
    pravy = data[stred:konec]
    i = 0
    j = 0
    k = zacatek
    while i < len(levy) or j < len(pravy):
        # bereme mensi z obou polovin (nebo co zbyva)
        if j >= len(pravy) or (i < len(levy) and levy[i] <= pravy[j]):
            data[k] = levy[i]
            i += 1
        else:
            data[k] = pravy[j]
            j += 1
        zapis(kroky, data, [k], "Slévání dvou polovin")
        k += 1


def quick_sort(data, kroky=None, zacatek=0, konec=None):
    # tridime cast seznamu od "zacatek" do "konec" (tady konec uz patri)
    if konec is None:
        konec = len(data) - 1
    if zacatek >= konec:
        return

    # pivot vezmeme z prostredka a dame ho na konec
    stred = (zacatek + konec) // 2
    prohod(data, stred, konec)
    pivot = data[konec]

    # vsechno mensi nez pivot presuneme doleva
    hranice = zacatek
    for i in range(zacatek, konec):
        zapis(kroky, data, [i, konec], "Porovnání s pivotem")
        if data[i] < pivot:
            prohod(data, i, hranice)
            zapis(kroky, data, [i, hranice], "Menší jde doleva")
            hranice += 1

    # pivot dame mezi mensi a vetsi
    prohod(data, hranice, konec)
    zapis(kroky, data, [hranice], "Pivot je na svém místě")

    # to same udelame pro levou a pravou cast
    quick_sort(data, kroky, zacatek, hranice - 1)
    quick_sort(data, kroky, hranice + 1, konec)


def prosej(data, i, n, kroky):
    # posouva prvek dolu v halde, dokud neni vetsi nez jeho deti
    while True:
        nejvetsi = i
        levy = 2 * i + 1
        pravy = 2 * i + 2
        if levy < n and data[levy] > data[nejvetsi]:
            nejvetsi = levy
        if pravy < n and data[pravy] > data[nejvetsi]:
            nejvetsi = pravy
        if nejvetsi == i:
            return
        prohod(data, i, nejvetsi)
        zapis(kroky, data, [i, nejvetsi], "Oprava haldy")
        i = nejvetsi


def heap_sort(data, kroky=None):
    n = len(data)
    # 1. udelame z seznamu haldu - nejvetsi prvek bude na zacatku
    for i in range(n // 2 - 1, -1, -1):
        prosej(data, i, n, kroky)
    # 2. nejvetsi prvek dame na konec, zbytek zase opravime na haldu
    for konec in range(n - 1, 0, -1):
        prohod(data, 0, konec)
        zapis(kroky, data, [0, konec], "Největší jde na konec")
        prosej(data, 0, konec, kroky)


def timsort(data, kroky=None):
    # vestaveny sort v pythonu, uvnitr neni videt, takze zadne kroky
    data.sort()


# seznam vsech algoritmu, podle nej se dela okno
# "pomaly" = O(n^2), ty pustime jen na mene datech
ALGORITMY = [
    {
        "nazev": "Bubble sort",
        "funkce": bubble_sort,
        "info": "O(n²), stabilní",
        "pomaly": True,
        "popis": "Porovnává sousední prvky a vymění je, pokud jsou ve špatném pořadí. "
                 "Po každém průchodu je největší zbývající hodnota na konci. "
                 "Průchody se opakují, dokud už není potřeba žádná výměna.",
    },
    {
        "nazev": "Selection sort",
        "funkce": selection_sort,
        "info": "O(n²), nestabilní",
        "pomaly": True,
        "popis": "Najde nejmenší prvek v neseřazené části a prohodí ho s prvním prvkem "
                 "této části. Seřazená část vlevo tak roste o jeden prvek za průchod.",
    },
    {
        "nazev": "Shell sort",
        "funkce": shell_sort,
        "info": "až O(n²), nestabilní",
        "pomaly": False,
        "popis": "Vylepšený insertion sort. Nejdřív řadí prvky, které jsou daleko od sebe "
                 "(velká mezera), a mezeru postupně zmenšuje až na 1. "
                 "Prvky se tak rychle dostanou blízko svého místa.",
    },
    {
        "nazev": "Merge sort",
        "funkce": merge_sort,
        "info": "O(n log n), stabilní",
        "pomaly": False,
        "popis": "Rozdělí seznam na dvě poloviny, každou seřadí (stejným způsobem) "
                 "a pak obě seřazené poloviny slije dohromady tak, "
                 "že vždy vezme menší z prvních prvků.",
    },
    {
        "nazev": "Heap sort",
        "funkce": heap_sort,
        "info": "O(n log n), nestabilní",
        "pomaly": False,
        "popis": "Z prvků udělá haldu (strom, kde je rodič větší než děti), takže největší "
                 "prvek je na začátku. Ten přesune na konec, haldu opraví a opakuje.",
    },
    {
        "nazev": "Timsort (Python)",
        "funkce": timsort,
        "info": "O(n log n), stabilní; vestavěný",
        "pomaly": False,
        "popis": "Vestavěné třídění v Pythonu (list.sort). Kombinuje merge sort a insertion "
                 "sort. Běží v jazyce C, takže je nejrychlejší, ale jeho kroky nejsou vidět.",
    },
    {
        "nazev": "Cocktail sort",
        "funkce": cocktail_sort,
        "info": "O(n²), stabilní",
        "pomaly": True,
        "popis": "Bubble sort, který chodí střídavě tam a zpátky. Cestou doprava posune "
                 "největší prvek na konec, cestou doleva nejmenší prvek na začátek.",
    },
    {
        "nazev": "Insertion sort",
        "funkce": insertion_sort,
        "info": "O(n²), stabilní",
        "pomaly": True,
        "popis": "Bere prvky jeden po druhém a každý posouvá doleva, dokud není "
                 "na správném místě mezi už seřazenými prvky. Jako řazení karet v ruce.",
    },
    {
        "nazev": "Comb sort",
        "funkce": comb_sort,
        "info": "až O(n²), nestabilní",
        "pomaly": False,
        "popis": "Vylepšený bubble sort. Neporovnává sousedy, ale prvky s mezerou, "
                 "která se každým průchodem zmenší (děleno 1,3), až je 1.",
    },
    {
        "nazev": "Quick sort",
        "funkce": quick_sort,
        "info": "průměr O(n log n), až O(n²), nestabilní",
        "pomaly": False,
        "popis": "Vybere pivot (tady prostřední prvek). Menší prvky dá doleva, větší doprava "
                 "a pivot mezi ně - tím je pivot na svém místě. "
                 "Pak stejně seřadí levou a pravou část.",
    },
    {
        "nazev": "Gnome sort",
        "funkce": gnome_sort,
        "info": "O(n²), stabilní",
        "pomaly": True,
        "popis": "Trpaslík jde doprava. Když jsou dva prvky ve špatném pořadí, prohodí je "
                 "a udělá krok zpět. Když jsou dobře, jde dál. Na konci je hotovo.",
    },
]
