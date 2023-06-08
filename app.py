from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import moviepy.editor as mp
import tkinter.ttk as ttk
import sys
import os
import threading
import time

def resource_path(relative_path):
    """Obtém o caminho absoluto para um arquivo, seja em desenvolvimento ou em execução em um bundle PyInstaller"""
    try:
        # Obtém o caminho do arquivo do código fonte Python
        base_path = sys._MEIPASS
    except Exception:
        # Se não estiver em execução em um bundle PyInstaller, usa o caminho do arquivo do script
        base_path = os.path.abspath(".")

    # Retorna o caminho absoluto para o arquivo
    return os.path.join(base_path, relative_path)

app = Tk()
app.title('MP4 para MP3 | V.0.1 | FREE')
app.iconbitmap(resource_path('icone.ico'))
app.geometry('500x300')
app.resizable(False, False)  # Desabilita o redimensionamento

filename = ""
onlyfilename = ""
output_folder = ""

def pesquisar_mp4():
    global filename, onlyfilename
    filename = filedialog.askopenfilename(initialdir="/", title='Selecionar arquivo', filetypes=[('Arquivos de vídeo', '*.mp4')])
    onlyfilename = os.path.basename(filename)
    fname.delete('1.0', END)
    fname.insert(END, onlyfilename)

def select_output_folder():
    global output_folder
    output_folder = filedialog.askdirectory(title='Selecionar pasta de destino')

def converter_mp3():
    global filename, output_folder
    if filename == "":
        messagebox.showwarning("Erro", "Nenhum arquivo MP4 selecionado!")
    elif output_folder == "":
        messagebox.showwarning("Erro", "Nenhuma pasta de destino selecionada!")
    else:
        try:
            mp4 = mp.VideoFileClip(filename)
            output_filename = os.path.join(output_folder, f"{onlyfilename}.mp3")
            total_duration = mp4.duration

            def conversion_thread():
                for i in range(int(total_duration)):
                    progress.set((i / total_duration) * 100)
                    app.update_idletasks()
                    time.sleep(1)

                mp4.audio.write_audiofile(output_filename)
                messagebox.showinfo("Conversão Concluída", "Convertido com sucesso!")
                clear_screen()

            t = threading.Thread(target=conversion_thread)
            t.start()

        except Exception as e:
            messagebox.showerror("Erro", str(e))

def clear_screen():
    fname.delete('1.0', END)
    progress.set(0)

# Topo
start = Label(text='Conversor de MP4 para MP3', font=('Arial', 12))
start.place(x=150, y=10)


path = 'img_mp4.png'
img1 = ImageTk.PhotoImage(Image.open(path))
pesquisar = Button(app, image=img1, command=pesquisar_mp4, bd=0)
pesquisar.place(x=100, y=55)

path = 'img_div.png'
img2 = ImageTk.PhotoImage(Image.open(path))
converter = Button(app, image=img2, command=converter_mp3, bd=0)
converter.place(x=225, y=55)

path = 'img_mp3.png'
img3 = ImageTk.PhotoImage(Image.open(path))
converter_button = Button(app, image=img3, command=converter_mp3, bd=0)
converter_button.place(x=300, y=55)

output_button = Button(app, text='Pasta de Destino', command=select_output_folder, font=('Arial', 8))
output_button.place(x=206, y=200)

# Meio
start = Label(text='Converta um arquivo por vez', font=('Arial', 8))
start.place(x=180, y=30)

# Créditos
start = Label(text='Reginaldo Guedes | Gráfica Card | 2024', font=('Arial', 7))
start.place(x=160, y=270)

# Barra de progresso
progress = DoubleVar()
progress.set(0)

pb = ttk.Progressbar(app, variable=progress, maximum=100)
pb.place(x=0, y=290, width=500, height=10)

# Campo para exibir o nome do arquivo selecionado
#fname = Text(app, height=1, width=40)
#fname.place(x=90, y=250)

app.mainloop()
