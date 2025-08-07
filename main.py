from voo_app.domain.entities.bagagem import Bagagem
from voo_app.domain.entities.pessoa import Pessoa
from voo_app.domain.entities.passageiro import Passageiro
from voo_app.domain.entities.funcionario import Funcionario
from voo_app.domain.entities.companhia_aerea import CompanhiaAerea
from voo_app.domain.entities.mini_aeronave import MiniAeronave
from voo_app.domain.entities.voo import Voo
from voo_app.infrastructure.database.connect import SessionLocal
from voo_app.infrastructure.database.models import CompanhiasModel, PessoaModel
from voo_app.infrastructure.database.models_method import cadastrar_companhia, mudar_nome_companhia, tabela_pessoas, tabela_companhias, tabela_passageiros, cadastrar_pessoa, listar_companhias, add_miniaeronave_db, tabela_funcionarios, tabela_voo, cadastrar_passageiro, tabela_aeronaves, cadastrar_voo
from voo_app.interface_adapters.presenters.relatorio_builder import _RelatorioBuilder
from voo_app.infrastructure.database.models_method import cadastrar_funcionario



pessoas = []
passageiros = []
funcionarios = []
voos = []
companhias = []

def encontrar_pessoa_por_cpf(cpf):
    session = SessionLocal()
    try:
        pessoa = session.query(PessoaModel).filter(PessoaModel.cpf == cpf).first()
        return pessoa
    finally:
        session.close()

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
    session = SessionLocal()
    try:
        companhia = session.query(CompanhiasModel).filter(CompanhiasModel.nome == nome).first()
        return companhia
    finally:
        session.close()

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
        print("15. Cadastrar Aeronave")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome da companhia: ")
            cadastrar_companhia(nome)
        elif opcao == "2":
            tabela_companhias()
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
                        nome_atual = companhia.nome
                        novo_nome = input("Novo nome: ")
                        mudar_nome_companhia(nome_atual, novo_nome)
                    elif sub_opcao == "2":
                        tabela_voos = companhia.listar_voos()
                        print(tabela_voos)
                    elif sub_opcao == "3":
                        tabela_voo()
                        companhiaclass = CompanhiaAerea(companhia.nome)
                        cod = input("Código do voo: ")
                        voo = companhiaclass.buscar_voo(cod)
                        if voo:
                            construro = _RelatorioBuilder(f"Voo {voo.codigo}")
                            construro.adicionar_colunas(
                                ("Origem", "yellow", "center"),
                                ("Destino", "green", "center"),
                                ("Aeronave", "white", "center")
                            )
                            construro.adicionar_linhas(
                                voo.origem,
                                voo.destino,
                                voo.aeronave
                            )
                            print(construro.construir())
                        else:
                            print("Voo não encontrado.")
                    elif sub_opcao == "4":
                        tabela_aeronaves()
                        aeronave_id = int(input("ID da aeronave: "))
                        origem = input("Origem do voo: ")
                        destino = input("Destino do voo: ")
                        cadastrar_voo(origem, destino, aeronave_id)
                    elif sub_opcao == "0":
                        break
            else:
                print("Companhia não encontrada.")

        elif opcao == "3":
            nome = input("Nome: ")
            cpf = input("CPF: ")
            cadastrar_pessoa(nome, cpf)

        elif opcao == "4":
            tabela_pessoas()
        elif opcao == "5":
            tabela_pessoas()
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
                    passageiro.adicionar_bagagem(bagagem) # Certifique-se de ter a função correta para cadastrar passageiro no banco
                cadastrar_passageiro(passageiro.nome, passageiro.cpf, passageiro.bagagens)
                print("Passageiro cadastrado.")
            else:
                print("Pessoa não encontrada.")

        elif opcao == "6":
            tabela_passageiros()
        elif opcao == "7":
            cpf = input("CPF: ")
            pessoa = encontrar_pessoa_por_cpf(cpf)
            if pessoa:
                cargo = input("Cargo: ")

                # Adiciona o funcionário no banco de dados
                cadastrar_funcionario(pessoa.nome, pessoa.cpf, cargo)
            else:
                print("Pessoa não encontrada")

        elif opcao == "8":
            tabela_funcionarios()

        elif opcao == "9":
            codigo = input("Código do voo: ")
            companhia_nome = input("Nome da companhia aérea: ")
            companhia = encontrar_companhia_por_nome(companhia_nome)
            if not companhia:
                print("Companhia não encontrada.")
            else:
                if companhia.buscar_voo(codigo):
                    print("Voo já cadastrado para esta companhia.")
                else:
                    novo_voo = Voo(codigo)
                    companhia.adicionar_voo(novo_voo)
                    print("Voo cadastrado com sucesso no banco de dados.")

        elif opcao == "10":
            tabela_voo()

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
        
        elif opcao == "15":
            modelo = input("Modelo da aeronave: ")
            capacidade = int(input("Capacidade: "))
            nova_aeronave = MiniAeronave(modelo, capacidade)
            add_miniaeronave_db(nova_aeronave)

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()