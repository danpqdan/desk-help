import tkinter as tk
from tkinter import *
# import bcrypt
from services.conexao import Database
from model.Cliente import Cliente
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
        var_email = self.txtemail.get()
        var_senha = self.txtsenha.get()
        try:
            db = Database()
            con = db.get_conexao()
            if not con:
                raise ConnectionError("Não foi possível conectar ao banco de dados.")
            
            sql_txt = f"SELECT email, nome, senha FROM clientes WHERE email = :email"
            params = {"email": var_email}
            rs = db.encontrar_um(sql_query=sql_txt, params=params) 
            if rs:
                db_email, db_nome, db_senha_hash = rs
                if Cliente.verificar_senha(senha=var_senha, senha_hash=db_senha_hash):
                    lblresult = tk.Label(self.form, text="**** Acesso Permitido ***", foreground='blue', bg='#D8EAF7')
                    lblresult.place(relx=0.2, y=150)
                    self.master.switch_to_menu()
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
