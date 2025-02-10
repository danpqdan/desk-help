import tkinter as tk
from tkinter import *
# import bcrypt
from services.conexao import Database
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
        var_login = self.txtusuario.get()
        var_senha = self.txtsenha.get()
        try:
            con = Database()
            if not con.db:
                raise ConnectionError("Não foi possível conectar ao banco de dados.")
            
            sql_txt = f"SELECT usuario, nome, senha FROM login WHERE usuario = '{var_login}'"
            rs = con.consultar(sql_txt)

            if rs:
                db_usuario, db_nome, db_senha_hash = rs
                if isinstance(db_senha_hash, bytes) and bcrypt.checkpw(var_senha.encode('utf-8'), db_senha_hash):
                    lblresult = tk.Label(self.form, text="**** Acesso Permitido ***", foreground='blue')
                    lblresult.grid(column=1, row=3)
                    con.fechar()

                    self.master.switch_to_menu()
                else:
                    lblresult = tk.Label(self.form, text="Usuário ou Senha Inválida", foreground='red')
                    lblresult.grid(column=1, row=3)
            else:
                lblresult = tk.Label(self.form, text="Usuário ou Senha Inválida", foreground='red')
                lblresult.grid(column=1, row=3)
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
