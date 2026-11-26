import tkinter as tk
from tkinter import ttk, messagebox
import calculos

AZUL = "#17365D"
FUNDO = "#EAF0F6"

def mostrar_vazao(v):
    q = calculos.calcular_vazao(v["volume"], v["tempo"])
    return (
        "VAZÃO DO FLUIDO\n\n"
        f"Volume: {v['volume']} m³\n"
        f"Tempo: {v['tempo']} min\n\n"
        f"Vazão: {q:.6f} m³/s"
    )


def mostrar_velocidade(v):
    espaco, tempo, velocidade = calculos.calcular_velocidade(
        v["tempo_ini"], v["tempo_fin"], v["pos_ini"], v["pos_fin"]
    )
    return (
        "VELOCIDADE MÉDIA\n\n"
        f"Variação de espaço: {espaco} m\n"
        f"Variação de tempo: {tempo} s\n\n"
        f"Velocidade média: {velocidade:.4f} m/s"
    )


def mostrar_perda_carga(v):
    perda = calculos.calcular_perda_carga(
        v["atrito"], v["comprimento"], v["diametro"], v["velocidade"]
    )
    return (
        "PERDA DE CARGA DISTRIBUÍDA\n\n"
        f"Comprimento: {v['comprimento']} m\n"
        f"Diâmetro: {v['diametro']} m\n\n"
        f"Perda de carga: {perda:.4f} m"
    )


def mostrar_reynolds(v):
    re = calculos.calcular_reynolds(
        v["densidade"], v["velocidade"], v["diametro"], v["viscosidade"]
    )
    return (
        "NÚMERO DE REYNOLDS\n\n"
        f"Reynolds: {re:.2f}\n\n"
        f"Regime: {calculos.classificar_regime(re)}"
    )


def mostrar_potencia_bomba(v):
    q, watts = calculos.calcular_potencia_bomba(
        v["vazao"], v["altura"], v["rendimento"]
    )
    return (
        "POTÊNCIA DA BOMBA\n\n"
        f"Vazão: {v['vazao']:.2f} m³/h ({q:.5f} m³/s)\n"
        f"HMT: {v['altura']:.2f} m\n"
        f"Rendimento: {v['rendimento']:.1f} %\n\n"
        f"Potência: {watts:.2f} W\n"
        f"Potência: {watts / 1000:.3f} kW\n"
        f"Potência: {watts / 735.5:.3f} cv"
    )


def mostrar_altura_manometrica(v):
    geometrica, perdas, hmt = calculos.calcular_altura_manometrica(
        v["h_sucao"], v["h_recalque"], v["perda_sucao"], v["perda_recalque"]
    )
    return (
        "ALTURA MANOMÉTRICA TOTAL\n\n"
        f"Altura geométrica: {geometrica:.2f} m\n"
        f"Perdas de carga totais: {perdas:.2f} m\n\n"
        f"HMT: {hmt:.2f} m"
    )


def mostrar_vazao_bomba(v):
    q = calculos.calcular_vazao_bomba(
        v["potencia"], v["altura"], v["rendimento"]
    )
    return (
        "VAZÃO DA BOMBA\n\n"
        f"Potência: {v['potencia']:.3f} kW\n"
        f"HMT: {v['altura']:.2f} m\n"
        f"Rendimento: {v['rendimento']:.1f} %\n\n"
        f"Vazão: {q:.5f} m³/s\n"
        f"Vazão: {q * 3600:.2f} m³/h\n"
        f"Vazão: {q * 1000:.2f} L/s"
    )


def mostrar_consumo(v):
    horas, energia, custo = calculos.calcular_consumo(
        v["potencia"], v["horas"], v["dias"], v["tarifa"]
    )
    mensagem = (
        "CONSUMO DE ENERGIA ELÉTRICA\n\n"
        f"Potência: {v['potencia']:.3f} kW\n"
        f"Tempo de operação: {horas:.2f} h\n\n"
        f"Consumo: {energia:.2f} kWh"
    )
    if v["tarifa"] > 0:
        mensagem += f"\nCusto estimado: R$ {custo:.2f}"
    return mensagem

# ==========================================
# MENUS
# "nome da operação": (função, [(chave, texto do campo), ...])
# Para criar uma operação nova, basta adicionar uma entrada aqui.
# ==========================================

OPERACOES_BASICAS = {
    "Vazão": (mostrar_vazao, [
        ("volume", "Volume do fluido (m³):"),
        ("tempo", "Tempo de vazão (min):"),
    ]),
    "Velocidade média": (mostrar_velocidade, [
        ("tempo_ini", "Tempo inicial (min):"),
        ("tempo_fin", "Tempo final (min):"),
        ("pos_ini", "Posição inicial (m):"),
        ("pos_fin", "Posição final (m):"),
    ]),
    "Perda de carga distribuída": (mostrar_perda_carga, [
        ("atrito", "Fator de atrito:"),
        ("comprimento", "Comprimento da tubulação (m):"),
        ("diametro", "Diâmetro interno (m):"),
        ("velocidade", "Velocidade média (m/s):"),
    ]),
    "Número de Reynolds": (mostrar_reynolds, [
        ("densidade", "Densidade do fluido (kg/m³):"),
        ("velocidade", "Velocidade média (m/s):"),
        ("diametro", "Diâmetro do tubo (m):"),
        ("viscosidade", "Viscosidade dinâmica (Pa.s):"),
    ]),
}

OPERACOES_BOMBAS = {
    "potência da bomba": (mostrar_potencia_bomba, [
        ("vazao", "Vazão da bomba (m³/h):"),
        ("altura", "Altura manométrica total - HMT (m):"),
        ("rendimento", "Rendimento da bomba (%):"),
    ]),
    "Altura manométrica total": (mostrar_altura_manometrica, [
        ("h_sucao", "Altura de sucção (m):"),
        ("h_recalque", "Altura de recalque (m):"),
        ("perda_sucao", "Perda de carga na sucção (m):"),
        ("perda_recalque", "Perda de carga no recalque (m):"),
    ]),
    "vazão da bomba": (mostrar_vazao_bomba, [
        ("potencia", "Potência da bomba (kW):"),
        ("altura", "Altura manométrica total - HMT (m):"),
        ("rendimento", "Rendimento da bomba (%):"),
    ]),
    "consumo de energia elétrica": (mostrar_consumo, [
        ("potencia", "Potência elétrica do motor (kW):"),
        ("horas", "Horas de funcionamento por dia (h):"),
        ("dias", "Número de dias:"),
        ("tarifa", "Tarifa de energia (R$/kWh) - opcional:"),
    ]),
}

# Campos que podem ficar vazios (valem zero)
CAMPOS_OPCIONAIS = {"perda_sucao", "perda_recalque", "tarifa"}


def ler_numero(entrada, chave, rotulo):
    texto = entrada.get().strip().replace(",", ".")
    nome = rotulo.rstrip(":")

    if texto == "":
        if chave in CAMPOS_OPCIONAIS:
            return 0.0
        raise ValueError(f"Preencha o campo: {nome}")

    try:
        return float(texto)
    except ValueError:
        raise ValueError(f"Valor inválido no campo: {nome}")


# ==========================================
# JANELA DE CALCULADORA (usada por todos os menus)
# ==========================================

def abrir_calculadora(root, titulo_janela, titulo, texto_menu, operacoes):
    janela = tk.Toplevel(root)
    janela.title(titulo_janela)
    janela.geometry("550x620")
    janela.minsize(550, 620)
    janela.configure(bg=FUNDO)

    tk.Label(janela, text=titulo, font=("Arial", 15, "bold"),
             bg=FUNDO, fg=AZUL).pack(pady=20)

    frame_menu = tk.Frame(janela, bg=FUNDO)
    frame_menu.pack(pady=10)

    tk.Label(frame_menu, text=texto_menu, font=("Arial", 11, "bold"),
             bg=FUNDO).pack()

    selecao = ttk.Combobox(frame_menu, values=list(operacoes),
                           state="readonly", width=35, font=("Arial", 11))
    selecao.pack(pady=10)
    selecao.current(0)

    frame_campos = tk.Frame(janela, bg=FUNDO)
    frame_campos.pack(pady=10)

    frame_resultado = tk.LabelFrame(
        janela, text="Resultado da operação", font=("Arial", 11, "bold"),
        bg="white", fg=AZUL, padx=15, pady=15
    )
    frame_resultado.pack(fill="both", padx=30, pady=10)

    resultado = tk.Label(frame_resultado, font=("Arial", 11), bg="white",
                         fg="#222222", justify="left")
    resultado.pack(anchor="w")

    campos = {}   # chave -> (caixa de texto, rótulo)

    def mostrar_campos(event=None):
        for widget in frame_campos.winfo_children():
            widget.destroy()
        campos.clear()
        resultado.config(text="Aguardando cálculo...")

        _, lista_campos = operacoes[selecao.get()]
        for chave, rotulo in lista_campos:
            tk.Label(frame_campos, text=rotulo, font=("Arial", 10),
                     bg=FUNDO).pack(anchor="w", pady=(8, 2))
            entrada = ttk.Entry(frame_campos, width=40, font=("Arial", 11))
            entrada.pack(pady=2)
            campos[chave] = (entrada, rotulo)

    def calcular():
        funcao, _ = operacoes[selecao.get()]
        try:
            valores = {
                chave: ler_numero(entrada, chave, rotulo)
                for chave, (entrada, rotulo) in campos.items()
            }
            resultado.config(text=funcao(valores))
        except ValueError as erro:
            messagebox.showerror("Erro de entrada", str(erro), parent=janela)

    def limpar():
        for entrada, _ in campos.values():
            entrada.delete(0, tk.END)
        resultado.config(text="Aguardando cálculo...")

    tk.Button(janela, text="CALCULAR", font=("Arial", 12, "bold"),
              bg=AZUL, fg="white", width=20, command=calcular).pack(pady=15)

    tk.Button(janela, text="LIMPAR CAMPOS", font=("Arial", 10),
              bg="#AAB7C4", width=20, command=limpar).pack(pady=5)

    selecao.bind("<<ComboboxSelected>>", mostrar_campos)
    mostrar_campos()


# ==========================================
# TELA INICIAL
# ==========================================

def criar_tela_inicial():
    root = tk.Tk()
    root.title("Mecânica dos Fluidos")
    root.geometry("550x620")
    root.minsize(550, 620)
    root.configure(bg="#FAFCFF")

    def abrir_basicos():
        abrir_calculadora(
            root,
            "Calculadora de Mecânica dos Fluidos",
            "CALCULADORA DE MECÂNICA DOS FLUIDOS",
            "Selecione a operação:",
            OPERACOES_BASICAS,
        )

    def abrir_bombas():
        abrir_calculadora(
            root,
            "Calculadora de bombas",
            "CALCULADORA DE BOMBAS",
            "Selecione o tipo de bomba:",
            OPERACOES_BOMBAS,
        )

    tk.Label(root, text="CALCULADORA DE MECÂNICA DOS FLUIDOS",
             font=("Arial", 15, "bold"), bg=FUNDO, fg=AZUL).pack(pady=30)

    tk.Label(root, text="Bem-vindo ao sistema!", font=("Arial", 13),
             bg=FUNDO).pack(pady=15)

    # "Simulaçao" abre a mesma tela de "basicos" (ainda não há simulação)
    botoes = [
        ("basicos", abrir_basicos, 30),
        ("bombas", abrir_bombas, 45),
        ("Simulaçao", abrir_basicos, 50),
    ]
    for texto, comando, espaco in botoes:
        tk.Button(root, text=texto, font=("Arial", 12, "bold"), bg=AZUL,
                  fg="white", width=20, command=comando).pack(pady=espaco)

    return root


if __name__ == "__main__":
    criar_tela_inicial().mainloop()