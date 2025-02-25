import platform
import locale
import tkinter as tk
from tkinter import ttk
from services.ProdutoTreeview import ProdutoTreeview
from PIL import Image, ImageTk


def create_widgets_produto(self):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    self.larguraTela = self.master.winfo_screenwidth()
    self.alturaTela = self.master.winfo_screenheight()
    self.master.geometry(f'{self.larguraTela}x{self.alturaTela}+0+0')
    self.master.title("Help-desk - Cadastro de Produtos/Serviços")
    limite_campo = self.master.register(self.limitar_tamanho)
    
    
    
    self.bg_label = tk.Label(self, bg="#D8EAF7")
    self.bg_label.pack(fill=tk.BOTH, expand=True)
    
    red_larguraTela = self.larguraTela // 2
    red_alturaTela = self.alturaTela // 2
    
    image_path = "assets/help_desk_market.png"
    image = Image.open(image_path)
    image = image.resize((red_larguraTela, red_alturaTela), Image.LANCZOS)
    image = image.convert("RGBA")
    self.tk_image = ImageTk.PhotoImage(image)
    canvas = tk.Canvas(self, bg="#D8EAF7", width=red_larguraTela, height=red_alturaTela, highlightthickness=0)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    self.form = tk.Frame(self, bg="#D8EAF7", width=self.larguraTela/2, height=self.alturaTela)
    self.form.place(relx=1.0, rely=0, anchor='ne')

    lblcodigo = tk.Label(self.form, text="Codigo:", bg="#D8EAF7", fg="black", font=('Calibri', 12), anchor='w')
    lblcodigo.place(relx=0.05, rely=0.02, width=90)
    self.txtcodigo = tk.Entry(self.form, validate='key', font=('Calibri', 12), validatecommand=(limite_campo, '%P', 13))
    self.txtcodigo.place(relx=0.22, rely=0.02, width=120)

    buscabtn = tk.Button(self.form, text="Pesquisar", bg='#D8EAF7', foreground='black', font=('Calibri', 12), command=self.buscar)
    buscabtn.place(relx=0.42, rely=0.02, width=80, height=28)

    tipos = ["PRODUTO", "SERVICO"]
    lbltipo = tk.Label(self.form, text="Tipo:", bg="#D8EAF7", fg="black", font=('Calibri', 12), anchor='w')
    lbltipo.place(relx=0.05, rely=0.08, width=90)
    self.cmbtipo = ttk.Combobox(self.form, values=tipos, font=('Calibri', 12))
    self.cmbtipo.place(relx=0.22, rely=0.08, width=120, height=25)


    self.txtdescricao_var = tk.StringVar()
    self.txtdescricao_var.trace_add("write", lambda *args: self.txtdescricao_var.set(self.txtdescricao_var.get().upper()))
    lbldescricao = tk.Label(self.form, text="Descrição:", bg="#D8EAF7", fg="black", font=('Calibri', 12), anchor='w')
    lbldescricao.place(relx=0.05, rely=0.14, width=90)
    self.txtdescricao = tk.Entry(self.form, font=('Calibri', 12),textvariable=self.txtdescricao_var, validate='key', validatecommand=(limite_campo, '%P', 60))
    self.txtdescricao.place(relx=0.22, rely=0.14, width=400)
    
    self.custo_var = tk.StringVar()
    self.custo_var.trace_add('write', lambda name, index, mode: formatar_campo(self.custo_var, "float"))
    lblcusto = tk.Label(self.form, text="Custo:", bg="#D8EAF7", fg="black", font=('Calibri', 12), anchor='w')
    lblcusto.place(relx=0.05, rely=0.20, width=90)
    self.txtcusto = tk.Entry(self.form, font=('Calibri', 12), textvariable=self.custo_var)
    self.txtcusto.place(relx=0.22, rely=0.20, width=90)
    self.txtcusto.bind("<KeyRelease>", lambda event: self.calcular())

    self.porcentagem_var = tk.StringVar()
    self.porcentagem_var.trace_add('write', lambda name, index, mode: formatar_campo(self.porcentagem_var, "float"))
    lblporcentagem = tk.Label(self.form, text="Porcentagem:", bg="#D8EAF7", fg="black", font=('Calibri', 12), anchor='w')
    lblporcentagem.place(relx=0.39, rely=0.20, width=90)
    self.txtporcentagem = tk.Entry(self.form, font=('Calibri', 12), textvariable=self.porcentagem_var)
    self.txtporcentagem.place(relx=0.56, rely=0.20, width=90)
    self.txtporcentagem.bind("<KeyRelease>", lambda event: self.calcular())

    self.valor_var = tk.StringVar()
    self.valor_var.trace_add('write', lambda name, index, mode: formatar_campo(self.valor_var, "float"))
    lblvalor = tk.Label(self.form, text="Preço:", bg="#D8EAF7", fg="black", font=('Calibri', 12), anchor='w')
    lblvalor.place(relx=0.05, rely=0.26, width=90)
    self.txtvalor = tk.Entry(self.form, font=('Calibri', 12), textvariable=self.valor_var)
    self.txtvalor.place(relx=0.22, rely=0.26, width=90)
    self.txtvalor.bind("<KeyRelease>", lambda event: self.calcular())
    
    lblquantidade = tk.Label(self.form, text="Quantidade:", bg="#D8EAF7", fg="black", font=('Calibri', 12), anchor='w')
    lblquantidade.place(relx=0.05, rely=0.32, width=90)
    self.txtquantidade = tk.Entry(self.form, font=('Calibri', 12))
    self.txtquantidade.place(relx=0.22, rely=0.32, width=90)

    btngravar = tk.Button(self.form, text="Gravar", bg='#D8EAF7', foreground='black', font=('Calibri', 12), command=self.gravar)
    btngravar.place(relx=0.25, rely=0.4, width=65)

    btnexcluir = tk.Button(self.form, text="Excluir", bg='#D8EAF7', foreground='black', font=('Calibri', 12), command=self.excluir)
    btnexcluir.place(relx=0.40, rely=0.4, width=65)

    btnlimpar = tk.Button(self.form, text="Limpar", bg='#D8EAF7', foreground='black', font=('Calibri', 12), command=self.limpar)
    btnlimpar.place(relx=0.55, rely=0.4, width=65)

    btnmenu = tk.Button(self.form, text="Menu", bg='#D8EAF7', foreground='black', font=('Calibri', 12), command=self.menu)
    btnmenu.place(relx=0.70, rely=0.4, width=65)

    self.txtcodigo.focus_set()

def validar_e_converter(self,texto):
    """Converte o texto para maiúsculas e aplica limite de caracteres."""
    self.set(texto.upper())
    return True


def formatar_campo(var, tipo=None):
    """ Formata o valor do campo para números float ou inteiros corretamente. """
    valor = var.get()
    if not valor:
        return
    if tipo == "float":
        valor = valor.strip().replace(',', '.')
        try:
            valor = float(valor)
            var.set(f"{valor:.2f}")
        except ValueError:
            var.set("")
    elif tipo == "int":
        if valor.isdigit():
            var.strip().set(int(valor))
        else:
            var.set("")