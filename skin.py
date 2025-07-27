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
            return 11 # Kuning
        elif pyxel.btnp(pyxel.KEY_4):
            return 12 # Biru muda
        elif pyxel.btnp(pyxel.KEY_5):
            return 10 # Oranye
        elif pyxel.btnp(pyxel.KEY_6):
            return 1  # Biru gelap
        elif pyxel.btnp(pyxel.KEY_7):
            return 13 # Merah muda
        elif pyxel.btnp(pyxel.KEY_8):
            return 3  # Cyan
        elif pyxel.btnp(pyxel.KEY_9):
            return 7  # Kembali ke menu (warna default)
        return None

    def draw(self):
        pyxel.text(50, 30, "PILIH SKIN", 7)
        pyxel.text(50, 50, "1. Merah", 8)
        pyxel.text(50, 60, "2. Hijau", 9)
        pyxel.text(50, 70, "3. Kuning", 11)
        pyxel.text(50, 80, "4. Biru Muda", 12)
        pyxel.text(50, 90, "5. Oranye", 10)
        pyxel.text(50, 100, "6. Biru Gelap", 1)
        pyxel.text(50, 110, "7. Merah Muda", 13)
        pyxel.text(50, 120, "8. Cyan", 3)
        pyxel.text(50, 130, "9: Kembali", 7)
