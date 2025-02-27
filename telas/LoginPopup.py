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
        self.popup_busca.config(bg="#D8EAF7")
        self.login_sucesso = False
        self.db = Database()
        
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

        with self.db.get_conexao() as session:
            try:
                rs = session.query(Vendedor).filter(Vendedor.usuario == var_usuario).first()

                if rs and Vendedor.verificar_senha(var_senha, rs.senha):
                    if rs.role in [Role.ADMIN, Role.GERENTE]:
                        self.fechar()
                        self.login_sucesso = True
                        messagebox.showinfo("Login", "Acesso concedido!")
                        self.popup_busca.destroy()
                        return self.login_sucesso
                else:
                    self.mostrar_mensagem_erro("Usuário ou Senha Inválida")

                return False

            except Exception as e:
                print(f"Erro: {e}")

    def mostrar_mensagem_erro(self, mensagem):
        """Exibe uma mensagem de erro na interface"""
        lblresult = tk.Label(self.form, text=mensagem, foreground='red', bg='#D8EAF7')
        lblresult.place(relx=0.2, y=150)


