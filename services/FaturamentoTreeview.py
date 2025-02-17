 
from tkinter import messagebox, ttk
import tkinter as tk

from sqlalchemy import text

from services.conexao import Database


class FaturamentoTreeview:
    def __init__(self, tela_faturamento):
        self.tela_faturamento = tela_faturamento
        self.selected_data = None
        self.tree = None
        self.tela_faturamento.update_idletasks()
        self.larguraTela = self.tela_faturamento.winfo_screenwidth()
        self.alturaTela = self.tela_faturamento.winfo_screenheight()
        self.criar_treeview_faturamento()
        
    def criar_treeview_faturamento(self):    
        largura_personalizada = self.larguraTela / 3
        altura_personalizada = self.alturaTela / 3
        largura_aside = self.larguraTela - largura_personalizada
        self.container_vis = tk.Frame(self.tela_faturamento, bg="#FFFFFF", width=largura_aside, height=self.alturaTela)
        self.container_vis.pack(side="bottom", fill="both", expand=True)
        
        # Arvore
        style = ttk.Style()
        style.configure("mystyle.Treeview", font=("Calibri", 10))
        style.configure("mystyle.Treeview.Heading", font=("Calibri", 12, "bold"))

        self.tree = ttk.Treeview(
            self.container_vis,
            column=("#1", "#2", "#3", "#4", "#5", "#6"),
            show='headings',
            style="mystyle.Treeview",
            padding=0
            )
        self.tree.column("#1", width=50, anchor='c')
        self.tree.heading("#1", text="id")
        
        self.tree.column("#2", width=100, anchor='c')
        self.tree.heading("#2", text="vendedor_usuario")
        
        self.tree.column("#3", width=200, anchor='w')
        self.tree.heading("#3", text="cliente_cpf")
        
        self.tree.column("#4", width=50, anchor='c')
        self.tree.heading("#4", text="Qts produtos")
        
        self.tree.column("#5", width=100, anchor='c')
        self.tree.heading("#5", text="total")
        
        self.tree.column("#6", width=150, anchor='c')
        self.tree.heading("#6", text="time_stamp")
        
        scrollbar = ttk.Scrollbar(self.container_vis, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)
        
        
