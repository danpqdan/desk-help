import tkinter as tk
from tkinter import ttk
from sqlalchemy import text
from tkcalendar import DateEntry
import locale
from services.VendaTreeview import VendaSacolaTreeview
from services.conexao import Database

def create_widgets_faturamento(self):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    larguraTela = self.master.winfo_screenwidth()
    alturaTela = self.master.winfo_screenheight()
    self.master.title("Help-desk - Faturamento")
    
    largura_personalizada = larguraTela / 3
    altura_personalizada = alturaTela / 3
    largura_aside = larguraTela - largura_personalizada

    self.container_filtros = tk.Frame(self, bg="#D8EAF7", width=largura_personalizada, height=alturaTela, bd=2, relief="solid")
    self.container_filtros.pack(side="right", fill="y") 
    
    self.container_dados = tk.Frame(self, bg="#D8EAF7", width=largura_aside, height=altura_personalizada)
    self.container_dados.pack(side="top", fill="x")
    
    self.container_vis = tk.Frame(self, bg="#FFFFFF", width=largura_aside, height=alturaTela)
    self.container_vis.pack(side="bottom", fill="both", expand=True)
    
    # Dados
    lblinformativo = tk.Label(self.container_dados, text="Dados informativos:", font=('Calibri', 16, 'bold'), bg='#D8EAF7', fg='black', anchor='w')
    lblinformativo.place(relx=0.5, rely=0.1, anchor='center', width=200, height=20)
    
    lbldatainicial = tk.Label(self.container_dados, text="Data inical:", font=('Calibri', 12, 'bold'), bg='#D8EAF7', fg='black', anchor='w')
    lbldatainicial.place(relx=0.05, rely=0.3, width=100, height=20)
    
    self.datainicial = tk.Entry(self.container_dados, font=('Calibri', 12), width=12, background='white')
    self.datainicial.place(relx=0.15, rely=0.3, width=120, height=20)
    
    lbldatafinal = tk.Label(self.container_dados, text="Data final:", font=('Calibri', 12, 'bold'), bg='#D8EAF7', fg='black', anchor='w')
    lbldatafinal.place(relx=0.45, rely=0.3, width=100, height=20)
    
    self.datafinal = tk.Entry(self.container_dados, font=('Calibri', 12), width=12, background='white')
    self.datafinal.place(relx=0.55, rely=0.3, width=120, height=20)
    
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
    
    self.boxtodosvendedores = ttk.Checkbutton(self.container_filtros, text="Todos os vendedores")
    self.boxtodosvendedores.place(relx=0.65, rely=0.2, width=140, height=20)
    
    lblcliente = tk.Label(self.container_filtros, text='Por cliente', font=('Calibri', 12, 'bold'), bg='#D8EAF7', fg='black', anchor='w')
    lblcliente.place(relx=0.05, rely=0.25, width=100, height=20)
    
    self.cliente = ttk.Combobox(self.container_filtros, values=obter_clientes, state="readonly")
    self.cliente.place(relx=0.35, rely=0.25, width=120, height=20)
    
    self.boxtodoscliente = ttk.Checkbutton(self.container_filtros, text="Todos clientes")
    self.boxtodoscliente.place(relx=0.65, rely=0.25, width=140, height=20)
    
    
    self.btnlimpar = tk.Button(self.container_filtros, text="LIMPAR", bg='#D8EAF7', border=1, relief="solid")
    self.btnlimpar.place(relx=0.5, rely=0.45, anchor="center", width=largura_personalizada - 25)
    self.btnlimpar.lift()

    self.btnfiltrar = tk.Button(self.container_filtros, text="FILTRAR", bg='#D8EAF7', border=1, relief="solid")
    self.btnfiltrar.place(relx=0.5, rely=0.50, anchor="center", width=largura_personalizada - 25)

    self.btnrelatorio = tk.Button(self.container_filtros, text="RELATORIO", bg='#D8EAF7', border=1, relief="solid")
    self.btnrelatorio.place(relx=0.5, rely=0.55, anchor="center", width=largura_personalizada - 25)

    
    # Arvore
    style = ttk.Style()
    style.configure("mystyle.Treeview", font=("Calibri", 10))
    style.configure("mystyle.Treeview.Heading", font=("Calibri", 12, "bold"))

    tree = ttk.Treeview(
        self.container_vis,
        column=("#1", "#2", "#3", "#4", "#5", "#6"),
        show='headings',
        style="mystyle.Treeview",
        padding=0
        )
    tree.column("#1", width=50, anchor='c')
    tree.heading("#1", text="id")
    
    tree.column("#2", width=100, anchor='c')
    tree.heading("#2", text="vendedor_usuario")
    
    tree.column("#3", width=200, anchor='w')
    tree.heading("#3", text="cliente_cpf")
    
    tree.column("#4", width=50, anchor='c')
    tree.heading("#4", text="Qts produtos")
    
    tree.column("#5", width=100, anchor='c')
    tree.heading("#5", text="total")
    
    tree.column("#6", width=150, anchor='c')
    tree.heading("#6", text="time_stamp")
    
    scrollbar = ttk.Scrollbar(self.container_vis, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)
    
    
    obter_clientes(self)
    obter_vendedores(self)
    


def obter_vendedores(self):
        """Recupera os vendedores do banco de dados"""
        try:
            con = Database()
            vendedores = con.encontrar_varios(text("SELECT usuario FROM vendedores"))
            self.vendedores = [vendedor[0] for vendedor in vendedores]
            
            self.cmbvendedor['values'] = self.vendedores

        except Exception as e:
            print(f"Erro ao obter vendedores: {e}")
            self.vendedores = []
            
            
def obter_clientes(self):
    """Recupera os clientes do banco de dados"""
    try:
        con = Database()
        clientes = con.encontrar_varios(text("SELECT nome FROM clientes"))
        self.clientes = [cliente[0] for cliente in clientes]
        
        # Atualiza o Combobox de clientes
        self.cliente['values'] = self.clientes

    except Exception as e:
        print(f"Erro ao obter clientes: {e}")
        self.clientes = []
    
    
    # btnbusprod = tk.Button(self.container_filtros, text="Buscar produto", bg='#000', foreground='white', font=('Calibri', 12, 'bold'), command=self.abrir_popup_busca_prodserv)
    # btnbusprod.place(relx=0.6, rely=0.1, width=120, height=20)
    
    
    # self.txtcodprod = tk.Entry(self.produtos)
    # self.txtcodprod.place(relx=0.3, rely=0.1, width=100, height=20)
    # self.txtcodprod.bind('<Return>', self.bus_prod)

    # lbldescricao = tk.Label(self.produtos, text="Descrição:", font=('Calibri', 12, 'bold'), bg='#D8EAF7', fg='black', anchor='w')
    # lbldescricao.place(relx=0.1, rely=0.2, width=100, height=20)

    # self.txtdescricao = tk.Entry(self.produtos)
    # self.txtdescricao.place(relx=0.3, rely=0.2, width=300, height=20)

    # lblqtde = tk.Label(self.produtos, text="Quantidade:", font=('Calibri', 12, 'bold'), bg='#D8EAF7', fg='black', anchor='w')
    # lblqtde.place(relx=0.1, rely=0.3, width=100, height=20)

    # self.txtqtde = tk.Entry(self.produtos)
    # self.txtqtde.place(relx=0.3, rely=0.3, width=100, height=20)
    # self.txtqtde.bind('<FocusOut>', self.entrar_qtde)
    # self.txtqtde.bind('<Return>', self.entrar_qtde)



