import tkinter as tk
from tkinter import messagebox
from model.Vendedor import Role
from telas.TelaCliente import TelaCliente
from telas.TelaProdutos import TelaProduto
from telas.TelaVenda import TelaVenda
from telas.LoginPopup import LoginPopup
from widgets.widgets_menu import create_widgets_menu

class TelaMenu(tk.Frame):
    def __init__(self, master, vendedor, role):
        super().__init__(master)
        self.master = master
        self.vendedor = vendedor
        self.role = role
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
        self.master.trocar_para_cliente(self.vendedor, self.role)

    def mostrar_produto(self):
        self.master.trocar_para_produto(self.vendedor, self.role)

    def mostrar_vendas(self):
        self.master.trocar_para_vendas(self.vendedor, self.role)
    
    def mostrar_faturamento(self):
        """Exibe a tela de faturamento se o usuário tiver permissão."""
        if self.validar_role():
            self.master.trocar_para_faturamento(self.vendedor, self.role)
        else:
            validar = self.tela_alerta()  # Removido o argumento errado
            if validar:
                self.master.trocar_para_faturamento(self.vendedor, self.role)
            else:
                messagebox.showinfo("Acesso negado", "Acesso não permitido.")
                
    def mostrar_estoque(self):
        pass

    def validar_role(self) -> bool:
        """Verifica se o usuário tem uma role permitida."""
        return self.role in {Role.ADMIN, Role.GERENTE}

    def tela_alerta(self) -> bool:
        """Solicita login adicional para acessar a tela, se necessário."""
        var_sair = messagebox.askyesno("Permissões necessárias", "Solicite ao superior login para acesso...")
        if var_sair:
            login_popup = LoginPopup(self.master)
            self.master.wait_window(login_popup.popup_busca)

            if login_popup.login_sucesso:
                return True
            else:
                messagebox.showinfo("Acesso negado", "Acesso não permitido.")
                return False
        return False

                    
                
        