# hlavni okno tridici aplikace
# spusteni: python main.py

import csv
import random
import statistics
import sys
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from algorithms import ALGORITHMS
from animation import AnimationWindow

# quick sort a merge sort volaji sami sebe, tak povolime vic volani v sobe
sys.setrecursionlimit(100000)

# pomale algoritmy O(n^2) pustime jen do tolika prvku
MAX_FOR_SLOW = 3000
# animace jen do tolika prvku
MAX_FOR_ANIMATION = 100

VALUE_TYPES = ["Automaticky", "Celá čísla", "Desetinná čísla", "Text"]
ORDERS = ["Náhodně", "Seřazeně", "Obráceně", "Skoro seřazeně"]


def generate_data(count, seed, value_type, order):
    # stejny seed = vzdycky stejna "nahodna" cisla
    rng = random.Random(seed)

    data = []
    for _ in range(count):
        if value_type == "Desetinná čísla":
            data.append(round(rng.uniform(0, 1000), 2))
        elif value_type == "Text":
            # nahodne slovo z 5 pismen
            word = ""
            for _ in range(5):
                word += rng.choice("abcdefghijklmnopqrstuvwxyz")
            data.append(word)
        else:
            data.append(rng.randint(0, 99999))

    # upravime poradi
    if order == "Seřazeně":
        data.sort()
    elif order == "Obráceně":
        data.sort(reverse=True)
    elif order == "Skoro seřazeně":
        data.sort()
        # prohodime par nahodnych dvojic
        for _ in range(max(1, count // 20)):
            a = rng.randrange(count)
            b = rng.randrange(count)
            data[a], data[b] = data[b], data[a]
    return data


def parse_text(text, value_type):
    # carky a stredniky nahradime mezerou a rozdelime podle mezer a radku
    text = text.replace(",", " ").replace(";", " ")
    parts = text.split()

    if value_type == "Celá čísla":
        return [int(p) for p in parts], value_type
    if value_type == "Desetinná čísla":
        return [float(p) for p in parts], value_type
    if value_type == "Text":
        return parts, value_type

    # automaticky: zkusime cela cisla, pak desetinna, jinak text
    try:
        return [int(p) for p in parts], "Celá čísla"
    except ValueError:
        pass
    try:
        return [float(p) for p in parts], "Desetinná čísla"
    except ValueError:
        pass
    return parts, "Text"


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("SortApp")
        self.root.geometry("1050x800")

        self.data = []                # data, ktera budeme tridit
        self.results = []             # vysledky posledniho porovnani
        self.stop_requested = False   # nastavi tlacitko Zastavit

        ttk.Label(root, text="SortApp", font=("", 20, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
        ttk.Label(root, text="Stejná data. Čtyři algoritmy. Porovnání skutečné doby třídění.").pack(anchor="w", padx=10)

        self.build_data_section()
        self.build_algorithms_section()
        self.build_results_section()

        ttk.Label(root, text=f"Pomalé metody O(n²): max. {MAX_FOR_SLOW} prvků. "
                             f"Animace: jeden algoritmus a max. {MAX_FOR_ANIMATION} hodnot.").pack(anchor="w", padx=10)
        self.status = ttk.Label(root, text="Připraveno.")
        self.status.pack(anchor="w", padx=10, pady=(0, 10))

        # na zacatku rovnou vygenerujeme data
        self.generate()

    # ---------- 1. cast: priprava dat ----------

    def build_data_section(self):
        frame = ttk.LabelFrame(self.root, text="1  Připravte data")
        frame.pack(fill="x", padx=10, pady=5)

        # radek 1: typ hodnot a nacteni souboru
        row = ttk.Frame(frame)
        row.pack(fill="x", padx=5, pady=3)
        ttk.Label(row, text="Typ hodnot").pack(side="left")
        self.type_box = ttk.Combobox(row, values=VALUE_TYPES, state="readonly", width=18)
        self.type_box.set("Automaticky")
        self.type_box.pack(side="left", padx=5)
        ttk.Button(row, text="Načíst TXT / CSV...", command=self.load_file).pack(side="right")

        # radek 2: generator
        row = ttk.Frame(frame)
        row.pack(fill="x", padx=5, pady=3)
        ttk.Label(row, text="Počet").pack(side="left")
        self.count_entry = ttk.Entry(row, width=10)
        self.count_entry.insert(0, "1000")
        self.count_entry.pack(side="left", padx=5)
        ttk.Label(row, text="Seed").pack(side="left", padx=(15, 0))
        self.seed_entry = ttk.Entry(row, width=10)
        self.seed_entry.insert(0, "42")
        self.seed_entry.pack(side="left", padx=5)
        self.order_box = ttk.Combobox(row, values=ORDERS, state="readonly", width=16)
        self.order_box.set("Náhodně")
        self.order_box.pack(side="left", padx=15)
        ttk.Button(row, text="Generovat data", command=self.generate).pack(side="left")

        # radek 3: rucni vstup
        ttk.Label(frame, text="Ruční vstup: mezery, nové řádky, čárky nebo středníky; desetinná čísla s tečkou.").pack(anchor="w", padx=5)
        row = ttk.Frame(frame)
        row.pack(fill="x", padx=5, pady=3)
        self.manual_input = tk.Text(row, height=2)
        self.manual_input.insert("1.0", "12 -5 8 0 12 3")
        self.manual_input.pack(side="left", fill="x", expand=True)
        ttk.Button(row, text="Použít ruční vstup", command=self.use_manual_input).pack(side="left", padx=5)

        # informace o aktualnich datech
        self.data_info = ttk.Label(frame, text="")
        self.data_info.pack(anchor="w", padx=5, pady=3)

    def set_data(self, data, description):
        # sem prijdou nova data odkudkoliv (generator, soubor, rucne)
        self.data = data
        self.data_info.config(text=f"{len(data)} hodnot • {description}")
        self.show_preview()
        self.update_animate_button()

    def generate(self):
        try:
            count = int(self.count_entry.get())
            seed = int(self.seed_entry.get())
        except ValueError:
            messagebox.showerror("Chyba", "Počet a seed musí být celá čísla.")
            return
        if count < 1:
            messagebox.showerror("Chyba", "Počet musí být aspoň 1.")
            return

        value_type = self.type_box.get()
        if value_type == "Automaticky":
            value_type = "Celá čísla"
        data = generate_data(count, seed, value_type, self.order_box.get())
        self.set_data(data, f"{value_type} • Generátor, seed {seed}, {self.order_box.get()}")

    def use_manual_input(self):
        self.load_from_text(self.manual_input.get("1.0", "end"), "Ruční vstup")

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text a CSV", "*.txt *.csv"), ("Všechny soubory", "*")])
        if not path:
            return
        with open(path, encoding="utf-8") as file:
            text = file.read()
        self.load_from_text(text, "Soubor " + path)

    def load_from_text(self, text, source):
        try:
            data, value_type = parse_text(text, self.type_box.get())
        except ValueError:
            messagebox.showerror("Chyba", f"Některé hodnoty nejsou typu: {self.type_box.get()}")
            return
        if not data:
            messagebox.showerror("Chyba", "Nejsou tam žádné hodnoty.")
            return
        self.set_data(data, f"{value_type} • {source}")

    # ---------- 2. cast: vyber algoritmu ----------

    def build_algorithms_section(self):
        frame = ttk.LabelFrame(self.root, text="2  Vyberte algoritmy")
        frame.pack(fill="x", padx=10, pady=5)

        # zaskrtavatka v mrizce 2 x 2
        grid = ttk.Frame(frame)
        grid.pack(fill="x", padx=5, pady=3)
        self.checked = []  # pro kazdy algoritmus jedna promenna True/False
        for i, alg in enumerate(ALGORITHMS):
            var = tk.BooleanVar(value=False)
            self.checked.append(var)
            text = f"{alg['name']}  •  {alg['info']}"
            checkbox = ttk.Checkbutton(grid, text=text, variable=var, command=self.update_animate_button)
            # prvni 2 vlevo, dalsi 2 vpravo
            checkbox.grid(row=i % 2, column=i // 2, sticky="w", padx=(0, 60))

        # tlacitka
        row = ttk.Frame(frame)
        row.pack(fill="x", padx=5, pady=5)
        ttk.Button(row, text="Vše", command=lambda: self.check_all(True)).pack(side="left")
        ttk.Button(row, text="Nic", command=lambda: self.check_all(False)).pack(side="left", padx=5)
        ttk.Label(row, text="Opakování (1–10):").pack(side="left", padx=(15, 5))
        self.repeats = ttk.Spinbox(row, from_=1, to=10, width=4)
        self.repeats.set(3)
        self.repeats.pack(side="left")
        self.compare_button = ttk.Button(row, text="Porovnat algoritmy", command=self.compare)
        self.compare_button.pack(side="left", padx=(15, 5))
        ttk.Button(row, text="Zastavit", command=self.stop).pack(side="left", padx=5)
        self.animate_button = ttk.Button(row, text="Animovat", command=self.animate)
        self.animate_button.pack(side="left", padx=5)

    def selected_algorithms(self):
        # vrati seznam algoritmu, ktere jsou zaskrtnute
        selected = []
        for i, alg in enumerate(ALGORITHMS):
            if self.checked[i].get():
                selected.append(alg)
        return selected

    def check_all(self, value):
        for var in self.checked:
            var.set(value)
        self.update_animate_button()

    def update_animate_button(self):
        # animovat jde jen s jednim algoritmem a malo daty
        if len(self.selected_algorithms()) == 1 and len(self.data) <= MAX_FOR_ANIMATION:
            self.animate_button.config(state="normal")
        else:
            self.animate_button.config(state="disabled")

    def animate(self):
        algorithm = self.selected_algorithms()[0]
        AnimationWindow(self.root, algorithm, self.data)

    def stop(self):
        self.stop_requested = True

    def compare(self):
        selected = self.selected_algorithms()
        if not selected:
            messagebox.showinfo("Porovnání", "Vyberte aspoň jeden algoritmus.")
            return
        try:
            repeats = int(self.repeats.get())
        except ValueError:
            repeats = 1
        repeats = max(1, min(10, repeats))

        # spravny vysledek, podle nej kontrolujeme ostatni algoritmy
        expected = sorted(self.data)

        self.stop_requested = False
        self.compare_button.config(state="disabled")
        self.results = []

        for alg in selected:
            # pomale algoritmy na moc datech preskocime
            if alg["slow"] and len(self.data) > MAX_FOR_SLOW:
                self.results.append((alg["name"], None, None, None, "Přeskočeno (moc dat)"))
                continue

            times = []
            for _ in range(repeats):
                self.status.config(text=f"Třídím: {alg['name']} ({len(times) + 1}/{repeats})...")
                # prekreslime okno, aby slo kliknout na Zastavit
                self.root.update()
                if self.stop_requested:
                    break

                # kazdy beh dostane kopii stejnych dat
                copy = self.data.copy()
                t_start = time.perf_counter()
                alg["func"](copy)
                t_end = time.perf_counter()
                times.append((t_end - t_start) * 1000)  # v milisekundach

            if self.stop_requested:
                break

            # zkontrolujeme, jestli algoritmus opravdu seradil spravne
            status = "Ověřeno" if copy == expected else "CHYBA"
            self.results.append((alg["name"], statistics.median(times), min(times), max(times), status))

        self.compare_button.config(state="normal")
        self.show_results()
        if self.stop_requested:
            self.status.config(text="Zastaveno. Zobrazeny jen dokončené algoritmy.")
        else:
            self.status.config(text="Hotovo.")

    # ---------- 3. cast: vysledky ----------

    def build_results_section(self):
        tabs = ttk.Notebook(self.root)
        tabs.pack(fill="both", expand=True, padx=10, pady=5)

        # zalozka s tabulkou casu
        page = ttk.Frame(tabs)
        tabs.add(page, text="3  Porovnání časů")
        columns = ("algorithm", "median", "minimum", "maximum", "status")
        self.table = ttk.Treeview(page, columns=columns, show="headings", height=8)
        headings = ["Algoritmus", "Medián (ms)", "Minimum (ms)", "Maximum (ms)", "Stav"]
        for column, heading in zip(columns, headings):
            self.table.heading(column, text=heading)
            self.table.column(column, width=150, anchor="e")
        self.table.column("algorithm", anchor="w")
        self.table.column("status", anchor="w")
        self.table.pack(fill="both", expand=True, padx=5, pady=5)

        self.fastest_label = ttk.Label(page, text="")
        self.fastest_label.pack(anchor="w", padx=5)
        ttk.Button(page, text="Export porovnání do CSV...", command=self.export_csv).pack(anchor="w", padx=5, pady=5)

        # zalozka s nahledem dat
        page = ttk.Frame(tabs)
        tabs.add(page, text="Náhled dat")
        self.preview = tk.Text(page, height=8, wrap="word")
        self.preview.pack(fill="both", expand=True, padx=5, pady=5)

    def show_preview(self):
        # ukazeme prvnich 500 hodnot, vic by bylo zbytecne
        self.preview.delete("1.0", "end")
        text = " ".join(str(v) for v in self.data[:500])
        if len(self.data) > 500:
            text += f" ... (a dalších {len(self.data) - 500})"
        self.preview.insert("1.0", text)

    def show_results(self):
        # smazeme starou tabulku
        for row in self.table.get_children():
            self.table.delete(row)

        # nejdriv ty s casem (od nejrychlejsiho), preskocene na konec
        timed = [r for r in self.results if r[1] is not None]
        untimed = [r for r in self.results if r[1] is None]
        timed.sort(key=lambda r: r[1])

        for name, median, minimum, maximum, status in timed:
            self.table.insert("", "end", values=(name, f"{median:.6f}", f"{minimum:.6f}", f"{maximum:.6f}", status))
        for name, _, _, _, status in untimed:
            self.table.insert("", "end", values=(name, "-", "-", "-", status))

        if timed:
            name, median = timed[0][0], timed[0][1]
            self.fastest_label.config(text=f"Nejrychlejší v tomto měření: {name} — {median:.6f} ms (medián).")
        else:
            self.fastest_label.config(text="")

    def export_csv(self):
        if not self.results:
            messagebox.showinfo("Export", "Nejdřív spusťte porovnání.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["Algoritmus", "Median (ms)", "Minimum (ms)", "Maximum (ms)", "Stav"])
            for row in self.results:
                writer.writerow(row)
        self.status.config(text="Uloženo do " + path)


# spusteni aplikace
root = tk.Tk()
App(root)
root.mainloop()
