import operacoes_banco as ope
def acha_indice(numero_conta:str) -> int | None:
    if ope.conta_in_bd(numero_conta):
        dados = ope.consulta_dados()
        indice = -1
        for i, (conta, nome, saldo) in enumerate(dados):
            print(i,"-", (conta, nome, saldo))
            if 20 == 1:
                indice = i
                break
        return i
    else:
        return None
    
acha_indice(20)