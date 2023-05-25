# import pandas as pd
# from sqlalchemy import create_engine
from tabelas.gerador import tables
import os

# Limpa o terminal
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

loggedIn = False

def SimNao():
    while True:
        escolha = input(  
                "* (S) Sim \n"
                "* (N) Não \n"
                "-> "
                ).upper()

        if escolha not in ["N", "S", "SIM", "NAO"]:
            print("\nResposta inválida, tente novamente...")
            continue
        else:
            return escolha

def checkEmail(Email):
    # checa se o email existe na tabela "cliente", se existe fala "O email inserido já possui cadastro na livraria"
    if tables['cliente'].read('email', email = Email, search_type = "email"):
        return False
    # se não, ele vai pra próxima etapa de registro
    return True


def checkUsername(Usuario):
    # checa se o nome do usuário existe na tabela "cliente", se não, para e fala: "Usuário não encontrado no registro"
    if tables['cliente'].read('usuario', usuario = Usuario, search_type = "usuario"):
        return False
    # se não, ele vai pra próxima etapa de registro
    return True


def checkPassword(Usuario, senha):
    # checa se a senha do usuário coincide com a senha registrada desse usuaŕio na tabela "cliente"
    if tables['cliente'].read('senha', usuario = Usuario, search_type = "usuario")[0][0] == senha:
        return True
    # se digitada corretamente, libera o login
    return False


def registered(Nome, Usuario, Email, Senha, flamengo):
    tables['cliente'].insert(nome = Nome, usuario = Usuario, email = Email, senha = Senha, isFlamengo = flamengo)
    clear_terminal()
    print("\n\tRegistro feito com sucesso!\n")
    main_menu()
    quit()


def Login():
    print("\n\t#####################"
            "\t### Tela de Login ###"
            "\t#####################")
          
    usuario = input("\n\tNome de usuário: ")
    if (checkUsername(usuario)):
        # print("\n\tEsse nome de usuário ainda não possui cadastro na livraria, voltando ao menu principal...\n")
        print("\n\tEsse nome de usuário ainda não possui cadastro na livraria, deseja fazer o cadastro?\n")
        deseja = SimNao()

        if deseja == "S" or deseja == "SIM":
            Register()
        else:
            print("\nVoltando ao menu principal...\n")
            main_menu()
            quit()

    senha = input("\tSenha: ")
    if (not checkPassword(usuario, senha)):
        print("\n\tA senha inserida não coincide com o usuário cadastrado, tente novamente:\n")
        senha = input("\tSenha: ")
        if (not checkPassword(usuario, senha)):
            print("\n\tA senha inserida não coincide com o usuário cadastrado, voltando ao menu principal...\n")
            main_menu()
            quit()

    clear_terminal()
    loggedIn = True
    menuloggedIn(loggedIn, usuario)
    quit()


def Register():
    print("\n\t######################"
            "  ### Tela de Cadastro ###  "
            "######################")
          
    name = input("\n\tNome completo: ")
    # aqui não precisa de verificação nenhuma pq podem existir vários usuários com o mesmo nome

    email = input("\tEmail: ")
    if(not checkEmail(email)):
        print("\n\tO email inserido já possui cadastro na livraria, voltando ao menu principal...\n")
        main_menu()
        quit()

    usuario = input("\tNome de usuário: ")
    if(not checkUsername(usuario)):
        print("\n\tEsse nome de usuário já possui cadastro na livraria, voltando ao menu principal...\n")
        main_menu()
        quit()

    senha = input("\tSenha: ")
    senha_verificacao = input("\tVerificação da senha: ")
    
    if senha != senha_verificacao:
        print("\n\tAs senhas digitadas não coincidem, por favor tente novamente:")
        senha = input("\tSenha: ")
        senha_verificacao = input("\tVerificação da senha: ")
        
    if senha != senha_verificacao:
        print("\n\tAs senhas digitadas não coincidem, voltando ao menu principal...\n")
        main_menu()
        quit()

    print(("\tÉ flamenguista?"))
    isFlamengo = SimNao()
    if isFlamengo == "S" or isFlamengo == "SIM":
        isFlamengo = True
    else:
        isFlamengo = False

    registered(name, usuario, email, senha, isFlamengo)


def pesquisa(p, loggedIn, usuario = ''):

    search_type = {
            "D" : "amostra",
            "T" : "titulo",
            "A" : "autor",
            "P" : "ano de publicacao",
            "V" : "Voltar"
            }[p]

    table_livro = tables['livro']

    if p == "V":
        clear_terminal()
        if loggedIn:
            print("\nVoltando ao menu da sua conta...\n")
            menuloggedIn(loggedIn, usuario)
        print("\nVoltando ao menu principal...\n")
        main_menu()
            

    if p == "D":
        if (ret := table_livro.read_all('titulo')):

            clear_terminal()
            print(f"\nAlguns livros contidos no estoque da nossa livraria:")
            i = 0
            for row in ret:
                if i <=50:
                    i +=1
                    print(f" {i} - {row[0]}")
                else:
                    print("...")
                    break

            if loggedIn:
                print("\nDeseja comprar algum livro destacado acima?\n")
                comprar = SimNao()
                if comprar == "S" or comprar == "SIM":
                    index = input("\nInforme o índice do livro que deseja comprar dentre os que estão destacado acima:\n-> ")
                    while not index.isnumeric() or int(index) <= 0 or int(index) > i:
                        index = input("\nPor favor informe um índice válido (número destacado a esquerda do título do livro):\n-> ")
                    compra(loggedIn, usuario, ret[int(index) - 1][0])
                else:
                    clear_terminal()
                    print("\nCompra cancelada")
                    print("\nVoltando ao menu da sua conta...\n")
                    menuloggedIn(loggedIn, usuario)
            else:
                print("\nDeseja fazer login para comprar algum livro destacado acima?\n")
                deseja = SimNao()
                if deseja == "S" or deseja == "SIM":
                    clear_terminal()
                    Login()
                else:
                    clear_terminal()
                    print("\nVoltando ao menu principal...\n")
                    main_menu()
                    
    else:
        clear_terminal()
        key_word = input(f"\nPor favor informe o {search_type} do livro desejado:\n-> ")
        
        if p == "T":
            Titulo = key_word
            if (table_livro.read('titulo', titulo = Titulo, search_type = 'titulo')):

                if loggedIn:
                    print("\nLivro encontrado, deseja comprá-lo?\n")
                    comprar = SimNao()
                    if comprar == "S" or comprar == "SIM":
                        compra(loggedIn, usuario, Titulo)
                    else:
                        clear_terminal()
                        print("\nCompra cancelada")
                        print("\nVoltando ao menu da sua conta...\n")
                        menuloggedIn(loggedIn, usuario)
                else:
                    print("\nLivro encontrado, deseja fazer login para comprá-lo?\n")
                    deseja = SimNao()
                    if deseja == "S" or deseja == "SIM":
                        clear_terminal()
                        Login()
                    else:
                        clear_terminal()
                        print("\nVoltando ao menu principal...\n")
                        main_menu()
                        


            else:
                print(f"\nNenhum livro no estoque da livraria possui o título '{Titulo}'.")
                if loggedIn:
                    print("\nVoltando ao menu da sua conta...\n")
                    menuloggedIn(loggedIn, usuario)
                else:
                    print("\nVoltando ao menu principal...\n")
                    main_menu()

        elif p == "A":
            Autor = key_word
            if (ret := table_livro.read('titulo', autor = Autor, search_type = 'autor')):

                clear_terminal()
                print(f"\nLivros escritos por {Autor}:")
                i = 0
                for row in ret:
                    if i <=50:
                        i +=1
                        print(f" {i} - {row[0]}")
                    else:
                        print("...")
                        break

                if loggedIn:
                    print("\nDeseja comprar algum livro destacado acima?\n")
                    comprar = SimNao()
                    if comprar == "S" or comprar == "SIM":
                        index = input("\nInforme o índice do livro que deseja comprar dentre os que estão destacado acima:\n-> ")
                        while not index.isnumeric() or int(index) <= 0 or int(index) > i:
                            index = input("\nPor favor informe um índice válido (número destacado a esquerda do título do livro):\n-> ")
                        
                        compra(loggedIn, usuario, ret[int(index) - 1][0])
                    else:
                        clear_terminal()
                        print("\nCompra cancelada")
                        print("\nVoltando ao menu da sua conta...\n")
                        menuloggedIn(loggedIn, usuario)
                else:
                    print("\nDeseja fazer login para comprar algum livro destacado acima?\n")
                    deseja = SimNao()
                    if deseja == "S" or deseja == "SIM":
                        clear_terminal()
                        Login()
                    else:
                        clear_terminal()
                        print("\nVoltando ao menu principal...\n")
                        main_menu()
            else:
                print(f"\nNenhum livro no estoque da livraria foi escrito por '{Autor}'.")
                if loggedIn:
                    print("\nVoltando ao menu da sua conta...\n")
                    menuloggedIn(loggedIn, usuario)
                else:
                    print("\nVoltando ao menu principal...\n")
                    main_menu()
        else:
            while not (key_word.isnumeric()) or int(key_word) >= 10000 or int(key_word) <= 0:
                key_word = input("\nPor favor informe um número válido para o ano de publicação do livro:\n-> ")
            anoPublicacao = key_word
            if (ret := table_livro.read('titulo', ano_publicacao = anoPublicacao, search_type = 'ano_publicacao')):

                clear_terminal()
                print(f"\nLivros publicados no ano de {anoPublicacao}:")
                i = 0
                for row in ret:
                    if i <=50: # pra mostrar só os 50 primeiros livros
                        i+=1
                        print(f" {i} - {row[0]}")
                    else:
                        print("...")
                        break

                if loggedIn:
                    print("\nDeseja comprar algum livro destacado acima?\n")
                    comprar = SimNao()
                    if comprar == "S" or comprar == "SIM":
                        index = input("\nInforme o índice do livro que deseja comprar dentre os que estão destacado acima:\n-> ")
                        while not index.isnumeric() or int(index) <= 0 or int(index) > i:
                            index = input("\nPor favor informe um índice válido (número destacado a esquerda do título do livro):\n-> ")
                        compra(loggedIn, usuario, ret[int(index) - 1][0])
                    else:
                        clear_terminal()
                        print("\nCompra cancelada")
                        print("\nVoltando ao menu da sua conta...\n")
                        menuloggedIn(loggedIn, usuario)
                else:
                    print("\nDeseja fazer login para comprar algum livro destacado acima?\n")
                    deseja = SimNao()
                    if deseja == "S" or deseja == "SIM":
                        clear_terminal()
                        Login()
                    else:
                        clear_terminal()
                        print("\nVoltando ao menu principal...\n")
                        main_menu()
            else:
                print(f"\nNenhum livro no estoque da livraria foi publicado no ano de {anoPublicacao}.")
                if loggedIn:
                    print("\nVoltando ao menu da sua conta...\n")
                    menuloggedIn(loggedIn, usuario)
                else:
                    print("\nVoltando ao menu principal...\n")
                    main_menu()
    quit()


def bookSearch(loggedIn, usuario = ''):
    clear_terminal()
    
    search_c = ["D", "T", "A", "P", "V"]
    print("\nAqui você consegue consultar os livros contidos no estoque da nossa livraria:\n")

    while True:
        p = input(
                "* (D) Ver alguns títulos disponíveis \n"
                "* (T) Pesquisa por título \n"
                "* (A) Pesquisa por autor \n"
                "* (P) Pesquisa por ano de publicação \n\n"
                "* (V) Voltar \n\n"
                "-> "
                )
        p = p.upper()

        if p not in search_c:
            print("\nDesculpe, tente novamente...\n")
            continue
        else:
            break

    pesquisa(p, loggedIn, usuario)


def quitLibrary():
    print("\n\tFechando o sistema...")
    print("\n\tObrigado por visitar a livraria Tuko!\n")
    quit()

def compra(loggedIn, Usuario, Titulo):
    livros = tables['livro']
    clientes = tables['cliente']
    pedidos = tables['pedido']

    idCliente = clientes.read('id_cliente', usuario = Usuario, search_type = 'usuario')[0][0]
    idLivro = livros.read('id_livro', titulo = Titulo, search_type = 'titulo')[0][0]
    preco = livros.read('preco', titulo = Titulo, search_type = 'titulo')[0][0]

    clear_terminal()
    print(f"\nConfirmar compra do livro '{Titulo}' no valor {preco:.2f}?")
    deseja = SimNao()
    
    flamenguista = clientes.read('isFlamengo', usuario = Usuario, search_type = 'usuario')[0][0]
    
    if deseja == "S" or deseja == "SIM":
        if flamenguista:
            print("\nParabéns, você acaba de ganhar um desconto de 15% nessa compra por ser flamenguista.")
            preco = preco * (1 - 0.15)
        
        print(f"\nProcessando pagamento...")
        print(f"Compra autorizada no valor de R$ {preco:.2f}.")
        
        pedidos.insert(id_cliente = idCliente, id_livro = idLivro, custo = preco)
        
        print("Livro comprado!")
        print("\nSeu livro agora pode ser visualizado na aba de pedidos no menu de sua conta.")
        print("\nVoltando ao menu da sua conta...")
        
        menuloggedIn(loggedIn, Usuario)
    else:
        clear_terminal()
        print("\nCompra cancelada")
        print("\nVoltando ao menu da sua conta...")
        menuloggedIn(loggedIn, Usuario)


def verPedidos(loggedIn, Usuario):
    clear_terminal()
    clientes = tables['cliente']

    idCliente = clientes.read('id_cliente', usuario = Usuario, search_type='usuario')[0][0]
    if(idLivro := clientes.query(f"SELECT id_livro FROM pedido WHERE {idCliente} = pedido.id_cliente")):
        print("\nHistórico dos seus pedidos:\n")
        qtd_pedidos = clientes.query(f"SELECT COUNT (id_livro) FROM pedido WHERE {idCliente} = pedido.id_cliente")[0][0]
        i = 0
        for i in range (qtd_pedidos):
            titulo = clientes.query(f"SELECT titulo FROM livro WHERE {idLivro[i][0]} = livro.id_livro")[0][0]
            # print(titulo)
            preco = clientes.query(f"SELECT custo FROM pedido WHERE {idCliente} = pedido.id_cliente")[i][0]
            # print(preco)
            print(f" {i+1} - {titulo} | R$ {preco:.2f}")    
        if i>=50:
            print("...")
        
    else:
        print("\nVocê ainda não fez nenhum pedido.")


    print("\nVoltando ao menu da sua conta...")
    menuloggedIn(loggedIn, Usuario)


def mostra_clientes():
    clear_terminal()
    clientes = tables['cliente']
    nomes = clientes.read_all('nome')
    if nomes:
        print("\nClientes cadastrados na livraria:\n")
        i = 0
        for row in nomes:
            if i <=50: # pra mostrar só os 50 primeiros clientes
                i+=1
                print(f"Cliente {i} - {row[0]}")
            else:
                print("...")
                break
    else:
        print("\nNão há nenhum cliente cadastrado ainda.")

    print("\nVoltando ao menu principal...\n")
    main_menu()


def mostra_vendas():
    clear_terminal()
    pedidos = tables['pedido']
    vendas = pedidos.read_all('id_pedido, custo')
    if vendas:
        print("\nVendas registradas na livraria:\n")
        i = 0
        for row in vendas:
            if i <=50: # pra mostrar só as 50 primeiras vendas
                i+=1
                print(f"Venda {row[0]} - R$ {row[1]:.2f}")
            else:
                print("...")
                break
    else:
        print("\nNão há nenhuma venda registrada ainda.")
        
    print("\nVoltando ao menu principal...\n")
    main_menu()


def menu(loggedIn):
    menu_c = ["L", "C", "P", "U", "V", "Q"]
    print("O que deseja fazer?")
    while True:
        choice = input( 
                "* (L) Realizar login \n"
                "* (C) Realizar cadastro \n"
                "* (P) Pesquisar livro \n"
                "* (U) Ver clientes cadastrados \n"
                "* (V) Ver vendas da livraria \n"
                "* (Q) Sair do sistema \n"
                "-> "
                )

        choice = choice.upper()

        if choice not in  menu_c:
            print("\nDesculpe, tente novamente...\n")
            continue
        else:
            break

    if choice   == "L":
        Login()
    elif choice == "C":
        Register()
    elif choice == "P":
        bookSearch(loggedIn)
    elif choice == "U":
        mostra_clientes()
    elif choice == "V":
        mostra_vendas()
    elif choice == "Q":
        quitLibrary()
    else:
        print("Deu ruim")
        exit(-666)


def menuloggedIn(loggedIn, usuario):

    print(f"\n\tOlá seja bem vindo de volta!\n")
    menu_c = ["C", "P", "S", "Q"]
    print("O que deseja fazer?")
    while True:
        choice = input(
                "* (C) Realizar compra\n"
                "* (P) Ver todos seus pedidos\n"
                "* (S) Sair da conta\n"
                "* (Q) Sair do sistema\n"
                "-> "
                )

        choice = choice.upper()

        if choice not in  menu_c:
            print("\nDesculpe, tente novamente...\n")
            continue
        else:
            break

    if choice   == "C":
        bookSearch(loggedIn, usuario)
    elif choice == "P":
        verPedidos(loggedIn, usuario)
    elif choice == "S":
        clear_terminal()
        print("\nCliente deslogado.")
        print("Voltando ao menu principal...\n")
        menu(loggedIn)
    elif choice == "Q":
        quitLibrary()
    else:
        print("Deu ruim")
        exit(-666)


def main_menu():
    loggedIn = False
    usuario = "\nbugou!!!\n"
    if loggedIn:
        menuloggedIn(loggedIn, usuario)
    else:
        menu(loggedIn)


def main():
    print("\n\t########################################################\n"
            "\t######## Olá seja bem vindo a livraria Tuko! ###########\n"
            "\t########################################################\n")
    main_menu()

if __name__ == "__main__":
    main()


# Testando o uso de dataFrames
# def get_books():
#     for row in tables['livro'].read_all():
#         print(row)
#     print()

# def get_users():
#     for row in tables['cliente'].read_all():
#         print(row)
#     print()

# def main():
#     # Create an engine instance
#     alchemyEngine   = create_engine('postgresql+psycopg2://postgres:1234@localhost:5432')
#     # Connect to PostgreSQL server
#     dbConnection    = alchemyEngine.connect()
#     # Create a dataframe
#     clienteDF = pd.read_sql_query("SELECT * FROM cliente;", dbConnection)
#     livroDF = pd.read_sql_query("SELECT * FROM livro;", dbConnection)

#     print(clienteDF.head())
#     print(livroDF.head())
    
#     get_books()
#     get_users()
# Testando o uso de dataFrames