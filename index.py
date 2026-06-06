import tkinter as tk
import random
import math


class FriendApp:
    def __init__(self, root):
        self.root = root
        self.root.title("A very important question 🐻")
        self.root.geometry("500x420")
        self.root.resizable(False, False)
        self.root.configure(bg="#fff0f6")

        self.no_clicks = 0
        self.confetti_particles = []
        self.animating = False

        self.show_question_screen()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_question_screen(self):
        self.clear()

        # Background canvas for question screen
        self.canvas = tk.Canvas(self.root, width=500, height=420,
                                bg="#fff0f6", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Sticker
        self.canvas.create_text(250, 90, text="🐻🐼", font=("Segoe UI Emoji", 52), fill="#c2185b")

        # Question text
        self.canvas.create_text(250, 175, text="Will you be my friend?",
                                font=("Georgia", 22, "bold"), fill="#c2185b")

        # Yes button
        yes_btn = tk.Button(
            self.root, text="  Yes!  ",
            font=("Georgia", 16, "bold"),
            bg="#e91e8c", fg="white",
            activebackground="#c2185b", activeforeground="white",
            relief="flat", cursor="hand2", bd=0,
            padx=20, pady=10,
            command=self.on_yes
        )
        self.yes_btn_window = self.canvas.create_window(210, 260, window=yes_btn)

        # No button
        self.no_btn = tk.Button(
            self.root, text="  No  ",
            font=("Georgia", 14),
            bg="#fff0f6", fg="#aaaaaa",
            activebackground="#fce4ec", activeforeground="#888",
            relief="flat", cursor="hand2", bd=1,
            padx=16, pady=8,
            command=self.on_no
        )
        self.no_btn_window = self.canvas.create_window(320, 260, window=self.no_btn)

        # Hint text
        self.hint = self.canvas.create_text(250, 360, text="",
                                            font=("Georgia", 11, "italic"), fill="#e91e8c")

        self.bounce_sticker()

    def bounce_sticker(self):
        if not hasattr(self, 'canvas') or not self.canvas.winfo_exists():
            return
        try:
            t = self.root.after_info  # check root alive
        except Exception:
            return
        self._bounce_step = getattr(self, '_bounce_step', 0)
        offset = int(6 * math.sin(self._bounce_step * 0.2))
        self.canvas.coords(self.canvas.find_all()[0], 250, 90 + offset)
        self._bounce_step += 1
        self.root.after(60, self.bounce_sticker)

    def on_no(self):
        self.no_clicks += 1

        # Shrink the No button over time
        size = max(9, 14 - self.no_clicks)
        padx = max(6, 16 - self.no_clicks * 2)
        pady = max(3, 8 - self.no_clicks)
        self.no_btn.config(font=("Georgia", size), padx=padx, pady=pady)

        # Move No button to random position
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        new_x = random.randint(60, w - 60)
        new_y = random.randint(220, h - 60)
        self.canvas.coords(self.no_btn_window, new_x, new_y)

        hints = [
            "", "", "Hmm... are you sure? 🤔",
            "That's not the right button! 😅",
            "You keep missing... 👀",
            "Maybe try the other one? 💕",
            "The No button is getting tired... 😴",
            "Just click Yes already! 🥺",
        ]
        idx = min(self.no_clicks, len(hints) - 1)
        self.canvas.itemconfig(self.hint, text=hints[idx])

        if self.no_clicks >= 7:
            self.no_btn.config(state="disabled", fg="#dddddd")
            self.canvas.itemconfig(self.hint, text="No is broken now. Just click Yes 😂")

    def on_yes(self):
        self.clear()
        self.show_celebration()

    def show_celebration(self):
        self.canvas = tk.Canvas(self.root, width=500, height=420,
                                bg="#fff0f6", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Big emoji
        self.canvas.create_text(250, 100, text="🎉🥳🎊",
                                font=("Segoe UI Emoji", 48), fill="#e91e8c")

        self.canvas.create_text(250, 200, text="Congratulations!",
                                font=("Georgia", 28, "bold"), fill="#c2185b")

        self.canvas.create_text(250, 248, text="You're my friend now!",
                                font=("Georgia", 18), fill="#e91e8c")

        self.canvas.create_text(250, 295, text="No take-backs. It's official. 🤝",
                                font=("Georgia", 13, "italic"), fill="#888888")

        # Start confetti
        self.confetti_particles = []
        colors = ["#e91e8c", "#ff6eb0", "#fff176", "#80deea",
                  "#b39ddb", "#a5d6a7", "#ffcc80", "#f48fb1"]
        for _ in range(70):
            self.confetti_particles.append({
                "x": random.randint(0, 500),
                "y": random.randint(-100, 0),
                "w": random.randint(8, 16),
                "h": random.randint(4, 9),
                "color": random.choice(colors),
                "vx": random.uniform(-2, 2),
                "vy": random.uniform(2, 5),
                "rot": random.uniform(0, 360),
                "vrot": random.uniform(-5, 5),
                "id": None
            })
        self.animating = True
        self.animate_confetti()

    def animate_confetti(self):
        if not self.animating:
            return
        if not self.canvas.winfo_exists():
            return

        # Remove old confetti
        for p in self.confetti_particles:
            if p["id"]:
                try:
                    self.canvas.delete(p["id"])
                except Exception:
                    pass

        for p in self.confetti_particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["rot"] += p["vrot"]

            # Rotate rectangle manually with polygon
            cx, cy = p["x"], p["y"]
            w2, h2 = p["w"] / 2, p["h"] / 2
            angle = math.radians(p["rot"])
            cos_a, sin_a = math.cos(angle), math.sin(angle)

            corners = [(-w2, -h2), (w2, -h2), (w2, h2), (-w2, h2)]
            points = []
            for dx, dy in corners:
                rx = cx + dx * cos_a - dy * sin_a
                ry = cy + dx * sin_a + dy * cos_a
                points.extend([rx, ry])

            p["id"] = self.canvas.create_polygon(points, fill=p["color"], outline="")

            if p["y"] > 440:
                p["y"] = random.randint(-30, -5)
                p["x"] = random.randint(0, 500)

        self.root.after(30, self.animate_confetti)


def main():
    root = tk.Tk()
    app = FriendApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
