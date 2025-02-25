import tkinter as tk
from tkinter import messagebox

import tkinter as tk

def create_widgets_menu(self):
    """Cria os widgets do menu principal com melhor formatação."""
    
    # Informações do Menu
    self.menu_info = tk.Label(
        self, 
        text=f"Bem-vindo ao Sistema {self.vendedor}", 
        bg="#007acc",
        fg="white",
        font=("Arial", 16, "bold"),
        padx=10,
        pady=10
    )
    self.menu_info.pack(side="top", fill="x")

    # Criar a barra de menus
    self.menu_bar = tk.Menu(self)
    self.master.config(menu=self.menu_bar)
    
    # Menu Funcionalidades
    menu_func = tk.Menu(self.menu_bar, tearoff=0)
    self.menu_bar.add_cascade(label="Funcionalidades", menu=menu_func)
    
    menu_func.add_command(label="📁 Clientes", command=self.mostrar_cliente)
    menu_func.add_command(label="🛒 Produtos/Serviços", command=self.mostrar_produto)
    menu_func.add_command(label="💰 Vendas", command=self.mostrar_vendas)
    menu_func.add_separator()
    menu_func.add_command(label="🚪 Sair", command=self.sair_app)
    
    # Menu Controle
    menu_gerencia = tk.Menu(self.menu_bar, tearoff=0)
    self.menu_bar.add_cascade(label="Controle", menu=menu_gerencia)
    menu_gerencia.add_command(label="📦 Estoque", command=self.mostrar_estoque)
    menu_gerencia.add_command(label="📊 Faturamento", command=self.mostrar_faturamento)

    # Menu Ajuda
    menu_ajuda = tk.Menu(self.menu_bar, tearoff=0)
    self.menu_bar.add_cascade(label="Ajuda", menu=menu_ajuda)
    menu_ajuda.add_command(label="ℹ️ Sobre", command=self.mostrar_sobre)

