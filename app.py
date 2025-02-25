import tkinter as tk
from telas.TelaVenda import TelaVenda
from telas.TelaCliente import TelaCliente
from telas.TelaProdutos import TelaProduto
from telas.TelaMenu import TelaMenu
from telas.TelaLogin import TelaLogin
from telas.TelaFaturamento import TelaFaturamento
from services.conexao import Database
from widgets.widgets_menu import create_widgets_menu

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Desk-Help")
        self.configurar_tela()

        self.frames = {}
        self.exibir_frame("login")

    def configurar_tela(self):
        self.config(bg="#D8EAF7")

    def exibir_frame(self, frame_name, vendedor=None, role=None):
        for frame in self.frames.values():
            frame.place_forget()
            frame.pack_forget()

        if frame_name not in self.frames:
            if frame_name == "login":
                frame = TelaLogin(self)
            elif frame_name == "menu":
                frame = TelaMenu(self, vendedor, role)
            elif frame_name == "Tela de Clientes":
                frame = TelaCliente(self, vendedor, role)
            elif frame_name == "Tela de Vendas":
                frame = TelaVenda(self, vendedor, role)
            elif frame_name == "Tela de Produtos":
                frame = TelaProduto(self, vendedor, role)
            elif frame_name == "Tela de Faturamento":
                frame = TelaFaturamento(self, vendedor, role)
            else:
                raise ValueError(f"Frame '{frame_name}' não encontrado.")
        
            self.frames[frame_name] = frame
            frame.pack(expand=True, fill=tk.BOTH) 
        else:
            self.frames[frame_name].pack(expand=True, fill=tk.BOTH)

    def trocar_para_menu(self, vendedor, role):
        self.exibir_frame("menu", vendedor, role)

    def trocar_para_login(self):
        for frame_name in ["menu", "Tela de Faturamento"]:
            if frame_name in self.frames:
                self.frames[frame_name].destroy()
                del self.frames[frame_name]

        self.exibir_frame("login")
        
    def trocar_para_cliente(self, vendedor, role):
        self.exibir_frame('Tela de Clientes', vendedor, role)
        
    def trocar_para_produto(self, vendedor, role):
        self.exibir_frame('Tela de Produtos', vendedor, role)
        
    def trocar_para_vendas(self, vendedor, role):
        self.exibir_frame('Tela de Vendas', vendedor, role)
    
    def trocar_para_faturamento(self, vendedor, role):
        self.exibir_frame('Tela de Faturamento', vendedor, role)
        


def iniciar_app():
    app = App()
    app.mainloop()
    
def iniciar_conexao():
    db_instance = Database()
    db_instance.criar_tabelas()

if __name__ == "__main__":
    iniciar_conexao()
    iniciar_app()
