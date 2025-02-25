# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime

from sqlalchemy import func, or_, text
from model.Cliente import Cliente
from model.ProdutoServico import ProdutoServico
from model.Sacola import Sacola, SacolaProduto
from model.Vendedor import Role
from services.PedidoVenda import PedidoVenda
from services.VendaTreeview import VendaSacolaTreeview
from services.SacolaTreeview import SacolaTreeview
from services.ClienteTreeview import ClienteTreeview
from services.ProdutoTreeview import ProdutoTreeview
from services.conexao import Database
from telas.LoginPopup import LoginPopup
from widgets.widgets_venda import create_widgets_vendas


class TelaVenda(tk.Frame):
    def __init__(self, master, vendedor, role):
        super().__init__(master)
        self.master = master
        self.vendedor = vendedor
        self.role = role
        self.config(bg="#D8EAF7")
        self.con = Database().SessionLocal()
        self.create_widgets()        
        self.numeracao()
        self.tree.visualizar()
        self.total()
        self.txtsacolaid.config(state="disabled")
        self.txtclicpf.focus_set()

    def create_widgets(self):
        create_widgets_vendas(self=self)
        self.tree = VendaSacolaTreeview(self)

        
    def abrir_popup_busca_vendas(self):
        if self.validar_role():
            popup_busca = tk.Toplevel(self.master)
            popup_busca.title("Buscar vendas")
            popup_busca.geometry(f"{self.master.winfo_screenwidth()}x{self.master.winfo_screenheight()}")
            popup_busca.resizable(True, True)
            tree = SacolaTreeview(popup_busca)
            tree.tree.pack(fill="both", expand=True)
            def handle_duplo_click(event):
                valores = tree.duplo_click(event)
                print(f"Dados selecionados: {valores}")
                if valores:
                    self.txtsacolaid.delete(0, tk.END)
                    self.txtsacolaid.insert(0, valores[0])
                popup_busca.destroy()
                self.bus_venda(cod_compra=valores[0])
            tree.tree.bind("<Double-1>", handle_duplo_click)
            pass
        else:
            messagebox.showinfo("Acesso negado", "Acesso não permitido.")

        

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
        self.txtsacolaid.config(state="normal")

        sacola_vazia = self.con.query(Sacola).filter(
            or_(Sacola.vendedor_usuario.is_(None), Sacola.cliente_cpf.is_(None))
        ).first()
        
        if sacola_vazia:
            print(f"Sacola encontrada com valores nulos: {sacola_vazia.__repr__}")
                        
            self.txtsacolaid.delete(0, "end")
            self.txtsacolaid.insert(0, sacola_vazia.id)
            self.txtsacolaid.config(state="disabled")
            
            # Atualizar vendedor se existir
            if sacola_vazia.vendedor_usuario:
                self.txtvendedor.delete(0, "end")
                self.txtvendedor.insert(0, sacola_vazia.vendedor_usuario)
                self.txtvendedor.config(state="disabled")
            else:
                self.txtvendedor.delete(0, "end")
                self.txtvendedor.insert(0, self.vendedor)
                self.txtvendedor.config(state="disabled")            
            # Atualizar cliente se existir
            if sacola_vazia.cliente_cpf:
                self.txtclicpf.delete(0, "end")
                self.txtclicpf.insert(0, sacola_vazia.cliente_cpf)
                self.bus_cli()
                self.txtclicpf.config(state="disabled")
        else:
            print("Nenhuma sacola com valores nulos encontrada. Criando nova sacola...")
            self.nova_sacola()

            
    def nova_sacola(self):
        vendedor = self.vendedor        
        rs = self.con.query(func.coalesce(func.max(Sacola.id),0)).scalar()
        
        if rs:
            num_venda = rs
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


                sacola = Sacola(cliente_id=None, vendedor_id=self.vendedor)
                self.con.add(sacola)
                self.con.commit()
        
                if sacola.id:
                    print(f"Nova sacola criada com num_venda: {sacola.id}")
                else:
                    print("Erro ao inserir a nova sacola no banco.")

                self.tree.limpar_arv()
                self.txtsacolaid.delete(0, "end")
                self.txtsacolaid.insert(0, sacola.id)

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
            sacola_produto = SacolaProduto(
                sacola_id=num_venda,
                produto_id=var_codprod,
                quantidade=var_qtde,
                valor_unit=var_vlrunit,
                total=var_valor,
                session=self.con
            )
            self.con.add(sacola_produto)
            self.con.commit()
            if sacola_produto.lin_venda:
                    messagebox.showinfo("Sucesso", "Linha gravada com sucesso!", parent=self.master)
                    self.limpar()
            else:
                messagebox.showerror("Erro", "Falha ao gravar a linha.", parent=self.master)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gravar linha: {e}", parent=self.master)

    def finalizar_linha(self, event=None):
        self.gravar_lin()
        self.tree.visualizar()
        self.total()

    def excluir(self):
        txtsacolaid = self.txtsacolaid.get()
        item = self.tree.limpar_lin()
        lin_venda = item['values'][0]

        lin_deletada = self.con.query(SacolaProduto).filter(
            SacolaProduto.sacola_id == txtsacolaid,
            SacolaProduto.lin_venda == lin_venda
        ).delete(synchronize_session=False)
        
        self.con.commit()
        
        if lin_deletada:
            self.tree.visualizar()
            self.total()
            print(f"{lin_deletada} registros deletados com sucesso.")
        else:
            print("Nenhum registro encontrado para deletar.")

    def excluir_inic(self):
        num_venda = self.txtsacolaid.get()
        try:
            self.con.query(SacolaProduto).filter(SacolaProduto.sacola_id == num_venda).delete(synchronize_session=False)
            self.con.query(Sacola).filter(Sacola.id == num_venda).delete(synchronize_session=False)
            self.con.commit()
            print(f"Sacola {num_venda} e seus produtos foram excluídos com sucesso!")
        except Exception as e:
            print(f"Erro ao excluir sacola e produtos: {e}")

    def total(self):
        num_venda = self.txtsacolaid.get()
        total = (
        self.con.query(func.coalesce(func.sum(SacolaProduto.total), 0))
        .filter(SacolaProduto.sacola_id == num_venda)
        .scalar()
        )
        if total:
            total_valor = total
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
        num_venda = self.txtsacolaid.get()
        clicpf = self.txtclicpf.get()
        
        venda_db = self.con.query(Sacola).filter(Sacola.id == num_venda).first()

        if self.validar_cab():
            if venda_db:
                venda_db.cliente_cpf = clicpf
                venda_db.vendedor_usuario = self.vendedor
                venda_db.time_stamp = datetime.now()
                self.con.commit()
                self.baixa_estoque()

                messagebox.showinfo("Sucesso", f"{self.vendedor}, dados atualizados com sucesso", parent=self.master)
                var_del = messagebox.askyesno("Imprimir", "Deseja Imprimir a Venda?", parent=self.master)
                if var_del:
                    self.hook_imprimir()
                var_continuar = messagebox.askyesno("Continuar", "Deseja incluir nova Venda?", parent=self.master)
                if var_continuar:
                    self.nova_sacola()
                else:
                    self.numeracao()
        else:
            messagebox.showwarning("Aviso", "Favor preencher os campos do cabeçalho", parent=self.master)
            
    def baixa_estoque(self):
        con = Database()
        for child in self.tree.tree.get_children():
            codigo = str(self.tree.tree.item(child)["values"][1])
            quantidade = str(self.tree.tree.item(child)["values"][3])
            self.con.query(ProdutoServico).filter(ProdutoServico.codigo == codigo).update(
                {ProdutoServico.quantidade: ProdutoServico.quantidade - quantidade}
            )
        self.con.commit()
            
            
    def bus_venda(self,cod_compra, event=None):
        con = Database()
        sql_txt = "SELECT id, cliente_cpf, vendedor_usuario FROM sacolas WHERE id = :cod_compra"
        venda = con.encontrar_um(sql_txt, params={"cod_compra": cod_compra})
        if venda:
            sql_txt = '''SELECT A.lin_venda, A.produto_id, B.descricao, A.quantidade, A.valor_unit, A.total
             FROM sacola_produto A
             JOIN produtos_servicos B ON A.produto_id = B.codigo
             WHERE A.sacola_id = :venda_id
             ORDER BY A.sacola_id, A.lin_venda'''
            linha_venda = con.encontrar_varios(sql_txt, params={"venda_id": venda[0]})
            if linha_venda:
                for linha in self.tree.tree.get_children():
                    self.tree.tree.delete(linha)
                for linha in linha_venda:
                    self.tree.tree.insert("", tk.END, values=tuple(linha))
                    
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
        var_codcli = self.txtclicpf.get()
        cliente = self.con.query(Cliente).filter(Cliente.cpf == var_codcli).first()
        if cliente:
            self.txtnomecli.config(state="normal")
            self.txtnomecli.delete(0, "end")
            self.txtnomecli.insert(0, cliente.nome)
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
        produto = self.con.query(ProdutoServico).filter(ProdutoServico.codigo == var_codprod).first()
        if produto:
            self.txtdescricao.config(state="normal")
            self.txtdescricao.delete(0, "end")
            self.txtdescricao.insert(0, produto.descricao)
            self.txtdescricao.config(state="disabled")
            self.lblvlrunit.config(state="normal")
            self.txtvlrunit.delete(0, "end")
            self.txtvlrunit.insert(0, produto.valor)
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
            sacola_id = self.txtsacolaid.get()
            sql = "DELETE * FROM sacola_produto where sacola_id = :sacola_id "
            self.con.query(SacolaProduto).filter(SacolaProduto.sacola_id == sacola_id).delete()
            self.limpar()
            self.limpar_cab()
            self.numeracao()
            self.tree.visualizar()
            self.total()
            self.txtsacolaid.config(state="disabled")

    
    def menu(self):
        self.con.close()
        self.master.trocar_para_menu(self.vendedor, self.role)

    def hook_imprimir(self):
        pedido = PedidoVenda(self.vendedor, self.txtsacolaid, self.txtclicpf, self.txtnomecli, self.tree, self.txt_total)
        pedido.imprimir_pdf()
        
    def validar_role(self) -> bool:
        """Verifica se o usuário tem uma role permitida."""
        return self.role in {Role.ADMIN.value, Role.GERENTE.value}

    def tela_alerta(self) -> bool:
        """Solicita login adicional para acessar a tela, se necessário."""
        var_sair = messagebox.askyesno("Permissões necessárias", "Solicite ao superior login para acesso...")
        if var_sair:
            login_popup = LoginPopup(self.master)
            self.master.wait_window(login_popup.popup_busca)

            if login_popup.login_sucesso:
                return True
            else:
                messagebox.showinfo("Acesso negado", "Acesso não permitido.")
                return False
        return False