import os
from moviepy.editor import VideoFileClip
from PIL import Image

def konwertuj_folder(folder, tryb="gif"):
    for plik in os.listdir(folder):
        if plik.endswith(".webm"):
            sciezka = os.path.join(folder, plik)
            if tryb == "gif":
                clip = VideoFileClip(sciezka)
                clip.write_gif(sciezka.replace(".webm", ".gif"))
            elif tryb == "png":
                clip = VideoFileClip(sciezka)
                frame = clip.get_frame(0)
                obraz = Image.fromarray(frame)
                obraz.save(sciezka.replace(".webm", ".png"))
            print(f"Przekonwertowano: {plik}")

print("=== Konwerter folderu WEBM ===")
folder = input("Podaj ścieżkę do folderu: ")
tryb = input("Wybierz format (gif/png): ").lower()
konwertuj_folder(folder, tryb)
