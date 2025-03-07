import sys
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import date
import os
import platform
from services.router_path import help_desk_pasta

class RelatorioFaturamento:
    def __init__(self, vendedor, txtdatainicial, txtdatafinal, txtvalortotal, txtticket, cmbvendedor, cliente, tree):
        self.vendedor = vendedor
        self.datainicial = txtdatainicial
        self.datafinal = txtdatafinal
        self.valortotal = txtvalortotal
        self.ticket = txtticket
        self.cmbvendedor = cmbvendedor
        self.cliente = cliente
        self.tree = tree

    def gerar_pdf_path(self):
        """Gera o caminho do arquivo PDF dinamicamente no mesmo diretório do executável"""
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        reports_dir = os.path.join(base_dir, 'relatorios')

        try:
            os.makedirs(reports_dir, exist_ok=True)
            print(f"Pasta criada: {reports_dir}")
        except Exception as e:
            print(f"Erro ao criar pasta: {e}")

        today = date.today().strftime("%Y-%m-%d")
        pdf_filename = f"relatorio_faturamento_{today}.pdf"
        pdf_path = os.path.join(reports_dir, pdf_filename)

        print(f"Arquivo será salvo em: {pdf_path}")

        return pdf_path

    def imprimir_pdf(self):
        pdf_path = self.gerar_pdf_path()

        today = date.today()
        d3 = today.strftime("%d/%m/%y")

        cnv = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4

        def desenhar_cabecalho():
            # Cabeçalho do PDF
            cnv.setFont('Times-Roman', 14)
            cnv.setFillColorRGB(0, 0, 255)
            cnv.drawImage(help_desk_pasta, 10, height - 50, width=50, height=50, mask='auto')
            cnv.setFont('Times-Roman', 14)
            cnv.setFillColorRGB(0, 0, 255)
            cnv.drawString(70, 810, "Desk-help")
            cnv.setFont('Times-Bold', 14)
            cnv.setFillColorRGB(0, 0, 0)
            cnv.drawString(250, 810, "Relatório de Vendas")
            cnv.setFont('Times-Roman', 14)
            cnv.setFillColorRGB(0, 0, 0)
            cnv.drawString(540, 810, d3)

            # Filtros
            cnv.setLineWidth(2)
            cnv.line(0, 790, 595, 790)
            cnv.setFont('Times-Roman', 12)
            cnv.drawString(10, 770, 'Gerado por: ' + self.vendedor)
            cnv.drawString(200, 770, 'Data inicial: ' + self.datainicial)
            cnv.drawString(400, 770, 'Data final: ' + self.datafinal)
            cnv.drawString(100, 750, 'Filtro por vendedor: ' + self.cmbvendedor.get())
            cnv.drawString(300, 750, 'Filtro por cliente: ' + self.cliente.get())

            # Vendas
            cnv.setLineWidth(1)
            cnv.line(0, 735, 595, 735)
            cnv.setFont('Times-Roman', 14)
            cnv.drawString(100, 719, "Ticket médio: " + self.ticket.get())
            cnv.drawString(300, 719, "Venda total: " + self.valortotal.get())

            cnv.setFont('Times-Roman', 12)
            cabecalho = ['Venda', 'Vendedor', 'cliente cpf', 'qts produtos', 'total', 'Ano/mes/dia - horario']
            x_positions = [10, 100, 180, 280, 380, 450]

            for i, texto in enumerate(cabecalho):
                cnv.drawString(x_positions[i], 680, texto)

            linha = 660
            return linha, x_positions

        linha, x_positions = desenhar_cabecalho()

        for child in self.tree.tree.get_children():
            valores = self.tree.tree.item(child)["values"]

            if linha < 50:
                cnv.showPage()
                linha, x_positions = desenhar_cabecalho()

            for i, valor in enumerate(valores):
                cnv.drawString(x_positions[i], linha, str(valor))

            linha -= 20

        cnv.showPage()
        cnv.save()

        if platform.system() == "Windows":
            os.startfile(pdf_path)
        else:
            os.system(f"xdg-open {pdf_path}")

