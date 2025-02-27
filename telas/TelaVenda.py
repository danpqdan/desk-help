# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime

from sqlalchemy import func, or_, text
from sqlalchemy.exc import SQLAlchemyError
from model.Cliente import Cliente
from model.ProdutoServico import ProdutoServico
from model.Sacola import Sacola, SacolaProduto, Status
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
        self.db = Database()
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

        def duplo_click_invalido(event):
            valores = tree.duplo_click_invalido(event)
            print(f"Dados selecionados: {valores}")
            if valores:
                self.txtcodprod.delete(0, tk.END)
                self.txtcodprod.insert(0, valores[0])
                self.txtcodprod.focus()
            popup_busca.destroy()
            self.txtclicpf.focus()
            self.bus_prod()
        tree.tree.bind("<Double-1>", duplo_click_invalido)

    def numeracao(self):
        self.txtsacolaid.config(state="normal")
        with self.db.get_conexao() as session:
            sacola_vazia = session.query(Sacola).filter(
                or_(Sacola.vendedor_usuario.is_(None), Sacola.status == Status.CANCELADA)).first()
            
            if sacola_vazia:
                self.tree.limpar_arv()
                self.txtsacolaid.delete(0, "end")
                self.txtsacolaid.insert(0, sacola_vazia.id)
                self.txtsacolaid.config(state="disabled")
                if sacola_vazia.vendedor_usuario:
                    self.txtvendedor.delete(0, "end")
                    self.txtvendedor.insert(0, sacola_vazia.vendedor_usuario)
                    self.txtvendedor.config(state="disabled")
                else:
                    self.txtvendedor.delete(0, "end")
                    self.txtvendedor.insert(0, self.vendedor)
                    self.txtvendedor.config(state="disabled")            
                if sacola_vazia.cliente_cpf:
                    self.txtclicpf.config(state="normal")
                    self.txtnomecli.config(state="normal")
                    self.txtclicpf.delete(0, "end")
                    self.txtnomecli.delete(0, "end")
                    self.txtclicpf.insert(0, "")
                    self.txtnomecli.insert(0, "")
                    self.txtclicpf.config(state="disabled")
            else:
                print("Nenhuma sacola com valores nulos encontrada. Criando nova sacola...")
                self.nova_sacola()

            
    def nova_sacola(self):
        vendedor = self.vendedor
        with self.db.get_conexao() as session:        
            rs = session.query(func.coalesce(func.max(Sacola.id),0)).scalar()    
            if rs:
                num_venda = rs + 1 if rs else 1
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
                    session.add(sacola)
            
                    if sacola.id:
                        print(f"Nova sacola criada com num_venda: {sacola.id}")
                    else:
                        print("Erro ao inserir a nova sacola no banco.")

                    self.tree.limpar_arv()
                    self.txtsacolaid.delete(0, "end")
                    self.txtsacolaid.insert(0, sacola.id)

                except SQLAlchemyError as e:
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
        
        with self.db.get_conexao() as session:
            if not self.baixa_estoque(var_codprod, int(var_qtde)):
                messagebox.showerror("Erro", "Item não adicionado erro no estoque.", parent=self.master)
                return

            try:
                sacola_produto = SacolaProduto(
                    sacola_id=num_venda,
                    produto_id=var_codprod,
                    quantidade=var_qtde,
                    valor_unit=var_vlrunit,
                    total=var_valor,
                    session=session
                )
                
                session.add(sacola_produto)
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
        with self.db.get_conexao() as session:
            lin_deletada = session.query(SacolaProduto).filter(
                SacolaProduto.sacola_id == txtsacolaid,
                SacolaProduto.lin_venda == lin_venda
            ).delete(synchronize_session=False)
                        
            if lin_deletada:
                self.repor_estoque(produto_id=item['values'][1], quantidade=int(item['values'][3]))
                print(f"{lin_deletada} registros deletados com sucesso.")
            else:
                print("Nenhum registro encontrado para deletar.")
                
        self.tree.visualizar()
        self.total()

    def excluir_inic(self):
        num_venda = self.txtsacolaid.get()
        with self.db.get_conexao() as session:
            try:
                session.query(SacolaProduto).filter(SacolaProduto.sacola_id == num_venda).delete(synchronize_session=False)
                session.query(Sacola).filter(Sacola.id == num_venda).delete(synchronize_session=False)
                print(f"Sacola {num_venda} e seus produtos foram excluídos com sucesso!")
            except Exception as e:
                print(f"Erro ao excluir sacola e produtos: {e}")

    def total(self):
        num_venda = self.txtsacolaid.get()
        with self.db.get_conexao() as session:
            total = (
            session.query(func.coalesce(func.sum(SacolaProduto.total), 0))
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
        var_continuar = messagebox.askyesno("Continuar", "Esse processo encerrará a venda. Continuar?", parent=self.master)
        if not var_continuar:
            return

        num_venda = self.txtsacolaid.get()
        clicpf = self.txtclicpf.get()

        if not self.validar_cab():
            messagebox.showwarning("Aviso", "Favor preencher os campos do cabeçalho", parent=self.master)
            return

        with self.db.get_conexao() as session:
            venda_db = session.query(Sacola).filter(Sacola.id == num_venda).first()

            if not venda_db:
                messagebox.showwarning("Aviso", "Venda não encontrada", parent=self.master)
                return

            venda_db.cliente_cpf = clicpf
            venda_db.vendedor_usuario = self.vendedor
            venda_db.time_stamp = datetime.now()
            venda_db.status = Status.FINALIZADA

            self.btngravar.config(state="disabled")
            self.btncancelar.config(state="disabled")
            messagebox.showinfo("Sucesso", f"{self.vendedor}, dados atualizados com sucesso", parent=self.master)

            var_del = messagebox.askyesno("Imprimir", "Deseja Imprimir a Venda?", parent=self.master)
            if var_del:
                self.hook_imprimir()
                self.numeracao()
            self.numeracao()


            
    def baixa_estoque(self, produto_id, quantidade):
        with self.db.get_conexao() as session:
            try:
                produto = session.query(ProdutoServico).filter(ProdutoServico.codigo == produto_id).first()
                
                if produto is None:
                    messagebox.showerror("Erro", f"Produto com código {produto_id} não encontrado.")
                    session.rollback()
                    return
                
                if produto.quantidade < quantidade:
                    messagebox.showerror("Erro", f"Estoque insuficiente para o produto {produto.descricao}. Quantidade: {produto.quantidade}")
                    session.rollback()
                    return

                session.query(ProdutoServico).filter(ProdutoServico.codigo == produto_id).update(
                    {ProdutoServico.quantidade: ProdutoServico.quantidade - quantidade}
                )

                return True
            except Exception as e:
                session.rollback()
                messagebox.showerror("Erro", f"Erro ao atualizar o estoque: {e}")
                
            
    def bus_venda(self, cod_compra, event=None):
        with self.db.get_conexao() as session:
            venda = session.query(Sacola).filter(Sacola.id == cod_compra).first()
            if venda:
                linha_venda = (
                    session.query(
                        SacolaProduto.lin_venda,
                        SacolaProduto.produto_id,
                        ProdutoServico.descricao,
                        SacolaProduto.quantidade,
                        SacolaProduto.valor_unit,
                        SacolaProduto.total
                    )
                    .join(ProdutoServico, SacolaProduto.produto_id == ProdutoServico.codigo)
                    .filter(SacolaProduto.sacola_id == venda.id)
                    .order_by(SacolaProduto.sacola_id, SacolaProduto.lin_venda)
                    .all()
                )
                if linha_venda:
                    for linha in self.tree.tree.get_children():
                        self.tree.tree.delete(linha)
                    for linha in linha_venda:
                        self.tree.tree.insert("", tk.END, values=tuple(linha))
                    
                    # config num_venda
                    self.txtsacolaid.config(state="normal")
                    self.txtsacolaid.delete(0, "end")
                    self.txtsacolaid.insert(0, venda.id)
                    self.txtsacolaid.config(state="disabled")
                    # config txtclicpf
                    self.txtclicpf.config(state="normal")
                    self.txtclicpf.delete(0, "end")
                    self.txtclicpf.insert(0, venda.cliente_cpf)
                    self.txtclicpf.config(state="disabled")
                    self.bus_cli()
            self.total()
            
    def bus_cli(self, event=None):
        var_codcli = self.txtclicpf.get()
        with self.db.get_conexao() as session:
            cliente = session.query(Cliente).filter(Cliente.cpf == var_codcli).first()
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
        var_codprod = self.txtcodprod.get()
        with self.db.get_conexao() as session:
            produto = session.query(ProdutoServico).filter(ProdutoServico.codigo == var_codprod).first()
        
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
            with self.db.get_conexao() as session:
                sacola = session.query(Sacola).filter(Sacola.id == sacola_id).first()
                if not sacola:
                    messagebox.showerror("Erro", "Sacola não encontrada.", parent=self.master)
                    return
                try:
                    self.repor_estoque(sacola_id=sacola_id)
                    sacola.status = Status.CANCELADA
                    sacola.cliente_cpf = None
                    sacola.vendedor_id = None
                    session.add(sacola)
                    messagebox.showinfo("Sucesso", "Venda cancelada com sucesso.", parent=self.master)
                    self.limpar()
                    self.limpar_cab()
                    self.numeracao()
                    self.tree.visualizar()
                    self.total()
                    self.txtsacolaid.config(state="disabled")

                except Exception as e:
                    session.rollback()
                    messagebox.showerror("Erro", f"Erro ao cancelar a venda: {e}", parent=self.master)

                
                
    def repor_estoque(self, sacola_id=None, produto_id=None, quantidade=None):
        """Repõe o estoque ao cancelar uma venda ou repõe o estoque de um único produto."""
        with self.db.get_conexao() as session:
            try:
                
                # Atualiza a linha das vendas
                if produto_id and quantidade is not None:
                    produto = session.query(ProdutoServico).filter(ProdutoServico.codigo == produto_id).first()
                    
                    if produto:
                        produto.quantidade += quantidade
                        session.add(produto)
                        messagebox.showinfo("Sucesso", f"Estoque do produto {produto_id} reposto com sucesso.", parent=self.master)
                    else:
                        messagebox.showwarning("Aviso", f"Produto com código {produto_id} não encontrado.", parent=self.master)
                        
                    return
                
                # Atualiza a sacola com todas as linhas
                elif sacola_id:
                    produtos_venda = session.query(SacolaProduto).filter(SacolaProduto.sacola_id == sacola_id).all()
                    
                    if not produtos_venda:
                        messagebox.showwarning("Aviso", "Nenhum produto encontrado para reposição de estoque.", parent=self.master)
                        return

                    produto_ids = [item.produto_id for item in produtos_venda]
                    produtos = session.query(ProdutoServico).filter(ProdutoServico.codigo.in_(produto_ids)).all()
                    produtos_dict = {produto.codigo: produto for produto in produtos}

                    for item in produtos_venda:
                        produto = produtos_dict.get(item.produto_id)
                        if produto:
                            produto.quantidade += item.quantidade
                            session.add(produto)
                        session.delete(item)
                        
                    messagebox.showinfo("Sucesso", "Estoque reposto com sucesso.", parent=self.master)


            except Exception as e:
                session.rollback()
                messagebox.showerror("Erro", f"Erro ao repor o estoque: {e}", parent=self.master)


    
    def menu(self):
        self.master.trocar_para_menu(self.vendedor, self.role)

    def hook_imprimir(self):
        pedido = PedidoVenda(self.vendedor, self.txtsacolaid.get(), self.txtclicpf.get(), self.txtnomecli.get(), self.tree, self.txt_total.get())
        pedido.gerar_pdf_pedido()
        
    def validar_role(self) -> bool:
        """Verifica se o usuário tem uma role permitida."""
        return self.role in {Role.ADMIN, Role.GERENTE}

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