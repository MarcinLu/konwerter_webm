import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from moviepy.editor import VideoFileClip
from PIL import Image
import threading

wybrane_pliki = []

def wybierz_pliki():
    global wybrane_pliki
    pliki = filedialog.askopenfilenames(
        title="Wybierz pliki .webm",
        filetypes=[("Pliki WEBM", "*.webm")]
    )
    if pliki:
        wybrane_pliki = list(pliki)
        status.delete(1.0, tk.END)
        status.insert(tk.END, f"✅ Wybrano {len(wybrane_pliki)} plików.\n")
        entry_pliki.delete(0, tk.END)
        entry_pliki.insert(0, "; ".join(os.path.basename(p) for p in wybrane_pliki))

def wybierz_folder_docelowy():
    folder = filedialog.askdirectory(title="Wybierz folder docelowy")
    if folder:
        entry_docelowy.delete(0, tk.END)
        entry_docelowy.insert(0, folder)

def konwertuj():
    global wybrane_pliki
    folder_doc = entry_docelowy.get()

    if not wybrane_pliki:
        messagebox.showerror("Błąd", "Nie wybrano żadnych plików .webm.")
        return
    if not folder_doc:
        messagebox.showerror("Błąd", "Wybierz folder docelowy.")
        return

    btn_start.config(state="disabled")
    btn_wybierz_pliki.config(state="disabled")
    btn_folder_doc.config(state="disabled")
    progress["value"] = 0
    progress["maximum"] = len(wybrane_pliki)
    status.delete(1.0, tk.END)

    def wykonaj_konwersje():
        for i, sciezka in enumerate(wybrane_pliki, start=1):
            plik = os.path.basename(sciezka)
            nazwa_docelowa = os.path.splitext(plik)[0]

            try:
                clip = VideoFileClip(sciezka)
                # Automatyczne wykrycie formatu
                # Jeśli długość > 1s → GIF, w przeciwnym razie → PNG
                if clip.duration > 1:
                    output_path = os.path.join(folder_doc, f"{nazwa_docelowa}.gif")
                    clip.write_gif(output_path, logger=None)
                    status.insert(tk.END, f"🎞️ {plik} → GIF\n")
                else:
                    frame = clip.get_frame(0)
                    obraz = Image.fromarray(frame)
                    output_path = os.path.join(folder_doc, f"{nazwa_docelowa}.png")
                    obraz.save(output_path)
                    status.insert(tk.END, f"🖼️ {plik} → PNG\n")

                clip.close()
            except Exception as e:
                status.insert(tk.END, f"❌ Błąd przy {plik}: {e}\n")

            progress["value"] = i
            root.update_idletasks()

        status.insert(tk.END, "\n✅ Konwersja zakończona!\n")
        messagebox.showinfo("Zakończono", "Konwersja wszystkich plików zakończona!")

        btn_start.config(state="normal")
        btn_wybierz_pliki.config(state="normal")
        btn_folder_doc.config(state="normal")

    threading.Thread(target=wykonaj_konwersje, daemon=True).start()

# --- GUI ---
root = tk.Tk()
root.title("Inteligentny konwerter WEBM → GIF/PNG")
root.geometry("600x470")
root.resizable(False, False)

# Wybór plików
tk.Label(root, text="Pliki źródłowe (.webm):").pack(anchor="w", padx=10, pady=(10, 0))
frame1 = tk.Frame(root)
frame1.pack(fill="x", padx=10)
entry_pliki = tk.Entry(frame1, width=50)
entry_pliki.pack(side="left", fill="x", expand=True)
btn_wybierz_pliki = tk.Button(frame1, text="Wybierz pliki...", command=wybierz_pliki)
btn_wybierz_pliki.pack(side="right", padx=5)

# Folder docelowy
tk.Label(root, text="Folder docelowy:").pack(anchor="w", padx=10, pady=(10, 0))
frame2 = tk.Frame(root)
frame2.pack(fill="x", padx=10)
entry_docelowy = tk.Entry(frame2, width=50)
entry_docelowy.pack(side="left", fill="x", expand=True)
btn_folder_doc = tk.Button(frame2, text="Wybierz...", command=wybierz_folder_docelowy)
btn_folder_doc.pack(side="right", padx=5)

# Przycisk start
btn_start = tk.Button(root, text="Rozpocznij konwersję", command=konwertuj, bg="#4CAF50", fg="white", height=2)
btn_start.pack(pady=15, fill="x", padx=10)

# Pasek postępu
progress = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
progress.pack(padx=20, pady=10)

# Status
tk.Label(root, text="Status:").pack(anchor="w", padx=10)
frame_status = tk.Frame(root)
frame_status.pack(fill="both", expand=True, padx=10, pady=(0, 10))
scrollbar = tk.Scrollbar(frame_status)
scrollbar.pack(side="right", fill="y")
status = tk.Text(frame_status, height=10, wrap="word", yscrollcommand=scrollbar.set)
status.pack(fill="both", expand=True)
scrollbar.config(command=status.yview)

root.mainloop()