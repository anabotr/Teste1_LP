"""
Contém funções para carregar os dados bancários do CSV para um dicionário em memória, 
e para salvar o dicionário de volta no CSV. 
"""

def carregar_contas_de_csv(caminho_arquivo: str = "contas22.csv") -> dict:
    """
    Carrega o arquivo csv para um dicionário. O arquivo não pode ser vazio.

    Args:
        caminho_arquivo (str): Caminho do arquivo que contém os dados em csv.

    Returns:
        dict: Dicionário que contém os dados devidamente organizados. Chave sendo o número da conta como str.

    Raises:
        FileNotFoundError: É retornado quando o caminho do arquivo não existe.
        IndexError: É retornado quando o arquivo está com algum problema, vazio, por exemplo.
    """    
    contas = {}
    try: 
        with open(caminho_arquivo, "r") as arquivo:
            linhas = arquivo.readlines()
            linhas = [linha.strip() for linha in linhas] 
            cabecalho = linhas[0].split(",")
            linhas = linhas[1:]

            for linha in linhas:
                if linha: 
                    colunas = linha.split(",")
                    numero_conta = colunas[0]
                    cliente = colunas[1]
                    saldo = colunas[2]
                    contas[numero_conta] = {"cliente": cliente, "saldo" : saldo}
    except FileNotFoundError:
        print("Arquivo não encontrado")
        contas = {}
    except IndexError: 
        print("O arquivo talvez esteja vazio")
        contas = {}
    return contas


def salvar_contas_para_csv(contas: dict, caminho_arquivo: str = "contas22.csv") -> None:
    """Abre um arquivo csv, lê as linhas, organiza os dados em ordem crescente, formata em dicionário especificado e então reescreve o documento csv.
    Ele só executa se o arquivo recebido for não vazio.

    Args:
        caminho_arquivo (str): Caminho do arquivo csv no qual os dados serão salvos.
        contas (dict): Dicionário a ser rescrito em csv.
    """    
    if contas != {}:
        with open(caminho_arquivo, "w") as file:
            file.write("numero_conta,cliente,saldo\n")
            def chave_para_int(item):
                return int(item[0])   # item[0] é a chave do dicionário
            contas = dict(sorted(contas.items(), key=chave_para_int))

            for numero_conta, info_saldo in contas.items():
                linha = f"{numero_conta},{info_saldo['cliente']},{info_saldo['saldo']}\n"
                file.write(linha)
    else:
        print("O arquivo está vazio.")
    return 

