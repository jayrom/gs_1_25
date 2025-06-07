# app_monitoramento.py
import streamlit as st
import pandas as pd
import time
import joblib

st.set_page_config(page_title="Monitoramento de Ponte", layout="wide")
st.title("Meu Aplicativo de Alerta")
st.write("Este é o meu app rodando a partir de um arquivo .py criado magicamente!")
 

# --- Configurações Iniciais e Carregamento de Dados ---

# Título e configuração da página
st.title("🚨 Dashboard de Monitoramento de Pressão na Ponte")

# Dicionário de dados da ponte (copiado do seu script)
PONTES_DATA = {
    1: {
        'equip_name': 'Ponte Principal',
        'equip_main_material': 'Concreto Armado',
        'equip_charge_rupture_limit': 350.0,
        'equip_safety_factor': 1.5
    },
    2: {
        'equip_name': 'Ponte Secundária',
        'equip_main_material': 'Aço',
        'equip_charge_rupture_limit': 400.0,
        'equip_safety_factor': 1.8
    }
}
PONTE_ID_SIMULACAO = 1
SIMULATION_INTERVAL_SECONDS = 2
SENSOR_READINGS_FILE = "4E047_sensor_readings.csv"

# Função para carregar o modelo e os dados (com cache para performance)
@st.cache_resource
def carregar_modelo():
    try:
        modelo = joblib.load('modelo_cheia.joblib')
        return modelo
    except FileNotFoundError:
        st.error("Arquivo 'modelo_cheia.joblib' não encontrado. Execute o script 'treinar_e_salvar_modelo.py' primeiro.")
        return None

@st.cache_data
def carregar_dados_simulacao():
    try:
        sim_data_df = pd.read_csv(
            SENSOR_READINGS_FILE,
            parse_dates=['reading_timestamp'],
            date_format='%d-%b-%y'
        ).sort_values(by='reading_timestamp')
        return sim_data_df
    except FileNotFoundError:
        st.error(f"Arquivo de simulação '{SENSOR_READINGS_FILE}' não encontrado.")
        return None

# Carrega os recursos
ml_model = carregar_modelo()
sim_data_df = carregar_dados_simulacao()

# --- Lógica de Alerta (copiada e adaptada do seu script) ---
# Esta função é a mesma que você criou, não precisa de alterações.
def gerar_alerta(id_ponte: int, pressao_agua_pilastra_kpa: float, ml_model_trained) -> dict:
    alerta_gerado = 0
    severidade_risco_engenharia = 0
    severidade_risco_ml = 0
    mensagem_alerta = "Condições Normais"
    probabilidade_ml = 0.0

    if ml_model_trained is None:
        return {"alerta_gerado": 0, "severidade_risco_ml": 0, "mensagem_alerta": "Modelo de ML não carregado", "probabilidade_ml": 0}

    ponte_info = PONTES_DATA.get(id_ponte)
    if ponte_info:
        limite_ruptura_kpa = ponte_info['equip_charge_rupture_limit']
        fator_seguranca = ponte_info['equip_safety_factor']
        limiar_critico_engenharia = limite_ruptura_kpa * fator_seguranca

        if pressao_agua_pilastra_kpa > limiar_critico_engenharia:
            alerta_gerado = 1
            severidade_risco_engenharia = 2
            mensagem_alerta = f"ALERTA CRÍTICO: Pressão da Água({pressao_agua_pilastra_kpa:.2f} kPa) EXCEDEU O LIMITE DE SEGURANÇA DA PONTE ({limiar_critico_engenharia:.2f} kPa)!"
        elif pressao_agua_pilastra_kpa >= (limiar_critico_engenharia * 0.8):
            alerta_gerado = 1
            severidade_risco_engenharia = 1
            if mensagem_alerta == "Condições Normais":
                mensagem_alerta = f"ALERTA MÉDIO: Pressão da Água({pressao_agua_pilastra_kpa:.2f} kPa) está próximo do limite de segurança da ponte ({limiar_critico_engenharia:.2f} kPa)."

    input_for_ml = pd.DataFrame({'reading_calculated_water_pressure': [pressao_agua_pilastra_kpa]})
    previsao_ml = ml_model_trained.predict(input_for_ml)[0]
    probabilidade_ml = ml_model_trained.predict_proba(input_for_ml)[0][1]

    if previsao_ml == 1:
        alerta_gerado = 1
        if probabilidade_ml >= 0.7:
            severidade_risco_ml = 2
            if severidade_risco_engenharia < 2:
                mensagem_alerta = f"ALERTA CRÍTICO (ML): Alta probabilidade de cheia ({probabilidade_ml:.2f}) detectada."
        else:
            severidade_risco_ml = 1
            if severidade_risco_engenharia == 0:
                mensagem_alerta = f"ALERTA MÉDIO (ML): Risco de cheia detectado ({probabilidade_ml:.2f})."

    severidade_final = max(severidade_risco_engenharia, severidade_risco_ml)

    return {"alerta_gerado": alerta_gerado, "severidade_final": severidade_final, "mensagem_alerta": mensagem_alerta, "probabilidade_ml": probabilidade_ml}


# --- Interface do Usuário e Lógica de Simulação ---

if ml_model and sim_data_df is not None:
    st.sidebar.header("Controles da Simulação")
    # Botão para iniciar a simulação
    if st.sidebar.button('Iniciar Monitoramento'):

        # Placeholders para os elementos dinâmicos do dashboard
        status_placeholder = st.empty()
        cols = st.columns(3)
        kpi1_placeholder = cols[0]
        kpi2_placeholder = cols[1]
        kpi3_placeholder = cols[2]
        chart_placeholder = st.empty()

        # Dataframe para o gráfico em tempo real
        history_df = pd.DataFrame(columns=['Leitura', 'Pressão (kPa)'])

        for index, row in sim_data_df.iterrows():
            simulated_pressure_kpa = float(row['reading_pressure'])

            # Gera o alerta com base na leitura atual
            alert_result = gerar_alerta(PONTE_ID_SIMULACAO, simulated_pressure_kpa, ml_model)

            # ===== AQUI ESTÁ A LÓGICA DO ALERTA POP-UP =====
            if alert_result['severidade_final'] == 2: # Alerta Crítico
                st.toast(f"URGENTE: {alert_result['mensagem_alerta']}", icon='🚨')
            elif alert_result['severidade_final'] == 1: # Alerta Médio
                st.toast(alert_result['mensagem_alerta'], icon='⚠️')
            # =======================================================

            # Atualiza o painel de status fixo
            with status_placeholder.container():
                if alert_result['severidade_final'] == 2:
                    st.error(f"**Status Atual:** {alert_result['mensagem_alerta']}", icon="🚨")
                elif alert_result['severidade_final'] == 1:
                    st.warning(f"**Status Atual:** {alert_result['mensagem_alerta']}", icon="⚠️")
                else:
                    st.success(f"**Status Atual:** {alert_result['mensagem_alerta']}", icon="✅")

            # Atualiza os KPIs
            limite_seguranca = PONTES_DATA[PONTE_ID_SIMULACAO]['equip_charge_rupture_limit'] * PONTES_DATA[PONTE_ID_SIMULACAO]['equip_safety_factor']
            kpi1_placeholder.metric(label="Pressão Atual", value=f"{simulated_pressure_kpa:.2f} kPa")
            kpi2_placeholder.metric(label="Limite de Segurança", value=f"{limite_seguranca:.2f} kPa")
            kpi3_placeholder.metric(label="Probabilidade de Cheia (ML)", value=f"{alert_result['probabilidade_ml']:.2%}")

            # Atualiza o gráfico
            new_row = pd.DataFrame({'Leitura': [row['reading_timestamp']], 'Pressão (kPa)': [simulated_pressure_kpa]})
            history_df = pd.concat([history_df, new_row], ignore_index=True)
            history_df['Leitura'] = pd.to_datetime(history_df['Leitura'])
            with chart_placeholder.container():
                st.line_chart(history_df.rename(columns={'Leitura':'index'}).set_index('index'))

            # Aguarda para a próxima leitura
            time.sleep(SIMULATION_INTERVAL_SECONDS)

        st.info("Simulação finalizada.")
else:
    st.warning("Não foi possível carregar o modelo ou os dados de simulação. Verifique os arquivos.")
