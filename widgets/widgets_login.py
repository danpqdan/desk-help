import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from services.router_path import help_desk_icon as icon

def create_widgets_login(self):
    
    self.bg_label = tk.Label(self, bg="#D8EAF7")
    self.bg_label.pack(fill=tk.BOTH)
    
    image = Image.open(icon)
    image = image.resize((300,200), Image.LANCZOS)
    image = image.convert("RGBA")
    self.tk_image = ImageTk.PhotoImage(image)
    canvas = tk.Canvas(self, width=image.width, height=image.height, bg="#D8EAF7", border=None, bd=None, confine=None, highlightthickness=0 )
    canvas.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
    canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)



    self.form = tk.Frame(self, bg="#D8EAF7", width=400, height=250)
    self.form.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    lblusuario = tk.Label(self.form, text="Usuario:", bg="#D8EAF7", font=('Calibri', 12, 'bold'))
    lblusuario.place(x=20, y=20)
    self.txtusuario = tk.Entry(self.form, font=('Calibri', 12), width=30)
    self.txtusuario.place(x=100, y=20)

    # Campos de senha
    lblsenha = tk.Label(self.form, text="Senha:", bg="#D8EAF7", font=('Calibri', 12, 'bold'))
    lblsenha.place(x=20, y=60)
    self.txtsenha = tk.Entry(self.form, font=('Calibri', 12), width=30, show="*")
    self.txtsenha.place(x=100, y=60)

    # Botão para mostrar a senha
    btnmostrar = tk.Button(self.form, text="Mostrar Senha", bg='#D8EAF7', fg='black', font=('Calibri', 12, 'bold'), command=self.mostrarsenha)
    btnmostrar.place(x=210, y=100)

    # Botão de login
    btnsubmeter = tk.Button(self.form, text="Login", bg='#D8EAF7', fg='black', font=('Calibri', 12, 'bold'), command=self.validasenha)
    btnsubmeter.place(x=50, y=100)
    btnsubmeter.bind('<Return>', self.validasenha)

    # Botão de sair
    btnsair = tk.Button(self.form, text="Sair", bg='#D8EAF7', fg='black', font=('Calibri', 12, 'bold'), command=self.sair)
    btnsair.place(x=135, y=100)

    self.txtsenha.bind('<Return>', lambda event: self.validasenha())
    self.txtusuario.focus_set()
