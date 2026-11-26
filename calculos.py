"""Cálculos de Mecânica dos Fluidos.

Este arquivo não conhece a interface: cada função recebe números,
devolve números e lança ValueError quando um valor não é permitido.
"""

G = 9.81          # aceleração da gravidade (m/s²)
RHO_AGUA = 1000   # densidade da água (kg/m³)
WATTS_POR_CV = 735.5


# ==========================================
# VALIDAÇÕES
# ==========================================

def _exigir_positivo(**valores):
    for nome, valor in valores.items():
        if valor <= 0:
            raise ValueError(f"{nome.replace('_', ' ')}: use um valor maior que zero.")


def _exigir_nao_negativo(**valores):
    for nome, valor in valores.items():
        if valor < 0:
            raise ValueError(f"{nome.replace('_', ' ')}: não pode ser negativo.")


def _rendimento_decimal(rendimento):
    """Converte o rendimento de % para decimal (ex.: 75 -> 0.75)."""
    if not 0 < rendimento <= 100:
        raise ValueError("Rendimento: use um valor entre 0 e 100%.")
    return rendimento / 100


# ==========================================
# CÁLCULOS BÁSICOS
# ==========================================

def calcular_vazao(volume, tempo_min):
    """Q = V / t. Retorna a vazão em m³/s."""
    _exigir_positivo(Volume=volume, Tempo=tempo_min)
    return volume / (tempo_min * 60)


def calcular_velocidade(tempo_ini, tempo_fin, pos_ini, pos_fin):
    """v = Δs / Δt. Retorna (espaço em m, tempo em s, velocidade em m/s)."""
    espaco = pos_fin - pos_ini
    tempo = (tempo_fin - tempo_ini) * 60
    _exigir_positivo(Variação_de_tempo=tempo)
    return espaco, tempo, espaco / tempo


def calcular_perda_carga(atrito, comprimento, diametro, velocidade):
    """Darcy-Weisbach: hf = f * (L / D) * v² / (2g). Retorna em m."""
    _exigir_positivo(Fator_de_atrito=atrito, Comprimento=comprimento,
                     Diâmetro=diametro)
    _exigir_nao_negativo(Velocidade=velocidade)
    return atrito * (comprimento / diametro) * velocidade ** 2 / (2 * G)


def calcular_reynolds(densidade, velocidade, diametro, viscosidade):
    """Re = ρ * v * D / μ."""
    _exigir_positivo(Densidade=densidade, Diâmetro=diametro,
                     Viscosidade=viscosidade)
    _exigir_nao_negativo(Velocidade=velocidade)
    return densidade * velocidade * diametro / viscosidade


def classificar_regime(reynolds):
    if reynolds < 2300:
        return "Laminar"
    if reynolds < 4000:
        return "Transição"
    return "Turbulento"


# ==========================================
# BOMBAS
# ==========================================

def calcular_potencia_bomba(vazao_m3h, altura, rendimento):
    """P = ρ * g * Q * H / η. Retorna (vazão em m³/s, potência em W)."""
    _exigir_positivo(Vazão=vazao_m3h, HMT=altura)
    eta = _rendimento_decimal(rendimento)
    vazao = vazao_m3h / 3600
    return vazao, RHO_AGUA * G * vazao * altura / eta


def calcular_altura_manometrica(altura_sucao, altura_recalque,
                                perda_sucao=0.0, perda_recalque=0.0):
    """Retorna (altura geométrica, perdas totais, HMT), tudo em m."""
    _exigir_positivo(Altura_de_recalque=altura_recalque)
    _exigir_nao_negativo(Perda_na_sucção=perda_sucao,
                         Perda_no_recalque=perda_recalque)
    geometrica = altura_sucao + altura_recalque
    perdas = perda_sucao + perda_recalque
    return geometrica, perdas, geometrica + perdas


def calcular_vazao_bomba(potencia_kw, altura, rendimento):
    """Q = P * η / (ρ * g * H). Retorna a vazão em m³/s."""
    _exigir_positivo(Potência=potencia_kw, HMT=altura)
    eta = _rendimento_decimal(rendimento)
    return potencia_kw * 1000 * eta / (RHO_AGUA * G * altura)


def calcular_consumo(potencia_kw, horas_dia, dias, tarifa=0.0):
    """Retorna (horas totais, energia em kWh, custo em R$)."""
    _exigir_positivo(Potência=potencia_kw, Horas_por_dia=horas_dia,
                     Número_de_dias=dias)
    _exigir_nao_negativo(Tarifa=tarifa)
    if horas_dia > 24:
        raise ValueError("Horas por dia: não podem passar de 24.")
    horas = horas_dia * dias
    energia = potencia_kw * horas
    return horas, energia, energia * tarifa