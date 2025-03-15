import pyxel

class Skin:
    def __init__(self):
        pass

    def update(self):
        if pyxel.btnp(pyxel.KEY_1):
            return 8  # Merah
        elif pyxel.btnp(pyxel.KEY_2):
            return 9  # Hijau
        elif pyxel.btnp(pyxel.KEY_3):
            return 11  # Kuning
        elif pyxel.btnp(pyxel.KEY_9):
            return  7  # Kembali
        return None

    def draw(self):
        pyxel.text(50, 30, "Pilih Skin", 7)
        pyxel.text(50, 50, "1. Merah", 8)
        pyxel.text(50, 60, "2. Hijau", 9)
        pyxel.text(50, 70, "3. Kuning", 11)
        pyxel.text(50, 80, "9: Kembali", 7)