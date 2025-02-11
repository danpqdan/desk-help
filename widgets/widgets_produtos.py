import platform
import locale
import tkinter as tk
from tkinter import ttk
from services.ProdutoTreeview import ProdutoTreeview

def create_widgets_produto(self):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    self.larguraTela = self.master.winfo_screenwidth()
    self.alturaTela = self.master.winfo_screenheight()
    self.master.geometry(f'{self.larguraTela}x{self.alturaTela}+0+0')
    
    self.master.title("Help-desk - Cadastro de Produtos/Serviços")
    
    self.bg_label = tk.Label(self, bg="#D8EAF7")
    self.bg_label.pack(fill=tk.BOTH, expand=True)
    
    self.form = tk.Frame(self, bg="#D8EAF7", width=self.larguraTela/2, height=self.alturaTela)
    self.form.place(relx=1.0, rely=0.7, anchor='e')

    limite_campo = self.master.register(self.limitar_tamanho)

    lblcodigo = tk.Label(self.form, text="Codigo:", bg="#D8EAF7", fg="black", font=('Calibri', 12), anchor='w')
    lblcodigo.place(x=50, y=20, width=90)
    self.txtcodigo = tk.Entry(self.form, validate='key', font=('Calibri', 12), validatecommand=(limite_campo, '%P', 13))
    self.txtcodigo.place(x=150, y=20, width=120)

    buscabtn = tk.Button(self.form, text="Pesquisar", bg='#D8EAF7', foreground='black', font=('Calibri', 12), command=self.buscar)
    buscabtn.place(x=290, y=20, width=80, height=25)

    lbltipo = tk.Label(self.form, text="Tipo:", bg="#D8EAF7", fg="black", font=('Calibri', 12), anchor='w')
    lbltipo.place(x=50, y=60, width=90)
    
    tipos = ["PRODUTO", "SERVICO", "OUTROS"]
    self.cmbtipo = ttk.Combobox(self.form, values=tipos, font=('Calibri', 12))
    self.cmbtipo.place(x=150, y=60, width=120, height=25)

    lbldescricao = tk.Label(self.form, text="Descrição:", bg="#D8EAF7", fg="black", font=('Calibri', 12), anchor='w')
    lbldescricao.place(x=50, y=100, width=90)
    self.txtdescricao = tk.Entry(self.form, font=('Calibri', 12), validate='key', validatecommand=(limite_campo, '%P', 60))
    self.txtdescricao.place(x=150, y=100, width=400)

    lblvalor = tk.Label(self.form, text="Preço:", bg="#D8EAF7", fg="black", font=('Calibri', 12), anchor='w')
    lblvalor.place(x=50, y=140, width=90)
    self.txtvalor = tk.Entry(self.form, font=('Calibri', 12), validate='key', validatecommand=(limite_campo, '%P', 13))
    self.txtvalor.place(x=150, y=140, width=90)

    btngravar = tk.Button(self.form, text="Gravar", bg='#D8EAF7', foreground='black', font=('Calibri', 12), command=self.gravar)
    btngravar.place(x=150, y=180, width=65)

    btnexcluir = tk.Button(self.form, text="Excluir", bg='#D8EAF7', foreground='black', font=('Calibri', 12), command=self.excluir)
    btnexcluir.place(x=230, y=180, width=65)

    btnlimpar = tk.Button(self.form, text="Limpar", bg='#D8EAF7', foreground='black', font=('Calibri', 12), command=self.limpar)
    btnlimpar.place(x=310, y=180, width=65)

    btnmenu = tk.Button(self.form, text="Menu", bg='#D8EAF7', foreground='black', font=('Calibri', 12), command=self.menu)
    btnmenu.place(x=390, y=180, width=65)

    self.text_fields = [self.txtcodigo, self.txtdescricao, self.cmbtipo, self.txtvalor]
    self.tree = ProdutoTreeview(self)
    self.tree.tree.bind("<Double-1>", lambda event: self.atualizar_filds(self.text_fields, self.tree.duplo_click(event)))

    self.txtcodigo.focus_set()
