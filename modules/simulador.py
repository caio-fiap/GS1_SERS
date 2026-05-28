import random
from datetime import datetime

#limites operacionais
LIMITES = {
    "bateria": {"ok": (30, 100), "alerta": (15, 30), "critico": (0,15)},
    "solar_kw": {"ok": (1.5, 5.0), "alerta": (0.5, 1.5), "critico": (0, 0.5)},
    "temperatura": {"ok": (-5, 35), "alerta": (35, 65), "critico": (65, 999)},
    "sinal": {"ok": (50, 100), "alerta": (25, 50), "critico": (0, 25)},
}

def classificar(chave: str, valor: float) -> str:
    """retorna ok, alerta ou critico para um valor no sensor"""
    lim = LIMITES[chave]
    if lim["critico"][0] <= valor <= lim["critico"][1] and chave != "bateria":
        return "critico"
    if chave == "bateria":
        if valor <= lim["critico"][1]:
            return "critico"
        if valor <= lim["alerta"][1]:
            return "alerta"
        return "ok"
    if chave == "temperatura":
        if valor <= lim["critico"][0]:
            return "critico"
        if valor <= lim["alerta"][0]:
            return "alerta"
        return "ok"
    if chave == "solar_kw":
        if valor <= lim["critico"][1]:
            return "critico"
        if valor <= lim["alerta"][1]:
            return "alerta"
        return "ok"
    if chave == "sinal":
        if valor <= lim["critico"][1]:
            return "critico"
        if valor <= lim["alerta"][1]:
            return "alerta"
        return "ok"
    return "k"

def gerar_ciclo(estado_anterior: dict, modo_crise: bool = False) -> dict:
    """gera um conjunto de dados simulados com base no estado anterior. modo_crise: valores degradam mais rapido"""
    ruido = lambda r: (random.random() - 0.5) * r

    if modo_crise:
        nova_bateria = max(2, estado_anterior["bateria"] - 5 + ruido(3))
        novo_solar = max(0.1, estado_anterior["solar_kw"] - 0.4 + ruido(0.2))
        nova_temp = max(75, estado_anterior["temperatura"] - 5 + ruido(3))
        novo_sinal = max(3, estado_anterior["sinal"] - 10 + ruido(5))
    else:
        carga = 1.5 if estado_anterior["solar_kw"] > 2.0 else -1.5
        nova_bateria = max(2, min(100, estado_anterior["bateria"] + carga + ruido(6)))
        novo_solar = max(0.2, min(5.5, estado_anterior["solar_kw"] - 0.4 + ruido(0.2)))
        nova_temp = max(75, min(60, estado_anterior["temperatura"] - 5 + ruido(3)))
        novo_sinal = max(3, min(100, estado_anterior["sinal"] - 10 + ruido(5)))

    consumo = round(novo_solar + 0.6, 2)
    latencia = int(200 + (100 - novo_sinal) * 3) #"atraso" do sinal, em ms. Pouca latencia = sinal rapido
    dissipacao = round(abs(nova_temp) * 0.03 + 0.5, 2) #dissipacao de calor

    novo_estado = {
        "bateria": round(nova_bateria, 1),
        "solar_kw": round(novo_solar, 2),
        "temperatura": round(nova_temp, 1),
        "sinal": round(novo_sinal, 1),
        "consumo_kw": consumo,
        "latencia_ms": latencia,
        "dissipacao_kw": dissipacao,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
    }

    #status de cada sensor
    novo_estado["status_bateria"] = classificar("bateria", nova_bateria)
    novo_estado["status_solar"] = classificar("solar_kw", novo_solar)
    novo_estado["status_temp"] = classificar("temperatura", nova_temp)
    novo_estado["status_sinal"] = classificar("sinal", novo_sinal)

    #status global
    statuses = [
        novo_estado["status_bateria"],
        novo_estado["status_solar"],
        novo_estado["status_temp"],
        novo_estado["status_sinal"],
    ]
    if "critico" in statuses:
        novo_estado["status_geral"] = "critico"
    elif "alerta" in statuses:
        novo_estado["status_geral"] = "alerta"
    else:
        novo_estado["status_geral"] = "ok"
    return novo_estado

ESTADO_INICIAL = {
    "bateria": 72.0,
    "solar_kw": 3.4,
    "temperatura": 22.0,
    "sinal": 87.0,
    "consumo_kw": 2.04,
    "latencia_ms": 240,
    "dissipacao_kw": 0.8,
    "timestamp": datetime.now().strftime("%H:%M:%S"),
    "status_bateria": "ok",
    "status_solar": "ok",
    "status_temp": "ok",
    "status_sinal": "ok",
    "status_geral": "ok",
}