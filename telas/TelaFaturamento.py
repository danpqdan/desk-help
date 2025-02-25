import tkinter as tk
from sqlalchemy import and_, func, text
from sqlalchemy.sql import text
from model.Sacola import Sacola, SacolaProduto
from services.FaturamentoTreeview import FaturamentoTreeview
from services.RelatorioFaturamento import RelatorioFaturamento
from services.conexao import Database
from widgets.widgets_faturamento import create_widgets_faturamento, obter_vendedores

class TelaFaturamento(tk.Frame):
    def __init__(self, master, vendedor, role):
        super().__init__(master)
        self.master = master
        self.con = Database().SessionLocal()
        self.vendedor = vendedor
        self.role = role
        self.vendedores = []
        self.clientes = []
        self.todos_clientes = None
        self.todos_vendedores = None
        self.create_widgets()
    
    def create_widgets(self):
        create_widgets_faturamento(self)
        self.tree = FaturamentoTreeview(self)

    

    def filtrar_dados(self):
        try:
            query = self.con.query(
                Sacola.id,
                Sacola.vendedor_usuario,
                Sacola.cliente_cpf,
                func.count(SacolaProduto.sacola_id).label("Qts produtos"),
                func.sum(SacolaProduto.total).label("Total"),
                Sacola.time_stamp
            ).join(SacolaProduto, Sacola.id == SacolaProduto.sacola_id)
            
            filtros = []

            data_inicial = self.datainicial.get_date()
            data_final = self.datafinal.get_date()
            if data_inicial and data_final:
                filtros.append(Sacola.time_stamp.between(data_inicial, data_final))

            vendedor, valido_vendedor = self.filtrar_por_vendedor()
            if valido_vendedor and vendedor != 'Todos':
                filtros.append(Sacola.vendedor_usuario == vendedor)

            cpf, valido_cliente = self.filtrar_por_cliente()
            if valido_cliente:
                filtros.append(Sacola.cliente_cpf == cpf)
                
            if filtros:
                query = query.filter(and_(*filtros))
            
            query = query.group_by(Sacola.id, Sacola.vendedor_usuario, Sacola.cliente_cpf, Sacola.time_stamp)
            resultados = query.all()

            self.filtrar_total(resultados)
            self.filtrar_ticket_medio(resultados)
            
            self.txtdatainicial.delete(0, "end")
            self.txtdatainicial.insert(0, data_inicial)
            self.txtdatainicial.config(state="disabled")
            self.txtdatafinal.delete(0, "end")
            self.txtdatafinal.insert(0, data_final)
            self.txtdatafinal.config(state="disabled")
            
            for item in self.tree.tree.get_children():
                self.tree.tree.delete(item)

            for linha in resultados:
                self.tree.tree.insert("", "end", values=tuple(linha))
                
                    
        except Exception as e:
            print(f"Erro ao executar a consulta: {e}")
            

    def filtrar_por_vendedor(self):
        cmbvendedor = self.cmbvendedor.get()
        
        if cmbvendedor:
            return cmbvendedor, True
        else:
            return self.vendedores, False
        
    def filtrar_por_cliente(self):
        cliente = self.cliente.get()
        print(cliente)
        con = Database()
        if cliente:
            query = f"SELECT cpf FROM clientes WHERE nome = '{cliente}'"
            cpf = con.encontrar_um(query)
            return cpf[0], True
        else: 
            cpf = con.encontrar_varios('select from clientes')
            return self.clientes, False
        
    def filtrar_total(self, dados):
        try:
            total = sum(linha[4] for linha in dados if linha[4] is not None)

            self.txtvalortotal.config(state="normal")
            self.txtvalortotal.delete(0, "end")
            self.txtvalortotal.insert(0, f"{total:.2f}")
            self.txtvalortotal.config(state="disabled")
        except:
            pass
        
    def filtrar_ticket_medio(self, dados):
        """Calcula o ticket médio a partir dos resultados já filtrados."""
        try:
            total = 0
            total_produtos = 0

            for linha in dados:
                if linha[4] is not None:
                    total += linha[4]
                if linha[3] is not None:
                    total_produtos += linha[3]

            if total_produtos > 0:
                ticket_medio = total / total_produtos
            else:
                ticket_medio = 0.0
            self.txtticket.config(state="normal")
            self.txtticket.delete(0, "end")
            self.txtticket.insert(0, f"{ticket_medio:.2f}")
            self.txtticket.config(state="disabled")

        except Exception as e:
            print(f"Erro ao calcular o ticket médio: {e}")
            
            
    def gerar_relatorio(self):
        relatorio = RelatorioFaturamento(
            self.vendedor,
            self.txtdatainicial,
            self.txtdatafinal,
            self.txtvalortotal,
            self.txtticket,
            self.cmbvendedor,
            self.cliente,
            self.tree.tree
        )
        relatorio.imprimir_pdf()
        

    
            