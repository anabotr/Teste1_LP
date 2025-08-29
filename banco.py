import banco_de_dados as bd 

#- consulta saldo
#- atualiza saldo
#- cria conta

contas = bd.carregar_contas_de_csv("C:/Users/lcone/.ipython/.vscode/lista1/contas22.csv")

def consulta_banco(conta: int) -> tuple[conta, nome, saldo]:
    dados = ()
    for numero_conta, info_saldo in contas.items(): 
        a = numero_conta 
        b = info_saldo 
        dados = (a,b)
    return dados
 


def criar_conta(numero_conta: str, nome_cliente: str) -> tuple[int, dict]:
    #comparar se existe a conta já 
    return aa