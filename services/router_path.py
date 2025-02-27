import os
import sys

global dir
global pathClientes
global pathCadLogin
global pathConexao
global pathLogin
global pathMenu
global pathProdutos
global pathVendas
global help_desk_data
global help_desk_icon
global help_desk_market
global help_desk_pasta
global help_desk_modelo_os
global help_desk_regras_os
dir = os.path.dirname(os.path.abspath(__file__))


if getattr(sys, 'frozen', False):
    # assets
    help_desk_data = os.path.join(sys._MEIPASS, 'assets/help_desk_data.png')
    help_desk_icon = os.path.join(sys._MEIPASS, 'assets/help_desk_icon.png')
    help_desk_market = os.path.join(sys._MEIPASS, 'assets/help_desk_market.png')
    help_desk_pasta = os.path.join(sys._MEIPASS, 'assets/pasta.png')
    help_desk_modelo_os = os.path.join(sys._MEIPASS, 'assets/Planilha Modelo de Ordem de Serviço.xlsx')
    help_desk_regras_os = os.path.join(sys._MEIPASS, 'assets/regras_de_servico.pdf')
    
    #Servico
    pathConexao = os.path.join(sys._MEIPASS, './services/conexao.py')
else:
    # assets
    help_desk_data = os.path.join(dir, '../assets', 'help_desk_data.png')
    help_desk_icon = os.path.join(dir, '../assets', 'help_desk_icon.png')
    help_desk_market = os.path.join(dir, '../assets', 'help_desk_market.png')
    help_desk_pasta = os.path.join(dir, '../assets', 'pasta.png')
    help_desk_modelo_os = os.path.join(dir, '../assets', 'Planilha Modelo de Ordem de Serviço.xlsx')
    help_desk_regras_os = os.path.join(dir, '../assets', 'regras_de_servico.pdf')