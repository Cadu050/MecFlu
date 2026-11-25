"""Cálculos de Mecânica dos Fluidos.

Este arquivo concentra tudo o que é relativo a conta:
fórmulas, constantes, operações disponíveis e listas de variáveis.
O main.py só cuida da interface e lê os dados daqui.
"""

# ==================================================
# CONSTANTES
# ==================================================

GRAVIDADE = 9.81            # m/s²
REYNOLDS_LAMINAR = 2300     # abaixo disso: escoamento laminar
REYNOLDS_TURBULENTO = 4000  # acima disso: escoamento turbulento


# ==================================================
# VAZÃO
# ==================================================

def calcular_vazao(volume, tempo_min):
    """Vazão volumétrica em m³/s.  Q = V / t"""

    if tempo_min == 0:
        raise ValueError("O tempo não pode ser zero.")

    return volume / (tempo_min * 60)


# ==================================================
# VELOCIDADE MÉDIA
# ==================================================

def calcular_velocidade(tempo_ini, tempo_fin, pos_ini, pos_fin):
    """Velocidade média.  v = Δs / Δt

    Tempos em minutos e posições em metros.
    Retorna (Δs em m, Δt em s, v em m/s).
    """

    espaco = pos_fin - pos_ini
    tempo = (tempo_fin - tempo_ini) * 60

    if tempo == 0:
        raise ValueError("A variação de tempo não pode ser zero.")

    return espaco, tempo, espaco / tempo


# ==================================================
# PERDA DE CARGA DISTRIBUÍDA
# ==================================================

def calcular_perda_carga(f, L, D, v, g=GRAVIDADE):
    """Perda de carga pela equação de Darcy-Weisbach, em metros.

    hf = f * (L / D) * (v² / 2g)
    """

    if D == 0:
        raise ValueError("O diâmetro não pode ser zero.")

    return f * (L / D) * (v ** 2) / (2 * g)


# ==================================================
# NÚMERO DE REYNOLDS
# ==================================================

def calcular_reynolds(densidade, velocidade, diametro, viscosidade):
    """Número de Reynolds (adimensional).  Re = ρ * v * D / μ"""

    if viscosidade == 0:
        raise ValueError("A viscosidade não pode ser zero.")

    return (densidade * velocidade * diametro) / viscosidade


# ==================================================
# CLASSIFICAÇÃO DO REGIME DE ESCOAMENTO
# ==================================================

def classificar_regime(reynolds):
    """Classifica o regime de escoamento a partir de Reynolds."""

    if reynolds < REYNOLDS_LAMINAR:
        return "Laminar"

    if reynolds < REYNOLDS_TURBULENTO:
        return "Transição"

    return "Turbulento"


# ==================================================
# TEXTOS DE RESULTADO
# (recebem um dicionário {campo: valor} e devolvem a mensagem)
# ==================================================

def _resultado_vazao(v):

    q = calcular_vazao(v["volume"], v["tempo"])

    return (
        "VAZÃO DO FLUIDO\n\n"
        f"Volume: {v['volume']} m³\n"
        f"Tempo: {v['tempo']} min\n\n"
        f"Vazão: {q:.6f} m³/s"
    )


def _resultado_velocidade(v):

    espaco, tempo, velocidade = calcular_velocidade(
        v["tempo_ini"], v["tempo_fin"], v["pos_ini"], v["pos_fin"]
    )

    return (
        "VELOCIDADE MÉDIA\n\n"
        f"Variação de espaço: {espaco} m\n"
        f"Variação de tempo: {tempo} s\n\n"
        f"Velocidade média: {velocidade:.4f} m/s"
    )


def _resultado_perda_carga(v):

    perda = calcular_perda_carga(
        v["atrito"], v["comprimento"], v["diametro"], v["velocidade"]
    )

    return (
        "PERDA DE CARGA DISTRIBUÍDA\n\n"
        f"Comprimento: {v['comprimento']} m\n"
        f"Diâmetro: {v['diametro']} m\n\n"
        f"Perda de carga: {perda:.4f} m"
    )


def _resultado_reynolds(v):

    re = calcular_reynolds(
        v["densidade"], v["velocidade"], v["diametro"], v["viscosidade"]
    )

    return (
        "NÚMERO DE REYNOLDS\n\n"
        f"Reynolds: {re:.2f}\n\n"
        f"Regime: {classificar_regime(re)}"
    )


# ==================================================
# OPERAÇÕES DA SEÇÃO BÁSICOS
# Para cada operação: campos (chave, rótulo) e função de resultado
# ==================================================

OPERACOES = {
    "Vazão": {
        "campos": [
            ("volume", "Volume do fluido (m³):"),
            ("tempo", "Tempo de vazão (min):"),
        ],
        "resultado": _resultado_vazao,
    },
    "Velocidade média": {
        "campos": [
            ("tempo_ini", "Tempo inicial (min):"),
            ("tempo_fin", "Tempo final (min):"),
            ("pos_ini", "Posição inicial (m):"),
            ("pos_fin", "Posição final (m):"),
        ],
        "resultado": _resultado_velocidade,
    },
    "Perda de carga distribuída": {
        "campos": [
            ("atrito", "Fator de atrito:"),
            ("comprimento", "Comprimento da tubulação (m):"),
            ("diametro", "Diâmetro interno (m):"),
            ("velocidade", "Velocidade média (m/s):"),
        ],
        "resultado": _resultado_perda_carga,
    },
    "Número de Reynolds": {
        "campos": [
            ("densidade", "Densidade do fluido (kg/m³):"),
            ("velocidade", "Velocidade média (m/s):"),
            ("diametro", "Diâmetro do tubo (m):"),
            ("viscosidade", "Viscosidade dinâmica (Pa.s):"),
        ],
        "resultado": _resultado_reynolds,
    },
}


def executar_operacao(nome, valores):
    """Executa a operação escolhida e devolve o texto do resultado.

    `valores` é um dicionário {chave do campo: número}.
    """

    return OPERACOES[nome]["resultado"](valores)


# ==================================================
# TÓPICOS DA SEÇÃO BOMBAS (apenas a lista, sem cálculos ainda)
# ==================================================

TOPICOS_BOMBAS = [
    "Altura manométrica",
    "Potência da bomba",
    "Rendimento",
    "NPSH",
]


# ==================================================
# VARIÁVEIS DA SEÇÃO SIMULAÇÃO
# Agrupadas por categoria: (chave, rótulo com unidade)
# ==================================================

VARIAVEIS_SIMULACAO = {
    "Escoamento": [
        ("vazao", "Vazão (m³/s)"),
        ("volume", "Volume (m³)"),
        ("tempo", "Tempo (min)"),
        ("velocidade", "Velocidade média (m/s)"),
        ("espaco", "Variação de espaço (m)"),
        ("reynolds", "Número de Reynolds"),
    ],
    "Fluido": [
        ("densidade", "Densidade (kg/m³)"),
        ("viscosidade_dinamica", "Viscosidade dinâmica (Pa.s)"),
        ("viscosidade_cinematica", "Viscosidade cinemática (m²/s)"),
        ("peso_especifico", "Peso específico (N/m³)"),
        ("temperatura", "Temperatura (°C)"),
    ],
    "Tubulação": [
        ("diametro", "Diâmetro interno (m)"),
        ("comprimento", "Comprimento (m)"),
        ("area", "Área da seção (m²)"),
        ("rugosidade", "Rugosidade (m)"),
        ("atrito", "Fator de atrito"),
    ],
    "Energia e pressão": [
        ("perda_carga", "Perda de carga (m)"),
        ("pressao", "Pressão (Pa)"),
        ("altura", "Altura / cota (m)"),
        ("gravidade", "Aceleração da gravidade (m/s²)"),
    ],
}