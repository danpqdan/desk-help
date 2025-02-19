import tkinter as tk
from sqlalchemy import text
from sqlalchemy.sql import text
from services.FaturamentoTreeview import FaturamentoTreeview
from services.conexao import Database
from widgets.widgets_faturamento import create_widgets_faturamento, obter_vendedores

class TelaFaturamento(tk.Frame):
    def __init__(self, master, vendedor, role):
        super().__init__(master)
        self.master = master
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
        # Obtendo os filtros
        filtros = []
        params = {}

        # Filtro por Data
        data_inicial = self.datainicial.get_date()
        data_final = self.datafinal.get_date()

        if data_inicial and data_final:
            filtros.append("DATE(s.time_stamp) BETWEEN :data_inicial AND :data_final")
            params['data_inicial'] = data_inicial.strftime('%Y-%m-%d')
            params['data_final'] = data_final.strftime('%Y-%m-%d')

        # Filtro por Vendedor
        vendedor, valido_vendedor = self.filtrar_por_vendedor()
        if valido_vendedor:
            filtros.append("s.vendedor_usuario = :vendedor")
            params['vendedor'] = vendedor

        cpf, valido_cliente = self.filtrar_por_cliente()
        if valido_cliente:
            filtros.append("s.cliente_cpf = :cpf")
            params['cpf'] = cpf
        

        sql = """
        SELECT 
            s.id, 
            s.vendedor_usuario, 
            s.cliente_cpf, 
            COUNT(sp.sacola_id) AS 'Qts produtos', 
            SUM(sp.total) AS 'total', 
            s.time_stamp
        FROM 
            sacolas s
        JOIN 
            sacola_produto sp ON s.id = sp.sacola_id
        """

        if filtros:
            sql += " WHERE " + " AND ".join(filtros)

        sql += " GROUP BY s.id, s.vendedor_usuario, s.cliente_cpf, s.time_stamp"

        try:
            con = Database()
            resultados = con.encontrar_varios(sql, params)

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
            