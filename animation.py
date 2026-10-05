# okno s animaci jednoho algoritmu
#
# jak to funguje:
# 1. algoritmus pustime hned na zacatku a on si zapise vsechny kroky do seznamu
# 2. kazdy krok je (seznam hodnot, aktivni pozice, popis)
# 3. animace pak jen kresli jeden krok za druhym

import tkinter as tk
from tkinter import ttk

# barvy
BACKGROUND = "#13203a"
BLUE = "#60a5fa"
ORANGE = "#f59e0b"
GREEN = "#22c55e"
TEXT = "#ffffff"

# rozmery sloupcu v pixelech
BAR_WIDTH = 60
GAP = 8
CHART_HEIGHT = 380
LABEL_HEIGHT = 45


class AnimationWindow:
    def __init__(self, parent, algorithm, data):
        self.window = tk.Toplevel(parent)
        self.window.title("Animace - " + algorithm["name"])
        self.window.geometry("1100x720")

        # spocitame vsechny kroky dopredu
        self.steps = [(data.copy(), [], "Výchozí pořadí")]
        copy = data.copy()
        algorithm["func"](copy, self.steps)
        self.steps.append((copy.copy(), [], "Hotovo, seřazeno"))

        # vyska sloupce = poradi hodnoty mezi unikatnimi hodnotami
        # (takze to funguje i pro zaporna cisla a text)
        unique = sorted(set(data))
        self.ranks = {}
        for i, value in enumerate(unique):
            self.ranks[value] = i + 1
        self.unique_count = len(unique)

        self.step = 0         # ktery krok zrovna ukazujeme
        self.playing = False  # jestli bezi prehravani
        self.timer = None     # id naplanovaneho dalsiho kroku

        self.build_controls(algorithm)
        self.draw()

        # kdyz se okno zavre krizkem, zastavime casovac
        self.window.protocol("WM_DELETE_WINDOW", self.close)

    def build_controls(self, algorithm):
        # nadpis a vysvetleni algoritmu
        ttk.Label(self.window, text=algorithm["name"], font=("", 20, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
        ttk.Label(self.window, text=algorithm["description"], wraplength=1050).pack(anchor="w", padx=10, pady=5)
        ttk.Label(self.window, text="Oranžová: aktivní prvky • Modrá: ostatní prvky • Zelená: hotovo").pack(anchor="w", padx=10)

        # platno na sloupce + posuvnik, kdyz se nevejdou
        frame = ttk.Frame(self.window)
        frame.pack(fill="x", padx=10, pady=5)
        self.canvas = tk.Canvas(frame, bg=BACKGROUND, height=CHART_HEIGHT + LABEL_HEIGHT, highlightthickness=0)
        self.canvas.pack(fill="x")
        scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=self.canvas.xview)
        scrollbar.pack(fill="x")
        self.canvas.config(xscrollcommand=scrollbar.set)
        # kdyz jedeme mysi nad sloupcem, ukazeme jeho hodnotu
        self.canvas.bind("<Motion>", self.on_mouse_move)

        ttk.Label(self.window, text="Výška sloupce = pořadí hodnoty mezi unikátními hodnotami; dole je její popisek.").pack(anchor="w", padx=10)
        self.position_label = ttk.Label(self.window, text="Najeď myší na sloupec")
        self.position_label.pack(anchor="w", padx=10, pady=5)

        # tlacitka dole
        buttons = ttk.Frame(self.window)
        buttons.pack(fill="x", padx=10, pady=10)
        self.play_button = ttk.Button(buttons, text="Přehrát", command=self.toggle_play)
        self.play_button.pack(side="left", padx=3)
        ttk.Button(buttons, text="Jeden krok", command=self.step_forward).pack(side="left", padx=3)
        ttk.Button(buttons, text="Od začátku", command=self.restart).pack(side="left", padx=3)

        ttk.Label(buttons, text="Rychlost:").pack(side="left", padx=(20, 5))
        self.speed = tk.IntVar(value=5)
        ttk.Scale(buttons, from_=1, to=50, variable=self.speed, length=200,
                  command=self.on_speed_change).pack(side="left")
        self.speed_label = ttk.Label(buttons, text="5 kroků / s", width=12)
        self.speed_label.pack(side="left", padx=5)

        ttk.Button(buttons, text="Zavřít", command=self.close).pack(side="right")

        self.step_label = ttk.Label(self.window, text="")
        self.step_label.pack(anchor="w", padx=10)

    def draw(self):
        # smazeme stare sloupce a nakreslime aktualni krok
        self.canvas.delete("all")
        values, active, label = self.steps[self.step]
        is_last = self.step == len(self.steps) - 1

        for i, value in enumerate(values):
            # vybereme barvu
            if is_last:
                color = GREEN
            elif i in active:
                color = ORANGE
            else:
                color = BLUE

            # vyska podle poradi hodnoty
            height = self.ranks[value] / self.unique_count * (CHART_HEIGHT - 20)
            x1 = i * (BAR_WIDTH + GAP) + GAP
            x2 = x1 + BAR_WIDTH
            y1 = CHART_HEIGHT - height
            y2 = CHART_HEIGHT
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

            # popisky pod sloupcem: hodnota a cislo pozice
            center = (x1 + x2) / 2
            self.canvas.create_text(center, CHART_HEIGHT + 15, text=str(value), fill=TEXT)
            self.canvas.create_text(center, CHART_HEIGHT + 32, text=str(i + 1), fill="#9ca3af", font=("", 8))

        # nastavime jak siroke je platno, aby fungoval posuvnik
        total_width = len(values) * (BAR_WIDTH + GAP) + GAP
        self.canvas.config(scrollregion=(0, 0, total_width, CHART_HEIGHT + LABEL_HEIGHT))

        # text pod grafem, co se zrovna deje
        text = f"Krok {self.step + 1} / {len(self.steps)} • {label}"
        if active:
            positions = " a ".join(str(p + 1) for p in active)
            text += f" (pozice {positions})"
        self.step_label.config(text=text)

    def on_mouse_move(self, event):
        # prepocitame x mysi na cislo sloupce (canvasx pocita i s posunutim)
        x = self.canvas.canvasx(event.x)
        i = int(x // (BAR_WIDTH + GAP))
        values = self.steps[self.step][0]
        if 0 <= i < len(values):
            self.position_label.config(text=f"Pozice {i + 1}: {values[i]}")

    def step_forward(self):
        # posuneme se o krok dal, pokud nejsme na konci
        if self.step < len(self.steps) - 1:
            self.step += 1
            self.draw()

    def toggle_play(self):
        if self.playing:
            self.stop()
        else:
            # kdyz jsme na konci, zacneme znovu
            if self.step == len(self.steps) - 1:
                self.step = 0
            self.playing = True
            self.play_button.config(text="Pauza")
            self.next_frame()

    def next_frame(self):
        # udela jeden krok a naplanuje dalsi (tak vznikne animace)
        if not self.playing:
            return
        self.step_forward()
        if self.step == len(self.steps) - 1:
            self.stop()
            return
        delay = int(1000 / self.speed.get())
        self.timer = self.window.after(delay, self.next_frame)

    def stop(self):
        self.playing = False
        self.play_button.config(text="Přehrát")
        if self.timer is not None:
            self.window.after_cancel(self.timer)
            self.timer = None

    def restart(self):
        self.stop()
        self.step = 0
        self.draw()

    def on_speed_change(self, value):
        # posuvnik vraci desetinne cislo, zaokrouhlime ho
        self.speed.set(round(float(value)))
        self.speed_label.config(text=f"{self.speed.get()} kroků / s")

    def close(self):
        self.stop()
        self.window.destroy()
