import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from sqlalchemy import text
from model.ProdutoServico import ProdutoServico
from services.conexao import Database

class ProdutoTreeview:
    def __init__(self, parent):
        self.parent = parent
        self.selected_data = None
        self.tree = None
        self.parent.update_idletasks()
        self.larguraTela = self.parent.winfo_screenwidth()
        self.alturaTela = self.parent.winfo_screenheight()
        self.db =Database()
        self.criar_treeview_produto()

    def criar_treeview_produto(self):
        self.container = tk.Frame(self.parent, bg='white', width=self.larguraTela, height=self.alturaTela/3)
        self.container.pack(side='bottom', fill='x')


        style = ttk.Style()
        style.configure("mystyle.Treeview", font=("Calibri", 10))
        style.configure("mystyle.Treeview.Heading", font=("Calibri", 12, "bold"))

        self.tree = ttk.Treeview(
            self.container,
            columns=("#1", "#2", "#3", "#4", "#5", "#6", "#7"), 
            show='headings',
            style="mystyle.Treeview"
        )
        self.tree.heading("#1", text="codigo", command=lambda: self.ordenar_coluna("#1", False))
        self.tree.column("#1", width=20, anchor='c')

        self.tree.heading("#2", text="descricao", command=lambda:self.ordenar_coluna("#2", False))
        self.tree.column("#2", width=200, anchor='w')

        self.tree.heading("#3", text="tipo", command=lambda:self.ordenar_coluna("#3", False))
        self.tree.column("#3", width=80, anchor='c')
        
        self.tree.heading("#4", text="valor", command=lambda: self.ordenar_coluna("#4", False))
        self.tree.column("#4", width=100, anchor='center')
        
        self.tree.heading("#5", text="custo", command=lambda: self.ordenar_coluna("#5", False))
        self.tree.column("#5", width=100, anchor='center')

        self.tree.heading("#6", text="porcentagem", command=lambda: self.ordenar_coluna("#6", False))
        self.tree.column("#6", width=100, anchor='center')
        
        self.tree.heading("#7", text="Quantidade", command=lambda: self.ordenar_coluna("#7", False))
        self.tree.column("#7", width=100, anchor='center')

        lbl_pes_nome = tk.Label(
            self.container,
            text="Pesquisar por Nome:",
            font=('Calibri', 12, 'bold'),
            anchor="w"
        )
        lbl_pes_nome.pack(side="top", fill="x", padx=10, pady=5)

        validate_pes_nome = self.parent.register(lambda p: self.pesquisar_nome(p))

        self.txt_pes_nome = tk.Entry(
            self.container,
            width=35,
            font=('Calibri', 12),
            validate='key',
            validatecommand=(validate_pes_nome, '%P')
        )
        self.txt_pes_nome.pack(side="top", fill="x", padx=10, pady=5)

        scrollbar = ttk.Scrollbar(self.container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        self.visualizar()

    def visualizar(self):
        with self.db.get_conexao() as session:
            rs = session.query(ProdutoServico).order_by(ProdutoServico.descricao).all()
            self.tree.bind("<Double-1>", self.duplo_click)

            for linha in self.tree.get_children():
                self.tree.delete(linha)

            for linha in rs:
                self.tree.insert("", tk.END, values=linha.get_values())

    def pesquisar_nome(self, p):
        with self.db.get_conexao() as session:
            try:
                rs = session.query(ProdutoServico).filter(ProdutoServico.descricao.ilike(f"%{p}%")).all()
                for linha in self.tree.get_children():
                    self.tree.delete(linha)

                for linha in rs:
                    self.tree.insert("", tk.END, values=linha.get_values())
            except:
                print(f'Conexão indisponivel...')

            return True
    
    def ordenar_coluna(self, col_id: str, reverse: bool) -> None:
        """Função para ordenar a coluna selecionada."""
        def tratar_valor(valor):
            """Função para tratar o valor da célula antes da ordenação."""
            try:
                return float(valor) if '.' in valor or valor.isdigit() else int(valor)
            except ValueError:
                return valor.lower()

        itens = [(tratar_valor(self.tree.set(k, col_id)), k) for k in self.tree.get_children("")]
        itens.sort(reverse=reverse, key=lambda x: x[0])
        
        for index, (_, k) in enumerate(itens):
            self.tree.move(k, '', index)

        self.tree.heading(col_id, command=lambda: self.ordenar_coluna(col_id, not reverse))
    
    def duplo_click_invalido(self, event):
        item_selecionado = self.tree.selection()
        if item_selecionado:
            valores = self.tree.item(item_selecionado[0], "values")
            if int(valores[6]) <= 0:
                messagebox.showwarning("Aviso", "Quantidade insulficiente", parent=self.parent)
            else:
                return valores
            
    def duplo_click(self, event):
        item_selecionado = self.tree.selection()
        if item_selecionado:
            valores = self.tree.item(item_selecionado[0], "values")
            return valores
        else:
            []