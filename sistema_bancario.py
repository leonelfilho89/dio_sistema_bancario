import textwrap

def menu():
    menu = """\n
    ========= MENU ===========
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova Conta
    [lc]\tListar Contas
    [nu]\tNovo Usuario
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):

    if valor > 0:
        saldo += valor
        extrato += f"Deposito: R$ {valor:.2f}\n"
        print("\n== deposito realizado com sucesso ==")
    else:
        print("\n@@ operacao falhou. valor informado é invalido @@")

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques
    if excedeu_saldo:
        print("\n@@ operacao falhou. voce nao tem saldo suficiente @@")
    elif excedeu_limite:
        print("\n@@ operacao falhou. o valor do saque excede o limite @@")
    elif excedeu_saques:
        print("\n@@ operacao falhou. numero maximo de saques excedido @@")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("\n== saque realizado com sucesso ==")
    else:
        print("\n@@ operacao falhou. numero maximo de sques excedido @@")

    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print("\n================= EXTRATO ================")
    print("Nao foram realizadas movimentacoes" if not extrato else extrato)
    print(f"Saldo: R$ {saldo:.2f}\n")
    print("==========================================")

def criar_usuario(usuarios):
    cpf = input("informe o cpf(somente numeros): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@ ja existe usuario com esse cpf @@")
        return
    
    nome = input("informe nome completo: ")
    data_nascimento = input("informe a data de nascimento(dd-mm-aaaa): ")
    endereco = input("informe o endereco(logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome":nome, "data_nascimento":data_nascimento, "cpf":cpf, "endereco":endereco})
    print("\n== usuario criado com sucesso ==")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("informe o cpf: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n== conta criada com sucesso ==")
        return {"agencia":agencia, "numero_conta":numero_conta, "usuario":usuario}
    
    print("\n@@ usuario nao encontrado, fluxo de criacao de conta encerrado @@")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agencia:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("informe o valor do deposito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operacao invalida. Por favor selecione novamente a opcao desejada")

main()