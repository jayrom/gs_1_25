
#---------------------------------------------------
# TiãoTech - Manutenção Preditiva de Infraestruturas Críticas (MPIC)
# Por favor, leia o README.md para mais informações.
#---------------------------------------------------


# Importa módulos.
import os
import oracledb
import pandas as pd

# Define arquivos de dados.
river_history_file = "document/data_inception/ITAICI_river_history.csv"
bridge_history_file = "document/data_inception/4E047_history.csv"
bridge_metadata_file = "document/data_inception/4E047_metadata.csv"
sensor_readings_file = "document/data_inception/4E047_sensor_readings.csv"

margem = ' ' * 4

# Popula histórico do rio

def store_river_history() -> None:

    print("Popular histórico do rio\n")

    river_history_data = None

    try:
        # Importa dados de leitura de sensores.
        river_history_data = pd.read_csv(river_history_file)
        print(f"Arquivo '{river_history_file}' carregado com sucesso.")

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{river_history_file}'")
        return
    except KeyError as e:
        print(f"Erro: coluna não encontrada. Verifique a correspondência com o arquivo de dados: {e}")
        return
    except Exception as e:
        print(f"Ocorreu um erro durante a importação: {e}")
        return

    # Verifica se o data frame está vazio.
    if river_history_data.empty:
        print("Erro: O data frame de histórico do rio está vazio.")
        return
    
    try:
        # Monta instruções SQL de inserção.
        sql_insert = """
        INSERT INTO T_4E_047_ITAICI_RIVER_HISTORY (
            reading_id,
            reading_timestamp,
            reading_water_level,
            flag_flood,
            reading_calculated_water_pressure,
            flag_overcharge
        ) VALUES (SEQ_T_4E_047_ITAICI_RIVER_HISTORY.NEXTVAL, :1, :2, :3, :4, :5)
        """

        # Itera sobre os registros do data frame de histórico.
        for index, row in river_history_data.iterrows():
            try:
                reading_timestamp = row['reading_timestamp']
                reading_water_level = float(row['reading_water_level']) 
                flag_flood = int(row['flag_flood'])
                reading_calculated_water_pressure = float(row['reading_calculated_water_pressure']) 
                flag_overcharge = int(row['flag_overcharge'])

                # Cria a tupla de um registro para inserção.
                values = (
                    reading_timestamp,
                    reading_water_level,
                    flag_flood,
                    reading_calculated_water_pressure,
                    flag_overcharge
                )

                # Monta os valores nas instruções SQL e executa a inserção do registro no banco. Comita os dados.
                inst_cadastro.execute(sql_insert, values)
                conn.commit()

                print(f"Inserindo registro: {values}")

            except Exception as e:
                print(f"Erro ao inserir registro {index}: {e}")

    except ValueError as ve:
        print("Erro: {ve}")
        return
    except:
        print("Erro na cponexão com o DB.")
        return
    else:
        print("Operação finalizada.")

    input("Pressione ENTER.")
    return

# Popula histórico da ponte

def store_bridge_history() -> None:

    print("Popular histórico da ponte\n")

    bridge_history_data = None

    try:
        # Importa dados de leitura de sensores.
        bridge_history_data = pd.read_csv(bridge_history_file)
        print(f"Arquivo '{bridge_history_file}' carregado com sucesso.")

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{bridge_history_file}'")
        return
    except KeyError as e:
        print(f"Erro: coluna não encontrada. Verifique a correspondência com o arquivo de dados: {e}")
        return
    except Exception as e:
        print(f"Ocorreu um erro durante a importação: {e}")
        return

    # Verifica se o data frame está vazio.
    if bridge_history_data.empty:
        print("Erro: O data frame de histórico da ponte está vazio.")
        return
    
    try:
        # Monta instruções SQL de inserção.
        sql_insert = """
        INSERT INTO T_4E_047_EQUIP_HISTORY (
            event_id,
            event_timestamp,
            equip_id,
            event_type,
            event_severity,
            event_description
        ) VALUES (SEQ_T_4E_047_EQUIP_HISTORY.NEXTVAL, :1, :2, :3, :4, :5)
        """

        # Itera sobre os registros do data frame de histórico.
        for index, row in bridge_history_data.iterrows():
            try:
                event_timestamp = row['event_timestamp'] 
                equip_id = int(row['equip_id'])
                event_type = row['event_type']
                event_severity = row['event_severity']
                event_description = row['event_description']

                # Cria a tupla de um registro para inserção.
                values = (
                    event_timestamp,
                    equip_id,
                    event_type,
                    event_severity,
                    event_description
                )

                # Monta os valores nas instruções SQL e executa a inserção do registro no banco. Comita os dados.
                inst_cadastro.execute(sql_insert, values)
                conn.commit()

                print(f"Inserindo registro: {values}")

            except Exception as e:
                print(f"Erro ao inserir registro {index}: {e}")

    except ValueError as ve:
        print("Erro: {ve}")
        return
    except:
        print("Erro na cponexão com o DB.")
        return
    else:
        print("Operação finalizada.")

    input("Pressione ENTER.")
    return

# Popula metadados da ponte

def store_bridge_metadata() -> None:

    print("Popular metadados da ponte")

    bridge_metadata_data = None

    try:
        # Importa metadados da ponte.
        bridge_metadata_data = pd.read_csv(bridge_metadata_file)
        print(f"Arquivo '{bridge_metadata_file}' carregado com sucesso.")

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{bridge_metadata_file}'")
        return
    except KeyError as e:
        print(f"Erro: coluna não encontrada. Verifique a correspondência com o arquivo de dados: {e}")
        return
    except Exception as e:
        print(f"Ocorreu um erro durante a importação: {e}")
        return

    # Verifica se o data frame está vazio.
    if bridge_metadata_data.empty:
        print("Erro: O data frame de metadados da ponte está vazio.")
        return
    
    try:
        # Monta instruções SQL de inserção.
        sql_insert = """
        INSERT INTO T_4E_047_EQUIP_METADATA (
            equip_id,
            equip_name,
            equip_main_material,
            equip_charge_rupture_limit,
            equip_safety_factor
        ) VALUES (SEQ_T_4E_047_EQUIP_METADATA.NEXTVAL, :1, :2, :3, :4)
        """

        # Itera sobre os registros do data frame de histórico.
        for index, row in bridge_metadata_data.iterrows():
            try:
                equip_name = row['equip_name']
                equip_main_material = row['equip_main_material'] 
                equip_charge_rupture_limit = float(row['equip_charge_rupture_limit'])
                equip_safety_factor = float (row['equip_safety_factor'])

                # Cria a tupla de um registro para inserção.
                values = (
                    equip_name,
                    equip_main_material,
                    equip_charge_rupture_limit,
                    equip_safety_factor
                )

                # Monta os valores nas instruções SQL e executa a inserção do registro no banco. Comita os dados.
                inst_cadastro.execute(sql_insert, values)
                conn.commit()

                print(f"Inserindo registro: {values}")

            except Exception as e:
                print(f"Erro ao inserir registro {index}: {e}")

    except ValueError as ve:
        print("Erro: {ve}")
        return
    except:
        print("Erro na cponexão com o DB.")
        return
    else:
        print("Operação finalizada.")

    input("Pressione ENTER.")
    return

# Popula leituras do sensor

def store_sensor_data() -> None:

    print("Popular leituras do sensor")

    sensor_readings_data = None

    try:
        # Importa dados de leitura de sensores.
        sensor_readings_data = pd.read_csv(sensor_readings_file)
        print(f"Arquivo '{sensor_readings_file}' carregado com sucesso.")

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{sensor_readings_file}'")
        return
    except KeyError as e:
        print(f"Erro: coluna não encontrada. Verifique a correspondência com o arquivo de dados: {e}")
        return
    except Exception as e:
        print(f"Ocorreu um erro durante a importação: {e}")
        return

    # Verifica se o data frame está vazio.
    if sensor_readings_data.empty:
        print("Erro: O data frame de histórico do sensor está vazio.")
        return
    
    try:
        # Monta instruções SQL de inserção.
        sql_insert = """
        INSERT INTO T_4E_047_SENSOR_READINGS (
            reading_id,
            reading_timestamp,
            reading_pressure
        ) VALUES (SEQ_T_4E_047_SENSOR_READINGS.NEXTVAL, :1, :2)
        """

        # Itera sobre os registros do data frame de histórico.
        for index, row in sensor_readings_data.iterrows():
            try:
                reading_timestamp = row['reading_timestamp']
                reading_pressure = float(row['reading_pressure']) 

                # Cria a tupla de um registro para inserção.
                values = (
                    reading_timestamp,
                    reading_pressure
                )

                # Monta os valores nas instruções SQL e executa a inserção do registro no banco. Comita os dados.
                inst_cadastro.execute(sql_insert, values)
                conn.commit()

                print(f"Inserindo registro: {values}")

            except Exception as e:
                print(f"Erro ao inserir registro {index}: {e}")

    except ValueError as ve:
        print("Erro: {ve}")
        return
    except:
        print("Erro na cponexão com o DB.")
        return
    else:
        print("Operação finalizada.")

    input("Pressione ENTER.")
    return



# Conecta banco de dados.

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
    print("--- Conexão com base de dados estabelecida. ---")

while conexao:

# Exibe menu
    
    # os.system('cls')

    print("--- Gravar dados históricos ---")
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
            
            try:
                inst_cadastro.close()
                inst_consulta.close()
                conn.close()
                print("Conexão com o banco de dados encerrada com sucesso.")
            except Exception as e:
                print(f"Erro ao fechar a conexão: {e}")
            finally:
                conexao = False
                 

