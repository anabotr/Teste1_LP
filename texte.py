import csv 

def carregar_contas_de_csv(caminho_arquivo: str) -> dict:
    contas = {}
    try: 
        with open(caminho_arquivo, "r") as arquivo:
            linhas = arquivo.readlines()
            linhas = [linha.strip() for linha in linhas] 
            cabecalho = linhas[0].split(",")
            
            for linha in linhas[1:]:
                colunas = linha.split(",")
                numero_conta = colunas[0]
                cliente = colunas[1]
                saldo = colunas[2]
                
                contas[numero_conta] = {"cliente": cliente, "saldo" : saldo}

    except FileNotFoundError:
        contas["numero_conta"] = {"cliente": None, "saldo" : None}
        print("Arquivo não encontrado, retornou um dicionário vazio", contas)
    return contas

def salvar_contas_para_csv(caminho_arquivo: str, contas: dict) -> None:
    with open(caminho_arquivo, "w") as file:
        file.write("numero_conta,cliente,saldo\n")

        for numero_conta, info_saldo in contas.items():
            linha = f"{numero_conta},{info_saldo['cliente']},{info_saldo['saldo']}\n"
            file.write(linha)
    return


teste= carregar_contas_de_csv("C:/Users/lcone/.ipython/.vscode/lista1/contas22.csv")
salvar_contas_para_csv("C:/Users/lcone/.ipython/.vscode/lista1/contas22.csv", teste)
