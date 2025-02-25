from tkinter import messagebox, ttk
import tkinter as tk
from sqlalchemy import func, text
from sqlalchemy.sql import and_
from model.Cliente import Cliente
from model.Sacola import Sacola, SacolaProduto
from services.conexao import Database

class SacolaTreeview:
    def __init__(self, tela_venda):
        self.tela_venda = tela_venda
        self.selected_data = None
        self.tree = None
        self.con = Database().SessionLocal()
        self.tela_venda.update_idletasks()
        self.larguraTela = self.tela_venda.winfo_screenwidth()
        self.alturaTela = self.tela_venda.winfo_screenheight()
        self.criar_treeview_sacola()
        
    def criar_treeview_sacola(self):
        self.container = tk.Frame(self.tela_venda, bg='white', width=self.larguraTela, height=self.alturaTela/3)
        self.container.pack(side='bottom', fill='x')
        
        style = ttk.Style()
        style.configure("mystyle.Treeview", font=("Calibri", 10))
        style.configure("mystyle.Treeview.Heading", font=("Calibri", 12, "bold"))

        self.tree = ttk.Treeview(
            self.container,
            column=("#1", "#2", "#3", "#4", "#5", "#6"),
            show='headings',
            style="mystyle.Treeview",
            padding=0
            )
        self.tree.column("#1", width=50, anchor='c')
        self.tree.heading("#1", text="id")
        
        self.tree.column("#2", width=100, anchor='c')
        self.tree.heading("#2", text="vendedor_usuario")
        
        self.tree.column("#3", width=200, anchor='c')
        self.tree.heading("#3", text="cliente_cpf")
        
        self.tree.column("#4", width=50, anchor='c')
        self.tree.heading("#4", text="Qts produtos")
        
        self.tree.column("#5", width=100, anchor='c')
        self.tree.heading("#5", text="total")
        
        self.tree.column("#6", width=150, anchor='c')
        self.tree.heading("#6", text="time_stamp")
                
        self.tree.place(x=50, y=350, height=180)
        scrollbar = ttk.Scrollbar(self.container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)
        
        self.visualizar()
        
    def visualizar(self):
        sacola = self.con.query(
            Sacola.id.label("id_sacola"), 
            Sacola.vendedor_usuario.label("vendedor"),
            Cliente.nome.label("cliente_nome"),
            func.max(SacolaProduto.quantidade).label("max_quantidade"),
            func.sum(SacolaProduto.total).label("total"),
            Sacola.time_stamp.label("Horario")
        ).join(Cliente, Cliente.cpf == Sacola.cliente_cpf
        ).join(SacolaProduto, Sacola.id == SacolaProduto.sacola_id
        ).group_by(Sacola.id, Cliente.nome, Sacola.vendedor_usuario, Sacola.time_stamp).all()

        if not sacola:
            messagebox.showerror("Erro", "Não foi possível consultar as vendas.")
            return

        for linha in self.tree.get_children():
            self.tree.delete(linha)

        for linha in sacola:
            self.tree.insert("", tk.END, values=tuple(linha))

    
    def duplo_click(self, event):
        item_selecionado = self.tree.selection()
        if item_selecionado:
            valores = self.tree.item(item_selecionado[0], "values")
            return valores 
        return []
