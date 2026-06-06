from datetime import datetime

# cores
VERMELHO = '\x1B[31m'
VERDE = '\x1B[32m'
AMARELO = '\x1B[33m'
RESET = '\x1B[0m'

# mensagens de alerta por sensor e nivel
MENSAGENS = {
    "bateria": {
        "alerta": f"{AMARELO}\u25CF{RESET} Bateria em {{val}}% - consumo não essencial reduzido",
        "critico": f"{VERMELHO}\u25CF{RESET} Bateria CRÍTICA ({{val}}%) - protocolo de emergência ativado",
    },
    "solar_kw": {
        "alerta": f"{AMARELO}\u25CF{RESET} Geração solar baixa ({{val}}kW) - verificar orientação dos painéis",
        "critico": f"{VERMELHO}\u25CF{RESET} Falha nos painéis solares ({{val}}kW) - trocando para reserva",
    },
    "temperatura": {
        "alerta": f"{AMARELO}\u25CF{RESET} Temperatura elevada ({{val}}ºC) - sistema de resfriamento aumentado",
        "critico": f"{VERMELHO}\u25CF{RESET} Falha nos painéis solares ({{val}}kW) - resfriamento de emergência ativado",
    },
    "sinal": {
        "alerta": f"{AMARELO}\u25CF{RESET} Sinal fraco ({{val}}%) - ajustando antena direcional",
        "critico": f"{VERMELHO}\u25CF{RESET} Perda de sinal ({{val}}%) - tentando reconexão automática",
    },
}

#respostas por sensor e nivel
RESPOSTAS = {
    "bateria": {
        "alerta":  "-> Ação: Módulos não essenciais desligados. Carga solar priorizada.",
        "critico": "-> Ação: Modo de sobrevivência ativado. Apenas sistemas críticos ativos",
    },
    "solar_kw": {
        "alerta":  "-> Ação: Painéis reorientados para maximizar captação.",
        "critico": "-> Ação: Bateria de reserva ativada. Diagnóstico de painel iniciado",
    },
    "temperatura": {
        "alerta":  "-> Ação: Sistema de resfriamento aumentado em 50%.",
        "critico": "-> Ação: Dissipador auxiliar acionado. Carga de processamento reduzida",
    },
    "sinal": {
        "alerta":  "-> Ação: Ganho de antena aumentado. Protocolo de compressão ativo.",
        "critico": "-> Ação: Antena secundária ativada. Beacon de emergência transmitido.",
    },
}

def _ts() -> str:
    return datetime.now().strftime("%H:%M:%S")

def verificar_alertas(estado: dict, alertas_existentes: list) -> list:
    """compara o estado atual com os limites; retorna lista de alertas"""

    mapa = {
        "bateria": ("status_bateria", estado["bateria"], "bateria"),
        "solar_kw": ("status_solar", estado["solar_kw"], "solar_kw"),
        "temperatura": ("status_temp", estado["temperatura"], "temperatura"),
        "sinal": ("status_sinal", estado["sinal"], "sinal"),
    }

    novos = list(alertas_existentes)

    for chave, (campo_status, valor, chave_msg) in mapa.items():
        nivel = estado[campo_status]
        if nivel == "ok":
            continue

        msg_alerta = MENSAGENS[chave_msg][nivel].replace("{{val}}", str(round(valor, 1)))
        msg_resposta = RESPOSTAS[chave_msg][nivel]

        ultimo_igual = any(
            a["sensor"] == chave and a["nivel"] == nivel
            for a in alertas_existentes[-4:]
        )
        if ultimo_igual:
            continue

        novos.append({
            "timestamp": _ts(),
            "sensor": chave,
            "nivel": nivel,
            "mensagem": msg_alerta,
            "resposta": msg_resposta,
        })

    return novos[-50:]

def gerar_log_entry(ciclo: int, estado: dict) -> dict:
    """cria um entrada de log para o cilco atual"""
    status = estado["status_geral"]
    emoji = {"ok": "\u2705", "alerta": f"{AMARELO}\u26A0{RESET}", "critico": "\U0001F6A8"}.get(status,"\u25CF")
    nivel = {"ok": "NORMAL", "alerta": "ALERTA", "critico": "CRÍTICO"}.get(status,"\u2500")

    return {
        "ciclo": ciclo,
        "timestamp": _ts(),
        "nivel": nivel,
        "emoji": emoji,
        "bateria": estado["bateria"],
        "solar": estado["solar_kw"],
        "temp": estado["temperatura"],
        "sinal": estado["sinal"],
        "status": status,
    }

