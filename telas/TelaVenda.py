# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox

from sqlalchemy import text
# from services import VendasTreeview
from services.ClienteTreeview import ClienteTreeview
from services.ProdutoTreeview import ProdutoTreeview
# from services.VendaTreeview import VendaTreeview
from services.conexao import Database
# from services.func_imprimir_vendas import imprimir
from widgets.widgets_venda import create_widgets_vendas


class TelaVenda(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        
        self.create_widgets()
        self.numeracao()
        self.excluir_inic()
        self.visualizar()
        self.total()
        self.txtsacolaid.config(state="disabled")
        self.txtclicpf.focus_set()

    def create_widgets(self):
        create_widgets_vendas(self=self)
        
    # def abrir_popup_busca_vendas(self):
    #     popup_busca = tk.Toplevel(self.master)
    #     popup_busca.title("Buscar vendas")
    #     popup_busca.geometry(f"{self.master.winfo_screenwidth()}x{self.master.winfo_screenheight()}")
    #     popup_busca.resizable(True, True)
    #     tree = VendasTreeview(popup_busca)
    #     tree.tree.place(x=0, y=0, width=self.master.winfo_screenwidth(), height=self.master.winfo_screenheight())
    #     def handle_duplo_click(event):
    #         valores = tree.duplo_click(event)
    #         print(f"Dados selecionados: {valores}")
    #         if valores:
    #             self.txtsacolaid.delete(0, tk.END)
    #             self.txtsacolaid.insert(0, valores[0])
    #         popup_busca.destroy()
    #         self.bus_venda(cod_compra=valores[0])
    #     tree.tree.bind("<Double-1>", handle_duplo_click)
        

    # def abrir_popup_busca_cliente(self):
    #     popup_busca = tk.Toplevel(self.master)
    #     popup_busca.title("Buscar Cliente")
    #     popup_busca.geometry(f"{self.master.winfo_screenwidth()}x{self.master.winfo_screenheight()}")
    #     popup_busca.resizable(True, True)
    #     tree = ClienteTreeview(popup_busca)
    #     tree.tree.place(x=0, y=0, width=self.master.winfo_screenwidth(), height=self.master.winfo_screenheight())

    #     def handle_duplo_click(event):
    #         valores = tree.duplo_click(event)
    #         print(f"Dados selecionados: {valores}")
    #         if valores:
    #             self.txtclicpf.delete(0, tk.END)
    #             self.txtclicpf.insert(0, valores[0])
    #         popup_busca.destroy()
    #         self.txtclicpf.focus()
    #         self.bus_cli()
    #     tree.tree.bind("<Double-1>", handle_duplo_click)

    # def abrir_popup_busca_prodserv(self):
    #     popup_busca = tk.Toplevel(self.master)
    #     popup_busca.title("Buscar Produto")
    #     popup_busca.geometry(f"{self.master.winfo_screenwidth()}x{self.master.winfo_screenheight()}")
    #     popup_busca.resizable(True, True)
    #     tree = ProdutoTreeview(popup_busca)
    #     tree.tree.place(x=0, y=0, width=(self.master.winfo_screenwidth() - 50), height=(self.master.winfo_screenheight() - 50))

    #     def handle_duplo_click(event):
    #         valores = tree.duplo_click(event)
    #         print(f"Dados selecionados: {valores}")
    #         if valores:
    #             self.txtcodprod.delete(0, tk.END)
    #             self.txtcodprod.insert(0, valores[0])
    #             self.txtcodprod.focus()
    #         popup_busca.destroy()
    #         self.txtclicpf.focus()
    #         self.bus_prod()
    #     tree.tree.bind("<Double-1>", handle_duplo_click)

    def numeracao(self):
        con = Database()
        self.txtsacolaid.config(state="normal")
        
        sql_txt = "SELECT COALESCE(MAX(id), 0) AS id FROM sacolas"
        rs = con.encontrar_um(sql_txt)
        
        if rs:
            num_venda = rs[0]
            
            if num_venda == 0:
                num_venda = 1
                try:
                    sql_insert = text("""INSERT INTO sacolas (id) VALUES (:id)""")
                    con.executar(sql_insert, {"id": num_venda})
                    print(f"Nova sacola criada com num_venda: {num_venda}")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao criar nova sacola: {e}")
                    return
            else:
                num_venda += 1
                try:
                    sql_insert = text("""INSERT INTO sacolas (id) VALUES (:id)""")
                    con.executar(sql_insert, {"id": num_venda})
                    print(f"Nova sacola criada com num_venda: {num_venda}")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao criar nova sacola: {e}")
                    return
            
            self.txtsacolaid.delete(0, "end")
            self.txtsacolaid.insert(0, num_venda)
        
        self.txtsacolaid.config(state="disabled")


    def limpar(self, event=None):
        self.txtdescricao.config(state="normal")
        self.txtvlrunit.config(state="normal")
        self.txtvalor.config(state="normal")
        self.txtcodprod.delete(0, "end")
        self.txtdescricao.delete(0, "end")
        self.txtqtde.delete(0, "end")
        self.txtvlrunit.delete(0, "end")
        self.txtvalor.delete("0", "end")
        self.txtcodprod.focus_set()

    def limpar_cab(self):
        self.txtclicpf.config(state="normal")
        self.txtnomecli.config(state="normal")
        self.txtsacolaid.delete(0, "end")
        self.txtnomecli.delete(0, "end")
        self.txtclicpf.delete(0, "end")
        self.txtclicpf.focus_set()

    def gravar_lin(self):
        con = Database()
        num_venda = self.txtsacolaid.get()
        var_clicpf = self.txtclicpf.get()
        var_codprod = self.txtcodprod.get()
        var_qtde = self.txtqtde.get()
        var_vlrunit = self.txtvlrunit.get()
        var_valor = self.txtvalor.get()

        if not var_clicpf:
            messagebox.showwarning("Aviso", "Favor preencher o código do cliente", parent=self.master)
            self.txtclicpf.focus_set()
            return
        if not var_codprod:
            messagebox.showwarning("Aviso", "Favor preencher o código do produto", parent=self.master)
            self.txtcodprod.focus_set()
            return
        if not (var_qtde and var_valor and var_vlrunit):
            messagebox.showwarning("Aviso", "Favor preencher a quantidade", parent=self.master)
            self.txtqtde.focus_set()
            return
        
        if not (float(var_qtde) * float(var_vlrunit) == float(var_valor)):
            messagebox.showwarning("Aviso", "Favor alterar apenas a quantidade", parent=self.master)
            self.txtqtde.focus_set()
            return
        
        try:
            sql_txt = "SELECT COALESCE(MAX(lin_venda), 0) + 1 AS lin_venda FROM sacola_produto WHERE sacola_id = :sacola_id"
            rs = con.encontrar_um(sql_txt, params={"sacola_id": num_venda})
            
            if rs:
                var_lin_venda = rs[0]                
                sql_text = text('''INSERT INTO sacola_produto (sacola_id, lin_venda, produto_id, quantidade, valor_unit, total) 
                                VALUES (:sacola_id, :lin_venda, :produto_id, :quantidade, :valor_unit, :total)''')
                
                params = {
                    "sacola_id": num_venda,
                    "lin_venda": var_lin_venda,
                    "produto_id": var_codprod,
                    "quantidade": var_qtde,
                    "valor_unit": var_vlrunit,
                    "total": var_valor
                }

                if con.executar(sql_text, params=params):
                    messagebox.showinfo("Sucesso", "Linha gravada com sucesso!", parent=self.master)
                    self.limpar()
                else:
                    messagebox.showerror("Erro", "Falha ao gravar a linha.", parent=self.master)
            else:
                messagebox.showerror("Erro", "Erro ao recuperar o próximo número de linha.", parent=self.master)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gravar linha: {e}", parent=self.master)

    def finalizar_linha(self, event=None):
        self.gravar_lin()
        self.visualizar()
        self.total()

    def excluir(self):
        con = Database()
        txtsacolaid = self.txtsacolaid.get()
        item = self.tree.item(self.tree.selection())
        
        try:
            lin_venda = item['values'][0]
            sql_text = '''DELETE FROM sacola_produto WHERE sacola_id = :sacola_id AND lin_venda = :lin_venda'''
            params = {
                'num_venda': txtsacolaid,
                'lin_venda': lin_venda
            }

            if con.executar(sql_text, params=params):
                self.visualizar()
                self.total()
            else:
                messagebox.showerror("Erro", "Falha ao executar a exclusão.", parent=self.master)

        except Exception as e:
            messagebox.showwarning("Aviso", f"Erro ao excluir: {e}", parent=self.master)


    def excluir_inic(self):
        con = Database()
        num_venda = self.txtsacolaid.get()
        
        sql_text = text('''DELETE FROM sacola_produto WHERE sacola_id = :sacola_id''')
        params = {'sacola_id': num_venda}

        con.executar(sql_text, params=params)


    def visualizar(self):
        con = Database()
        num_venda = self.txtsacolaid.get()
        print("Num_venda", num_venda)
        sql_txt = '''SELECT A.lin_venda, A.produto_id, B.descricao, A.quantidade, A.valor_unit, A.total
                 FROM sacola_produto A
                 JOIN produtos_servicos B ON A.produto_id = B.codigo
                 WHERE A.sacola_id = :sacola_id
                 ORDER BY A.sacola_id, A.lin_venda'''
        rs = con.encontrar_varios(sql_txt, {'sacola_id': num_venda})
        if rs is None:
            messagebox.showerror("Erro", "Não foi possível consultar as vendas.")
            return
        for linha in self.tree.get_children():
            self.tree.delete(linha)
        for linha in rs:
            self.tree.insert("", tk.END, values=tuple(linha))

        

    def total(self):
        con = Database()
        num_venda = self.txtsacolaid.get()
        
        sql_txt = '''SELECT IFNULL(SUM(A.total), 0) AS valor FROM sacola_produto A WHERE A.sacola_id = :num_venda'''
        params = {'num_venda': num_venda}
        
        rs = con.encontrar_um(sql_txt, params=params)
        
        if rs:
            total_valor = rs[0]
        else:
            total_valor = 0.0

        try:
            var_total = float(total_valor)
        except ValueError:
            var_total = 0.0
        
        self.txt_total.config(state="normal")
        self.txt_total.delete("0", "end")
        self.txt_total.insert(0, f"{var_total:.2f}")
        
        if var_total > 0:
            self.btngravar.config(state="normal")
            self.btnimprimir.config(state="normal")
        else:
            self.txtclicpf.config(state="normal")
            self.btngravar.config(state="disabled")
            self.btnimprimir.config(state="disabled")

            
    def gravar(self):
        con = Database()
        num_venda = self.txtsacolaid.get()
        var_codcli = self.txtclicpf.get()
        var_vendedor = self.var_vendedor.get()
        var_total = float(self.txt_total.get())
        sql_venda_check = f"select * from sacola where id = {num_venda}"
        rs = con.encontrar_um(sql_venda_check)
        if rs:
            sql_text = f"UPDATE sacola SET cliente_cpf = {var_codcli}, vendedor_usuario = {var_vendedor} WHERE id = {num_venda};"
            con.executar(sql_text)
        else:                       
            if var_total > 0:
                sql_get_max_num_venda = "SELECT MAX(id) FROM sacola"
                rs_max_num = con.encontrar_um(sql_get_max_num_venda)
                if rs_max_num:
                    num_venda = rs_max_num[0][0] + 1
                else:
                    num_venda = 1

                sql_text = f"INSERT INTO sacola (id, cliente_cpf, vendedor_usuario) VALUES ({num_venda}, {var_codcli}, {var_vendedor});"
                print(sql_text)
                con.executar(sql_text)
                
                var_del = messagebox.askyesno("Imprimir", "Deseja Imprimir a Venda?", parent=self.master)
                if var_del:
                    self.imprimir()

                # Limpa os campos após o registro
                self.limpar()
                self.limpar_cab()
                self.numeracao()
                self.visualizar()
                self.total()
            
            
    def bus_venda(self,cod_compra, event=None):
        con = Database()
        sql_txt = "SELECT id, cliente_cpf, vendedor_usuario FROM sacola WHERE num_venda = :cod_compra"
        venda = con.encontrar_um(sql_txt, params={"cod_compra": cod_compra})
        if venda:
            sql_txt = '''SELECT A.lin_venda, A.codigo, B.descricao, A.quantidade, A.valor_unit, A.total
             FROM sacola_produto A
             JOIN produto B ON A.codigo = B.codigo
             WHERE A.id = :venda_id
             ORDER BY A.id, A.lin_venda'''
            linha_venda = con.encontrar_varios(sql_txt, params={"venda_id": venda[0]})
            if linha_venda:
                for linha in self.tree.get_children():
                    self.tree.delete(linha)
                for linha in linha_venda:
                    self.tree.insert("", tk.END, values=linha)
                    
                # config num_venda
                self.txtsacolaid.config(state="normal")
                self.txtsacolaid.delete(0, "end")
                self.txtsacolaid.insert(0, venda[0])
                self.txtsacolaid.config(state="disabled")
                #config txtclicpf
                self.txtclicpf.config(state="normal")
                self.txtclicpf.delete(0, "end")
                self.txtclicpf.insert(0, venda[1])
                self.txtclicpf.config(state="disabled")
                self.bus_cli()
                # config total_venda
                self.txt_total.config(state="normal")
                self.txt_total.delete(0, "end")
                self.txt_total.insert(0, venda[2])
                self.txt_total.config(state="disabled")
            
    def bus_cli(self, event=None):
        con = Database()
        var_codcli = self.txtclicpf.get()
        sql_txt = f"select nome from clientes where cpf = {var_codcli}"
        rs = con.encontrar_um(sql_txt)
        if rs:
            self.txtnomecli.config(state="normal")
            self.txtnomecli.delete(0, "end")
            self.txtnomecli.insert(0, rs[0])
            self.txtnomecli.config(state="disabled")
            self.txtcodprod.focus_set()
        else:
            messagebox.showwarning("Aviso", "Cliente Não Encontrado", parent=self.master)
            self.txtnomecli.config(state="normal")
            self.txtclicpf.delete(0, "end")
            self.txtnomecli.delete(0, "end")
            self.txtnomecli.config(state="disabled")
            self.txtclicpf.focus_set()

    def bus_prod(self, event=None):
        con = Database()
        var_codprod = self.txtcodprod.get()
        sql_txt = f"select descricao, valor from produtos_servicos where codigo = {var_codprod}"
        rs = con.encontrar_um(sql_txt)
        if rs:
            self.txtdescricao.config(state="normal")
            self.txtdescricao.delete(0, "end")
            self.txtdescricao.insert(0, rs[0])
            self.txtdescricao.config(state="disabled")
            self.lblvlrunit.config(state="normal")
            self.txtvlrunit.delete(0, "end")
            self.txtvlrunit.insert(0, rs[1])
            self.txtvlrunit.config(state="disabled")
            self.txtqtde.focus_set()
        else:
            self.txtcodprod.focus_set()
            messagebox.showwarning("Aviso", "Produto não Encontrado", parent=self.master)

    def entrar_qtde(self, event=None):
        try:
            self.txtvalor.config(state="normal")
            qtde = float(self.txtqtde.get())
            vlr_unit = float(self.txtvlrunit.get())
            if qtde > 0 and vlr_unit > 0:
                valor = qtde * vlr_unit
                self.txtvalor.delete(0, tk.END)
                self.txtvalor.insert(0, f"{valor:.2f}")
                self.btnincluir.focus_set()
            else:
                self.txtvalor.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos para quantidade e valor unitário.", parent=self.master)
        finally:
            self.txtvalor.config(state="readonly")

    def cancelar(self):
        var_del = messagebox.askyesno("Cancelar", "Deseja Cancelar a Venda?", parent=self.master)
        if var_del:
            con = Database()
            sacola_id = self.txtsacolaid.get()
            sql = "DELETE * FROM sacola_produto where sacola_id = :sacola_id "
            params = sacola_id
            con.executar(sql, params)
            self.limpar()
            self.limpar_cab()
            self.visualizar()
            self.total()
    
    def menu(self):
        self.master.mudar_para_menu()

    def hook_imprimir(self):
        # imprimir(self=self)
        pass