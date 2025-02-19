# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from sqlalchemy import text
from services.ProdutoTreeview import ProdutoTreeview
from services.conexao import Database
import locale
from widgets.widgets_produtos import create_widgets_produto

class TelaProduto(tk.Frame):
    def __init__(self, master, vendedor, role):
        super().__init__(master)
        self.master = master
        self.vendedor = vendedor
        self.role = role
        self.master.title('Tela de Produtos')
        self.create_widgets()    
    
    def create_widgets(self):
        create_widgets_produto(self=self)
        self.text_fields = [self.txtcodigo, self.txtdescricao, self.cmbtipo, self.txtvalor, self.txtcusto, self.txtporcentagem, self.txtquantidade]
        self.tree = ProdutoTreeview(self)
        self.tree.tree.bind("<Double-1>", lambda event: self.atualizar_filds(self.text_fields, self.tree.duplo_click(event)))
    
        
        
    def calcular(self, *args):
        try:
            custo = float(self.custo_var.get()) if self.custo_var.get().replace('.', '', 1).isdigit() else None
            porcentagem = float(self.porcentagem_var.get()) if self.porcentagem_var.get().replace('.', '', 1).isdigit() else None
            valor_final = float(self.valor_var.get()) if self.valor_var.get().replace('.', '', 1).isdigit() else None


            if custo is not None:
                if porcentagem is not None and (valor_final is None or valor_final == custo + (custo * porcentagem / 100)):
                    novo_valor = custo + (custo * porcentagem / 100)
                    if self.valor_var.get() != f"{novo_valor:.2f}":
                        self.valor_var.set(f"{novo_valor:.2f}")

                elif valor_final is not None and (porcentagem is None or porcentagem == ((valor_final - custo) / custo) * 100):
                    nova_porcentagem = ((valor_final - custo) / custo) * 100
                    if self.porcentagem_var.get() != f"{nova_porcentagem:.2f}":
                        self.porcentagem_var.set(f"{nova_porcentagem:.2f}")

        except ValueError:
            pass

        
    def limpar(self):
        self.txtcodigo.delete(0, "end")
        self.cmbtipo.delete(0, "end")
        self.txtdescricao.delete(0, "end")
        self.txtvalor.delete(0, "end")
        self.txtcusto.delete(0,"end")
        self.txtquantidade.delete(0,"end")
        self.txtporcentagem.delete(0,"end")
        self.txtcodigo.focus_set()

    def buscar(self):
        var_codigo = self.txtcodigo.get()
        con = Database()
        sql_txt = f"select codigo, descricao, tipo, valor, custo, porcentagem, quantidade from produtos_servicos where codigo = :codigo"
        rs = con.encontrar_um(sql_query=sql_txt, params={"codigo": var_codigo})

        if rs:
            codigo, descricao, tipo, valor, custo, porcentagem, quantidade = rs
            self.limpar()
            self.txtcodigo.insert(0, codigo)
            self.cmbtipo.insert(0, tipo)
            self.txtdescricao.insert(0, descricao)
            self.txtvalor.insert(0, valor)
            self.txtcusto.insert(0, custo)
            self.txtporcentagem.insert(0, porcentagem)
            self.txtquantidade.insert(0, quantidade)
        else:
            messagebox.showwarning("Aviso", "Código não Encontrado", parent=self.master)
            self.limpar()
            self.txtcodigo.focus_set()

    def gravar(self):
        var_codigo = self.txtcodigo.get()
        var_tipo = self.cmbtipo.get().strip()
        var_descricao = self.txtdescricao.get().upper()
        var_valor = self.valor_var.get()
        var_custo = self.custo_var.get()
        var_porcentagem = self.porcentagem_var.get()
        var_quantidade = self.txtquantidade.get()

        con = Database()
        sql_txt = f"select * from produtos_servicos where codigo = :codigo"

        rs = con.encontrar_um(sql_txt, params={"codigo": str(var_codigo)})

        if rs:
            sql_text = "UPDATE produtos_servicos SET custo=:custo, porcentagem=:porcentagem, quantidade=:quantidade, tipo=:tipo, descricao=:descricao, valor=:valor WHERE codigo = :codigo"
        else:
            sql_text = "INSERT INTO produtos_servicos (codigo, tipo, descricao, valor, custo, quantidade, porcentagem) VALUES (:codigo, :tipo, :descricao, :valor, :custo, :quantidade, :porcentagem)"
        
        params = {
            "codigo": var_codigo,
            "tipo": var_tipo,
            "descricao": var_descricao,
            "valor": var_valor,
            "custo": var_custo,
            "quantidade": var_quantidade,
            "porcentagem": var_porcentagem
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
            
    def baixa_estoque(self):
        con = Database()
        for child in self.tree.get_children():
            codigo = str(self.tree.item(child)["values"][1])
            quantidade = str(self.tree.item(child)["values"][3])
            sql_text = f"UPDATE prodserv SET quantidade = quantidade - {quantidade} WHERE codigo = '{codigo}';"
            print(sql_text)
            con.gravar(sql_text)

    def menu(self):
        self.master.trocar_para_menu(self.vendedor, self.role)

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
                        

    
