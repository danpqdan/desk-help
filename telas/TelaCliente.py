# -*- coding: utf-8 -*-
import platform
import tkinter as tk
from tkinter import messagebox

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from model.Cliente import Cliente
from services.conexao import Database
from widgets.widgets_cliente import create_widgets_cliente

class TelaCliente(tk.Frame):
    def __init__(self, master, vendedor, role):
        super().__init__(master)
        self.master = master
        self.db = Database()
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
        var_cpf = self.txtcpf.get().strip()
        self.txtcpf.delete(0, "end")
        with self.db.get_conexao() as session:
            try:
                rs = session.query(Cliente).filter(Cliente.cpf == var_cpf).first()
                if rs:
                    self.txtcpf.insert(0, rs.cpf)
                    self.txtnome.insert(0, rs.nome)
                    self.txttelefone.insert(0, rs.telefone)
                    self.txtemail.insert(0, rs.email)
                else:
                    messagebox.showwarning("Aviso", "Cliente não encontrado.", parent=self.master)
                    self.limpar()
                    self.txtcpf.focus_set()
            except SQLAlchemyError as e:
                messagebox.showerror("Erro", "Ocorreu um erro ao buscar o cliente.", parent=self.master)
                print(f"Erro ao buscar cliente: {e}")
                self.limpar()
                self.txtcpf.focus_set()

    def gravar(self):
        var_cpf = self.txtcpf.get()
        var_nome = self.txtnome.get()
        var_telefone = self.txttelefone.get()
        var_email = self.txtemail.get()
        
        with self.db.get_conexao() as session:
            try:
                rs = session.query(Cliente).filter(Cliente.cpf == var_cpf).first()
                
                if rs:
                    rs.nome = var_nome
                    rs.telefone = var_telefone
                    rs.email = var_email
                else:
                    cliente = Cliente(cpf=var_cpf, nome=var_nome, telefone=var_telefone, email=var_email)
                    session.add(cliente)

                messagebox.showinfo("Aviso", "Item Gravado com Sucesso", parent=self.master)
                self.limpar()
            
            except SQLAlchemyError as e:
                session.rollback()
                messagebox.showerror("Erro", f"Houve um Erro na Gravação: {e}", parent=self.master)
                print(f"Erro ao gravar cliente: {e}")
                self.limpar()

    def excluir(self):
        var_del = messagebox.askyesno("Exclusão", "Tem certeza que deseja excluir?", parent=self.master)
        if var_del:
            var_cpf = self.txtcpf.get()
            with self.db.get_conexao() as session:
                try:
                    rs = session.query(Cliente).filter(Cliente.cpf == var_cpf).first()
                    if rs:
                        session.delete(rs)
                        messagebox.showinfo("Aviso", "Item Excluído com Sucesso", parent=self.master)
                        self.limpar()
                    else:
                        messagebox.showerror("Erro", "Cliente não encontrado", parent=self.master)
                        self.limpar()
                except SQLAlchemyError as e:
                    messagebox.showerror("Erro", "Ocorreu um erro interno. Tente novamente.", parent=self.master)
                    print(f"Erro ao buscar cliente: {e}")   
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