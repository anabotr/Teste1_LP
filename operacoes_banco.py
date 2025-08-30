import banco_de_dados as bd  
"""
FALTA FAZER 

#TODO: dar um jeito nos índices fora de ordem!

DEPOSITAR(NUM CONTA, VALOR) -> TUPLA (BOOL, STR) 
SACAR 
SOMAR SALDOS GERAIS 
IDENTIFAR CLIENTE MAIS RICO 
SOMAR SALDOS EM LOTE
SUBTRAIR SALDOS EM LOTE
REALIZAR TRANSFERENCIA 

FUNCAO TRATA STRING PARA TIRAR A VIRGULA E BOTAR PONTO
"""



#NOTE:PRONTAAAAAAAAAAAAAAAAAAAA
def trata_float(string : str) -> str:
    try:
        valor = float(string)
    except ValueError:
        valor = string[::-1].replace(',', '.', 1)[::-1]
    return f"{round(float(valor),2):.2f}"

#NOTE:PRONTAAAAAAAAAAAAAAAAAAAA
def saldo_suficiente(numero_conta: str, valor: str) -> bool:
    dados_banco = consulta_dados()
    numero_conta = int(numero_conta)
    pesquisa = numero_conta - 1
    if pesquisa > len(dados_banco): 
        print("Essa conta ainda não existe")
        return None
    else:  
        if float(dados_banco[pesquisa - 1][2]) >= float(valor):
            return True
        else:
            return False

#NOTE: PRONTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
#NOTE:AUXILIAR!
def consulta_dados():
    dados = []
    conta = bd.carregar_contas_de_csv()
    for numero_conta, info_saldo in conta.items():
        tupla = (numero_conta, info_saldo["cliente"], info_saldo["saldo"])
        dados.append(tupla)
    return dados

#NOTE: PRONTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
#NOTE: AUXILIAR!
def consulta_banco(numero_conta: str) -> tuple[str, str, str]:
    try:
        dados_banco = consulta_dados()
        numero_conta = int(numero_conta)
        pesquisa = numero_conta - 1 
        if pesquisa > len(dados_banco): 
            return None
        else:
            return(dados_banco[pesquisa][0], dados_banco[pesquisa][1], dados_banco[pesquisa][2])
    except ValueError: 
        print("Você deve inserir um número") 
    return 

#NOTE: PRONTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
def atualiza_saldo(numero_conta: str, valor: float):
    dados_banco = consulta_dados()
    conta = bd.carregar_contas_de_csv()
    numero_conta = int(numero_conta)
    pesquisa = numero_conta - 1
    if pesquisa > len(dados_banco): 
        print("Essa conta ainda não existe")
        return None
    else:
        conta[f"{numero_conta:04d}"] = {"cliente": dados_banco[numero_conta-1][1], "saldo": f"{valor:.2f}"}
        bd.salvar_contas_para_csv(conta)  
    return "a"


#NOTE: PRONTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
def criar_conta(numero_conta: str, nome_cliente: str) -> tuple[int, dict]:
    conta = bd.carregar_contas_de_csv()
    teste = consulta_banco(numero_conta)
    if teste == None: 
        numero_conta = int(numero_conta)
        conta[f"{numero_conta:04d}"] = {"cliente": nome_cliente, "saldo": f"{00:05.2f}"}
        bd.salvar_contas_para_csv(conta)
    else:
        print("Conta já existe!")
    return

def consultar_saldo(numero_conta: str) -> float | None:
    conta = bd.carregar_contas_de_csv()
    numero_conta = int(numero_conta)
    print("Seu saldo atual é de:" , conta[f"{numero_conta:04d}"]["saldo"])
    return 

def somar_saldos_gerais() -> float:
    soma = 0
    dados = consulta_dados() 
    quantidade = len(dados)
    for i in range(quantidade):
       valor = dados[i][2]
       valor = float(valor)
       soma += valor
    
    return soma
