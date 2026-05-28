"""AETHER-1 Space Monitor
Sistema de monitoramento para missão espacial experimental
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from modules.simulador import gerar_ciclo, ESTADO_INICIAL
from modules.alertas import verificar_alertas, gerar_log_entry

#configuracao da pagina
st.set_page_config(
    page_title="AETHER-1 \u2501 Space Monitor",
    page_icon= "\U00002604",
    layout="wide",
    initial_sidebar_state="expanded",
)
#css
st.markdown("""
<style>
    [data-testid="stMetricValue"] {font-size: 2rem !important;}
    .alert-ok { background: #d4edda; border-left: 4px solid #28a745; padding: 8px 12px; border-radius: 6px; margin: 4px 0; color:#155724; font-size:0.85rem;}
    .alert-alerta { background: #fff3cd; border-left: 4px solid #ffc107; padding: 8px 12px; box-radius: 6px; margin: 4px 0; color: #856404; font-size: 0.85rem;}
    .alert-critico { background: #f8d7da; border-left: 4px solid #dc3545; padding: 8px 12px; box-radius: 6px; margin: px 0; color: #721c24; font-size: 0.85rem;}
    .badge-ok { background: #28a745; color: white; padding:3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600;}
    .badge-alerta { background: #ffc107; color: white; padding:3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600;}
    .badge-critico { background: #dc3545; color: white; padding:3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600;}
    .module-box { border: 1px solid #dee2e6; border-radius: 10px; padding: 14px; margin-bottom: 10px;}
    .stButton>button { widith: 100%; }
</style> 
""", unsafe_allow_html=True)

#inicializar estado
def inicializar_estado():
    if "estado" not in st.session_state:
        st.session_state.estado = ESTADO_INICIAL.copy()
        st.session_state.ciclo = 0
        st.session_state.historico = [ESTADO_INICIAL.copy()]
        st.session_state.alertas = []
        st.session_state.logs = []
        st.session_state.modo_crise = False

inicializar_estado()

#visuais
COR_STATUS = {"ok": "#28a745", "alerta": "#ffc107", "critico": "#dc3545"}
LABEL_STATUS = {"ok": "NORMAL", "alerta": "ALERTA", "critico": "CRÍTICO"}
EMOJI_STATUS = {"ok": "\U0001F7E2", "alerta": "\U0001F7E1", "critico": "\U0001F534"}

def badge(nivel: str) -> str:
    return f'<span class="badge-{nivel}">{EMOJI_STATUS[nivel]}{LABEL_STATUS[nivel]}</span>'

def delta_color(status: str) -> str:
    return "normal" if status == "ok" else "inverse"

#gauge -> medidor/grafico
def gauge(valor: float, minv: float, maxv: float, titulo: str, status: str) -> go.Figure:
    cor = COR_STATUS[status]
    fig = go.Figure(go.Indicator(mode="gauge+number", value="valor", title={"text": titulo, "font": {"size": 13}}, gauge={"axis": {"range": [minv, maxv], "tickfont": {"size": 10}}, "bar": {"color": cor, "thickness": 0.25}, "bgcolor": "#f8f9fa", "steps": [{"range": [minv, maxv], "color": "#e9ecef"}], "threshold": {"line": {"color": cor, "width": 3}, "value": valor}, }, number = {"font": {"size": 22, "color": cor}}, ))
    fig.update_layout(height=160, margin=dict(l=15, r=15, t=30, b=5))
    return fig

#sidebar
with st.sidebar:
    st.markdown("##\U00002604 AETHER-1 Control")
    st.markdown("---")

    status_atual = st.session_state.estado["status_geral"]
    st.markdown(f"**Status:**{badge(status_atual)}", unsafe_allow_html=True)
    st.markdown(f"**Ciclo:**{st.session_state.ciclo}")
    st.markdown(f"**Alertas:**{len(st.session_state.alertas)}")
    st.markdown("---")

    if st.button("\u25B6 Próximo ciclo", type="primary"):
        novo = gerar_ciclo(st.session_state.estado, st.session_state.modo_crise)
        st.session_state.estado = novo
        st.session_state.ciclo += 1
        st.session_state.historioc.append(novo)
        if len(st.session_state.historico) > 50:
            st.session_state.historico.pop(0)
        st.session_state.alertas = verificar_alertas(novo, st.session_state.alertas)
        log = gerar_log_entry(st.session_state.ciclo, novo)
        st.session_state.logs.append(log)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("\U000026A0 Crise"):
            st.session_state.modo_crise = True
            st.session_state.alertas.append({"timestamp": st.session_state.estado["timestamp"], "sensor": "sistema", "nivel": "critico", "mensagem": "\U0001F534 EVENTO CRÍTICO - Impacto de micrometeoro simulado", "resposta": "-> Ação: Todos os sistemas em modo de emergência",})
    with col2:
        if st.button("\U0001F7E2 Normal"):
            st.session_state.modo_crise = False

        if st.session_state.modo_crise:
            st.error("\U0001F6A8 MODO CRISE ATIVADO")

        st.markdown("---")
        if st.button("\U0001F504 Reiniciar Simulação"):
            for k in ["estado", "ciclo", "historico","alertas", "logs","modo_crise"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()

        st.markdown("---")
        st.markdown("### \U00002699 CONFIGURAÇÕES")
        intervalo = st.slider("Ciclos do gráfico", 5, 50, 20)
        mostrar_log = st.checkbox("Mostrar log completo", value = False)

#cabecalho
c1, c2 = st.columns([3, 1])

with c1:
    st.markdown("#\U00002604 AETHER-1 Space Monitor")
    st.caption("Sistema de monitormaneto - Missão espacial experimental")

with c2:
    st.markdown("<br>", unsafe_allow_html = True)
    status_geral = st.session_state.estado["status_geral"]
    st.markdown(f"### {badge(status_geral)}", unsafe_allow_html = True)

st.markdown("---")

#metricas

e = st.session_state.estado
hist = st.session_state.historico

m1, m2, m3, m4 = st.columns(4)
with m1:
    delta_bat = round(e["bateria"] - hist[-2]["bateria"], 1) if len(hist) > 1 else 0
    st.metric("\U0001F50B Bateria" f"{e['bateria']}%", f"{delta_bat:+.1f}%", delta_color = delta_color(e["status_bateria"]))
with m2:
    delta_solar = round(e["solar_kw"] - hist[-2]["solar-kw"], 2) if len(hist) > 1 else 0
    st.metric("\U00002600 Painel Solar", f"{e['solar_kw']} kW", f"{delta_solar:+.2f} kW", delta_color = delta_color(e["status_solar"]))
with m3:
    delta_temp = round(e["temperatura"] - hist[-2]["temperatura"], 1) if len(hist) > 1 else 0
    st.metric("\U0001F321 Temperatura", f"{e['temperatura']}ºC", f"{delta_temp:+.1f}ºC", delta_color = delta_color(e["status_temp"]))
with m4:
    delta_sinal = round(e["sinal"] - hist[-2]["sinal"], 1) if len(hist) > 1 else 0
    st.metric("\U0001F4E1 Sinal", f"{e['sinal']}%", f"{delta_sinal:+.1f}%", delta_color = delta_color(e['status_sinal']))

st.markdown("---")

#gauges e modulos
