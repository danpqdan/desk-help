import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import date
import locale
import os
import platform

class PedidoVenda:
    def __init__(self, vendedor, txtsacolaid, txtclicpf, txtnomecli, tree, txt_total):
        self.vendedor = vendedor
        self.txtsacolaid = txtsacolaid
        self.txtclicpf = txtclicpf
        self.txtnomecli = txtnomecli
        self.tree = tree
        self.txt_total = txt_total

    def imprimir_pdf(self):
        today = date.today()
        d3 = today.strftime("%d/%m/%y")
        cnv = canvas.Canvas("vendas.pdf", pagesize=A4)
        width, height = A4
        icon = 'assets/pasta.png'
        regras = 'assets/regras_de_servico.pdf'
        texto_regras = self.ler_pdf(regras)  # Usando a função para ler o PDF

        # Cabeçalho do Relatório
        cnv.setFont('Times-Roman', 14)
        cnv.setFillColorRGB(0, 0, 255)
        cnv.drawImage(icon, 10, height - 50, width=50, height=50, mask='auto')
        cnv.drawString(70, 810, "Desk-help")
        cnv.setFont('Times-Bold', 14)
        cnv.setFillColorRGB(0, 0, 0)
        cnv.drawString(250, height-25, "Ordem de serviço")
        cnv.drawString(280, height-38, "& venda")
        cnv.setFont('Times-Roman', 14)
        cnv.setFillColorRGB(0, 0, 0)
        cnv.drawString(540, 810, d3)

        # Cabeçalho do Pedido
        cnv.setLineWidth(2)
        cnv.line(0, 790, 595, 790)
        cnv.setFont('Times-Roman', 12)
        cnv.setFillColorRGB(0, 0, 0)
        cnv.drawString(10, 760, "Número do Pedido: " + self.txtsacolaid.get())
        cnv.drawString(200, 760, "Data do Pedido:   " + d3)
        cnv.drawString(450, 760, "Vendedor: " + self.vendedor)

        cnv.drawString(10, 745, "CPF do Cliente: " + self.txtclicpf.get())
        cnv.drawString(200, 745, "Nome do Cliente:  " + self.txtnomecli.get())
        cnv.setLineWidth(1)
        cnv.line(0, 720, 595, 720)

        # Cabeçalho da Tabela
        cabecalho = ["Cod. Prod", "Descrição", "Qts", "Valor Unitário", "Valor"]
        col_widths = [50, 280, 80, 100, 60]
        x_positions = [1, 70, 400, 450, 530]
        
        # Desenha o cabeçalho
        for i, texto in enumerate(cabecalho):
            cnv.drawString(x_positions[i], 700, texto)
        
        cnv.setFont('Times-Roman', 12)
        linha = 680

        for child in self.tree.tree.get_children():
            valores = self.tree.tree.item(child)["values"]
            
            for i, valor in enumerate(valores[1:]):
                if i == 2:
                    descricao = str(valor)
                    self.quebrar_texto(cnv, descricao, x_positions[i], linha, col_widths[i])
                else:
                    cnv.drawString(x_positions[i], linha, str(valor))
            
            linha -= 20

        cnv.setLineWidth(1)
        cnv.line(0, linha, 595, linha)

        cnv.line(0, linha, 595, linha)
        linha = linha - 20
        cnv.setFont('Times-Bold', 12)
        cnv.drawString(420, linha, "Total do Pedido ->")
        cnv.drawString(530, linha, locale.currency(float(self.txt_total.get().strip())))
        
        linha -= 30
        cnv.setFont('Times-Roman', 10)

        self.quebrar_texto(cnv, texto_regras, 10, linha - 12, width)
        
        cnv.setLineWidth(1)
        cnv.line(100, 100, 200, 100 )
        cnv.setFont('Times-Roman',10)
        cnv.drawString(120, 80, "Ass: desk-help")
        
        cnv.setLineWidth(1)
        cnv.line(300, 100, 500, 100 )
        cnv.setFont('Times-Roman',10)
        cnv.drawString(320, 80, f"Ass: {self.txtnomecli.get()}")

        cnv.save()

        if platform.system() == "Windows":
            os.startfile("vendas.pdf")
        else:
            os.system("xdg-open vendas.pdf")
        
    def ler_pdf(self, caminho_pdf):
        """Lê o conteúdo de um arquivo PDF"""
        texto = ""
        doc = fitz.open(caminho_pdf)
        for pagina in doc:
            texto += pagina.get_text("text")
        return texto

    def quebrar_texto(self, cnv, texto, x, y, largura_max):
        """Quebra o texto caso ultrapasse a largura máxima da célula"""
        linhas = []
        linha_atual = ""
        
        texto = texto.replace('\n', ' ').replace('\r', '')
        
        for palavra in texto.split(" "):
            nova_linha = linha_atual + " " + palavra if linha_atual else palavra
            largura_linha = cnv.stringWidth(nova_linha, "Times-Roman", 12)

            if largura_linha < largura_max:
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


