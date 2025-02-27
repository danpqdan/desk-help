import platform
import locale
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from services.ClienteTreeview import ClienteTreeview
from services.router_path import help_desk_market as market

def create_widgets_cliente(self):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    
    self.master.title("Help-desk - Cadastro de Clientes")
    larguraTela = self.winfo_screenwidth()
    alturaTela = self.winfo_screenheight()
    self.bg_label = tk.Label(self, bg="#D8EAF7")
    self.bg_label.pack(fill=tk.BOTH, expand=True)
    
    red_larguraTela = larguraTela // 2
    red_alturaTela = alturaTela // 2
    image = Image.open(market)
    image = image.resize((red_larguraTela, red_alturaTela), Image.LANCZOS)
    image = image.convert("RGBA")
    self.tk_image = ImageTk.PhotoImage(image)
    canvas = tk.Canvas(self, bg="#D8EAF7", width=red_larguraTela, height=red_alturaTela, highlightthickness=0)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    
    self.form = tk.Frame(self, bg="#D8EAF7", width=larguraTela/2, height=alturaTela)
    self.form.place(relx=1.0, rely=0.7, anchor='e')

    limite_campo = self.master.register(self.limitar_tamanho)

    lblcpf = tk.Label(self.form, text="CPF:", bg="#D8EAF7", fg="black", font=('Calibri', 12), anchor='w')
    lblcpf.place(x=50, y=20, width=90)
    self.txtcpf = tk.Entry(self.form, validate='key', font=('Calibri', 12), validatecommand=(limite_campo, '%P', 13))
    self.txtcpf.place(x=150, y=20, width=120)
    buscabtn = tk.Button(self.form, text="Pesquisar", bg='#D8EAF7', foreground='black', font=('Calibri', 12), command=self.buscar)
    buscabtn.place(x=290, y=20, width=80, height=25)

    lblnome = tk.Label(self.form, text="Nome:", bg="#D8EAF7", fg="black", font=('Calibri', 12), anchor='w')
    lblnome.place(x=50, y=60, width=90)
    self.txtnome = tk.Entry(self.form, validate='key', font=('Calibri', 12))
    self.txtnome.place(x=150, y=60, width=120, height=25)

    lbltelefone = tk.Label(self.form, text="Telefone:", bg="#D8EAF7", fg="black", font=('Calibri', 12), anchor='w')
    lbltelefone.place(x=50, y=100, width=90)
    self.txttelefone = tk.Entry(self.form, validate='key', font=('Calibri', 12))
    self.txttelefone.place(x=150, y=100, width=400)

    lblemail = tk.Label(self.form, text="Email:", bg="#D8EAF7", fg="black", font=('Calibri', 12), anchor='w')
    lblemail.place(x=50, y=140, width=90)
    self.txtemail = tk.Entry(self.form, validate='key', font=('Calibri', 12))
    self.txtemail.place(x=150, y=140, width=400)

    btngravar = tk.Button(self.form, text="Gravar", bg='#D8EAF7', foreground='black', font=('Calibri', 12), command=self.gravar)
    btngravar.place(x=150, y=180, width=65)

    btnexcluir = tk.Button(self.form, text="Excluir", bg='#D8EAF7', foreground='black', font=('Calibri', 12), command=self.excluir)
    btnexcluir.place(x=230, y=180, width=65)

    btnlimpar = tk.Button(self.form, text="Limpar", bg='#D8EAF7', foreground='black', font=('Calibri', 12), command=self.limpar)
    btnlimpar.place(x=310, y=180, width=65)

    btnmenu = tk.Button(self.form, text="Menu", bg='#D8EAF7', foreground='black', font=('Calibri', 12), command=self.menu)
    btnmenu.place(x=390, y=180, width=65)

    self.text_fields = [self.txtcpf, self.txtnome, self.txttelefone, self.txtemail]
    self.tree = ClienteTreeview(self)
    self.tree.tree.bind("<Double-1>", lambda event: self.atualizar_filds(self.text_fields, self.tree.duplo_click(event)))

    self.txtcpf.focus_set()
