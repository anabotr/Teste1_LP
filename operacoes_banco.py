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
    soma = round(soma, 2)
    return soma


def somar_saldos_em_lote(**kwargs) -> int:
    """Recebe como chave os numeros das contas e os valores a serem adicionados"""
    conta = bd.carregar_contas_de_csv()
    a = kwargs
    contas = a["numero_conta"]
    depositos = a["deposito"]

    for i in contas:
        if int(i) > 0:      
            indice = contas.index(i)
            depositos_corres = depositos[indice] 
            a = conta[f"{int(i):04d}"]
            saldo_original = conta[f"{int(i):04d}"]["saldo"] 
            saldo_novo = float(saldo_original) + float(depositos_corres)
            conta[f"{int(i):04d}"]["saldo"] = round(saldo_novo,2)
            bd.salvar_contas_para_csv(conta)
        else: 
            pass
    
    print("As contas foram atualizadas com sucesso")

    return 

def subtrair_saldos_em_lote(**kwargs) -> int:
    """Recebe como chave os numeros das contas e os valores a serem subtraidos"""
    conta = bd.carregar_contas_de_csv()
    a = kwargs
    contas = a["numero_conta"]
    saque = a["saque"]
    lista_contas = 0 

    for i in contas:
        if int(i) > 0:
            indice = contas.index(i)
            saque_corres = saque[indice]
            saldo_original = conta[f"{int(i):04d}"]["saldo"] 
            a = conta[f"{int(i):04d}"]
            saldo_novo = float(saldo_original) - float(saque_corres)
            conta[f"{int(i):04d}"]["saldo"] = round(saldo_novo, 2)
            if saldo_novo <= 0:
                conta[f"{int(i):04d}"]["saldo"] = saldo_original
                bd.salvar_contas_para_csv(conta)
            else: 
                lista_contas += 1
            bd.salvar_contas_para_csv(conta)
        else: 
            pass

    return f"{lista_contas} conta(s) tiveram o saldo removido com sucesso"

def realizar_transferencia(conta_origem: str, conta_destino: str, valor: float) -> tuple[bool, str]:
    conta = bd.carregar_contas_de_csv()
    opera = True
    erro1 = False
    erro2 = False
    try: 
        saldo_conta_origem = conta[f"{int(conta_origem):04d}"]["saldo"]
        saldo_conta_destino = conta[f"{int(conta_destino):04d}"]["saldo"]
        if saldo_conta_origem < valor: 
            erro1_descrição = "Operação não realizada, saldo insuficiente"
            tupla = (erro1, erro1_descrição)
        else: 
            opera_descricao = "Operação realizada com sucesso"
            saldo_novo_origem = (float(saldo_conta_origem) - float(valor))
            saldo_novo_destino = (float(saldo_conta_destino) + float(valor))
            conta[f"{int(conta_origem):04d}"]["saldo"] = round(float(saldo_novo_origem),2)
            conta[f"{int(conta_destino):04d}"]["saldo"] = round(float(saldo_novo_destino),2)        
            bd.salvar_contas_para_csv(conta)
            tupla = (opera, opera_descricao)

    except KeyError: 
        erro2_descricao = "Operação não realizada, conta não existe"
        tupla = (erro2, erro2_descricao)

    return tupla

#somar_saldos_em_lote(numero_conta = ["259", "1", "2"], deposito = ["1", "1", "1"] )

