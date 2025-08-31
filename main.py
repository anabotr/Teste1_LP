import operacoes_banco as ope
"""
Módulo de interação do banco com o usuário, seu comportamento é guiado pelas escolhas do usuário no terminal. 
"""

#Foram criadas flags para definir se os loops devem ou não continuar rodando, sendo uma para o loop geral, e uma para cada tipo de usuário
flag = True
fgerente = False
fcliente = False

while flag:
    print("""Bem-vindo ao Banco Digital!\n
        Escolha o modo de operação:\n
        1 - Operações de Gerente\n
        2 - Operações de Cliente\n
        3 - Sair\n""")
    print('-'*80)
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
            print('-'*80)
            resp_gerente = input()

            if resp_gerente == '1':
                total = ope.somar_saldos_gerais()
                print(f"R$:{total}")
                print('-'*80)

            elif resp_gerente == '2':
                rico = ope.identificar_cliente_mais_rico()
                print(f"O cliente mais rico é {list(rico.values())[0]}")
                print('-'*80)

            elif resp_gerente == '3':
                numero_conta = []
                deposito = []
                print('Insira os dados solicitados, quando acabar, deixe o campo conta vazio.')
                print('-'*80)
                conta_deposito = input("Conta: ")
                numero_conta.append(conta_deposito)
                while conta_deposito != "": 
                    valor_deposito = ope.trata_float(input("Valor: "))
                    print("-"*80)
                    deposito.append(valor_deposito)
                    conta_deposito = input("Conta:")
                    numero_conta.append(conta_deposito)
                
                numero = ope.somar_saldos_em_lote(numero_conta = numero_conta, deposito = deposito)
                print(f"Operação realizada com sucesso, {numero} conta(s) modificadas")
                print('-'*80)
                
            elif resp_gerente == '4':
                numero_conta = []
                saque = []
                print('Insira os dados solicitados, quando acabar, deixe o campo conta vazio.')
                print('-'*80)
                conta_saque = input("Conta: ")
                numero_conta.append(conta_saque)
                while conta_saque != "": 
                    valor_saque = ope.trata_float(input("Valor: "))
                    print("-"*80)
                    saque.append(valor_saque)
                    conta_saque = input("Conta: ")
                    numero_conta.append(conta_saque)
                numero = ope.subtrair_saldos_em_lote(numero_conta = numero_conta, saque = saque)
                print(f"Operação realizada com sucesso, {numero} conta(s) modificadas.")
                print('-'*80)

            elif resp_gerente == '5':
                print('Insira o número da conta:')
                numero_conta = input()
                print("Insira o Nome do cliente: ")
                nome_cliente = input()
                conta = ope.criar_conta(numero_conta, nome_cliente)
                if conta != None: 
                    print(f"Conta criada com sucesso! \"Numero da conta\": {conta[0]}, \"Cliente\": {conta[1]}"  )
                    print('-'*80)
                else: 
                    print("Informações inválidas")

            elif resp_gerente == '6':
                fgerente = False
                print('-'*80)

            else:
                print("Entrada inválida")
                print('-'*80)

    elif resposta == "2":
        print("Digite o número da conta:")
        conta = input()
    
        if ope.conta_in_bd(conta) != True: #quando deixa como true ele mostra o index value do carrega banco de dados e continua
            print("Erro: Conta inexistente.")
            print('-'*80)
        else:
            print('-'*80)
            fcliente = True
            while fcliente:
                print("""Escolha uma operação:\n
                    1 - Consultar meu saldo\n
                    2 - Realizar um depósito\n
                    3 - Realizar um saque\n
                    4 - Realizar uma transferência\n
                    5 - Voltar ao menu principal\n""")
                print('-'*80)
                resp_cliente = input()

                if resp_cliente == '1':
                    print("Seu saldo atual é de:" , ope.consultar_saldo(conta))
                    print('-'*80)
                if resp_cliente == '2':
                    print('Insira o valor do depósito: ')
                    valor = ope.trata_float(input())
                    if valor != None:
                        operacao = ope.depositar(conta, valor)
                        total = ope.consultar_saldo(conta)
                        print(f"{operacao[1]}! Seu saldo atual é: {total}" )
                    else: 
                        print('Valor inválido')
                    print('-'*80)

                if resp_cliente == '3':
                    print('Insira o valor do saque: ')
                    valor = ope.trata_float(input())
                    if valor != None:
                        operacao = ope.sacar(conta, valor)
                        total = ope.consultar_saldo(conta)
                        print(f"{operacao[1]}! Seu saldo atual é: {total}" )
                    else: 
                        print('Valor inválido')
                    print('-'*80)

                if resp_cliente == '4':
                    print("Insira a conta que receberá o depósito: ")
                    conta_destino = input()
                    if conta_destino.isnumeric() == True: 
                        print("Insira o valor: ")
                        valor = ope.trata_float(input())
                        if valor == None: 
                            print("Valor inválido")
                        if valor != None: 
                            tupla = ope.realizar_transferencia(conta_origem = conta, conta_destino=conta_destino, valor=valor)
                            print(tupla[1])
                    else: 
                        print("Valor inválido")
                    print('-'*80)
                if resp_cliente == '5':
                    fcliente = False
                    print('-'*80)
    elif resposta == '3': 
        flag = False
        print('-'*80)
    else:
        flag = True 
        print("Entrada inválida, escolha novamente")
        print('-'*80)

