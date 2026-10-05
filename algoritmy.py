# ctyri tridici algoritmy: bubble sort, quick sort, merge sort a selection sort
#
# kazdy algoritmus dostane seznam "data" a seradi ho primo (zmeni ho),
# nic nevraci - stejne jako list.sort() v pythonu
#
# navic muze dostat seznam "kroky" - do nej si zapisuje co zrovna dela,
# z toho se pak dela animace. kdyz kroky nedostane (je None), nic nezapisuje,
# takze funkce jdou pouzit i samostatne, napr. bubble_sort(muj_seznam)


def zapis(kroky, data, aktivni, popis):
    # kdyz nechceme animaci, tak nic nezapisujeme
    if kroky is not None:
        # ulozime kopii seznamu, jake prvky jsou zrovna aktivni a co se deje
        kroky.append((data.copy(), aktivni, popis))


def prohod(data, a, b):
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

def bubble_sort(data, kroky=None):
    n = len(data)
    # kazdy pruchod da na konec jeden prvek, takze staci n - 1 pruchodu
    for i in range(n - 1):
        prohozeno = False
        # poslednich i prvku uz je serazenych, ty neporovnavame
        for j in range(n - 1 - i):
            zapis(kroky, data, [j, j + 1], "Porovnání sousedů")
            # levy soused je vetsi -> spatne poradi, prohodime je
            if data[j] > data[j + 1]:
                prohod(data, j, j + 1)
                prohozeno = True
                zapis(kroky, data, [j, j + 1], "Výměna")
        # kdyz jsme za cely pruchod nic neprohodili, je hotovo
        if not prohozeno:
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

def selection_sort(data, kroky=None):
    n = len(data)
    # i = prvni pozice neserazene casti, vse pred ni uz je serazene
    for i in range(n - 1):
        # najdeme nejmensi prvek ve zbytku seznamu (od i do konce)
        # zatim predpokladame, ze nejmensi je hned ten prvni
        nejmensi = i
        for j in range(i + 1, n):
            zapis(kroky, data, [nejmensi, j], "Hledání nejmenšího")
            if data[j] < data[nejmensi]:
                nejmensi = j
        # a dame ho na pozici i - tim se serazena cast prodlouzi o jeden prvek
        prohod(data, i, nejmensi)
        zapis(kroky, data, [i, nejmensi], "Nejmenší jde dopředu")


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

def merge_sort(data, kroky=None, zacatek=0, konec=None):
    # tridime cast seznamu od "zacatek" do "konec" (konec uz tam nepatri)
    if konec is None:
        konec = len(data)
    # cast s jednim (nebo zadnym) prvkem je uz serazena - tady rekurze konci
    if konec - zacatek <= 1:
        return

    # 1. a 2. krok: rozdelime na dve poloviny a kazdou seradime zvlast
    stred = (zacatek + konec) // 2
    merge_sort(data, kroky, zacatek, stred)
    merge_sort(data, kroky, stred, konec)

    # 3. krok: slijeme dve serazene poloviny dohromady
    # udelame si jejich kopie, protoze do "data" budeme prepisovat vysledek
    levy = data[zacatek:stred]
    pravy = data[stred:konec]
    i = 0          # kde jsme v leve polovine
    j = 0          # kde jsme v prave polovine
    k = zacatek    # kam v "data" zapiseme dalsi prvek
    while i < len(levy) or j < len(pravy):
        # bereme mensi z obou polovin (nebo co zbyva, kdyz je jedna uz prazdna)
        # "<=" znamena, ze pri shode bereme z leve - proto je trideni stabilni
        if j >= len(pravy) or (i < len(levy) and levy[i] <= pravy[j]):
            data[k] = levy[i]
            i += 1
        else:
            data[k] = pravy[j]
            j += 1
        zapis(kroky, data, [k], "Slévání dvou polovin")
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
# - "hranice" ukazuje, kam patri dalsi prvek mensi nez pivot
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

def quick_sort(data, kroky=None, zacatek=0, konec=None):
    # tridime cast seznamu od "zacatek" do "konec" (tady konec uz patri)
    if konec is None:
        konec = len(data) - 1
    # cast s jednim (nebo zadnym) prvkem je uz serazena - tady rekurze konci
    if zacatek >= konec:
        return

    # pivot vezmeme z prostredka a dame ho na konec
    stred = (zacatek + konec) // 2
    prohod(data, stred, konec)
    pivot = data[konec]

    # vsechno mensi nez pivot presuneme doleva
    # vlevo od "hranice" jsou jen prvky mensi nez pivot
    hranice = zacatek
    for i in range(zacatek, konec):
        zapis(kroky, data, [i, konec], "Porovnání s pivotem")
        if data[i] < pivot:
            prohod(data, i, hranice)
            zapis(kroky, data, [i, hranice], "Menší jde doleva")
            hranice += 1

    # pivot dame mezi mensi a vetsi - tim je na svem konecnem miste
    prohod(data, hranice, konec)
    zapis(kroky, data, [hranice], "Pivot je na svém místě")

    # to same udelame pro levou a pravou cast (pivot uz nepocitame)
    quick_sort(data, kroky, zacatek, hranice - 1)
    quick_sort(data, kroky, hranice + 1, konec)


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
        "nazev": "Quick sort",
        "funkce": quick_sort,
        "info": "průměr O(n log n), až O(n²), nestabilní",
        "pomaly": False,
        "popis": "Vybere pivot (tady prostřední prvek). Menší prvky dá doleva, větší doprava "
                 "a pivot mezi ně - tím je pivot na svém místě. "
                 "Pak stejně seřadí levou a pravou část.",
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
        "nazev": "Selection sort",
        "funkce": selection_sort,
        "info": "O(n²), nestabilní",
        "pomaly": True,
        "popis": "Najde nejmenší prvek v neseřazené části a prohodí ho s prvním prvkem "
                 "této části. Seřazená část vlevo tak roste o jeden prvek za průchod.",
    },
]


# kratka ukazka, kdyz se tento soubor spusti samostatne: python algoritmy.py
# (kdyz ho importuje main.py, tahle cast se nespusti)
if __name__ == "__main__":
    import random

    for alg in ALGORITMY:
        cisla = [random.randint(-100, 100) for _ in range(12)]
        print(alg["nazev"])
        print("  před:", cisla)
        alg["funkce"](cisla)
        print("  po:  ", cisla)
