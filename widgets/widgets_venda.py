import tkinter as tk
import locale
from tkinter import ttk

def create_widgets_vendas(self):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    larguraTela = self.master.winfo_screenwidth()
    alturaTela = self.master.winfo_screenheight()
    self.master.geometry(f'{larguraTela}x{alturaTela}+0+0')
    tk.Label(self, bg='#D8EAF7').grid()

    lblnumvenda = tk.Label(self, text="Núm. Venda:", font=('Calibri', 12, 'bold'), bg='lightskyblue', fg='black', anchor='w')
    lblnumvenda.place(x=50, y=25, width=100, height=20)

    self.txtsacolaid = tk.Entry(self, justify='center', font=('Calibri', 12, 'bold'))
    self.txtsacolaid.place(x=160, y=25, width=100, height=20)
    
    # btnbusvendas = tk.Button(self, text="Buscar venda", bg='gold', foreground='black', font=('Calibri', 12, 'bold'), command=self.abrir_popup_busca_vendas)
    # btnbusvendas.place(x=280, y=23, width=120, height=30)

    lblcodcli = tk.Label(self, text="Cod. Cliente:", font=('Calibri', 12, 'bold'), bg='lightskyblue', fg='black', anchor='w')
    lblcodcli.place(x=50, y=60, width=100, height=20)

    self.txtclicpf = tk.Entry(self)
    self.txtclicpf.place(x=160, y=60, width=100, height=20)
    self.txtclicpf.bind('<Return>', self.bus_cli)

    # btnbuscli = tk.Button(self, text="Buscar cliente", bg='gold', foreground='black', font=('Calibri', 12, 'bold'), command=self.abrir_popup_busca_cliente)
    # btnbuscli.place(x=280, y=58, width=120, height=30)

    lblnomecli = tk.Label(self, text="Nome Cliente:", font=('Calibri', 12, 'bold'), bg='lightskyblue', fg='black', anchor='w')
    lblnomecli.place(x=50, y=100, width=100, height=20)

    self.txtnomecli = tk.Entry(self)
    self.txtnomecli.place(x=160, y=100, width=560, height=20)
    self.txtnomecli.config(state="disabled")

    lblcodprod = tk.Label(self, text="Cód. Prod:", font=('Calibri', 10, 'bold'), bg='lightskyblue', fg='black', anchor='w')
    lblcodprod.place(x=50, y=160, width=100, height=20)

    # btnbusprod = tk.Button(self, text="Buscar produto", bg='gold', foreground='black', font=('Calibri', 12, 'bold'), command=self.abrir_popup_busca_prodserv)
    # btnbusprod.place(x=280, y=158, width=120, height=30)

    self.txtcodprod = tk.Entry(self)
    self.txtcodprod.place(x=160, y=160, width=100, height=20)
    self.txtcodprod.bind('<Return>', self.bus_prod)

    lbldescricao = tk.Label(self, text="Descrição:", font=('Calibri', 10, 'bold'), bg='lightskyblue', fg='black', anchor='w')
    lbldescricao.place(x=50, y=200, width=100, height=20)

    self.txtdescricao = tk.Entry(self)
    self.txtdescricao.place(x=160, y=200, width=560, height=20)

    lblqtde = tk.Label(self, text="Quantidade:", font=('Calibri', 10, 'bold'), bg='lightskyblue', fg='black', anchor='w')
    lblqtde.place(x=50, y=240, width=100, height=20)

    self.txtqtde = tk.Entry(self)
    self.txtqtde.place(x=160, y=240, width=100, height=20)
    self.txtqtde.bind('<FocusOut>', self.entrar_qtde)
    self.txtqtde.bind('<Return>', self.entrar_qtde)

    self.btnincluir = tk.Button(self, text="Incluir - F1", bg='gold', foreground='black', font=('Calibri', 12, 'bold'), command=self.gravar_lin)
    self.btnincluir.place(x=160, y=290, width=100, height=30)
    self.master.bind('<F1>', self.finalizar_linha)
    self.btnincluir.bind('<Button-1>', self.finalizar_linha)
    self.btnincluir.bind('<Return>', self.finalizar_linha)

    self.lblvlrunit = tk.Label(self, text="Valor Unit:", font=('Calibri', 10, 'bold'), bg='lightskyblue', fg='black', anchor='w')
    self.lblvlrunit.place(x=280, y=240, width=100, height=20)
    self.lblvlrunit.config(state="disabled")

    self.txtvlrunit = tk.Entry(self)
    self.txtvlrunit.place(x=390, y=240, width=100, height=20)

    lblvalor = tk.Label(self, text="Valor:", font=('Calibri', 10, 'bold'), bg='lightskyblue', fg='black', anchor='w')
    lblvalor.place(x=510, y=240, width=100, height=20)

    self.txtvalor = tk.Entry(self)
    self.txtvalor.place(x=620, y=240, width=100, height=20)
    self.txtvalor.config(state="disabled")

    lbltotal = tk.Label(self, text="Total ->", font=('Calibri', 16, 'bold'), bg='lightskyblue', fg="black", anchor='c')
    lbltotal.place(x=548, y=520, width=100, height=40)

    self.txt_total = tk.Entry(self, justify='center', bg="silver", fg="blue", font=('Calibri', 16, 'bold'))
    self.txt_total.place(x=650, y=520, width=150, height=40)
    self.txt_total.config(state="readonly")

    btnlimpar = tk.Button(self, text="Limpar - F2", bg='gold', foreground='black', font=('Calibri', 12, 'bold'), command=self.limpar)
    btnlimpar.place(x=390, y=290, width=100, height=30)
    btnlimpar.bind('<Button-1>', self.limpar)
    self.master.bind('<F2>', self.limpar)

    btnexcluir = tk.Button(self, text="Excluir", bg='gold', foreground='black', font=('Calibri', 12, 'bold'), command=self.excluir)
    btnexcluir.place(x=620, y=290, width=100, height=30)

    self.btngravar = tk.Button(self, text="Gravar", bg='black', foreground='white', font=('Calibri', 12, 'bold'), command=self.gravar)
    self.btngravar.place(x=160, y=600, width=100, height=50)

    self.btnimprimir = tk.Button(self, text="Imprimir", bg='green', foreground='white', font=('Calibri', 12, 'bold'), command=self.hook_imprimir)
    self.btnimprimir.place(x=280, y=600, width=100, height=50)

    self.btncancelar = tk.Button(self, text="Cancelar", bg='red', foreground='white', font=('Calibri', 12, 'bold'), command=self.cancelar)
    self.btncancelar.place(x=400, y=600, width=100, height=50)

    self.btnmenu = tk.Button(self, text="Menu", bg='yellow', foreground='black', font=('Calibri', 12, 'bold'), command=self.menu)
    self.btnmenu.place(x=520, y=600, width=100, height=50)

    style = ttk.Style()
    style.configure("mystyle.Treeview", font=("Calibri", 10))
    style.configure("mystyle.Treeview.Heading", font=("Calibri", 12, "bold"))

    self.tree = ttk.Treeview(self, column=("c1", "c2", "c3", "c4", "c5", "c6"), show='headings', style="mystyle.Treeview", padding=0)
    self.tree.column("#1", width=50, anchor='c')
    self.tree.heading("#1", text="Linha")
    self.tree.column("#2", width=100, anchor='c')
    self.tree.heading("#2", text="Código")
    self.tree.column("#3", width=200, anchor='w')
    self.tree.heading("#3", text="Descrição")
    self.tree.column("#4", width=150, anchor='c')
    self.tree.heading("#4", text="Quantidade")
    self.tree.column("#5", width=100, anchor='c')
    self.tree.heading("#5", text="Valor Unit")
    self.tree.column("#6", width=150, anchor='c')
    self.tree.heading("#6", text="Valor")
    self.tree.place(x=50, y=350, height=180)

    scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
    self.tree.configure(yscroll=scrollbar.set)
    scrollbar.place(x=801, y=350, height=180)
