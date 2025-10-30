from moviepy.editor import VideoFileClip

def konwertuj_webm_na_gif(nazwa_pliku):
    if not nazwa_pliku.endswith(".webm"):
        print("To nie jest plik .webm!")
        return
    clip = VideoFileClip(nazwa_pliku)
    clip.write_gif(nazwa_pliku.replace(".webm", ".gif"))
    print("Zapisano plik GIF!")

def konwertuj_webm_na_png(nazwa_pliku):
    if not nazwa_pliku.endswith(".webm"):
        print("To nie jest plik .webm!")
        return
    clip = VideoFileClip(nazwa_pliku)
    frame = clip.get_frame(0)  # pierwszy kadr
    from PIL import Image
    obraz = Image.fromarray(frame)
    obraz.save(nazwa_pliku.replace(".webm", ".png"))
    print("Zapisano plik PNG!")

print("=== Konwerter plików WEBM ===")
plik = input("Podaj nazwę pliku .webm: ")

print("1. Konwersja na GIF")
print("2. Konwersja na PNG")
wybor = input("Wybierz (1 lub 2): ")

if wybor == "1":
    konwertuj_webm_na_gif(plik)
elif wybor == "2":
    konwertuj_webm_na_png(plik)
else:
    print("Nieprawidłowy wybór.")