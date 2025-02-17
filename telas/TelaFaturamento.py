import tkinter as tk
from widgets.widgets_faturamento import create_widgets_faturamento, obter_vendedores

class TelaFaturamento(tk.Frame):
    def __init__(self, master, vendedor, role):
        super().__init__(master)
        self.master = master
        self.vendedor = vendedor
        self.role = role
        self.vendedores = []
        self.clientes = []
        self.create_widgets()
    
    def create_widgets(self):
        create_widgets_faturamento(self)
