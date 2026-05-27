from datetime import datetime

# cores
VERMELHO = '\x1B[31m'
AMARELO = '\x1B[33m'
RESET = '\x1B[0m'

# mensagens de alerta por sensor e nivel
MENSAGENS = {
    "bateria": {
        "alerta:" f"{AMARELO}\u25CF{RESET} Bateria em {{val}}% - consumo não essencial reduzido",
        "critico:" f"{VERMELHO}\u25CF{RESET} Bateria CRÍTICA ({{val}}%) - protocolo de emergência ativado",
    },
    "solar_kw": {
        "alerta:" f"{AMARELO}\u25CF{RESET} Geração solar baixa ({{val}}kW) - verificar orientação dos painéis",
        "critico:" f"{VERMELHO}\u25CF{RESET} Falha nos painéis solares ({{val}}kW) - trocando para reserva",
    },
    "temperatura": {
        "alerta:" f"{AMARELO}\u25CF{RESET} Temperatura elevada ({{val}}ºC) - sistema de resfriamento aumentado",
        "critico:" f"{VERMELHO}\u25CF{RESET} Falha nos painéis solares ({{val}}kW) - resfriamento de emergência ativado",
    },
    "sinal": {
        "alerta:" f"{AMARELO}\u25CF{RESET} Sinal fraco ({{val}}%) - ajustando antena direcional",
        "critico:" f"{VERMELHO}\u25CF{RESET} Perda de sinal ({{val}}%) - tentando reconexão automática",
    },
}

#respostas por sensor e nivel