import tkinter as tk
from tkinter import *
# import bcrypt
from services.conexao import Database
from model.Vendedor import Vendedor
from widgets.widgets_login import create_widgets_login

class TelaLogin(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.geometry(f'{self.master.winfo_screenwidth()}x{self.master.winfo_screenheight()}+0+0')
        self.config(bg="#D8EAF7")
        self.create_widgets()
        
    def create_widgets(self):
        create_widgets_login(self=self)


    def validasenha(self):
        """Validate login credentials and switch to menu on success."""
        var_usuario = self.txtusuario.get()
        var_senha = self.txtsenha.get()
        try:
            db = Database()
            con = db.get_conexao()
            if not con:
                raise ConnectionError("Não foi possível conectar ao banco de dados.")
            
            sql_txt = f"SELECT usuario, senha, role FROM vendedores WHERE usuario = :usuario"
            params = {"usuario": var_usuario}
            rs = db.encontrar_um(sql_query=sql_txt, params=params) 
            if rs:
                db_usuario, db_senha_hash, role = rs
                if Vendedor.verificar_senha(senha=var_senha, senha_hash=db_senha_hash):
                    lblresult = tk.Label(self.form, text="**** Acesso Permitido ***", foreground='blue', bg='#D8EAF7')
                    lblresult.place(relx=0.2, y=150)
                    self.usuario_logado = var_usuario
                    self.usuario_role = role
                    self.txtusuario.focus_set()
                    self.master.trocar_para_menu(self.usuario_logado, self.usuario_role)
                    self.txtusuario.delete(0, 'end')
                    self.txtsenha.delete(0, 'end')
                else:
                    lblresult = tk.Label(self.form, text="Usuário ou Senha Inválida", foreground='red', bg='#D8EAF7')
                    lblresult.place(relx=0.2, y=150)
            else:
                lblresult = tk.Label(self.form, text="Usuário ou Senha Inválida", foreground='red', bg='#D8EAF7')
                lblresult.place(relx=0.2, y=150)
        except Exception as e:
            print(f"Erro: {e}")

    def mostrarsenha(self):
        """Toggle password visibility."""
        if self.txtsenha.cget('show') == '':
            self.txtsenha.config(show='*')
        else:
            self.txtsenha.config(show='')

    def sair(self):
        self.master.destroy()
