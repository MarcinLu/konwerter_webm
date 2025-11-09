import os
import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip
from PIL import Image

def wybierz_folder_wejsciowy():
    folder = filedialog.askdirectory(title="Wybierz folder z plikami .webm")
    if folder:
        entry_wejsciowy.delete(0, tk.END)
        entry_wejsciowy.insert(0, folder)

def wybierz_folder_docelowy():
    folder = filedialog.askdirectory(title="Wybierz folder docelowy")
    if folder:
        entry_docelowy.delete(0, tk.END)
        entry_docelowy.insert(0, folder)

def konwertuj_folder():
    folder_wej = entry_wejsciowy.get()
    folder_doc = entry_docelowy.get()
    tryb = var_tryb.get()

    if not folder_wej or not folder_doc:
        messagebox.showerror("Błąd", "Wybierz oba foldery: źródłowy i docelowy.")
        return

    pliki = [p for p in os.listdir(folder_wej) if p.endswith(".webm")]
    if not pliki:
        messagebox.showinfo("Brak plików", "Nie znaleziono plików .webm w podanym folderze.")
        return

    for plik in pliki:
        sciezka = os.path.join(folder_wej, plik)
        nazwa_docelowa = os.path.splitext(plik)[0]

        try:
            clip = VideoFileClip(sciezka)
            if tryb == "gif":
                output_path = os.path.join(folder_doc, f"{nazwa_docelowa}.gif")
                clip.write_gif(output_path)
            elif tryb == "png":
                output_path = os.path.join(folder_doc, f"{nazwa_docelowa}.png")
                frame = clip.get_frame(0)
                obraz = Image.fromarray(frame)
                obraz.save(output_path)
            clip.close()
            status.insert(tk.END, f"✅ Przekonwertowano: {plik}\n")
        except Exception as e:
            status.insert(tk.END, f"❌ Błąd przy {plik}: {e}\n")

    messagebox.showinfo("Zakończono", "Konwersja zakończona!")

# --- GUI ---
root = tk.Tk()
root.title("Konwerter WEBM → GIF/PNG")
root.geometry("550x400")
root.resizable(False, False)

# Folder źródłowy
tk.Label(root, text="Folder z plikami .webm:").pack(anchor="w", padx=10, pady=(10, 0))
frame1 = tk.Frame(root)
frame1.pack(fill="x", padx=10)
entry_wejsciowy = tk.Entry(frame1, width=50)
entry_wejsciowy.pack(side="left", fill="x", expand=True)
tk.Button(frame1, text="Wybierz...", command=wybierz_folder_wejsciowy).pack(side="right", padx=5)

# Folder docelowy
tk.Label(root, text="Folder docelowy:").pack(anchor="w", padx=10, pady=(10, 0))
frame2 = tk.Frame(root)
frame2.pack(fill="x", padx=10)
entry_docelowy = tk.Entry(frame2, width=50)
entry_docelowy.pack(side="left", fill="x", expand=True)
tk.Button(frame2, text="Wybierz...", command=wybierz_folder_docelowy).pack(side="right", padx=5)

# Wybór formatu
tk.Label(root, text="Wybierz format:").pack(anchor="w", padx=10, pady=(10, 0))
var_tryb = tk.StringVar(value="gif")
frame3 = tk.Frame(root)
frame3.pack(anchor="w", padx=20)
tk.Radiobutton(frame3, text="GIF", variable=var_tryb, value="gif").pack(side="left")
tk.Radiobutton(frame3, text="PNG", variable=var_tryb, value="png").pack(side="left")

# Przycisk konwersji
tk.Button(root, text="Rozpocznij konwersję", command=konwertuj_folder, bg="#4CAF50", fg="white").pack(pady=15)

# Pole statusu
tk.Label(root, text="Status:").pack(anchor="w", padx=10)
status = tk.Text(root, height=10, wrap="word")
status.pack(fill="both", expand=True, padx=10, pady=(0, 10))

root.mainloop()