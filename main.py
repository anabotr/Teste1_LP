#Foram criadas flags para definir se os loops devem ou não continuar rodando, sendo uma para o loop geral, e uma para cada tipo de usuário
flag = True
fgerente = False
fcliente = False

import operacoes_banco as ope

while flag:
    print("""Bem-vindo ao Banco Digital!\n
        Escolha o modo de operação:\n
        1 - Operações de Gerente\n
        2 - Operações de Cliente\n
        3 - Sair\n""")
    resposta = input()

    if resposta == "1":
        fgerente = True
        while fgerente:
            print("""Escolha uma operação:\n
                1 - Verificar saldo total do banco\n
                2 - Identificar cliente mais rico\n
                3 - Adicionar fundos em lote\n
                4 - Debitar fundos em lote\n
                5 - Abrir uma nova conta no banco\n
                6 - Voltar ao menu principal\n""")
            resp_gerente = input()

            if resp_gerente == '1':
                total = ope.somar_saldos_gerais()
                print(total)
            elif resp_gerente == '2':
                rico = ope.identificar_cliente_mais_rico()
                print(rico)
            elif resp_gerente == '3':
                numero_conta = []
                deposito = []
                print('coloca dindin ai pra mim')
                conta_deposito = input("Em qual conta?")
                valor_deposito = input("Qual valor?")
                numero_conta.append(conta_deposito)
                deposito.append(valor_deposito)
                print("Mais alguma conta?\n 1. SIM\n 2. NÃO")
                resp_gerente3 = input()
                while resp_gerente3 == '1': 
                    conta_deposito = input("Em qual conta?")
                    valor_deposito = input("Qual valor")
                    numero_conta.append(conta_deposito)
                    deposito.append(valor_deposito)
                    resp_gerente3 = input("Mais alguma conta?\n 1. SIM\n 2. NÃO")
                if resp_gerente3 != '1':
                    pass
                ope.somar_saldos_em_lote(numero_conta = numero_conta, deposito = deposito)
            elif resp_gerente == '4':
                print('jesus ta tirando dinheiro')
                fundos_rm = input()
            elif resp_gerente == '5':
                print('abra essaconta')
                numero_conta = input()
                nome_cliente = input()
            elif resp_gerente == '6':
                fgerente = False
            else:
                print("Entrada inválida")
    elif resposta == "2":
        print("Digite o número da conta:")
        conta = input()
        # verifica se a conta ta no banco de dados
        if conta == 'false':
            esta = False
            print("Erro: Conta inexistente.")

        else:
            esta = True
            while esta:
                print("""Escolha uma operação:\n
                    1 - Consultar meu saldo\n
                    2 - Realizar um depósito\n
                    3 - Realizar um saque\n
                    4 - Realizar uma transferência\n
                    5 - Voltar ao menu principal\n""")
                resp_cliente = input()

                if resp_cliente == '1':
                    print('oia o saldo ai')
                if resp_cliente == '2':
                    print("deposita essa grana ai")
                    valor = input()
                if resp_cliente == '3':
                    print('saca o dindin')
                    valor = input()
                if resp_cliente == '4':
                    print('transfere pra eu')
                    conta_destino = input()
                    valor = input()
                if resp_cliente == '5':
                    esta = False
    elif resposta == '3': 
        flag = False
    else:
        print("Entrava inválida")

