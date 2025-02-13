import tkinter as tk
from tkinter import messagebox
from telas.TelaCliente import TelaCliente
from telas.TelaProdutos import TelaProduto
from telas.TelaVenda import TelaVenda
from widgets.widgets_menu import create_widgets_menu

class TelaMenu(tk.Frame):
    def __init__(self, master, vendedor):
        super().__init__(master)
        self.master = master
        self.vendedor = vendedor
        self.config(bg="#D8EAF7")
        self.master.title("Menu Principal")
        # self.geometry(f'{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0')

        self.frames = {}
        self.create_widgets()

    def create_widgets(self):
        create_widgets_menu(self)

    def mostrar_sobre(self):
        messagebox.showinfo("Sobre", "Sistema Comercial 1.0")

    def sair_app(self):
        """Fecha a TelaMenu e retorna para o login"""
        var_sair = messagebox.askyesno("Sair", "Tem certeza que deseja sair?")
        if var_sair:
            self.master.trocar_para_login()

    def mostrar_cliente(self):
        self.master.trocar_para_cliente(self.vendedor)

    def mostrar_produto(self):
        self.master.trocar_para_produto(self.vendedor)

    def mostrar_vendas(self):
        self.master.trocar_para_vendas(self.vendedor)
