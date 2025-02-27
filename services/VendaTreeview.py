from tkinter import messagebox, ttk
import tkinter as tk
from sqlalchemy import text
from sqlalchemy.orm import aliased
from model.ProdutoServico import ProdutoServico
from model.Sacola import SacolaProduto
from services.conexao import Database

class VendaSacolaTreeview:
    def __init__(self, tela_venda):
        self.tela_venda = tela_venda
        self.selected_data = None
        self.tree = None
        self.tela_venda.update_idletasks()
        self.larguraTela = self.tela_venda.winfo_screenwidth()
        self.alturaTela = self.tela_venda.winfo_screenheight()
        self.db = Database()
        self.criar_treeview_venda()
        
    def criar_treeview_venda(self):
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
        scrollbar = ttk.Scrollbar(self.container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)
        
        self.visualizar()
        
    from sqlalchemy.orm import aliased

    def visualizar(self):
        num_venda = self.tela_venda.txtsacolaid.get()
        print("Num_venda", num_venda)
        
        sacola_produto = aliased(SacolaProduto)
        produtos_servicos = aliased(ProdutoServico)
        
        with self.db.get_conexao() as session:
            try:
                results = session.query(
                    sacola_produto.lin_venda,
                    sacola_produto.produto_id,
                    produtos_servicos.descricao,
                    sacola_produto.quantidade,
                    produtos_servicos.valor,
                    sacola_produto.total,
                ).join(
                    produtos_servicos, sacola_produto.produto_id == produtos_servicos.codigo
                ).filter(
                    sacola_produto.sacola_id == num_venda
                ).order_by(
                    sacola_produto.sacola_id, sacola_produto.lin_venda
                ).all()
                
                if not results:
                    return None

                for linha in self.tree.get_children():
                    self.tree.delete(linha)

                for linha in results:
                    self.tree.insert("", tk.END, values=tuple(linha))

            except Exception as e:
                print(f"Erro: {e}")
                messagebox.showerror("Erro", "Não foi possível consultar as vendas.")


            
    def limpar_arv(self):
        for linha in self.tree.get_children():
            self.tree.delete(linha)
            
    def limpar_lin(self):
        item_selecionado = self.tree.selection()
        if item_selecionado:
            item = self.tree.item(item_selecionado)
            self.tree.delete(item_selecionado)
            return item

        return None
            
    def duplo_click(self, event):
        item_selecionado = self.tree.selection()
        if item_selecionado:
            valores = self.tree.item(item_selecionado[0], "values")
            return valores 
        return []
