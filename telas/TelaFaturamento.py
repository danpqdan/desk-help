import tkinter as tk

from sqlalchemy import text
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
        self.create_widgets()
    
    def create_widgets(self):
        create_widgets_faturamento(self)
        self.tree = FaturamentoTreeview(self)

    def filtrar_por_data(self):
        # Obtendo as datas do DateEntry
        data_inicial = self.datainicial.get_date()
        data_final = self.datafinal.get_date()

        # Convertendo para o formato 'YYYY-MM-DD' para comparação
        data_inicial_str = data_inicial.strftime('%Y-%m-%d')
        data_final_str = data_final.strftime('%Y-%m-%d')

        # Consulta SQL corrigida
        query = text("""
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
        WHERE 
            DATE(s.time_stamp) BETWEEN :data_inicial AND :data_final
        GROUP BY 
            s.id, s.vendedor_usuario, s.cliente_cpf, s.time_stamp
        """)

        try:
            con = Database()
            params = {'data_inicial': data_inicial_str, 'data_final': data_final_str}
            resultados = con.encontrar_varios(query, params)
            
            for item in self.tree.tree.get_children():
                self.tree.tree.delete(item)

            for linha in resultados:
                self.tree.tree.insert("", "end", values=tuple(linha))

        except Exception as e:
            print(f"Erro ao executar a consulta: {e}")

