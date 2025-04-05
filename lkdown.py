
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import re
import pyperclip
import datetime

# Globals
destino_padrao = ""
historico_path = "lkdown_history.txt"

# URLs aceitas
URLS_VALIDAS = [
    "https://www.instagram.com/",
    "https://fb.watch/",
    "https://www.facebook.com/",
    "https://www.youtube.com/",
    "https://youtu.be/",
    "https://twitter.com/",
    "https://www.tiktok.com/"
]

# Verifica se a URL é válida
def validar_url(url):
    return any(url.startswith(p) for p in URLS_VALIDAS)

def escolher_pasta():
    global destino_padrao
    destino = filedialog.askdirectory()
    if destino:
        destino_padrao = destino
        status_pasta.config(text=f"Pasta: {destino_padrao}", fg="white")

def abrir_pasta():
    if destino_padrao:
        os.startfile(destino_padrao)

def salvar_historico(urls):
    with open(historico_path, "a", encoding="utf-8") as f:
        for url in urls:
            f.write(url + "\n")

def baixar():
    urls = entry.get("1.0", tk.END).strip().splitlines()
    urls = [u.strip() for u in urls if validar_url(u.strip())]

    if not urls:
        messagebox.showerror("Erro", "Cole pelo menos uma URL válida.")
        return

    if not destino_padrao:
        messagebox.showwarning("Aviso", "Escolha uma pasta de destino antes de baixar.")
        return

    qualidade = qualidade_var.get()
    data_str = datetime.datetime.now().strftime("%Y-%m-%d")
    erro_ocorrido = False

    for url in urls:
        status_label.config(text=f"⬇ Baixando: {url}")
        root.update()

        output_path_template = os.path.join(destino_padrao, "%(title).100s_" + data_str + ".%(ext)s")

        comando = [
            "yt-dlp",
            "-o", output_path_template,
            url
        ]

        if qualidade == "Áudio":
            comando += ["-f", "bestaudio"]
        elif qualidade == "720p":
            comando += ["-f", "bestvideo[height<=720]+bestaudio/best"]
        elif qualidade == "1080p":
            comando += ["-f", "bestvideo[height<=1080]+bestaudio/best"]

        if os.path.exists("cookies.txt"):
            comando += ["--cookies", "cookies.txt"]

        try:
            resultado = subprocess.run(comando, capture_output=True, text=True)
            if resultado.returncode != 0:
                erro_ocorrido = True
                messagebox.showerror("Erro ao baixar", f"Ocorreu um erro ao baixar:\n\n{resultado.stderr}")
            else:
                salvar_historico([url])
        except Exception as e:
            erro_ocorrido = True
            messagebox.showerror("Erro ao executar", str(e))

    if not erro_ocorrido:
        status_label.config(text="✅ Download finalizado.")
    else:
        status_label.config(text="⚠️ Alguns vídeos não foram baixados.")


def colar_automaticamente():
    try:
        link = pyperclip.paste()
        if validar_url(link):
            entry.insert(tk.END, link + "\n")
    except:
        pass

# Janela
root = tk.Tk()
root.title("LKDown - Downloader Completo")
root.geometry("600x400")
root.configure(bg="#2c2c2c")

style = ttk.Style(root)
style.theme_use("clam")

# Entrada de links
tk.Label(root, text="Cole os links (um por linha):", fg="white", bg="#2c2c2c").pack(pady=5)
entry = tk.Text(root, height=6, width=70, bg="#1e1e1e", fg="white", insertbackground="white")
entry.pack()

# Botões
frame = tk.Frame(root, bg="#2c2c2c")
frame.pack(pady=5)

btn_pasta = tk.Button(frame, text="📂 Escolher Pasta", command=escolher_pasta)
btn_pasta.grid(row=0, column=0, padx=5)

btn_abrir = tk.Button(frame, text="📁 Abrir Pasta", command=abrir_pasta)
btn_abrir.grid(row=0, column=1, padx=5)

qualidade_var = tk.StringVar()
qualidade_var.set("Automática")
opcoes = ["Automática", "720p", "1080p", "Áudio"]
drop = ttk.OptionMenu(frame, qualidade_var, *opcoes)
drop.grid(row=0, column=2, padx=5)

btn = tk.Button(frame, text="⬇ Baixar Vídeo(s)", command=baixar)
btn.grid(row=0, column=3, padx=5)

# Status
status_pasta = tk.Label(root, text="Pasta: (nenhuma selecionada)", fg="gray", bg="#2c2c2c")
status_pasta.pack()

status_label = tk.Label(root, text="", fg="white", bg="#2c2c2c")
status_label.pack(pady=5)

# Ações iniciais


root.mainloop()
