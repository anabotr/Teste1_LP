import banco_de_dados as bd  

#Funções auxiliares

def consulta_dados() -> list[tuple[str, str, str]]:
    """Pega o banco de dados e tranforma em uma lista de tuplas, para colocar todas as 
    informações em um mesmo nível (em termos de índice) e facilitar a maniuplação.

    Returns:
        list[tuple[str,str,str]]: Lista de tuplas com os dados em forma de string, cada tupla é do formato
        (numero_da_conta, nome_do_cliente, valor_da_conta)
    """
    dados = []
    conta = bd.carregar_contas_de_csv()
    for numero_conta, info_saldo in conta.items():
        tupla = (numero_conta, info_saldo["cliente"], info_saldo["saldo"])
        dados.append(tupla)
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
    conta = bd.carregar_contas_de_csv()
    try:
        numero_conta = int(numero_conta)
        if f"{numero_conta:04d}" in conta:
            return True
        return False
    except ValueError:
        print("Insira uma conta válida.")

def acha_indice(numero_conta:str, dados = consulta_dados()) -> int | None:
    """Encontra o índice da conta solicitada no dicionário do banco de dados.
    Podem ser passadas outras fontes de dados, mas o padrão é a lista que criamos com base no nosso banco de dados.

    Args:
        numero_conta (str): Número da conta a ser procurada

    Returns:
        int | None: Retorna o índice ou none, caso a conta não exista no banco de dados.
    """
    if conta_in_bd(numero_conta):
        for i, (conta, nome, saldo) in enumerate(dados):
            if f"{int(numero_conta):04d}" == str(conta):
                return i
    else:
        return None

def trata_float(valor : str|float|int) -> str:
    """Trata as entradas numéricas, garantindo que os valores sigam o padrão americano.

    Args:
        string (str | float | int): Número a ser modificado, passado em forma de string, int ou float.

    Returns:
        str: Valor inserido com ponto no separamento decimal e arredondamento para duas casas.
    """

    try:
        valor_final = float(valor)
    except ValueError:
        valor_final = valor[::-1].replace(',', '.', 1)[::-1]
    return float(f"{round(float(valor_final),2):02f}")

def saldo_suficiente(numero_conta: str, valor: str) -> bool:
    """_summary_

    Args:
        numero_conta (str): _description_
        valor (str): _description_

    Returns:
        bool: _description_
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
    conta = bd.carregar_contas_de_csv()
    indice = acha_indice(numero_conta)        
    if conta_in_bd(numero_conta):
        conta[f"{int(numero_conta):04d}"] = {"cliente": dados_banco[indice][1], "saldo": f"{valor:.2f}"}
        bd.salvar_contas_para_csv(conta)
        
    return 


#Funções solicitadas

def criar_conta(numero_conta: str, nome_cliente: str) -> tuple[int,dict]:
    """Cria uma conta, coom base no número e nome forneci

    Args:
        numero_conta (str): Número da conta que será aberta.
        nome_cliente (str): Nome do cliente para a abertura de conta.

    Returns:
        tuple[int,dict]: Tupla com dois elementos, o número da conta e um dicionário com 
        as chaves "cliente" e "saldo", e seus respectivos valores.
    """
    conta = bd.carregar_contas_de_csv()
    if not conta_in_bd(numero_conta): 
        numero_conta = int(numero_conta)
        conta[f"{numero_conta:04d}"] = {"cliente": nome_cliente, "saldo": float(f"{00:05.2f}")}
        bd.salvar_contas_para_csv(conta)
        return (int(f"{numero_conta:04d}"),  conta[f"{numero_conta:04d}"])

def consultar_saldo(numero_conta: str) -> float | None:
    """Função que retorna o saldo de uma conta específica.

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
    soma = 0
    dados = consulta_dados() 
    quantidade = len(dados)
    for i in range(quantidade):
       valor = dados[i][2]
       valor = float(valor)
       soma += valor
    soma = round(soma, 2)
    return soma

def identificar_cliente_mais_rico() -> dict | None: 
    """Percorre todos os clientes e retorna os dados do cliente com mais dinheiro na conta do banco.

    Returns:
        dict|None: Se a conta existir, retorna um dicionário com as chaves "cliente" e "saldo" e seus respectivos valores.
        Se a conta não existir, retorna None
    """
    dados = consulta_dados()
    lista = []
    lista2 = {}
    quantidade = len(dados)
    if dados != []:
        for i in range(quantidade): 
            lista.append(float(dados[i][2]))
        localiza_max = lista.index(max(lista))
        maior_saldo = dados[localiza_max]   
        lista2[f"{maior_saldo[0]}"] = {"cliente" : maior_saldo[1], "saldo" : maior_saldo[2]}
        return lista2 
    return

def somar_saldos_em_lote(**kwargs) -> int:
    """Soma valores aos saldos de múltiplas contas de uma vez.
    No kwargs, as chaves são os números das contas e os valores serão os montantes a serem adicionados.
    Se forem inseridas contas inexistentes ou valores negativos, eles serão ignorados.

    Returns:
        int: Quantidade de contas que tiveram saldo atualizado.
    """    

    contas = 0
    conta = bd.carregar_contas_de_csv()
    info = kwargs
    contas = info["numero_conta"]
    depositos = info["deposito"]

    for numero_conta in contas:
        if conta_in_bd(numero_conta):      
            indice_contas = contas.index(info)
            indice_csv = acha_indice(numero_conta)
            depositos_corresp = depositos[indice_contas] 
            if float(depositos_corresp) >= 0:
                info_colunas = conta[indice_csv]
                saldo_original = info_colunas["saldo"] 
                saldo_novo = round(float(saldo_original) + float(depositos_corresp),2)
                atualiza_saldo(numero_conta, saldo_novo)
                contas += 1
        else: 
            pass
    
    return contas

def subtrair_saldos_em_lote(**kwargs) -> int:
    """Subtrai valores aos saldos de múltiplas contas de uma vez.
    No kwargs, as chaves são os números das contas e os valores serão os montantes a serem adicionados.
    Se uma conta tiver saldo menor do que o retirado, o saque falha para ela, mas continua para as outras.
    Contas inexistentes, valores negativos ou tentativas de saque maiores que o saldo serão ignoradas.

    Returns:
        int: Quantidade de contas que tiveram saldo alterado com sucesso.
    """    

    conta = bd.carregar_contas_de_csv()
    info = kwargs
    contas = info["numero_conta"]
    saque = info["saque"]
    numero_contas = 0 

    for numero_conta in contas:
        if conta_in_bd(numero_conta):
            indice_contas = contas.index(numero_conta)
            saque_corresp = saque[indice_contas]
            if (saldo_suficiente(numero_conta, saque_corresp) and saque_corresp >= 0):
                indice_csv = acha_indice(numero_conta)
                saldo_original = conta[indice_csv]["saldo"] 
                saldo_novo = round(float(saldo_original) - float(saque_corresp),2)
                conta[indice_csv]["saldo"] = saldo_novo
                numero_contas += 1
                atualiza_saldo(numero_conta, saldo_novo)
    return contas

def realizar_transferencia(conta_origem: str, conta_destino: str, valor: float) -> tuple[bool,str]:
    """Realiza uma transferência entre duas contas especificadas, com base no valor dado.
    Contas inexistentes ou saldos insuficientes serão notificados no caso de insucesso.

    Args:
        conta_origem (str): Conta de ondde o dinheiro será debitado.
        conta_destino (str): Conta que recebrá o valor inserido.
        valor (float): Quantidade transacinada.

    Returns:
        tuple[bool,str]: Tupla com dois elementos, o primeiro é True se a operação fucionou e False se deu errado. 
        O segundo elemento é uma string com a descrição da operação/erro, se ocorreu.
    """
    conta = bd.carregar_contas_de_csv()
    operacao = True
    erro1 = False
    erro2 = False
    if conta_in_bd(conta_origem) and conta_in_bd(conta_destino):
        indice_csv_contaorigem = acha_indice(conta_origem)
        indice_csv_contadestino = acha_indice(conta_destino)
        saldo_conta_origem = conta[indice_csv_contaorigem]["saldo"]
        saldo_conta_destino = conta[indice_csv_contadestino]["saldo"]
        if not saldo_suficiente(conta_origem, valor):
            erro1_descrição = "Operação não realizada, saldo insuficiente"
            tupla = (erro1, erro1_descrição)
        else: 
            operacao_descricao = "Operação realizada com sucesso"
            saldo_novo_origem = round((float(saldo_conta_origem) - float(valor)),2)
            saldo_novo_destino = (float(saldo_conta_destino) + float(valor))
            atualiza_saldo(conta_origem, saldo_novo_origem)
            atualiza_saldo(conta_destino, saldo_conta_destino)
            tupla = (operacao, operacao_descricao)
    else:
        erro2_descricao = "Operação não realizada, conta não existe"
        tupla = (erro2, erro2_descricao)

    return tupla

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
    conta = bd.carregar_contas_de_csv()
    verifica = False
    indice = acha_indice(numero_conta)
    if valor > 0:
        if conta_in_bd(numero_conta):
            saldo_atual = conta[indice]["saldo"]
            saldo_novo = round((float(saldo_atual) + float(valor)),2)
            atualiza_saldo(numero_conta, saldo_novo)
            verifica = True 
            motivo = "Depósito concluído"
        else: 
            motivo = "Erro: conta inexistente."
    else: 
        motivo = "Impossível depositar valores negativos"
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
    conta = bd.carregar_contas_de_csv()
    verifica = False
    indice = acha_indice(numero_conta)
    if valor > 0:
        if saldo_suficiente(numero_conta, valor) == True:
            if conta_in_bd(numero_conta):
                saldo_atual = conta[indice]["saldo"]
                saldo_novo = round((float(saldo_atual) - float(valor)),2)
                atualiza_saldo(numero_conta, saldo_novo)
                verifica = True 
                motivo = "Saque concluído"
            else: 
                motivo = "Conta inexistente."
        else: 
            motivo = "Erro: saldo insuficiente."
    else: 
        motivo = "Impossível sacar valores negativos"
    return (verifica, motivo)

#Descrição: Verifica se a conta existe, se o valor é positivo e se há saldo suficiente. Se tudo estiver OK, subtrai o valor do saldo.
#Retorno: Uma tupla indicando sucesso/falha com uma mensagem apropriada (ex: (False, "Erro: saldo insuficiente.")).

