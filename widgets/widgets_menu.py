import tkinter as tk
from tkinter import messagebox

def create_widgets_menu(self):
    """Cria os widgets do menu principal."""
    
    self.container = tk.Frame(self, bg="#D8EAF7")
    self.container.pack(fill=tk.BOTH, expand=True)

    self.bg_label = tk.Label(self.container, text="Bem-vindo ao Sistema", bg="#D8EAF7", font=("Arial", 16))
    self.bg_label.pack(pady=20)

    self.menu_bar = tk.Menu(self)
    self.config(menu=self.menu_bar)
    
    menu_func = tk.Menu(self.menu_bar, tearoff=0)
    self.menu_bar.add_cascade(label="Funcionalidades", menu=menu_func)
    
    menu_func.add_command(label="Clientes", command=self.mostrar_cliente)
    menu_func.add_command(label="Produtos/Serviços", command=self.mostrar_produto)
    menu_func.add_command(label="Vendas", command=self.mostrar_vendas)
    menu_func.add_separator()
    menu_func.add_command(label="Sair", command=self.sair_app)

    menu_ajuda = tk.Menu(self.menu_bar, tearoff=0)
    self.menu_bar.add_cascade(label="Ajuda", menu=menu_ajuda)
    menu_ajuda.add_command(label="Sobre", command=self.mostrar_sobre)
