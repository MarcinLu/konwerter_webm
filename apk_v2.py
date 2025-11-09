import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from moviepy.editor import VideoFileClip
from PIL import Image
import threading

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

    # Zablokuj przyciski w trakcie konwersji
    btn_start.config(state="disabled")
    btn_folder_wej.config(state="disabled")
    btn_folder_doc.config(state="disabled")
    progress["value"] = 0
    progress["maximum"] = len(pliki)
    status.delete(1.0, tk.END)

    def wykonaj_konwersje():
        for i, plik in enumerate(pliki, start=1):
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

            # Aktualizuj pasek postępu
            progress["value"] = i
            root.update_idletasks()

        status.insert(tk.END, "\n✅ Konwersja zakończona!\n")
        messagebox.showinfo("Zakończono", "Konwersja zakończona!")

        # Odblokuj przyciski
        btn_start.config(state="normal")
        btn_folder_wej.config(state="normal")
        btn_folder_doc.config(state="normal")

    # Uruchom w wątku, by GUI się nie zawieszało
    threading.Thread(target=wykonaj_konwersje, daemon=True).start()

# --- GUI ---
root = tk.Tk()
root.title("Konwerter WEBM → GIF/PNG")
root.geometry("580x450")
root.resizable(False, False)

# Folder źródłowy
tk.Label(root, text="Folder z plikami .webm:").pack(anchor="w", padx=10, pady=(10, 0))
frame1 = tk.Frame(root)
frame1.pack(fill="x", padx=10)
entry_wejsciowy = tk.Entry(frame1, width=50)
entry_wejsciowy.pack(side="left", fill="x", expand=True)
btn_folder_wej = tk.Button(frame1, text="Wybierz...", command=wybierz_folder_wejsciowy)
btn_folder_wej.pack(side="right", padx=5)

# Folder docelowy
tk.Label(root, text="Folder docelowy:").pack(anchor="w", padx=10, pady=(10, 0))
frame2 = tk.Frame(root)
frame2.pack(fill="x", padx=10)
entry_docelowy = tk.Entry(frame2, width=50)
entry_docelowy.pack(side="left", fill="x", expand=True)
btn_folder_doc = tk.Button(frame2, text="Wybierz...", command=wybierz_folder_docelowy)
btn_folder_doc.pack(side="right", padx=5)

# Wybór formatu
tk.Label(root, text="Wybierz format:").pack(anchor="w", padx=10, pady=(10, 0))
var_tryb = tk.StringVar(value="gif")
frame3 = tk.Frame(root)
frame3.pack(anchor="w", padx=20)
tk.Radiobutton(frame3, text="GIF", variable=var_tryb, value="gif").pack(side="left")
tk.Radiobutton(frame3, text="PNG", variable=var_tryb, value="png").pack(side="left")

# Przycisk konwersji
btn_start = tk.Button(root, text="Rozpocznij konwersję", command=konwertuj_folder, bg="#4CAF50", fg="white", height=2)
btn_start.pack(pady=10, fill="x", padx=10)

# Pasek postępu
progress = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
progress.pack(padx=20, pady=10)

# Pole statusu (z przewijaniem)
tk.Label(root, text="Status:").pack(anchor="w", padx=10)
frame_status = tk.Frame(root)
frame_status.pack(fill="both", expand=True, padx=10, pady=(0, 10))
scrollbar = tk.Scrollbar(frame_status)
scrollbar.pack(side="right", fill="y")
status = tk.Text(frame_status, height=10, wrap="word", yscrollcommand=scrollbar.set)
status.pack(fill="both", expand=True)
scrollbar.config(command=status.yview)

root.mainloop()