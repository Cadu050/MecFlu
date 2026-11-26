"""
Motor da Simulação.

O usuário informa as variáveis que possui; este módulo aplica as fórmulas do
calculos.py (e suas inversas) repetidamente até não conseguir calcular mais
nada. Se o usuário pediu uma variável específica e ela não saiu, o resultado
diz exatamente o que faltou informar.

Para adicionar uma variável nova:  coloque-a em GRUPOS.
Para adicionar uma fórmula nova:   crie as regras com _regra() mais abaixo.
"""

import math
from collections import namedtuple

import calculos
from calculos import G, RHO_AGUA

_pos = calculos._exigir_positivo
_nao_neg = calculos._exigir_nao_negativo


# ==========================================
# VARIÁVEIS (aparecem na check list)
# grupo -> [(chave, texto com unidade), ...]
# ==========================================

GRUPOS = {
    "Vazão e velocidade": [
        ("volume", "Volume do fluido (m³)"),
        ("tempo", "Tempo de vazão (min)"),
        ("vazao", "Vazão (m³/h)"),
        ("tempo_ini", "Tempo inicial (min)"),
        ("tempo_fin", "Tempo final (min)"),
        ("pos_ini", "Posição inicial (m)"),
        ("pos_fin", "Posição final (m)"),
        ("velocidade", "Velocidade média (m/s)"),
    ],
    "Tubulação e escoamento": [
        ("atrito", "Fator de atrito"),
        ("comprimento", "Comprimento da tubulação (m)"),
        ("diametro", "Diâmetro interno (m)"),
        ("perda_carga", "Perda de carga distribuída (m)"),
        ("densidade", "Densidade do fluido (kg/m³)"),
        ("viscosidade", "Viscosidade dinâmica (Pa·s)"),
        ("reynolds", "Número de Reynolds"),
    ],
    "Bomba": [
        ("altura_sucao", "Altura de sucção (m)"),
        ("altura_recalque", "Altura de recalque (m)"),
        ("perda_sucao", "Perda na sucção (m) - opcional"),
        ("perda_recalque", "Perda no recalque (m) - opcional"),
        ("hmt", "HMT - altura manométrica total (m)"),
        ("rendimento", "Rendimento (%)"),
        ("potencia", "Potência da bomba/motor (kW)"),
    ],
    "Consumo de energia": [
        ("horas_dia", "Horas por dia (h)"),
        ("dias", "Número de dias"),
        ("horas_total", "Tempo total de operação (h)"),
        ("energia", "Consumo de energia (kWh)"),
        ("tarifa", "Tarifa (R$/kWh)"),
        ("custo", "Custo estimado (R$)"),
    ],
}

ROTULOS = {chave: rotulo
           for variaveis in GRUPOS.values() for chave, rotulo in variaveis}

# Como na tela de Bombas: se não forem informadas, valem 0 (só quando precisar)
OPCIONAIS_ZERO = ("perda_sucao", "perda_recalque")


# ==========================================
# REGRAS: cada fórmula, em todas as direções
# Regra = (equação, variável calculada, variáveis necessárias, função)
# ==========================================

Regra = namedtuple("Regra", "equacao saida entradas funcao")
REGRAS = []


def _regra(equacao, saida, entradas, funcao):
    REGRAS.append(Regra(equacao, saida, tuple(entradas), funcao))


# ---------- Vazão: Q = V / t  (Q em m³/h) ----------
EQ = "Vazão (Q = V / t)"


def _volume(k):
    _pos(Vazão=k["vazao"], Tempo=k["tempo"])
    return k["vazao"] * k["tempo"] / 60


def _tempo_vazao(k):
    _pos(Vazão=k["vazao"], Volume=k["volume"])
    return k["volume"] * 60 / k["vazao"]


_regra(EQ, "vazao", ["volume", "tempo"],
       lambda k: calculos.calcular_vazao(k["volume"], k["tempo"]) * 3600)
_regra(EQ, "volume", ["vazao", "tempo"], _volume)
_regra(EQ, "tempo", ["vazao", "volume"], _tempo_vazao)


# ---------- Velocidade média: v = Δs / Δt ----------
EQ = "Velocidade média (v = Δs / Δt)"


def _dt_s(k):
    return (k["tempo_fin"] - k["tempo_ini"]) * 60


def _pos_fin(k):
    _pos(Variação_de_tempo=_dt_s(k))
    return k["pos_ini"] + k["velocidade"] * _dt_s(k)


def _pos_ini(k):
    _pos(Variação_de_tempo=_dt_s(k))
    return k["pos_fin"] - k["velocidade"] * _dt_s(k)


def _dt_min_pela_velocidade(k):
    if k["velocidade"] == 0:
        raise ValueError("Velocidade média: não pode ser zero para achar o tempo.")
    dt = (k["pos_fin"] - k["pos_ini"]) / k["velocidade"]   # segundos
    _pos(Variação_de_tempo=dt)
    return dt / 60


_regra(EQ, "velocidade", ["tempo_ini", "tempo_fin", "pos_ini", "pos_fin"],
       lambda k: calculos.calcular_velocidade(
           k["tempo_ini"], k["tempo_fin"], k["pos_ini"], k["pos_fin"])[2])
_regra(EQ, "pos_fin", ["velocidade", "pos_ini", "tempo_ini", "tempo_fin"], _pos_fin)
_regra(EQ, "pos_ini", ["velocidade", "pos_fin", "tempo_ini", "tempo_fin"], _pos_ini)
_regra(EQ, "tempo_fin", ["velocidade", "pos_ini", "pos_fin", "tempo_ini"],
       lambda k: k["tempo_ini"] + _dt_min_pela_velocidade(k))
_regra(EQ, "tempo_ini", ["velocidade", "pos_ini", "pos_fin", "tempo_fin"],
       lambda k: k["tempo_fin"] - _dt_min_pela_velocidade(k))


# ---------- Perda de carga: hf = f * (L / D) * v² / (2g) ----------
EQ = "Perda de carga (Darcy-Weisbach)"


def _atrito(k):
    _pos(Perda_de_carga=k["perda_carga"], Comprimento=k["comprimento"],
         Diâmetro=k["diametro"], Velocidade=k["velocidade"])
    return (k["perda_carga"] * k["diametro"] * 2 * G
            / (k["comprimento"] * k["velocidade"] ** 2))


def _comprimento(k):
    _pos(Perda_de_carga=k["perda_carga"], Fator_de_atrito=k["atrito"],
         Diâmetro=k["diametro"], Velocidade=k["velocidade"])
    return (k["perda_carga"] * k["diametro"] * 2 * G
            / (k["atrito"] * k["velocidade"] ** 2))


def _diametro_hf(k):
    _pos(Perda_de_carga=k["perda_carga"], Fator_de_atrito=k["atrito"],
         Comprimento=k["comprimento"], Velocidade=k["velocidade"])
    return (k["atrito"] * k["comprimento"] * k["velocidade"] ** 2
            / (2 * G * k["perda_carga"]))


def _velocidade_hf(k):
    _pos(Perda_de_carga=k["perda_carga"], Fator_de_atrito=k["atrito"],
         Comprimento=k["comprimento"], Diâmetro=k["diametro"])
    return math.sqrt(k["perda_carga"] * k["diametro"] * 2 * G
                     / (k["atrito"] * k["comprimento"]))


_regra(EQ, "perda_carga", ["atrito", "comprimento", "diametro", "velocidade"],
       lambda k: calculos.calcular_perda_carga(
           k["atrito"], k["comprimento"], k["diametro"], k["velocidade"]))
_regra(EQ, "atrito", ["perda_carga", "comprimento", "diametro", "velocidade"], _atrito)
_regra(EQ, "comprimento", ["perda_carga", "atrito", "diametro", "velocidade"], _comprimento)
_regra(EQ, "diametro", ["perda_carga", "atrito", "comprimento", "velocidade"], _diametro_hf)
_regra(EQ, "velocidade", ["perda_carga", "atrito", "comprimento", "diametro"], _velocidade_hf)


# ---------- Reynolds: Re = ρ * v * D / μ ----------
EQ = "Número de Reynolds (Re = ρ·v·D / μ)"


def _densidade(k):
    _pos(Reynolds=k["reynolds"], Viscosidade=k["viscosidade"],
         Velocidade=k["velocidade"], Diâmetro=k["diametro"])
    return k["reynolds"] * k["viscosidade"] / (k["velocidade"] * k["diametro"])


def _velocidade_re(k):
    _pos(Reynolds=k["reynolds"], Viscosidade=k["viscosidade"],
         Densidade=k["densidade"], Diâmetro=k["diametro"])
    return k["reynolds"] * k["viscosidade"] / (k["densidade"] * k["diametro"])


def _diametro_re(k):
    _pos(Reynolds=k["reynolds"], Viscosidade=k["viscosidade"],
         Densidade=k["densidade"], Velocidade=k["velocidade"])
    return k["reynolds"] * k["viscosidade"] / (k["densidade"] * k["velocidade"])


def _viscosidade(k):
    _pos(Reynolds=k["reynolds"], Densidade=k["densidade"],
         Velocidade=k["velocidade"], Diâmetro=k["diametro"])
    return k["densidade"] * k["velocidade"] * k["diametro"] / k["reynolds"]


_regra(EQ, "reynolds", ["densidade", "velocidade", "diametro", "viscosidade"],
       lambda k: calculos.calcular_reynolds(
           k["densidade"], k["velocidade"], k["diametro"], k["viscosidade"]))
_regra(EQ, "densidade", ["reynolds", "velocidade", "diametro", "viscosidade"], _densidade)
_regra(EQ, "velocidade", ["reynolds", "densidade", "diametro", "viscosidade"], _velocidade_re)
_regra(EQ, "diametro", ["reynolds", "densidade", "velocidade", "viscosidade"], _diametro_re)
_regra(EQ, "viscosidade", ["reynolds", "densidade", "velocidade", "diametro"], _viscosidade)


# ---------- Potência da bomba: P = ρ * g * Q * H / η  (P em kW, Q em m³/h) ----------
EQ = "Potência da bomba (P = ρ·g·Q·H / η)"


def _hmt_bomba(k):
    _pos(Potência=k["potencia"], Vazão=k["vazao"])
    eta = calculos._rendimento_decimal(k["rendimento"])
    return k["potencia"] * 1000 * eta / (RHO_AGUA * G * k["vazao"] / 3600)


def _rendimento(k):
    _pos(Potência=k["potencia"], Vazão=k["vazao"], HMT=k["hmt"])
    valor = (RHO_AGUA * G * (k["vazao"] / 3600) * k["hmt"]
             / (k["potencia"] * 1000) * 100)
    if valor > 100:
        raise ValueError("Rendimento: o valor calculado passa de 100%. "
                         "Confira potência, vazão e HMT.")
    return valor


_regra(EQ, "potencia", ["vazao", "hmt", "rendimento"],
       lambda k: calculos.calcular_potencia_bomba(
           k["vazao"], k["hmt"], k["rendimento"])[1] / 1000)
_regra(EQ, "vazao", ["potencia", "hmt", "rendimento"],
       lambda k: calculos.calcular_vazao_bomba(
           k["potencia"], k["hmt"], k["rendimento"]) * 3600)
_regra(EQ, "hmt", ["potencia", "vazao", "rendimento"], _hmt_bomba)
_regra(EQ, "rendimento", ["potencia", "vazao", "hmt"], _rendimento)


# ---------- Altura manométrica: HMT = alturas + perdas ----------
EQ = "Altura manométrica (HMT = alturas + perdas)"
_ALTURAS = ["altura_sucao", "altura_recalque", "perda_sucao", "perda_recalque"]


def _resto(k, ignorar):
    """HMT menos todas as parcelas, exceto a que está sendo calculada."""
    return k["hmt"] - sum(k[c] for c in _ALTURAS if c != ignorar)


def _altura_recalque(k):
    valor = _resto(k, "altura_recalque")
    _pos(Altura_de_recalque=valor)
    return valor


def _perda_sucao(k):
    valor = _resto(k, "perda_sucao")
    _nao_neg(Perda_na_sucção=valor)
    return valor


def _perda_recalque(k):
    valor = _resto(k, "perda_recalque")
    _nao_neg(Perda_no_recalque=valor)
    return valor


_regra(EQ, "hmt", _ALTURAS,
       lambda k: calculos.calcular_altura_manometrica(
           k["altura_sucao"], k["altura_recalque"],
           k["perda_sucao"], k["perda_recalque"])[2])
_regra(EQ, "altura_sucao", ["hmt", "altura_recalque", "perda_sucao", "perda_recalque"],
       lambda k: _resto(k, "altura_sucao"))
_regra(EQ, "altura_recalque", ["hmt", "altura_sucao", "perda_sucao", "perda_recalque"],
       _altura_recalque)
_regra(EQ, "perda_sucao", ["hmt", "altura_sucao", "altura_recalque", "perda_recalque"],
       _perda_sucao)
_regra(EQ, "perda_recalque", ["hmt", "altura_sucao", "altura_recalque", "perda_sucao"],
       _perda_recalque)


# ---------- Tempo de operação: horas totais = horas/dia * dias ----------
EQ = "Tempo de operação (h total = h/dia × dias)"


def _limite_24(horas_dia):
    if horas_dia > 24:
        raise ValueError("Horas por dia: não podem passar de 24.")


def _horas_total(k):
    _pos(Horas_por_dia=k["horas_dia"], Número_de_dias=k["dias"])
    _limite_24(k["horas_dia"])
    return k["horas_dia"] * k["dias"]


def _horas_dia(k):
    _pos(Tempo_total=k["horas_total"], Número_de_dias=k["dias"])
    valor = k["horas_total"] / k["dias"]
    _limite_24(valor)
    return valor


def _dias(k):
    _pos(Tempo_total=k["horas_total"], Horas_por_dia=k["horas_dia"])
    _limite_24(k["horas_dia"])
    return k["horas_total"] / k["horas_dia"]


_regra(EQ, "horas_total", ["horas_dia", "dias"], _horas_total)
_regra(EQ, "horas_dia", ["horas_total", "dias"], _horas_dia)
_regra(EQ, "dias", ["horas_total", "horas_dia"], _dias)


# ---------- Energia: E = P * h ----------
EQ = "Energia (E = P × h)"


def _energia(k):
    _pos(Potência=k["potencia"], Tempo_total=k["horas_total"])
    return k["potencia"] * k["horas_total"]


def _potencia_energia(k):
    _pos(Energia=k["energia"], Tempo_total=k["horas_total"])
    return k["energia"] / k["horas_total"]


def _horas_energia(k):
    _pos(Energia=k["energia"], Potência=k["potencia"])
    return k["energia"] / k["potencia"]


_regra(EQ, "energia", ["potencia", "horas_total"], _energia)
_regra(EQ, "potencia", ["energia", "horas_total"], _potencia_energia)
_regra(EQ, "horas_total", ["energia", "potencia"], _horas_energia)


# ---------- Custo: C = E * tarifa ----------
EQ = "Custo (C = E × tarifa)"


def _custo(k):
    _pos(Energia=k["energia"])
    _nao_neg(Tarifa=k["tarifa"])
    return k["energia"] * k["tarifa"]


def _energia_custo(k):
    _pos(Custo=k["custo"], Tarifa=k["tarifa"])
    return k["custo"] / k["tarifa"]


def _tarifa(k):
    _pos(Custo=k["custo"], Energia=k["energia"])
    return k["custo"] / k["energia"]


_regra(EQ, "custo", ["energia", "tarifa"], _custo)
_regra(EQ, "energia", ["custo", "tarifa"], _energia_custo)
_regra(EQ, "tarifa", ["custo", "energia"], _tarifa)


# Índices auxiliares (montados automaticamente a partir das regras)
REGRAS_POR_SAIDA = {}
EQUACOES = {}   # equação -> variáveis que participam dela
for _r in REGRAS:
    REGRAS_POR_SAIDA.setdefault(_r.saida, []).append(_r)
    EQUACOES.setdefault(_r.equacao, {}).update(
        dict.fromkeys((_r.saida, *_r.entradas)))


# ==========================================
# SOLUÇÃO
# ==========================================

def _propagar(conhecidas):
    """Aplica as regras até não sair mais nada novo."""
    valores = dict(conhecidas)
    calculadas = {}   # variável -> regra que a calculou (na ordem do cálculo)
    erros = {}        # (variável, equação) -> mensagem
    mudou = True
    while mudou:
        mudou = False
        for regra in REGRAS:
            if regra.saida in valores:
                continue
            if not all(e in valores for e in regra.entradas):
                continue
            try:
                valores[regra.saida] = regra.funcao(valores)
            except ValueError as erro:
                erros[(regra.saida, regra.equacao)] = f"{regra.equacao}: {erro}"
                continue
            calculadas[regra.saida] = regra
            mudou = True
    return valores, calculadas, erros


def resolver(informadas, alvo=None):
    """
    informadas: {chave: valor} com o que o usuário tem.
    alvo: chave da variável desejada, ou None para calcular tudo o que der.

    Devolve um dicionário com:
      valores        todas as variáveis conhecidas (informadas + calculadas)
      calculadas     {variável: regra usada}, na ordem do cálculo
      assumidas      perdas opcionais consideradas 0
      erros          problemas de valores (divisão por zero, negativo etc.)
      alternativas   (só com alvo não resolvido) listas do que faltou informar
      parciais       (só sem alvo) equações que ficaram incompletas
    """
    valores, calculadas, erros = _propagar(informadas)

    # Perdas opcionais valem 0, mas só se ainda houver o que calcular
    zeros = {}
    if alvo is None or alvo not in valores:
        zeros = {c: 0.0 for c in OPCIONAIS_ZERO
                 if c not in valores and c != alvo}
        if zeros:
            valores, calculadas, erros = _propagar({**informadas, **zeros})

    com_zeros = dict(valores)
    usadas = {e for regra in calculadas.values() for e in regra.entradas}
    assumidas = [c for c in zeros if c in usadas]
    valores = {c: v for c, v in valores.items()
               if c not in zeros or c in assumidas}

    alternativas = []
    if alvo is not None and alvo not in valores:
        for regra in REGRAS_POR_SAIDA.get(alvo, []):
            faltam = [e for e in regra.entradas if e not in com_zeros]
            if faltam and faltam not in alternativas:
                alternativas.append(faltam)
        alternativas.sort(key=len)
        alternativas = alternativas[:3]
        assumidas = [c for c in zeros
                     if any(c in r.entradas for r in REGRAS_POR_SAIDA.get(alvo, []))]

    parciais = []
    if alvo is None:
        for equacao, variaveis in EQUACOES.items():
            sem_valor = [v for v in variaveis if v not in valores]
            if len(sem_valor) < len(variaveis) and len(sem_valor) >= 2:
                parciais.append((equacao, len(sem_valor) - 1, sem_valor))

    return {
        "alvo": alvo,
        "alvo_informado": alvo in informadas,
        "valores": valores,
        "calculadas": calculadas,
        "assumidas": assumidas,
        "erros": [msg for (saida, _), msg in erros.items() if saida not in valores],
        "alternativas": alternativas,
        "parciais": parciais,
    }
