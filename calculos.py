G = 9.81      # aceleração da gravidade (m/s²)
RHO = 1000    # densidade da água (kg/m³)

# ==========================================
# VALIDAÇÕES
# ==========================================

def _exigir_positivo(valor, nome):
    if valor <= 0:
        raise ValueError(f"O campo '{nome}' deve ser maior que zero.")


def _rendimento_decimal(rendimento):
    _exigir_positivo(rendimento, "Rendimento")
    if rendimento > 100:
        raise ValueError("O rendimento deve estar entre 0 e 100%.")
    return rendimento / 100

# ==========================================
# CÁLCULOS BÁSICOS
# ==========================================

def calcular_vazao(volume, tempo_min):
    """Q = V / t. Retorna a vazão em m³/s."""
    if tempo_min == 0:
        raise ValueError("O tempo não pode ser zero.")
    return volume / (tempo_min * 60)


def calcular_velocidade(tempo_ini, tempo_fin, pos_ini, pos_fin):
    """v = Δs / Δt. Retorna (espaço em m, tempo em s, velocidade em m/s)."""
    espaco = pos_fin - pos_ini
    tempo = (tempo_fin - tempo_ini) * 60
    if tempo == 0:
        raise ValueError("A variação de tempo não pode ser zero.")
    return espaco, tempo, espaco / tempo


def calcular_perda_carga(f, L, D, v):
    """Darcy-Weisbach: hf = f * (L / D) * v² / (2g). Retorna em m."""
    if D == 0:
        raise ValueError("O diâmetro não pode ser zero.")
    return f * (L / D) * (v ** 2) / (2 * G)


def calcular_reynolds(densidade, v, D, viscosidade):
    """Re = ρ * v * D / μ."""
    if viscosidade == 0:
        raise ValueError("A viscosidade não pode ser zero.")
    return densidade * v * D / viscosidade


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
    _exigir_positivo(vazao_m3h, "Vazão")
    _exigir_positivo(altura, "HMT")
    eta = _rendimento_decimal(rendimento)

    q = vazao_m3h / 3600
    return q, RHO * G * q * altura / eta


def calcular_altura_manometrica(h_sucao, h_recalque,
                                perda_sucao=0.0, perda_recalque=0.0):
    """Retorna (altura geométrica, perdas totais, HMT), tudo em m."""
    _exigir_positivo(h_recalque, "Altura de recalque")

    geometrica = h_sucao + h_recalque
    perdas = perda_sucao + perda_recalque
    return geometrica, perdas, geometrica + perdas


def calcular_vazao_bomba(potencia_kw, altura, rendimento):
    """Q = P * η / (ρ * g * H). Retorna a vazão em m³/s."""
    _exigir_positivo(potencia_kw, "Potência")
    _exigir_positivo(altura, "HMT")
    eta = _rendimento_decimal(rendimento)

    return (potencia_kw * 1000 * eta) / (RHO * G * altura)


def calcular_consumo(potencia_kw, horas_dia, dias, tarifa=0.0):
    """Retorna (horas totais, energia em kWh, custo em R$)."""
    _exigir_positivo(potencia_kw, "Potência")
    _exigir_positivo(horas_dia, "Horas por dia")
    _exigir_positivo(dias, "Número de dias")
    if horas_dia > 24:
        raise ValueError("As horas por dia não podem passar de 24.")

    horas = horas_dia * dias
    energia = potencia_kw * horas
    return horas, energia, energia * tarifa