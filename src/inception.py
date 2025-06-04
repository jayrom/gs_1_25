
#---------------------------------------------------
# TiãoTech - Manutenção Preditiva de Infraestruturas Críticas (MPIC)
# Por favor, leia o README.md para mais informações.
#---------------------------------------------------


# Importa módulos.
import os
import oracledb
import pandas as pd

# Define arquivos de dados.
river_history_file = "input/ITAICI_river_history.csv"
bridge_history_file = "input/4E047_history.csv"
bridge_metadata_file = "input/4E047_metadata.csv"

margem = ' ' * 4

print("1 - OK")

# Popular histórico do rio

def store_river_history() -> None:

    print("Popular histórico do rio")
    input("Pressione ENTER.")

# Popular histórico da ponte

def store_bridge_history() -> None:

    print("Popular histórico da ponte")
    input("Pressione ENTER.")
    return

# Popular metadados da ponte

def store_bridge_metadata() -> None:

    print("Popular metadados da ponte")
    input("Pressione ENTER.")
    return

# Popular leituras do sensor

def store_sensor_data() -> None:

    print("Popular leituras do sensor")
    input("Pressione ENTER.")
    return

# Exibe menu

def exibe_menu() -> None:
    
    os.system('cls')

    # print("--- Gerenciar dados da base ---")
    print("""
        1 - Popular histórico do rio
        2 - Popular histórico da ponte
        3 - Popular metadados da ponte
        4 - Popular leituras do sensor
        5 - Sair
    """)

    menu_choice = int(input(margem + "Escolha -> "))

    match menu_choice:

        case 1:
            store_river_history()

        case 2:
            store_bridge_history()

        case 3:
            store_bridge_metadata()

        case 4:
            store_sensor_data()

        case 5:
            print("Encerrando o programa...")


 # Executa a aplicação se e enquanto houver conexão com o banco de dados.


# Conecta banco de dados.

def db_connect() -> None:
    try:
        # Efetua a conexão com o Usuário no servidor
        db_user = 'RM565576' # Insira a matrícula (ex.: RM123456)
        db_pass = 'Fiap#2025' # Insira a senha 
        conn = oracledb.connect(user=db_user, password=db_pass, dsn='oracle.fiap.com.br:1521/ORCL')

        # Cria as instruções para cada módulo
        inst_cadastro = conn.cursor()
        inst_consulta = conn.cursor()

    except Exception as e:   
        print("Erro: ", e) # Informa o erro
        conexao = False    # Não há conexão

    else:
        conexao = True    # Há conexão
        print("Conexão OK")

    while conexao:
        # os.system('cls')  
        exibe_menu()

db_connect()

