import tkinter as tk
from tkinter import messagebox
from telas.TelaCliente import TelaCliente
from telas.TelaProdutos import TelaProduto
from telas.TelaVenda import TelaVenda
from widgets.widgets_menu import create_widgets_menu

class TelaMenu(tk.Toplevel):  # Alterado para Toplevel
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("Menu Principal")
        self.geometry(f'{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0')

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

    def mostrar_frames(self, frame_class):
        """Alterna entre os frames internos"""
        for frame in self.frames.values():
            frame.place_forget()

        if frame_class not in self.frames:
            frame = frame_class(self)
            self.frames[frame_class] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            self.frames[frame_class].place(x=0, y=0, relwidth=1, relheight=1)

    def mostrar_cliente(self):
        self.mostrar_frames(TelaCliente)

    def mostrar_produto(self):
        self.mostrar_frames(TelaProduto)

    def mostrar_vendas(self):
        self.mostrar_frames(TelaVenda)
