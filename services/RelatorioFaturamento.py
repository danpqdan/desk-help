import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import date
import locale
import os
import platform

import io
import os
import platform
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

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

    def imprimir_pdf(self):
        today = date.today()
        d3 = today.strftime("%d/%m/%y")
        icon = 'assets/pasta.png'


        buffer = io.BytesIO()
        cnv = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        #Cabecalho pdf
        cnv.setFont('Times-Roman', 14)
        cnv.setFillColorRGB(0, 0, 255)
        cnv.drawImage(icon, 10, height - 50, width=50, height=50, mask='auto')
        cnv.setFont('Times-Roman', 14)
        cnv.setFillColorRGB(0, 0, 255)
        cnv.drawString(70, 810, "Desk-help")
        cnv.setFont('Times-Bold', 14)
        cnv.setFillColorRGB(0, 0, 0)
        cnv.drawString(250, 810, "Relatório de Vendas")
        cnv.setFont('Times-Roman', 14)
        cnv.setFillColorRGB(0, 0, 0)
        cnv.drawString(540, 810, d3)

        cnv.showPage()
        cnv.save()





        buffer.seek(0)
        if platform.system() == "Windows":
            with open("temp_vendas.pdf", "wb") as f:
                f.write(buffer.read())
            os.startfile("temp_vendas.pdf")
        else:
            with open("/tmp/temp_vendas.pdf", "wb") as f:
                f.write(buffer.read())
            os.system("xdg-open /tmp/temp_vendas.pdf")

        buffer.close()
