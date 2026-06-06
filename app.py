"""AETHER-1 Space Monitor
Sistema de monitoramento para missão espacial experimental
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import Literal
from modules.simulador import gerar_ciclo, ESTADO_INICIAL
from modules.alertas import verificar_alertas, gerar_log_entry

#configuracao da pagina
st.set_page_config(
    page_title="AETHER-1 \u2501 Space Monitor",
    page_icon= "️☄️",
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

def delta_color(status: str) -> Literal["normal", "inverse"]:
    return "normal" if status == "ok" else "inverse"

#gauge -> medidor/grafico
def gauge(valor: float, minv: float, maxv: float, titulo: str, status: str) -> go.Figure:
    cor = COR_STATUS[status]
    fig = go.Figure(go.Indicator(mode="gauge+number", value=valor, title={"text": titulo, "font": {"size": 13}}, gauge={"axis": {"range": [minv, maxv], "tickfont": {"size": 10}}, "bar": {"color": cor, "thickness": 0.25}, "bgcolor": "#f8f9fa", "steps": [{"range": [minv, maxv], "color": "#e9ecef"}], "threshold": {"line": {"color": cor, "width": 3}, "value": valor}, }, number = {"font": {"size": 22, "color": cor}}, ))
    fig.update_layout(height=160, margin=dict(l=15, r=15, t=30, b=5))
    return fig

#sidebar
with st.sidebar:
    st.markdown("## ☄️ AETHER-1 Control")
    st.markdown("---")

    status_atual = st.session_state.estado["status_geral"]
    st.markdown(f"**Status:** {badge(status_atual)}", unsafe_allow_html=True)
    st.markdown(f"**Ciclo:** {st.session_state.ciclo}")
    st.markdown(f"**Alertas:** {len(st.session_state.alertas)}")
    st.markdown("---")

    if st.button("\u25B6 Próximo ciclo", type="primary"):
        novo = gerar_ciclo(st.session_state.estado, st.session_state.modo_crise)
        st.session_state.estado = novo
        st.session_state.ciclo += 1
        st.session_state.historico.append(novo)
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
    st.markdown("# ☄️ AETHER-1 Space Monitor")
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
    st.metric("\U0001F50B Bateria", f"{e['bateria']}%", f"{delta_bat:+.1f}%", delta_color = delta_color(e["status_bateria"]))
with m2:
    delta_solar = round(e["solar_kw"] - hist[-2]["solar_kw"], 2) if len(hist) > 1 else 0
    st.metric("\U00002600 Painel Solar", f"{e['solar_kw']} kW", f"{delta_solar:+.2f} kW", delta_color = delta_color(e["status_solar"]))
with m3:
    delta_temp = round(e["temperatura"] - hist[-2]["temperatura"], 1) if len(hist) > 1 else 0
    st.metric("\U0001F321 Temperatura", f"{e['temperatura']}ºC", f"{delta_temp:+.1f}ºC", delta_color = delta_color(e["status_temp"]))
with m4:
    delta_sinal = round(e["sinal"] - hist[-2]["sinal"], 1) if len(hist) > 1 else 0
    st.metric("\U0001F4E1 Sinal", f"{e['sinal']}%", f"{delta_sinal:+.1f}%", delta_color = delta_color(e['status_sinal']))

st.markdown("---")

#gauges e modulos
col_gauges, col_modulos = st.columns([2, 1])

with col_gauges:
    st.markdown("#### \U0001F4CA Leituras em tempo real")
    g1, g2, g3, g4 = st.columns(4)
    with g1:
        st.plotly_chart(gauge(e["bateria"], 0, 100, "Bateria (%)", e["status_bateria"]), use_container_width = True, key = "g_bat")
    with g2:
        st.plotly_chart(gauge(e["solar_kw"], 0, 5.5, "Solar (kW)", e["status_solar"]), use_container_width=True, key="g_solar")
    with g3:
        st.plotly_chart(gauge(e["temperatura"], -20, 70, "Temperatura (ºC)", e["status_temp"]), use_container_width=True, key="g_temp")
    with g4:
        st.plotly_chart(gauge(e["sinal"], 0, 100, "Sinal (%)", e["status_sinal"]), use_container_width=True, key="g_sinal")

with col_modulos:
    st.markdown("#### \U0001F9E9 Status dos módulos")

    modulos = [
        ("A - Energia", e["status_bateria"], f"Geração: {e['solar_kw']}kW\nCosnumo: {e['consumo_kw']} kW"),
        ("B - Térmico", e["status_temp"], f"Temp: {e['temperatura']}ºC\nDissipação: {e['dissipacao_kw']} kW"),
        ("C - Comunicação", e["status_sinal"], f"Sinal: {e['sinal']}%\nLatência: {e['latencia_ms']} ms"),
    ]
    for nome, status, detalhe in modulos:
        cor = COR_STATUS[status]
        emoji = EMOJI_STATUS[status]
        st.markdown(f"""
            <div class="module-box">
                <b>{emoji} Módulo {nome}</b><br>
                <small style="color: {cor}; font-weight:600">
                    {LABEL_STATUS[status]}</small><br>
                <small style="color: #666">
                    {detalhe.replace(chr(10), '<br>')}
                </small>
            </div>
        """, unsafe_allow_html = True)

st.markdown("---")

#grafico historico
st.markdown("#### \U0001F4C8 Histórico da Missão")

if len(hist) > 1:
    df = pd.DataFrame(hist[-intervalo:])
    df["ciclo_idx"] = range(len(df))

    ch1, ch2 = st.columns(2)

    with ch1:
        fig_energia = go.Figure()
        fig_energia.add_trace(go.Scatter(x = df["ciclo_idx"], y = df["bateria"], name = "Bateria (%)", line = dict(color = "#007bff", width = 2), fill = "tozeroy", fillcolor = "rgba(0, 123, 255, 0.1)"))
        fig_energia.add_trace(go.Scatter(x = df["ciclo_idx"], y = df["solar_kw"] * 20, name = "Solar x20(%)", line = dict(color = "#28a745", width = 2, dash = "dot")))
        fig_energia.add_hline(y = 30, line_dash = "dash", line_color = "#ffc107", annotation_text="\U0001F7E1 Alerta bateria")
        fig_energia.add_hline(y = 15, line_dash = "dash", line_color = "#dc3545", annotation_text="\U0001F534 Crítico")
        fig_energia.update_layout(title = "Energia - Bateria & Solar", height = 260, margin = dict(l = 0, r = 0, t = 35, b = 0), legend = dict(orientation = "h", y = -0.25), xaxis_title = "Ciclo", yaxis_title = "Valor")
        st.plotly_chart(fig_energia, use_container_width = True)

    with ch2:
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(x = df["ciclo_idx"], y = df["temperatura"], name = "Temperatura (ºC)", line = dict(color = "#fd7e14", width = 2)))
        fig_temp.add_trace(go.Scatter(x = df["ciclo_idx"], y = df["sinal"], name = "Sinal (%)", line = dict(color = "#6f42c1", width = 2)))
        fig_temp.add_hline(y=45, line_dash="dash", line_color="#ffc107", annotation_text="\U0001F7E1 Alerta temp")
        fig_temp.add_hline(y=55, line_dash="dash", line_color="#dc3545", annotation_text="\U0001F534 Crítico")
        fig_temp.update_layout(title = "Temperatura & Sinal de Comunicação", height = 260, margin = dict(l = 0, r = 0, t = 35, b = 0), legend = dict(orientation = "h", y = -0.25), xaxis_title = "Ciclo", yaxis_title = "Valor")
        st.plotly_chart(fig_temp, use_container_width = True)

else:
    st.info("Clique em **Próximo Ciclo** para gerar dados históricos.")

st.markdown("---")

#alerta
col_alertas, col_log = st.columns([1, 1])

with col_alertas:
    st.markdown("#### \U0001F514 Alertas Ativos")
    alertas_exibir = list(reversed(st.session_state.alertas[-10:]))

    if alertas_exibir:
        for alerta in alertas_exibir:
            nivel = alerta["nivel"]
            st.markdown(f"""
                <div class="alert-{nivel}">
                    <b>[{alerta['timestamp']}]</b> {alerta['mensagem']} <br>
                    <i>{alerta['resposta']}</i>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-ok">\U0001F7E2 Nenhum alerta - todos os sistemas normais</div>', unsafe_allow_html=True)

with col_log:
    st.markdown("#### \U0001F4CB Log Operacional")
    if st.session_state.logs:
        logs_df = pd.DataFrame(st.session_state.logs)
        logs_exibir = logs_df[["ciclo", "timestamp", "nivel", "bateria", "solar", "temp", "sinal"]].copy()
        logs_exibir.columns = ["Ciclo", "Hora", "Status", "Bat %", "Solar kW", "Temp ºC", "Sinal %"]
        logs_exibir = logs_exibir.iloc[::-1].head(15 if mostrar_log else 8)

        def colorir_status(val):
            cores = {"NORMAL": "background-color: #d4edda", "ALERTA": "background-color: #fff3cd", "CRÍTICO": "background-color: #5c1e16"}
            return cores.get(val, "")

        st.dataframe(
            logs_exibir.style.map(colorir_status, subset=["Status"]),
            use_container_width = True,
            hide_index = True,
            height = 280,
        )
    else:
        st.info("Log vazio - execute ciclos para registrar dados.")

#footer
st.markdown("---")
st.caption("☄️ AETHER-1 Space Monitor | Missão Espacial Experimental | Soluções em Energias Renováveis e Sustentabilidade")
