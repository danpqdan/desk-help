import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from services.router_path import help_desk_icon as icon

def create_widgets_menu(self):
    """Cria os widgets do menu principal com melhor formatação."""
    larguraTela = self.master.winfo_screenwidth()
    alturaTela = self.master.winfo_screenheight()
    red_larguraTela = larguraTela // 2
    red_alturaTela = alturaTela // 2
    
    image = Image.open(icon)
    image = image.resize((red_larguraTela, red_alturaTela), Image.LANCZOS)
    image = image.convert("RGBA")
    self.tk_image = ImageTk.PhotoImage(image)
    canvas = tk.Canvas(self, bg="#D8EAF7", width=red_larguraTela, height=red_alturaTela, highlightthickness=0)
    canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    canvas.create_image(red_larguraTela//2, red_alturaTela//2, anchor=tk.CENTER, image=self.tk_image)
    
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

