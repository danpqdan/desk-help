import os
import platform
import subprocess
import locale
import sys
import fitz
from datetime import date
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from services.router_path import help_desk_pasta, help_desk_regras_os

class PedidoVenda:
    def __init__(self, vendedor, txtsacolaid, txtclicpf, txtnomecli, tree, txt_total):
        self.vendedor = vendedor
        self.txtsacolaid = txtsacolaid
        self.txtclicpf = txtclicpf
        self.txtnomecli = txtnomecli
        self.tree = tree
        self.txt_total = txt_total
        
        
    def gerar_pdf_path(self):
        """Gera o caminho do arquivo PDF dinamicamente no mesmo diretório do executável"""
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        reports_dir = os.path.join(base_dir, 'vendas')

        try:
            os.makedirs(reports_dir, exist_ok=True)
            print(f"Pasta criada: {reports_dir}")
        except Exception as e:
            print(f"Erro ao criar pasta: {e}")
            
        
        today = date.today()
        d3 = today.strftime("%d-%m-%y")


        today = date.today().strftime("%Y-%m-%d")
        pdf_filename = f"relatorio_venda_{self.txtsacolaid}_{d3}.pdf"
        pdf_path = os.path.join(reports_dir, pdf_filename)

        print(f"Arquivo será salvo em: {pdf_path}")

        return pdf_path

    def gerar_pdf_pedido(self):
        """Gera e imprime um PDF com os detalhes do pedido de venda"""
        pdf_path = self.gerar_pdf_path()
        # Criar PDF
        today_formatted = date.today().strftime("%d/%m/%y")
        cnv = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4
        texto_regras = self.ler_pdf(help_desk_regras_os)

        # Cabeçalho
        cnv.setFont('Times-Roman', 14)
        cnv.setFillColorRGB(0, 0, 255)
        cnv.drawImage(help_desk_pasta, 10, height - 50, width=50, height=50, mask='auto')
        cnv.drawString(70, 810, "Desk-help")
        cnv.setFont('Times-Bold', 14)
        cnv.setFillColorRGB(0, 0, 0)
        cnv.drawString(250, height - 25, "Ordem de serviço")
        cnv.drawString(280, height - 38, "& venda")
        cnv.drawString(540, 810, today_formatted)

        # Informações do pedido
        cnv.line(0, 790, 595, 790)
        cnv.drawString(10, 760, f"Número do Pedido: {self.txtsacolaid}")
        cnv.drawString(200, 760, f"Data do Pedido: {today_formatted}")
        cnv.drawString(450, 760, f"Vendedor: {self.vendedor}")
        cnv.drawString(10, 745, f"CPF do Cliente: {self.txtclicpf}")
        cnv.drawString(200, 745, f"Nome do Cliente: {self.txtnomecli}")
        cnv.line(0, 720, 595, 720)

        # Tabela
        cabecalho = ["Cod. Prod", "Descrição", "Qts", "Valor Unitário", "Valor"]
        col_widths = [50, 280, 80, 100, 60]
        x_positions = [1, 70, 400, 450, 530]

        for i, texto in enumerate(cabecalho):
            cnv.drawString(x_positions[i], 700, texto)

        linha = 680
        for child in self.tree.tree.get_children():
            valores = self.tree.tree.item(child)["values"]
            for i, valor in enumerate(valores[1:]):
                if i == 2:
                    self.quebrar_texto(cnv, str(valor), x_positions[i], linha, col_widths[i])
                else:
                    cnv.drawString(x_positions[i], linha, str(valor))
            linha -= 20

        cnv.line(0, linha, 595, linha)
        linha -= 20

        # Total do pedido
        try:
            total_float = float(self.txt_total.strip())
        except ValueError:
            total_float = 0.0

        cnv.drawString(420, linha, "Total do Pedido ->")
        cnv.drawString(530, linha, locale.currency(total_float))
        
        # Regras do serviço
        linha -= 30
        cnv.setFont('Times-Roman', 10)
        self.quebrar_texto(cnv, texto_regras, 10, linha - 12, width)

        # Assinaturas
        cnv.line(100, 100, 200, 100)
        cnv.drawString(120, 80, "Ass: desk-help")
        cnv.line(300, 100, 500, 100)
        cnv.drawString(320, 80, f"Ass: {self.txtnomecli}")

        cnv.save()

        if platform.system() == "Windows":
            os.startfile(pdf_path)
        elif platform.system() == "Darwin":
            subprocess.run(["open", pdf_path])
        else:
            subprocess.run(["xdg-open", pdf_path])

    def ler_pdf(self, caminho_pdf):
        """Lê o conteúdo de um arquivo PDF"""
        texto = ""
        try:
            doc = fitz.open(caminho_pdf)
            for pagina in doc:
                texto += pagina.get_text("text")
        except Exception as e:
            print(f"Erro ao ler o PDF {caminho_pdf}: {e}")
        return texto

    def quebrar_texto(self, cnv, texto, x, y, largura_max):
        """Quebra o texto caso ultrapasse a largura máxima da célula"""
        linhas = []
        linha_atual = ""

        texto = texto.replace('\n', ' ').replace('\r', '')

        for palavra in texto.split(" "):
            nova_linha = linha_atual + " " + palavra if linha_atual else palavra
            if cnv.stringWidth(nova_linha, "Times-Roman", 12) < largura_max:
                linha_atual = nova_linha
            else:
                linhas.append(linha_atual)
                linha_atual = palavra

        if linha_atual:
            linhas.append(linha_atual)

        altura = y
        for linha in linhas:
            cnv.drawString(x, altura, linha)
            altura -= 15
