import pandas as pd 

def carregar_contas_de_csv(caminho_arquivo: str) -> dict: 
    arquivo = pd.read_csv(caminho_arquivo)
    saldo = [] 
    clientes = [] 
    numero_conta = []
    dicionario = {}


    for j in arquivo['numero_conta']:
        numero_conta.append(j)

    for m in arquivo['cliente']: 
        clientes.append(m)

    for p in arquivo['saldo']: 
        saldo.append(p)

    for i in range(len(clientes)):
        k = clientes[i]
        j = saldo[i]
        dicionario[f'{int(numero_conta[i]):04d}'] = {"cliente": k, "saldo": j}
    
        #dict['cliente'] = clientes[i-1]
        #dict['saldo'] = saldo[i-1] 
    print(dicionario)

carregar_contas_de_csv("C:/Users/lcone/.ipython/.vscode/lista1/contas.csv")
    


