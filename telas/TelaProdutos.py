# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from sqlalchemy import text
from services.conexao import Database
import locale
from widgets.widgets_produtos import create_widgets_produto

class TelaProduto(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title('produtos')
        self.create_widgets()    
    
    def create_widgets(self):
        create_widgets_produto(self=self)   
        
    def limpar(self):
        self.txtcodigo.delete(0, "end")
        self.cmbtipo.delete(0, "end")
        self.txtdescricao.delete(0, "end")
        self.txtvalor.delete(0, "end")
        self.txtcodigo.focus_set()

    def buscar(self):
        var_codigo = self.txtcodigo.get()
        con = Database()
        sql_txt = f"select codigo, tipo, descricao, valor from produtos_servicos where codigo = {var_codigo}"
        rs = con.encontrar_um(sql_query=sql_txt)

        if rs:
            self.limpar()
            self.txtcodigo.insert(0, rs[0])
            self.cmbtipo.insert(0, rs[1])
            self.txtdescricao.insert(0, rs[2])
            self.txtvalor.insert(0, locale.currency(rs[3]))
        else:
            messagebox.showwarning("Aviso", "Código não Encontrado", parent=self.master)
            self.limpar()
            self.txtcodigo.focus_set()

    def gravar(self):
        var_codigo = self.txtcodigo.get()
        var_tipo = self.cmbtipo.get()
        var_descricao = str.upper(self.txtdescricao.get())
        var_valor = self.txtvalor.get()
        var_valor = float(var_valor.replace('R$', '').strip().replace('.', '').replace(',', '.'))

        con = Database()
        sql_txt = f"select codigo, descricao, tipo, valor from produtos_servicos where codigo = {var_codigo}"
        rs = con.encontrar_um(sql_txt)

        if rs:
            sql_text = text("UPDATE produtos_servicos SET tipo=:tipo, descricao=:descricao, valor=:valor WHERE codigo = :codigo")
        else:
            sql_text = text("INSERT INTO produtos_servicos (codigo, tipo, descricao, valor) VALUES (:codigo, :tipo, :descricao, :valor)")
        
        params = {
            "codigo": var_codigo,
            "tipo": var_tipo,
            "descricao": var_descricao,
            "valor": var_valor
        }

        if con.executar(sql_text=sql_text, params=params):
            messagebox.showinfo("Aviso", "Item Gravado com Sucesso", parent=self.master)
            self.limpar()
        else:
            messagebox.showerror("Erro", "Houve um Erro na Gravação", parent=self.master)

    def excluir(self):
        var_del = messagebox.askyesno("Exclusão", "Tem certeza que deseja excluir?", parent=self.master)
        if var_del:
            var_codigo = self.txtcodigo.get()
            con = Database()
            sql_text = f"delete from produtos_servicos where codigo = '{var_codigo}'"
            if con.executar(sql_text):
                messagebox.showinfo("Aviso", "Item Excluído com Sucesso", parent=self.master)
                self.limpar()
            else:
                messagebox.showerror("Erro", "Houve um Erro na Exclusão", parent=self.master)
            con.fechar()
        else:
            self.limpar()

    def menu(self):
        self.master.trocar_para_menu()

    def limitar_tamanho(self, p, limite):
        return len(p) <= int(limite)

    def atualizar_filds(self, fields, valores):
        if len(valores) == len(fields):
            for field, valor in zip(fields, valores):
                if isinstance(field, tk.Entry):
                    field.delete(0, tk.END)
                    field.insert(0, valor)
                elif isinstance(field, tk.Text):
                    field.delete("1.0", tk.END)
                    field.insert("1.0", valor)
                elif isinstance(field, ttk.Combobox):
                    if valor in field['values']:
                        field.set(valor)
                    else:
                        print(f"Valor '{valor}' não encontrado na lista do Combobox.")
