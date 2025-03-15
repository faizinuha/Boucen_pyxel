import pyxel

class Leaderboard:
    def __init__(self):
        self.scores = []

    def add_score(self, name, score):
        self.scores.append((name, score))
        self.scores.sort(key=lambda x: x[1], reverse=True)  # Sort by score (highest first)

    def update(self):
        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            return "menu"
        return None

    def draw(self):
        pyxel.text(50, 30, "Leaderboard", 7)
        for i, (name, score) in enumerate(self.scores[:5]):  # Tampilkan top 5
            pyxel.text(50, 50 + i * 10, f"{name}: {score}", 7)
        pyxel.text(50, 100, "Backspace: Kembali", 7)