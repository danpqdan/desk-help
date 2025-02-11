import tkinter as tk
from tkinter import messagebox

def create_widgets_menu(self):
    """Create the widgets for the main menu."""
    
    self.bg_label = tk.Label(self, bg="#D8EAF7")
    self.bg_label.pack(fill=tk.BOTH, expand=True)
    
    self.menu_bar = tk.Menu(self)
    self.master.config(menu=self.menu_bar)
    
    menu_func = tk.Menu(self.menu_bar, tearoff=0)
    self.menu_bar.add_cascade(label="Funcionalidades", menu=menu_func)
    # Add additional functionality commands (e.g. clientes, produtos)
    # menu_func.add_command(label="Clientes", command=self.show_clientes)
    # menu_func.add_command(label="Produtos/Serviços", command=self.show_produtos)
    # menu_func.add_command(label="Vendas", command=self.show_vendas)
    # menu_func.add_command(label="Gestão de Acessos", command=self.show_cadlogin)
    menu_func.add_separator()
    menu_func.add_command(label="Sair", command=self.sair_app)

    menu_ajuda = tk.Menu(self.menu_bar, tearoff=0)
    self.menu_bar.add_cascade(label="Ajuda", menu=menu_ajuda)
    menu_ajuda.add_command(label="Sobre", command=self.mostrar_sobre)
