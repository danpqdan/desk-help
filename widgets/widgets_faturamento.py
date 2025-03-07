import tkinter as tk
from tkinter import ttk
from sqlalchemy import text
from tkcalendar import DateEntry
import locale
from model.Cliente import Cliente
from model.Vendedor import Vendedor
from services.FaturamentoTreeview import FaturamentoTreeview
from services.conexao import Database
from PIL import Image, ImageTk
from services.router_path import help_desk_data as data


def create_widgets_faturamento(self):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    larguraTela = self.master.winfo_screenwidth()
    alturaTela = self.master.winfo_screenheight()
    self.master.title("Help-desk - Faturamento")
    
    largura_personalizada = larguraTela / 3
    altura_personalizada = alturaTela / 3
    largura_aside = larguraTela - largura_personalizada
    
    red_larguraTela = int(largura_personalizada)
    red_alturaTela =  int(altura_personalizada)

    self.container_filtros = tk.Frame(self, bg="#D8EAF7", width=largura_personalizada, height=alturaTela, bd=2, relief="solid")
    self.container_filtros.pack(side="right", fill="y") 
    
    self.container_dados = tk.Frame(self, bg="#D8EAF7", width=largura_aside, height=altura_personalizada)
    self.container_dados.pack(side="top", fill="x")
    
    # Dados
    lblinformativo = tk.Label(self.container_dados, text="Dados informativos:", font=('Calibri', 16, 'bold'), bg='#D8EAF7', fg='black', anchor='w')
    lblinformativo.place(relx=0.5, rely=0.1, anchor='center', width=200, height=20)
    
    lbldatainicial = tk.Label(self.container_dados, text="Data inical:", font=('Calibri', 12, 'bold'), bg='#D8EAF7', fg='black', anchor='w')
    lbldatainicial.place(relx=0.05, rely=0.3, width=100, height=20)
    
    self.txtdatainicial = tk.Entry(self.container_dados, font=('Calibri', 12), width=12, background='white')
    self.txtdatainicial.place(relx=0.15, rely=0.3, width=120, height=20)
    
    lbldatafinal = tk.Label(self.container_dados, text="Data final:", font=('Calibri', 12, 'bold'), bg='#D8EAF7', fg='black', anchor='w')
    lbldatafinal.place(relx=0.45, rely=0.3, width=100, height=20)
    
    self.txtdatafinal = tk.Entry(self.container_dados, font=('Calibri', 12), width=12, background='white')
    self.txtdatafinal.place(relx=0.55, rely=0.3, width=120, height=20)
    
    lblvalortotal = tk.Label(self.container_dados, text="Valor total:", font=('Calibri', 12, 'bold'), bg='#D8EAF7', fg='black', anchor='w')
    lblvalortotal.place(relx=0.05, rely=0.5, width=100, height=20)
    
    self.txtvalortotal = tk.Entry(self.container_dados,  font=('Calibri', 12), width=12, background='white', foreground='white')
    self.txtvalortotal.place(relx=0.15, rely=0.5, width=100, height=20)
    
    lblticketmedio = tk.Label(self.container_dados, text="Ticket médio: ", font=('Calibri', 12, 'bold'), bg='#D8EAF7', fg='black', anchor='w')
    lblticketmedio.place(relx=0.45, rely=0.5, width=100, height=20)
    
    self.txtticket = tk.Entry(self.container_dados,  font=('Calibri', 12), width=12, background='white', foreground='white')
    self.txtticket.place(relx=0.60, rely=0.5, width=100, height=20)
    
    # Filtros
    lblinformativo = tk.Label(self.container_filtros, text="Filtros:", font=('Calibri', 16, 'bold'), bg='#D8EAF7', fg='black', anchor='w')
    lblinformativo.place(relx=0.5, rely=0.05, anchor='center', width=200, height=20)
    
    image = Image.open(data)
    image = image.resize((red_larguraTela, red_alturaTela), Image.LANCZOS)
    self.tk_image = ImageTk.PhotoImage(image)
    canvas = tk.Canvas(self.container_filtros, bg="black", width=red_larguraTela, height=red_alturaTela, highlightthickness=0)
    canvas.place(relx=0.5, rely=1.0, anchor=tk.S)
    canvas.create_image(red_larguraTela // 2, red_alturaTela // 2, anchor=tk.CENTER, image=self.tk_image)

    lbldatainicial = tk.Label(self.container_filtros, text="Data inical:", font=('Calibri', 12, 'bold'), bg='#D8EAF7', fg='black', anchor='w')
    lbldatainicial.place(relx=0.05, rely=0.1, width=100, height=20)
    
    self.datainicial = DateEntry(self.container_filtros, font=('Calibri', 12), width=12, background='darkblue', foreground='white', borderwidth=2)
    self.datainicial.place(relx=0.35, rely=0.1, width=120, height=20)
    
    lbldatafinal = tk.Label(self.container_filtros, text="Data final:", font=('Calibri', 12, 'bold'), bg='#D8EAF7', fg='black', anchor='w')
    lbldatafinal.place(relx=0.05, rely=0.15, width=100, height=20)
    
    self.datafinal = DateEntry(self.container_filtros, font=('Calibri', 12), width=12, background='darkblue', foreground='white', borderwidth=2)
    self.datafinal.place(relx=0.35, rely=0.15, width=120, height=20)
    
    lblvendedor = tk.Label(self.container_filtros, text="Por vendedor", font=('Calibri', 12, 'bold'), bg='#D8EAF7', fg='black', anchor='w')
    lblvendedor.place(relx=0.05, rely=0.2, width=100, height=20)
    
    self.cmbvendedor = ttk.Combobox(self.container_filtros, values=obter_vendedores, state="readonly")
    self.cmbvendedor.place(relx=0.35, rely=0.2, width=120, height=20)
    
    lblcliente = tk.Label(self.container_filtros, text='Por cliente', font=('Calibri', 12, 'bold'), bg='#D8EAF7', fg='black', anchor='w')
    lblcliente.place(relx=0.05, rely=0.25, width=100, height=20)
    
    self.cliente = ttk.Combobox(self.container_filtros, values=obter_clientes, state="readonly")
    self.cliente.place(relx=0.35, rely=0.25, width=120, height=20)
    
    self.btnlimpar = tk.Button(self.container_filtros, text="LIMPAR", bg='#D8EAF7', border=1, relief="solid")
    self.btnlimpar.place(relx=0.5, rely=0.45, anchor="center", width=largura_personalizada - 25)
    self.btnlimpar.lift()

    self.btnfiltrar = tk.Button(self.container_filtros, text="FILTRAR", bg='#D8EAF7', border=1, relief="solid", command=self.filtrar_dados)
    self.btnfiltrar.place(relx=0.5, rely=0.50, anchor="center", width=largura_personalizada - 25)

    self.btnrelatorio = tk.Button(self.container_filtros, text="RELATORIO", bg='#D8EAF7', border=1, relief="solid", command=self.gerar_relatorio)
    self.btnrelatorio.place(relx=0.5, rely=0.55, anchor="center", width=largura_personalizada - 25)
    
    self.menu = tk.Button(self.container_filtros, text="MENU", bg='#D8EAF7', border=1, relief="solid", command=self.menu)
    self.menu.place(relx=0.5, rely=0.60, anchor="center", width=largura_personalizada - 25)

    
    
    obter_clientes(self)
    obter_vendedores(self)
    


def obter_vendedores(self):
    """Recupera os vendedores do banco de dados"""
    con = Database()
    with con.get_conexao() as session:
        try:
            vendedores = session.query(Vendedor.usuario).all()
            self.vendedores = ['Todos'] + [vendedor[0] for vendedor in vendedores]
            self.cmbvendedor['values'] = self.vendedores

        except Exception as e:
            print(f"Erro ao obter vendedores: {e}")
            self.vendedores = ['Recarregue']
            
            
def obter_clientes(self):
    """Recupera os clientes do banco de dados"""
    con = Database()
    with con.get_conexao() as session:
        try:
            clientes = session.query(Cliente.nome).all()
            self.clientes = ['Todos'] + [cliente[0] for cliente in clientes]
            self.cliente['values'] = self.clientes

        except Exception as e:
            print(f"Erro ao obter clientes: {e}")
            self.clientes = ['Recarregue']