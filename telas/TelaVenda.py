# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from sqlalchemy import text
from services.imprimir import PedidoVenda
from services.VendaTreeview import VendaSacolaTreeview
from services.ClienteTreeview import ClienteTreeview
from services.ProdutoTreeview import ProdutoTreeview
from services.conexao import Database
# from services.func_imprimir_vendas import imprimir
from widgets.widgets_venda import create_widgets_vendas


class TelaVenda(tk.Frame):
    def __init__(self, master, vendedor):
        super().__init__(master)
        self.master = master
        self.vendedor = vendedor
        self.config(bg="#D8EAF7")
        self.create_widgets()        
        self.numeracao()
        self.tree.visualizar()
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
    #     tree = VendaTreeview(popup_busca)
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
        

    def abrir_popup_busca_cliente(self):
        popup_busca = tk.Toplevel(self.master)
        popup_busca.title("Buscar Cliente")
        popup_busca.geometry(f"{self.master.winfo_screenwidth()}x{self.master.winfo_screenheight()}")
        popup_busca.resizable(True, True)
        tree = ClienteTreeview(popup_busca)
        tree.tree.pack(fill="both", expand=True)

        def handle_duplo_click(event):
            valores = tree.duplo_click(event)
            print(f"Dados selecionados: {valores}")
            if valores:
                self.txtclicpf.delete(0, tk.END)
                self.txtclicpf.insert(0, valores[0])
            popup_busca.destroy()
            self.txtclicpf.focus()
            self.bus_cli()
        tree.tree.bind("<Double-1>", handle_duplo_click)

    def abrir_popup_busca_prodserv(self):
        popup_busca = tk.Toplevel(self.master)
        popup_busca.title("Buscar Produto")
        popup_busca.geometry(f"{self.master.winfo_screenwidth()}x{self.master.winfo_screenheight()}")
        popup_busca.resizable(True, True)
        tree = ProdutoTreeview(popup_busca)
        tree.tree.pack(fill="both", expand=True)

        def handle_duplo_click(event):
            valores = tree.duplo_click(event)
            print(f"Dados selecionados: {valores}")
            if valores:
                self.txtcodprod.delete(0, tk.END)
                self.txtcodprod.insert(0, valores[0])
                self.txtcodprod.focus()
            popup_busca.destroy()
            self.txtclicpf.focus()
            self.bus_prod()
        tree.tree.bind("<Double-1>", handle_duplo_click)

    def numeracao(self):
        con = Database()
        self.txtsacolaid.config(state="normal")

        # Buscar sacolas onde vendedor ou cliente estão nulos
        encontrar_nulo = text('''SELECT id, vendedor_usuario, cliente_cpf FROM sacolas 
                                WHERE vendedor_usuario IS NULL OR cliente_cpf IS NULL;''')
        dados_nulo = con.encontrar_varios(encontrar_nulo)

        if dados_nulo:
            print(f"Sacola encontrada com valores nulos: {dados_nulo}")
            sacola_id, vendedor, cliente = tuple(dados_nulo[0])  # Pega o primeiro registro válido
            
            # Atualizar txtsacolaid
            self.txtsacolaid.delete(0, "end")
            self.txtsacolaid.insert(0, sacola_id)
            
            # Atualizar vendedor se existir
            if vendedor:
                self.txtvendedor.delete(0, "end")
                self.txtvendedor.insert(0, vendedor)
                self.txtvendedor.config(state="disabled")
            else:
                self.txtvendedor.delete(0, "end")
                self.txtvendedor.insert(0, self.vendedor)
                self.txtvendedor.config(state="disabled")            
            # Atualizar cliente se existir
            if cliente:
                self.txtclicpf.delete(0, "end")
                self.txtclicpf.insert(0, cliente)
                self.bus_cli()
                self.txtclicpf.config(state="disabled")
        else:
            print("Nenhuma sacola com valores nulos encontrada. Criando nova sacola...")
            self.nova_sacola()

            
    def nova_sacola(self):
        con = Database()
        vendedor = self.vendedor        
        sql_txt = "SELECT COALESCE(MAX(id), 0) AS id FROM sacolas"
        rs = con.encontrar_um(sql_txt)
        
        if rs:
            num_venda = rs[0]
            if num_venda == 0:
                num_venda = 1
            else:
                num_venda += 1

            try:
                self.limpar_cab()
                self.txtsacolaid.config(state="normal")
                self.txtsacolaid.delete(0, "end")
                self.txtsacolaid.insert(0, num_venda)
                self.txtsacolaid.config(state="disabled")
                self.txtvendedor.delete(0, "end")
                self.txtvendedor.insert(0, vendedor)
                self.txtvendedor.config(state="disabled")


                sql_insert = text("INSERT INTO sacolas (id, vendedor_usuario) VALUES (:id, :vendedor)")
                resultado = con.executar(sql_insert, {"id": num_venda, "vendedor": vendedor})

                if resultado:
                    print(f"Nova sacola criada com num_venda: {num_venda}")
                else:
                    print("Erro ao inserir a nova sacola no banco.")

                self.tree.limpar_arv()
                self.txtsacolaid.delete(0, "end")
                self.txtsacolaid.insert(0, num_venda)
                print(f"Campo txtsacolaid atualizado para: {num_venda}")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao criar nova sacola: {e}")
                return
            


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
        self.txtnomecli.config(state="disabled")
        self.txtsacolaid.config(state="disabled")
        self.txtclicpf.focus_set()
        
    def validar_cab(self)-> bool:
        num_venda= self.txtsacolaid.get()
        cpf_cli= self.txtclicpf.get()
        nome_cli=self.txtnomecli.get()
        if not num_venda or not cpf_cli or not nome_cli:
            return False
        else:
            return True

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
        self.tree.visualizar()
        self.total()

    def excluir(self):
        con = Database()
        txtsacolaid = self.txtsacolaid.get()
        item = self.tree.limpar_lin()
        print("Item retornado:", item)
        
        try:
            lin_venda = item['values'][0]
            sql_text = text('''DELETE FROM sacola_produto WHERE sacola_id = :sacola_id AND lin_venda = :lin_venda''')
            params = {
                'sacola_id': txtsacolaid,
                'lin_venda': lin_venda
            }

            if con.executar(sql_text, params):
                self.tree.visualizar()
                self.total()
            else:
                messagebox.showerror("Erro", "Falha ao executar a exclusão.", parent=self.master)

        except Exception as e:
            messagebox.showwarning("Aviso", f"Erro ao excluir: {e}", parent=self.master)


    def excluir_inic(self):
        con = Database()
        num_venda = self.txtsacolaid.get()
        try:
            sql_delete_produtos = text("DELETE FROM sacola_produto WHERE sacola_id = :sacola_id")
            con.executar(sql_delete_produtos, {'sacola_id': num_venda})
            print(f"Sacola {num_venda} e seus produtos foram excluídos com sucesso!")
        except Exception as e:
            print(f"Erro ao excluir sacola e produtos: {e}")

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
        var_total = float(self.txt_total.get())
        sql_venda_check = f"select * from sacolas where id = {num_venda}"
        rs = con.encontrar_um(sql_venda_check)
        if self.validar_cab():
            if rs:
                sql_text = text(f"UPDATE sacolas SET cliente_cpf = {var_codcli}, vendedor_usuario = '{self.vendedor}' WHERE id = {num_venda};")
                con.executar(sql_text)
                messagebox.showwarning("Sucesso", f"{self.vendedor}, dados atualizado com sucesso", parent=self.master)
                var_continuar = messagebox.askyesno("Continuar", "Deseja incluir nova Venda?", parent=self.master)
                if var_continuar:
                    self.nova_sacola()
            else:                       
                if var_total > 0:
                    sql_get_max_num_venda = "SELECT MAX(id) FROM sacola"
                    rs_max_num = con.encontrar_um(sql_get_max_num_venda)
                    if rs_max_num:
                        num_venda = rs_max_num[0][0] + 1
                    else:
                        num_venda = 1
                    sql_text = text(f"INSERT INTO sacolas (id, cliente_cpf, vendedor_usuario) VALUES ({num_venda}, {var_codcli}, {self.vendedor});")
                    print(sql_text)
                    con.executar(sql_text)
                    var_del = messagebox.askyesno("Imprimir", "Deseja Imprimir a Venda?", parent=self.master)
                    if var_del:
                        self.imprimir()
                    self.limpar()
                    self.limpar_cab()
                    self.numeracao()
                    self.tree.visualizar()
                    self.total()
        else:
            messagebox.showwarning("Aviso", "Favor preencher os campos do cabeçalho", parent=self.master)
            
            
            
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
            self.numeracao()
            self.tree.visualizar()
            self.total()
            self.txtsacolaid.config(state="disabled")

    
    def menu(self):
        self.master.trocar_para_menu(self.vendedor)

    def hook_imprimir(self):
        pedido = PedidoVenda(self.vendedor, self.txtsacolaid, self.txtclicpf, self.txtnomecli, self.tree, self.txt_total)
        pedido.imprimir_pdf()