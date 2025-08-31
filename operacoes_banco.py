"""
Contém as funções principais realacionadas às operações bancárias. 
Dividido em funções auxiliares e funções solicitadas. 
"""
import banco_de_dados as bd  

#Funções auxiliares

def consulta_dados() -> list[tuple[str, str, str]]:
    """Pega o banco de dados e tranforma em uma lista de tuplas, para colocar todas as 
    informações em um mesmo nível (em termos de índice) e facilitar a manipulação.

    Returns:
        list[tuple[str,str,str]]: Lista de tuplas com os dados em forma de string, cada tupla é do formato
        (numero_da_conta, nome_do_cliente, valor_da_conta)
    """
    dados = []
    contas_banco = bd.carregar_contas_de_csv()
    for numero_conta, info_saldo in contas_banco.items():
        info_cada_conta = (numero_conta, info_saldo["cliente"], info_saldo["saldo"])
        dados.append(info_cada_conta)
    return dados

def conta_in_bd(numero_conta: str) -> bool:
    """Verifica se a conta existe no dicionário do banco de dados. Ela deve ser composta apenas de números.

    Args:
        numero_conta (str): Número da conta a ser procurada.

    Returns:
        bool: True, se a conta existe. False, se a conta não existe.

    Raises:
        ValueError: Se a conta não é convertível para número.
    """
    contas_banco = bd.carregar_contas_de_csv()
    try:
        numero_conta = int(numero_conta)
        if f"{numero_conta:04d}" in contas_banco:
            return True
        return False
    except ValueError:
        return False
    

def acha_indice(numero_conta:str, dados = consulta_dados()) -> int | None:
    """Encontra o índice da conta solicitada no dicionário do banco de dados atráves da lista de tuplas.
    Podem ser passadas outras fontes de dados, mas o padrão é a lista que criamos com base no nosso banco de dados.

    Args:
        numero_conta (str): Número da conta a ser procurada

    Returns:
        int | None: Retorna o índice ou none, caso a conta não exista no banco de dados.
    """
    if conta_in_bd(numero_conta):
        for indice, (conta, _, _) in enumerate(dados):
            if f"{int(numero_conta):04d}" == str(conta):
                return indice
    else:
        return None

def trata_float(valor : str|float|int) -> str:
    """Trata as entradas numéricas, garantindo que os valores sigam o padrão do banco: apenas separador decimal, sendo ele um ponto final.
    Se a entrada for vazia, retorna 0.

    Args:
        string (str | float | int): Número a ser modificado, passado em forma de string, int ou float.

    Returns:
        str: Valor inserido com ponto no separamento decimal e arredondamento para duas casas.
    """
    if valor == "" or valor is None:
        return 0.0
    try:
        valor_final = float(valor)
        return valor_final
    except:
        valor = valor.strip()
        tem_letra = any(c.isalpha() for c in valor)
        if tem_letra: 
            return None
        valor_final = valor[:-3].replace('.', '').replace(',', '')
        valor_final += valor[-3:].replace(',', '.')
        try:
            return float(f"{round(float(valor_final),2):02f}")
        except ValueError:
            return None

def saldo_suficiente(numero_conta: str, valor: str|float|int) -> bool:
    """Verifica se a conta tem saldo suficiente para retirar algum valor específico.

    Args:
        numero_conta (str): Número da conta a ter saldo modificado.
        valor (str | float | int): Valor a ser debitado da conta.

    Returns:
        bool: Um valor booleano, True se é possível realizar a operação e False se não.
    """
    dados_banco = consulta_dados()
    indice = acha_indice(numero_conta)        
    if conta_in_bd(numero_conta):  
        if float(dados_banco[indice][2]) >= float(valor):
            return True
        else:
            return False
        
def atualiza_saldo(numero_conta: str, valor: float):
    """Dado o número da conta e o novo valor do cliente, a função atualiza o arquivo do banco de dados com as novas informações.

    Args:
        numero_conta (str): Número da conta para modificação do saldo.
        valor (float): Novo saldo.
    """
    dados_banco = consulta_dados()
    contas_banco = bd.carregar_contas_de_csv()
    indice = acha_indice(numero_conta)        
    if conta_in_bd(numero_conta):
        contas_banco[f"{int(numero_conta):04d}"] = {"cliente": dados_banco[indice][1], "saldo": f"{float(valor):.2f}"}
        bd.salvar_contas_para_csv(contas_banco)
        
    return 


#Funções solicitadas

def criar_conta(numero_conta: str, nome_cliente: str) -> tuple[int,dict]:
    """Abre uma conta no banco de dados com saldo inicial sendo 0 reais, com base no número da conta e nome do cliente fornecidos

    Args:
        numero_conta (str): Número da conta que será aberta.
        nome_cliente (str): Nome do cliente para a abertura de conta.

    Returns:
        tuple[int,dict]: Tupla com dois elementos, o número da conta e um dicionário com 
        as chaves "cliente" e "saldo", e seus respectivos valores.
    """
    contas_banco = bd.carregar_contas_de_csv()
    if not conta_in_bd(numero_conta): 
        if numero_conta.isdigit():
            numero_conta = int(numero_conta)
            contas_banco[f"{numero_conta:04d}"] = {"cliente": nome_cliente, "saldo": float(f"{00:05.2f}")}
            bd.salvar_contas_para_csv(contas_banco)
            return (int(f"{numero_conta:04d}"),  contas_banco[f"{numero_conta:04d}"])
        else: 
            return None


def depositar(numero_conta: str, valor: float) -> tuple[bool, str]:
    """Depositar o valor inserido na conta especificada.
    Valores negativos ou contas inexistentes serão notificados no caso de insucesso da operação.

    Args:
        numero_conta (str): Número da conta a receber dinheiro.
        valor (float): Valor que será depositado.

    Returns:
        tuple[bool,str]: Tupla na qual o primeiro elemento é um booleano que retorna True se a operação deu certo e False se não.
        O segundo elemento é uma string com a descrição da operação/erro, se ocorreu.
    """
    contas_banco = bd.carregar_contas_de_csv()
    verifica = False
    if valor > 0:
        if conta_in_bd(numero_conta):
            saldo_atual = contas_banco[f"{int(numero_conta):04d}"]["saldo"]
            saldo_novo = round((float(saldo_atual) + float(valor)),2)
            atualiza_saldo(numero_conta, saldo_novo)
            verifica = True 
            motivo = "Operação concluída"
        else: 
            motivo = "Erro: conta inexistente."
    else: 
        motivo = "Impossível operar com valores negativos"
    return (verifica, motivo)


def sacar(numero_conta: str, valor: float) -> tuple[bool, str]:
    """Sacar o valor inserido na conta especificada.
    Valores negativos, saldos insuficientes ou contas inexistentes serão notificados no caso de insucesso da operação.

    Args:
        numero_conta (str): Número da conta a receber dinheiro.
        valor (float): Valor que será depositado.

    Returns:
        tuple[bool,str]: Tupla na qual o primeiro elemento é um booleano que retorna True se a operação deu certo e False se não.
        O segundo elemento é uma string com a descrição da operação/erro, se ocorreu.
    """
    contas_banco = bd.carregar_contas_de_csv()
    verifica = False
    indice = acha_indice(numero_conta)
    if valor > 0:
        if saldo_suficiente(numero_conta, valor) == True:
            if conta_in_bd(numero_conta):
                saldo_atual = contas_banco[f"{int(numero_conta):04d}"]["saldo"]
                saldo_novo = round((float(saldo_atual) - float(valor)),2)
                atualiza_saldo(numero_conta, saldo_novo)
                verifica = True 
                motivo = "Operação concluída"
            else: 
                motivo = "Conta inexistente."
        else: 
            motivo = "Erro: saldo insuficiente."
    else: 
        motivo = "Impossível operar com valores negativos"
    return (verifica, motivo)

def consultar_saldo(numero_conta: str) -> float | None:
    """Função que consulta o saldo de uma conta informada no banco de dados. Contas inexistentes retornam None.

    Args:
        numero_conta (str): Número da conta com saldo a ser consultado.

    Returns:
        float | None: Retorna o valor que está na conta (float) ou None, se a conta não existir.
    """
    if conta_in_bd(numero_conta):
        conta = bd.carregar_contas_de_csv()
        numero_conta = int(numero_conta)
        return conta[f"{numero_conta:04d}"]["saldo"]
    else:
        return None
    

def somar_saldos_gerais() -> float:
    """Soma o saldo de todas as contas existentes no banco.

    Returns:
        float: Soma de todos os valores dos saldos.
    """
    soma_inicial = 0
    lista_contas = consulta_dados() 
    quantidade = len(lista_contas)
    for cada_conta in range(quantidade):
       saldo = lista_contas[cada_conta][2]
       saldo_formatado = float(saldo)
       soma_inicial += saldo_formatado
    soma_total = round(soma_inicial, 2)
    return soma_total

def identificar_cliente_mais_rico() -> dict | None: 
    """Percorre todos os clientes e retorna os dados do cliente com mais dinheiro na conta do banco.

    Returns:
        dict|None: Se a conta existir, retorna um dicionário com as chaves "cliente" e "saldo" e seus respectivos valores.
        Se a conta não existir, retorna None
    """
    lista_contas = consulta_dados()
    lista_saldos = []
    dict_cliente_rico = {}
    quantidade = len(lista_contas)
    if lista_contas != []:
        for cada_conta in range(quantidade): 
            lista_saldos.append(float(lista_contas[cada_conta][2]))
        localiza_max = lista_saldos.index(max(lista_saldos))
        maior_saldo = lista_contas[localiza_max]   
        dict_cliente_rico[f"{maior_saldo[0]}"] = {"cliente" : maior_saldo[1], "saldo" : maior_saldo[2]}
        return dict_cliente_rico
    return

def somar_saldos_em_lote(**kwargs) -> int:
    """Soma valores aos saldos de múltiplas contas de uma vez.
    No kwargs, as chaves são os números das contas e os valores serão os montantes a serem adicionados.
    Se forem inseridas contas inexistentes ou valores negativos, eles serão ignorados.

    Returns:
        int: Quantidade de contas que tiveram saldo atualizado.
    """    

    contar_contas = 0
    contas_banco = bd.carregar_contas_de_csv()
    info = kwargs
    lista_contas = info["numero_conta"] 
    valor_depositos = info["deposito"] 


    for numero_conta in lista_contas: #para cada item em contas vai verificar  
        if conta_in_bd(numero_conta):    #se o número da conta existe
            indice_contas = lista_contas.index(numero_conta) #vai pegar o indece da lista contas
            numero_conta = str(numero_conta).zfill(4)
            depositos_corresp = trata_float(valor_depositos[indice_contas])  #vai pesquisar o mesmo 
            if depositos_corresp == None: 
                continue
            if depositos_corresp >= 0: # se o float for maior que zero 
                info_colunas = contas_banco[numero_conta] 
                saldo_original = info_colunas["saldo"] 
                saldo_novo = round((float(saldo_original) + float(depositos_corresp)),2)
                atualiza_saldo(numero_conta, saldo_novo)
                contar_contas += 1
        else: 
            pass
    
    return contar_contas

def subtrair_saldos_em_lote(**kwargs) -> int:
    """Subtrai valores aos saldos de múltiplas contas de uma vez.
    No kwargs, as chaves são os números das contas e os valores serão os montantes a serem adicionados.
    Se uma conta tiver saldo menor do que o retirado, o saque falha para ela, mas continua para as outras.
    Contas inexistentes, valores negativos ou tentativas de saque maiores que o saldo serão ignoradas.

    Returns:
        int: Quantidade de contas que tiveram saldo alterado com sucesso.
    """    

    contas_banco = bd.carregar_contas_de_csv()
    info = kwargs
    lista_contas = info["numero_conta"]
    valor_saques = info["saque"]
    numero_contas = 0 

    for numero_conta in lista_contas:
        if conta_in_bd(numero_conta):
            indice_contas = lista_contas.index(numero_conta)
            numero_conta = str(numero_conta).zfill(4)
            saque_corresp = valor_saques[indice_contas]
            if saque_corresp == None: 
                numero_contas = 0
                continue
            if int(saque_corresp) >= 0:
                if saldo_suficiente(numero_conta, saque_corresp): 
                    indice_csv = acha_indice(numero_conta)
                    saldo_original = contas_banco[numero_conta]["saldo"] 
                    saldo_novo = round((float(saldo_original) - float(saque_corresp)), 2)
                    contas_banco[numero_conta]["saldo"] = saldo_novo
                    numero_contas += 1
                    atualiza_saldo(numero_conta, saldo_novo)
    return numero_contas

def realizar_transferencia(conta_origem: str, conta_destino: str, valor: float) -> tuple[bool,str]:
    """Realiza uma transferência entre duas contas especificadas, com base no valor dado.
    Contas inexistentes ou saldos insuficientes serão notificados no caso de insucesso.

    Args:
        conta_origem (str): Conta de ondde o dinheiro será debitado.
        conta_destino (str): Conta que recebrá o valor inserido.
        valor (float): Quantidade transacionada.

    Returns:
        tuple[bool,str]: Tupla com dois elementos, o primeiro é True se a operação fucionou e False se deu errado. 
        O segundo elemento é uma string com a descrição da operação/erro, se ocorreu.
    """
    operacao = True
    if conta_in_bd(conta_origem) and conta_in_bd(conta_destino):
        resultado_saque = sacar(conta_origem, valor)
        if resultado_saque[0] == False: 
            operacao = False
            ope_descri = resultado_saque[1]
        else:
            resultado_deposito = depositar(conta_destino, valor)
            if resultado_deposito[0] == True:
                operacao = True
                ope_descri = "Transferência realizada com sucesso"
            else:
                operacao = False
                ope_descri = resultado_deposito[1]
    return (operacao, ope_descri) 