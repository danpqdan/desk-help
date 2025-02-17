import tkinter as tk
from tkinter import messagebox

from sqlalchemy import text
from model.Vendedor import Role, Vendedor
from services.conexao import Database

class LoginPopup:
    def __init__(self, master):
        self.master = master
        self.popup_busca = tk.Toplevel(self.master)
        self.popup_busca.title("Buscar Cliente")
        self.popup_busca.geometry(f"{self.master.winfo_screenwidth()//2}x{self.master.winfo_screenheight()//2}")
        self.popup_busca.resizable(True, True)
        self.login_sucesso = False
        
        self.form = tk.Frame(self.popup_busca, bg="#D8EAF7", width=400, height=250)
        self.form.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        lblusuario = tk.Label(self.form, text="Usuário:", bg="#D8EAF7", font=('Calibri', 12, 'bold'))
        lblusuario.place(x=20, y=20)
        self.txtusuario = tk.Entry(self.form, font=('Calibri', 12), width=30)
        self.txtusuario.place(x=100, y=20)

        lblsenha = tk.Label(self.form, text="Senha:", bg="#D8EAF7", font=('Calibri', 12, 'bold'))
        lblsenha.place(x=20, y=60)
        self.txtsenha = tk.Entry(self.form, font=('Calibri', 12), width=30, show="*")
        self.txtsenha.place(x=100, y=60)
        
        # Botão de login
        btnsubmeter = tk.Button(self.form, text="Login", bg='#D8EAF7', fg='black', font=('Calibri', 12, 'bold'), command=self.validasenha)
        btnsubmeter.place(x=50, y=100)

        # Botão de sair
        btnsair = tk.Button(self.form, text="Fechar", bg='#D8EAF7', fg='black', font=('Calibri', 12, 'bold'), command=self.fechar)
        btnsair.place(x=135, y=100)

        self.txtsenha.bind('<Return>', lambda event: self.validasenha())
        self.txtusuario.focus_set()

    def fechar(self):
        """Fecha a janela de login"""
        self.popup_busca.destroy()

    def validasenha(self):
        """Valida as credenciais de login"""
        var_usuario = self.txtusuario.get()
        var_senha = self.txtsenha.get()
        
        try:
            db = Database()
            con = db.get_conexao()
            if not con:
                raise ConnectionError("Não foi possível conectar ao banco de dados.")

            sql_txt = "SELECT usuario, senha, role FROM vendedores WHERE usuario = :vendedor"
            params = {'vendedor': var_usuario}
            rs = db.encontrar_um(sql_query=sql_txt, params=params)
            
            if rs:
                db_usuario, db_senha_hash, role = rs
                if Vendedor.verificar_senha(var_senha, db_senha_hash):

                    if role in [Role.ADMIN.value, Role.GERENTE.value]:
                        self.fechar()
                        self.login_sucesso = True
                        messagebox.showinfo("Login", "Acesso concedido!")
                        self.popup_busca.destroy()
                        return self.login_sucesso
                    return False
                else:
                    lblresult = tk.Label(self.form, text="Usuário ou Senha Inválida", foreground='red', bg='#D8EAF7')
                    lblresult.place(relx=0.2, y=150)
            else:
                lblresult = tk.Label(self.form, text="Usuário ou Senha Inválida", foreground='red', bg='#D8EAF7')
                lblresult.place(relx=0.2, y=150)
        except Exception as e:
            print(f"Erro: {e}")


