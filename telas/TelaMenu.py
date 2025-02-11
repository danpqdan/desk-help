import tkinter as tk
from tkinter import messagebox
from widgets.widgets_menu import create_widgets_menu

class TelaMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.geometry(f'{self.master.winfo_screenwidth()}x{self.master.winfo_screenheight()}+0+0')
        self.frames = {}
        self.create_widgets()

    def create_widgets(self):
        create_widgets_menu(self)

    def mostrar_sobre(self):
        messagebox.showinfo("Sobre", "Sistema Comercial 1.0")

    def sair_app(self):
        var_sair = messagebox.askyesno("Sair", "Tem certeza que deseja sair?")
        if var_sair:
            self.master.destroy()
            
    def mostrar_frames(self, frame_class):
        """Switch between frames in the menu."""
        for frame in self.frames.values():
            frame.place_forget()

        if frame_class not in self.frames:
            frame = frame_class(self.master)
            self.frames[frame_class] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            self.frames[frame_class].place(x=0, y=0, relwidth=1, relheight=1)

    # Placeholder methods for other functionalities
    # def show_clientes(self):
    #     self.master.switch_to_clientes()

    # def show_produtos(self):
    #     self.master.switch_to_produtos()

    # def show_vendas(self):
    #     self.master.switch_to_vendas()

    # def show_cadlogin(self):
    #     self.master.switch_to_cadlogin()
