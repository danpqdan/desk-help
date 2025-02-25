import tkinter as tk
import locale
from services.VendaTreeview import VendaSacolaTreeview

def create_widgets_vendas(self):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    larguraTela = self.master.winfo_screenwidth()
    alturaTela = self.master.winfo_screenheight()
    self.master.title("Help-desk - Vendas")
    
    # Widgets de cabeçalho
    
    self.cabecalho = tk.Frame(self, bg="#D8EAF7", width=larguraTela/2, height=alturaTela/3)
    self.cabecalho.place(relx=0.25, rely=0.15, anchor='n')

    lblnumvenda = tk.Label(self.cabecalho, text="Sacola ID:", font=('Calibri', 12, 'bold'), bg='#D8EAF7', fg='black', anchor='w')
    lblnumvenda.place(relx=0.1, rely=0.02, width=100)
    self.txtsacolaid = tk.Entry(self.cabecalho, justify='center', font=('Calibri', 12, 'bold'))
    self.txtsacolaid.place(relx=0.3, rely=0.02, width=100, height=25)
    
    lblcodcli = tk.Label(self.cabecalho, text="Cod. Cliente:", font=('Calibri', 12, 'bold'), bg='#D8EAF7', fg='black', anchor='w')
    lblcodcli.place(relx=0.1, rely=0.16, width=100)
    self.txtclicpf = tk.Entry(self.cabecalho)
    self.txtclicpf.place(relx=0.3, rely=0.16, width=100, height=25)
    self.txtclicpf.bind('<Return>', self.bus_cli)

    lblnomecli = tk.Label(self.cabecalho, text="Nome Cliente:", font=('Calibri', 12, 'bold'), bg='#D8EAF7', fg='black', anchor='w')
    lblnomecli.place(relx=0.1, rely=0.30, width=100)
    self.txtnomecli = tk.Entry(self.cabecalho)
    self.txtnomecli.place(relx=0.3, rely=0.30, width=300)
    self.txtnomecli.config(state="disabled")
    
    lblvendedor = tk.Label(self.cabecalho, text="Vendedor: ", font=('Calibri', 12, 'bold'), bg='#D8EAF7', fg='black', anchor='w')
    lblvendedor.place(relx=0.1, rely=0.44, width=100)
    self.txtvendedor = tk.Entry(self.cabecalho)
    self.txtvendedor.place(relx=0.3, rely=0.44, width=300)
    
    btnbuscli = tk.Button(self.cabecalho, text="Buscar cliente", bg='black', foreground='white', font=('Calibri', 12, 'bold'), command=self.abrir_popup_busca_cliente)
    btnbuscli.place(relx=0.5, rely=0.6, width=120)
    
    btnbusvendas = tk.Button(self.cabecalho, text="Buscar venda", bg='black', foreground='white', font=('Calibri', 12, 'bold'), command=self.abrir_popup_busca_vendas)
    btnbusvendas.place(relx=0.2, rely=0.6, width=120)

    # Widgets produtos
    
    self.produtos = tk.Frame(self, bg="#D8EAF7", width=larguraTela/2, height=alturaTela/3)
    self.produtos.place(relx=0.75, rely=0.15, anchor='n')

    btnbusprod = tk.Button(self.produtos, text="Buscar produto", bg='#000', foreground='white', font=('Calibri', 12, 'bold'), command=self.abrir_popup_busca_prodserv)
    btnbusprod.place(relx=0.6, rely=0.0, width=120)
    
    lblcodprod = tk.Label(self.produtos, text="Cód. Prod:", font=('Calibri', 12, 'bold'), bg='#D8EAF7', fg='black', anchor='w')
    lblcodprod.place(relx=0.1, rely=0.02, width=100)
    self.txtcodprod = tk.Entry(self.produtos)
    self.txtcodprod.place(relx=0.3, rely=0.02, width=100, height=25)
    self.txtcodprod.bind('<Return>', self.bus_prod)

    lbldescricao = tk.Label(self.produtos, text="Descrição:", font=('Calibri', 12, 'bold'), bg='#D8EAF7', fg='black', anchor='w')
    lbldescricao.place(relx=0.1, rely=0.16, width=100)
    self.txtdescricao = tk.Entry(self.produtos)
    self.txtdescricao.place(relx=0.3, rely=0.16, width=300, height=25)

    lblqtde = tk.Label(self.produtos, text="Quantidade:", font=('Calibri', 12, 'bold'), bg='#D8EAF7', fg='black', anchor='w')
    lblqtde.place(relx=0.1, rely=0.30, width=100)
    self.txtqtde = tk.Entry(self.produtos)
    self.txtqtde.place(relx=0.3, rely=0.30, width=100)
    self.txtqtde.bind('<FocusOut>', self.entrar_qtde)
    self.txtqtde.bind('<Return>', self.entrar_qtde)

    self.btnincluir = tk.Button(self.produtos, text="Incluir - F1", bg='#D8EAF7', foreground='black', font=('Calibri', 12, 'bold'), command=self.gravar_lin)
    self.btnincluir.place(relx=0.3, rely=0.6, width=100)
    self.master.bind('<F1>', self.finalizar_linha)
    self.btnincluir.bind('<Button-1>', self.finalizar_linha)
    self.btnincluir.bind('<Return>', self.finalizar_linha)

    self.lblvlrunit = tk.Label(self.produtos, text="Valor Unit:", font=('Calibri', 12, 'bold'), bg='#D8EAF7', fg='black', anchor='w')
    self.lblvlrunit.place(relx=0.5, rely=0.3, width=100)
    self.txtvlrunit = tk.Entry(self.produtos)
    self.txtvlrunit.place(relx=0.7, rely=0.3, width=100)

    lblvalor = tk.Label(self.produtos, text="Valor:", font=('Calibri', 12, 'bold'), bg='#D8EAF7', fg='black', anchor='w')
    lblvalor.place(relx=0.1, rely=0.44, width=100)
    self.txtvalor = tk.Entry(self.produtos)
    self.txtvalor.place(relx=0.3, rely=0.44, width=100)
    self.txtvalor.config(state="disabled")

    lbltotal = tk.Label(self, text="Total ->", font=('Calibri', 16, 'bold'), bg='lightskyblue', fg="black", anchor='c')
    lbltotal.place(x=548, y=520, width=100)

    self.txt_total = tk.Entry(self, justify='center', bg="silver", fg="blue", font=('Calibri', 16, 'bold'))
    self.txt_total.place(relx=0.9, rely=0.6, width=150)
    self.txt_total.config(state="readonly")

    btnlimpar = tk.Button(self.produtos, text="Limpar - F2", bg='#000', foreground='white', font=('Calibri', 12, 'bold'), command=self.limpar)
    btnlimpar.place(relx=0.5, rely=0.42, width=100)
    btnlimpar.bind('<Button-1>', self.limpar)
    self.master.bind('<F2>', self.limpar)

    btnexcluir = tk.Button(self.produtos, text="Excluir", bg='#D8EAF7', foreground='black', font=('Calibri', 12, 'bold'), command=self.excluir)
    btnexcluir.place(relx=0.6, rely=0.6, width=100)

    self.btngravar = tk.Button(self, text="Gravar", bg='#00FFFF', foreground='black', font=('Calibri', 12, 'bold'), command=self.gravar)
    self.btngravar.place(relx=0.30, rely=0.55, width=100, height=50)

    self.btnimprimir = tk.Button(self, text="Imprimir", bg='#00FFFF', foreground='black', font=('Calibri', 12, 'bold'), command=self.hook_imprimir)
    self.btnimprimir.place(relx=0.40, rely=0.55, width=100, height=50)

    self.btncancelar = tk.Button(self, text="Cancelar", bg='#B22222', foreground='black', font=('Calibri', 12, 'bold'), command=self.cancelar)
    self.btncancelar.place(relx=0.50, rely=0.55, width=100, height=50)

    self.btnmenu = tk.Button(self, text="Menu", bg='#00FFFF', foreground='black', font=('Calibri', 12, 'bold'), command=self.menu)
    self.btnmenu.place(relx=0.60, rely=0.55, width=100, height=50)

   
