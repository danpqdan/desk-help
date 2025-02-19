# Desk-help

### **Aplicativo comercial para gerenciamento e controle comercial**

- Python >= 3.0
- Tkinter
- SqlAlquemy
- MySql
- pytho-dotenv

---

### Variaveis de ambiente

**O banco de dados conta com variaveis de ambiente para poder iniciar**
**Necessário criar o banco de dados para o projeto**

```Bash
# Env banco de dados
USUARIO_DB=(Usuario do banco)
SENHA_DB=(Senha do banco)
NOME_BANCO=(Banco criado préviamente)
```

**SQLAlchemy tomará conta de iniciar as tabelas e a criação do ORM**

---

## **Funcionalidade:** 
- Produtos e Serviços: Possibilidade de adicionar, remover, alterar produtos em seu próprio banco de dados. Além de ordenalos da forma que achar melhor.

- Clientes: Possibilidade de adicionar clientes, registralos por email e telefone falicitando futuras features de push notification.

- Vendas: Sistema possui controle de vendas bem elaborado, podendo encontrar de forma direta os clientes e produtos, conta com bind keys para facilitar o processo de venda e sistema de emissão de ordem de serviço.

- Controle de acesso: Atualmente sistema possui controle de acesso aos ambientes privilegiados, podendo gerenciar de forma dinamica onde cada usuario terá acesso.

- Faturamento: Implementado setor de faturamento para que você como logista possa utilizar um controle aprimorado de filtros, dessa forma, poderá filtrar suas vendas por datas especificas, vendedores e clientes. Poderá também analiser seus tickets médio, sua venda total com filtros, analisar a entrada em custos e a saída em valor bruto e ter métricas para suas vendas futuras.