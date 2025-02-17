# -*- coding: utf-8 -*-
import platform
import tkinter as tk
from tkinter import messagebox

from sqlalchemy import text
from services.conexao import Database
from widgets.widgets_cliente import create_widgets_cliente

class TelaCliente(tk.Frame):
    def __init__(self, master, vendedor, role):
        super().__init__(master)
        self.master = master
        self.vendedor = vendedor
        self.role = role
        self.create_widgets()

    def create_widgets(self):
        create_widgets_cliente(self=self)

    def limpar(self):
        self.txtcpf.delete(0, "end")
        self.txtnome.delete(0, "end")
        self.txttelefone.delete(0, "end")
        self.txtemail.delete(0, "end")

    def buscar(self):
        var_cpf = self.txtcpf.get()
        self.txtcpf.delete(0, "end")

        con = Database()
        sql_txt = text(f"select cpf, nome, telefone, email from clientes where cpf = :cpf")
        params = var_cpf
        rs = con.encontrar_um(sql_txt, params=params)
        if rs:
            self.txtcpf.insert(0, rs[0])
            self.txtnome.insert(0, rs[1])
            self.txttelefone.insert(0, rs[2])
            self.txtemail.insert(0, rs[3])
        else:
            messagebox.showwarning("Aviso", "Código não Encontrado", parent=self.master)
            self.limpar()
            self.txtcpf.focus_set()

    def gravar(self):
        var_cpf = self.txtcpf.get()
        var_nome = self.txtnome.get()
        var_telefone = self.txttelefone.get()
        var_email = self.txtemail.get()

        con = Database()
        sql_txt = text("SELECT cpf, nome, telefone, email FROM clientes WHERE cpf = :cpf")
        params = {"cpf": var_cpf}
        rs = con.encontrar_um(sql_txt, params)

        if rs:
            sql_text = text("UPDATE clientes SET nome = :nome, telefone = :telefone, email = :email WHERE cpf = :cpf")
        else:
            sql_text = text("INSERT INTO clientes (cpf, nome, telefone, email) VALUES (:cpf, :nome, :telefone, :email)")
        params = {
            "cpf": var_cpf,
            "nome": var_nome,
            "telefone": var_telefone,
            "email": var_email
        }

        if con.executar(sql_text, params):
            messagebox.showinfo("Aviso", "Item Gravado com Sucesso", parent=self.master)
            self.limpar()
        else:
            messagebox.showerror("Erro", "Houve um Erro na Gravação", parent=self.master)

    def excluir(self):
        var_del = messagebox.askyesno("Exclusão", "Tem certeza que deseja excluir?", parent=self.master)
        if var_del:
            var_cpf = self.txtcpf.get()

            con = Database()
            sql_text = text(f"delete from clientes where cpf = :cpf")
            params = var_cpf
            if con.executar(sql_text, params):
                messagebox.showinfo("Aviso", "Item Excluido com Sucesso", parent=self.master)
                self.limpar()
            else:
                messagebox.showerror("Erro", "Houve um Erro na Exclusão", parent=self.master)

            self.limpar()
        else:
            self.limpar()

    def menu(self): 
        self.master.trocar_para_menu(self.vendedor, self.role)

    def atualizar_filds(self, fields, valores):
        if len(valores) == len(fields):
            for field, valor in zip(fields, valores):
                if isinstance(field, tk.Entry):
                    field.delete(0, tk.END)
                    field.insert(0, valor)
                elif isinstance(field, tk.Text):
                    field.delete("1.0", tk.END)
                    field.insert("1.0", valor)

    def limitar_tamanho(self, p, limite):
        return len(p) <= int(limite)