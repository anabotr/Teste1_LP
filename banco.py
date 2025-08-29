import banco_de_dados as bd 

#- consulta saldo
#- atualiza saldo
#- cria conta

contas = bd.carregar_contas_de_csv("C:/Users/lcone/.ipython/.vscode/lista1/contas22.csv")

def consulta_banco(conta: int):
    dados = []
    indice_conta = 1
    indice_nome = 2 
    indice_saldo = 3
    for numero_conta, info_saldo in contas.items():
        tupla = (numero_conta, info_saldo["cliente"], info_saldo["saldo"])
        dados.append(tupla)
    pesquisa = conta - 1
    if pesquisa > len(dados): 
        print("Essa conta ainda não existe")
        return print("Crie sua conta!")
    else:
        return(dados[pesquisa][0], dados[pesquisa][1], dados[pesquisa][2])
 
a = consulta_banco(123)
print(a)


def criar_conta(numero_conta: str, nome_cliente: str) -> tuple[int, dict]:
     
    return aa