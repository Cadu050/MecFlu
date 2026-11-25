
# ==================================================
# CALCULOS DE MECANICA DOS FLUIDOS
# ==================================================


# ==================================================
# VAZAO
# ==================================================

def calcular_vazao(volume, tempo_min):

    # Q = V / t

    if tempo_min == 0:
        raise ValueError("O tempo não pode ser zero.")

    tempo_segundos = tempo_min * 60

    return volume / tempo_segundos


# ==================================================
# VELOCIDADE MEDIA
# ==================================================

def calcular_velocidade(tempo_ini, tempo_fin, pos_ini, pos_fin):

    # v = Δs / Δt

    espaco = pos_fin - pos_ini

    tempo = (tempo_fin - tempo_ini) * 60

    if tempo == 0:
        raise ValueError("A variacao de tempo nao pode ser zero.")

    velocidade = espaco / tempo

    return espaco, tempo, velocidade


# ==================================================
# PERDA DE CARGA DISTRIBUIDA
# ==================================================

def calcular_perda_carga(f, L, D, v, g=9.81):

    # Equacao de Darcy-Weisbach
    # hf = f * (L / D) * (v² / 2g)

    if D == 0:
        raise ValueError("O diametro nao pode ser zero.")

    perda = f * (L / D) * (v ** 2) / (2 * g)

    return perda


# ==================================================
# NUMERO DE REYNOLDS
# ==================================================

def calcular_reynolds(densidade, velocidade, diametro, viscosidade):

    # Re = ρ * v * D / μ

    if viscosidade == 0:
        raise ValueError("A viscosidade nao pode ser zero.")

    reynolds = (densidade * velocidade * diametro) / viscosidade

    return reynolds


# ==================================================
# CLASSIFICACAO DO REGIME DE ESCOAMENTO
# ==================================================

def classificar_regime(reynolds):

    if reynolds < 2300:
        return "Laminar"

    elif reynolds < 4000:
        return "Transicao"

    else:
        return "Turbulento"
