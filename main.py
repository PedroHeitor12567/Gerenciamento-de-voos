from voo_app.domain.entities.bagagem import Bagagem
from voo_app.domain.entities.pessoa import Pessoa
from voo_app.domain.entities.passageiro import Passageiro
from voo_app.domain.entities.funcionario import Funcionario
from voo_app.domain.entities.voo import Voo
from voo_app.domain.entities.companhia_aerea import CompanhiaAerea

pessoas = []
passageiros = []
funcionarios = []
voos = []
companhias = []

def encontrar_pessoa_por_cpf(cpf):
    for pessoa in pessoas:
        if pessoa.cpf == cpf:
            return pessoa
    return None

def encontrar_passageiro_por_cpf(cpf):
    for passageiro in passageiros:
        if passageiro.cpf == cpf:
            return passageiro
    return None

def encontrar_funcionario_por_cpf(cpf):
    for funcionario in funcionarios:
        if funcionario.cpf == cpf:
            return funcionario
    return None

def encontrar_voo_por_codigo(codigo):
    for voo in voos:
        if voo.codigo == codigo:
            return voo
    return None

def encontrar_companhia_por_nome(nome):
    for companhia in companhias:
        if companhia.nome == nome:
            return companhia
    return None

def menu():
    while True:
        print("\n--- MENU ---")
        print("1. Criar Companhia Aérea")
        print("2. Acessar Companhias Aéreas")
        print("3. Cadastrar Pessoa")
        print("4. Listar Pessoas")
        print("5. Cadastrar Passageiro")
        print("6. Listar Passageiros")
        print("7. Cadastrar Funcionário")
        print("8. Listar Funcionários")
        print("9. Cadastrar Voo")
        print("10. Listar Voos")
        print("11. Adicionar Passageiro ao Voo")
        print("12. Adicionar Tripulação ao Voo")
        print("13. Listar Passageiros no Voo")
        print("14. Listar Tripulação no Voo")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome da companhia: ")
            companhias.append(CompanhiaAerea(nome))
            print("Companhia criada.")

        elif opcao == "2":
            nome = input("Nome da companhia a acessar: ")
            companhia = encontrar_companhia_por_nome(nome)
            if companhia:
                while True:
                    print(f"\n--- Companhia {companhia.nome} ---")
                    print("1. Mudar nome")
                    print("2. Listar voos")
                    print("3. Buscar voo")
                    print("4. Adicionar voo")
                    print("0. Voltar")
                    sub_opcao = input("Escolha uma opção: ")
                    if sub_opcao == "1":
                        novo_nome = input("Novo nome: ")
                        companhia.nome = novo_nome
                    elif sub_opcao == "2":
                        for v in companhia.listar_voos():
                            print(v)
                    elif sub_opcao == "3":
                        cod = input("Código do voo: ")
                        voo = companhia.buscar_voo(cod)
                        if voo:
                            print(voo)
                            print("Passageiros:")
                            for p in voo.passageiros:
                                print(p)
                                for b in p.listar_bagagens():
                                    print(f"  - {b}")
                            print("Tripulação:")
                            for f in voo.tripulacao:
                                print(f)
                        else:
                            print("Voo não encontrado.")
                    elif sub_opcao == "4":
                        codigo = input("Código do novo voo: ")
                        novo_voo = Voo(codigo)
                        companhia.adicionar_voo(novo_voo)
                        voos.append(novo_voo)
                        print("Voo adicionado.")
                    elif sub_opcao == "0":
                        break
            else:
                print("Companhia não encontrada.")

        elif opcao == "3":
            nome = input("Nome: ")
            cpf = input("CPF: ")
            if encontrar_pessoa_por_cpf(cpf):
                print("Pessoa já cadastrada.")
            else:
                pessoas.append(Pessoa(nome, cpf))
                print("Pessoa cadastrada.")

        elif opcao == "4":
            for p in pessoas:
                print(p)

        elif opcao == "5":
            cpf = input("CPF da pessoa: ")
            pessoa = encontrar_pessoa_por_cpf(cpf)
            if pessoa:
                passageiro = Passageiro(pessoa.nome, pessoa.cpf)
                while True:
                    desc = input("Descrição da bagagem (ou 'sair'): ")
                    if desc.lower() == 'sair':
                        break
                    peso = float(input("Peso da bagagem: "))
                    bagagem = Bagagem(desc, peso)
                    passageiro.adicionar_bagagem(bagagem)
                passageiros.append(passageiro)
                print("Passageiro cadastrado.")
            else:
                print("Pessoa não encontrada.")

        elif opcao == "6":
            for p in passageiros:
                print(p)
                for b in p.listar_bagagens():
                    print(f"  - {b}")

        elif opcao == "7":
            cpf = input("CPF: ")
            pessoa = encontrar_pessoa_por_cpf(cpf)
            if pessoa:
                funcionario = Funcionario(pessoa.nome, pessoa.cpf)
                cargo = input("Cargo: ")
                matricula = input("Matricula")
                funcionarios.append(Funcionario(cargo, matricula))
                print("Funcionário cadastrado.")
            else:
                print("Pessoa não encontrada")

        elif opcao == "8":
            for f in funcionarios:
                print(f)

        elif opcao == "9":
            codigo = input("Código do voo: ")
            if encontrar_voo_por_codigo(codigo):
                print("Voo já existe.")
            else:
                novo_voo = Voo(codigo)
                voos.append(novo_voo)
                print("Voo cadastrado.")

        elif opcao == "10":
            for v in voos:
                print(v)

        elif opcao == "11":
            cod = input("Código do voo: ")
            voo = encontrar_voo_por_codigo(cod)
            if voo:
                cpf = input("CPF do passageiro: ")
                passageiro = encontrar_passageiro_por_cpf(cpf)
                if passageiro:
                    voo.adicionar_passageiro(passageiro)
                    print("Passageiro adicionado ao voo.")
                else:
                    print("Passageiro não encontrado.")
            else:
                print("Voo não encontrado.")

        elif opcao == "12":
            cod = input("Código do voo: ")
            voo = encontrar_voo_por_codigo(cod)
            if voo:
                cpf = input("CPF do funcionário: ")
                funcionario = encontrar_funcionario_por_cpf(cpf)
                if funcionario:
                    voo.adicionar_funcionario(funcionario)
                    print("Funcionário adicionado ao voo.")
                else:
                    print("Funcionário não encontrado.")
            else:
                print("Voo não encontrado.")

        elif opcao == "13":
            cod = input("Código do voo: ")
            voo = encontrar_voo_por_codigo(cod)
            if voo:
                for p in voo.passageiros:
                    print(p)
                    for b in p.listar_bagagens():
                        print(f"  - {b}")
            else:
                print("Voo não encontrado.")

        elif opcao == "14":
            cod = input("Código do voo: ")
            voo = encontrar_voo_por_codigo(cod)
            if voo:
                for f in voo.tripulacao:
                    print(f)
            else:
                print("Voo não encontrado.")

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()