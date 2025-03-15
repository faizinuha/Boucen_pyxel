import pyxel

class Menu:
    def __init__(self):
        pass

    def update(self):
        if pyxel.btnp(pyxel.KEY_1):
            return "play"
        elif pyxel.btnp(pyxel.KEY_2):
            return "skin"
        elif pyxel.btnp(pyxel.KEY_3):
            return "leaderboard"
        elif pyxel.btnp(pyxel.KEY_4):
            return "quit"
        return None

    def draw(self):
        pyxel.text(50, 30, "Bounce Modern", 7)
        pyxel.text(50, 50, "1. Main", 7)
        pyxel.text(50, 60, "2. Pilih Skin", 7)
        pyxel.text(50, 70, "3. Leaderboard", 7)
        pyxel.text(50, 80, "4. Keluar", 7)