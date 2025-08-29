#import pandas as pd 
import csv as cs


def carregar_contas_de_csv(caminho_arquivo: str) -> dict: 
    arquivo = read_csv(caminho_arquivo)
    saldo = [] 
    clientes = [] 
    numero_conta = []
    contas = {}


    for j in arquivo['numero_conta']:
        numero_conta.append(j)

    for m in arquivo['cliente']: 
        clientes.append(m)

    for p in arquivo['saldo']: 
        saldo.append(p)

    for i in range(len(clientes)):
        nome_clientes = clientes[i]
        quantidade_disponivel = saldo[i]
        contas[f'{int(numero_conta[i]):04d}'] = {"cliente": nome_clientes, "saldo": quantidade_disponivel}
    
        #dict['cliente'] = clientes[i-1]
        #dict['saldo'] = saldo[i-1] 
    return contas


def salvar_contas_para_csv(caminho_arquivo: str, contas: dict) -> None:
    with open(caminho_arquivo, "r") as file, open("temp12.txt", "w") as arquivo_temp:
        linhas = file.readlines()
        lista_contas = [] #lista dos clinetes
        k = 0
        for i in contas: 
            lista_contas.append([i,contas[f'{i}']])
        listadelinhas = []
        for i in linhas: 
            listadelinhas.append(i)
        cc= []
        for i in range(len(lista_contas)): 
            cc.append(f"{lista_contas[i]}")
    return 


    
conta = carregar_contas_de_csv("C:/Users/lcone/.ipython/.vscode/lista1/contas15.csv")
salvar_contas_para_csv("C:/Users/lcone/.ipython/.vscode/lista1/contas15.csv", conta)



