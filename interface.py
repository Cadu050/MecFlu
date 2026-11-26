"""Interface gráfica. Execute este arquivo para abrir o programa.

As telas só leem os campos, chamam as funções de calculos.py
e mostram o resultado.
"""

import tkinter as tk
from tkinter import ttk, messagebox

import calculos

# ==========================================
# APARÊNCIA (altere aqui para mudar todas as telas)
# ==========================================

AZUL = "#17365D"
AZUL_CLARO = "#24518A"
FUNDO = "#EAF0F6"
BRANCO = "#FFFFFF"
TEXTO = "#222222"
CINZA = "#D5DDE6"

FONTE = ("Arial", 11)
FONTE_NEGRITO = ("Arial", 11, "bold")
FONTE_TITULO = ("Arial", 15, "bold")

AGUARDANDO = "Preencha os campos e clique em Calcular."


def configurar_estilos(root):
    estilo = ttk.Style(root)
    estilo.theme_use("clam")

    estilo.configure("TFrame", background=FUNDO)
    estilo.configure("Cartao.TFrame", background=BRANCO)
    estilo.configure("TLabel", background=FUNDO, foreground=TEXTO, font=FONTE)
    estilo.configure("Cartao.TLabel", background=BRANCO)
    estilo.configure("Secao.Cartao.TLabel", foreground=AZUL, font=FONTE_NEGRITO)

    estilo.configure("TButton", font=FONTE_NEGRITO, padding=10, borderwidth=0,
                     background=AZUL, foreground=BRANCO)
    estilo.map("TButton", background=[("active", AZUL_CLARO)])
    estilo.configure("Secundario.TButton", background=CINZA, foreground=AZUL)
    estilo.map("Secundario.TButton", background=[("active", "#C3CEDA")])

    estilo.configure("TEntry", padding=5, fieldbackground=BRANCO)
    estilo.configure("TCombobox", padding=5)
    estilo.map("TCombobox", fieldbackground=[("readonly", BRANCO)])


def criar_cabecalho(janela, titulo):
    tk.Label(janela, text=titulo, font=FONTE_TITULO, bg=AZUL, fg=BRANCO,
             pady=18).pack(fill="x")


def configurar_janela(janela, titulo, largura=560, altura=680):
    janela.title(titulo)
    janela.geometry(f"{largura}x{altura}")
    janela.minsize(largura, altura)
    janela.configure(bg=FUNDO)
    criar_cabecalho(janela, titulo.upper())


def criar_cartao(pai):
    cartao = ttk.Frame(pai, style="Cartao.TFrame", padding=16)
    cartao.pack(fill="x", padx=24, pady=(16, 0))
    cartao.columnconfigure(1, weight=1)
    return cartao


# ==========================================
# TEXTOS DE RESULTADO
# Cada função recebe os valores digitados (v),
# chama o cálculo e devolve o texto.
# ==========================================

def numero(valor, casas=2):
    """Formata com vírgula decimal: 3.5 -> '3,50'."""
    return f"{valor:.{casas}f}".replace(".", ",")


def formatar_vazao(v):
    vazao = calculos.calcular_vazao(v["volume"], v["tempo"])
    return f"Vazão: {numero(vazao, 6)} m³/s"


def formatar_velocidade(v):
    espaco, tempo, velocidade = calculos.calcular_velocidade(
        v["tempo_ini"], v["tempo_fin"], v["pos_ini"], v["pos_fin"])
    return (f"Variação de espaço: {numero(espaco)} m\n"
            f"Variação de tempo: {numero(tempo)} s\n"
            f"Velocidade média: {numero(velocidade, 4)} m/s")


def formatar_perda_carga(v):
    perda = calculos.calcular_perda_carga(
        v["atrito"], v["comprimento"], v["diametro"], v["velocidade"])
    return f"Perda de carga: {numero(perda, 4)} m"


def formatar_reynolds(v):
    reynolds = calculos.calcular_reynolds(
        v["densidade"], v["velocidade"], v["diametro"], v["viscosidade"])
    return (f"Reynolds: {numero(reynolds)}\n"
            f"Regime: {calculos.classificar_regime(reynolds)}")


def formatar_potencia_bomba(v):
    vazao, watts = calculos.calcular_potencia_bomba(
        v["vazao"], v["altura"], v["rendimento"])
    return (f"Vazão: {numero(vazao, 5)} m³/s\n"
            f"Potência: {numero(watts)} W\n"
            f"Potência: {numero(watts / 1000, 3)} kW\n"
            f"Potência: {numero(watts / calculos.WATTS_POR_CV, 3)} cv")


def formatar_altura_manometrica(v):
    geometrica, perdas, hmt = calculos.calcular_altura_manometrica(
        v["altura_sucao"], v["altura_recalque"],
        v["perda_sucao"], v["perda_recalque"])
    return (f"Altura geométrica: {numero(geometrica)} m\n"
            f"Perdas de carga totais: {numero(perdas)} m\n"
            f"HMT: {numero(hmt)} m")


def formatar_vazao_bomba(v):
    vazao = calculos.calcular_vazao_bomba(
        v["potencia"], v["altura"], v["rendimento"])
    return (f"Vazão: {numero(vazao, 5)} m³/s\n"
            f"Vazão: {numero(vazao * 3600)} m³/h\n"
            f"Vazão: {numero(vazao * 1000)} L/s")


def formatar_consumo(v):
    horas, energia, custo = calculos.calcular_consumo(
        v["potencia"], v["horas"], v["dias"], v["tarifa"])
    texto = (f"Tempo de operação: {numero(horas)} h\n"
             f"Consumo: {numero(energia)} kWh")
    if v["tarifa"] > 0:
        texto += f"\nCusto estimado: R$ {numero(custo)}"
    return texto


# ==========================================
# MENUS
# "Nome da operação": (função, [(chave, texto do campo), ...])
# Para criar uma operação nova, adicione uma entrada aqui.
# ==========================================

OPERACOES_BASICAS = {
    "Vazão": (formatar_vazao, [
        ("volume", "Volume do fluido (m³)"),
        ("tempo", "Tempo de vazão (min)"),
    ]),
    "Velocidade média": (formatar_velocidade, [
        ("tempo_ini", "Tempo inicial (min)"),
        ("tempo_fin", "Tempo final (min)"),
        ("pos_ini", "Posição inicial (m)"),
        ("pos_fin", "Posição final (m)"),
    ]),
    "Perda de carga distribuída": (formatar_perda_carga, [
        ("atrito", "Fator de atrito"),
        ("comprimento", "Comprimento da tubulação (m)"),
        ("diametro", "Diâmetro interno (m)"),
        ("velocidade", "Velocidade média (m/s)"),
    ]),
    "Número de Reynolds": (formatar_reynolds, [
        ("densidade", "Densidade do fluido (kg/m³)"),
        ("velocidade", "Velocidade média (m/s)"),
        ("diametro", "Diâmetro do tubo (m)"),
        ("viscosidade", "Viscosidade dinâmica (Pa·s)"),
    ]),
}

OPERACOES_BOMBAS = {
    "Potência da bomba": (formatar_potencia_bomba, [
        ("vazao", "Vazão da bomba (m³/h)"),
        ("altura", "HMT (m)"),
        ("rendimento", "Rendimento (%)"),
    ]),
    "Altura manométrica total": (formatar_altura_manometrica, [
        ("altura_sucao", "Altura de sucção (m)"),
        ("altura_recalque", "Altura de recalque (m)"),
        ("perda_sucao", "Perda na sucção (m) - opcional"),
        ("perda_recalque", "Perda no recalque (m) - opcional"),
    ]),
    "Vazão da bomba": (formatar_vazao_bomba, [
        ("potencia", "Potência da bomba (kW)"),
        ("altura", "HMT (m)"),
        ("rendimento", "Rendimento (%)"),
    ]),
    "Consumo de energia elétrica": (formatar_consumo, [
        ("potencia", "Potência do motor (kW)"),
        ("horas", "Horas por dia (h)"),
        ("dias", "Número de dias"),
        ("tarifa", "Tarifa (R$/kWh) - opcional"),
    ]),
}

# Campos que podem ficar vazios (valem zero)
CAMPOS_OPCIONAIS = {"perda_sucao", "perda_recalque", "tarifa"}


def ler_numero(texto, chave, rotulo):
    texto = texto.strip().replace(",", ".")

    if texto == "":
        if chave in CAMPOS_OPCIONAIS:
            return 0.0
        raise ValueError(f"Preencha o campo: {rotulo}")

    try:
        return float(texto)
    except ValueError:
        raise ValueError(f"Valor inválido no campo: {rotulo}")


# ==========================================
# JANELAS
# ==========================================

def abrir_calculadora(root, titulo, operacoes):
    janela = tk.Toplevel(root)
    configurar_janela(janela, titulo)

    cartao_menu = criar_cartao(janela)
    ttk.Label(cartao_menu, text="Operação",
              style="Secao.Cartao.TLabel").grid(row=0, column=0, sticky="w")
    selecao = ttk.Combobox(cartao_menu, values=list(operacoes),
                           state="readonly", font=FONTE)
    selecao.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(6, 0))
    selecao.current(0)

    cartao_campos = criar_cartao(janela)

    barra = ttk.Frame(janela)
    barra.pack(fill="x", padx=24, pady=(16, 0))
    barra.columnconfigure((0, 1), weight=1, uniform="botoes")

    cartao_resultado = criar_cartao(janela)
    ttk.Label(cartao_resultado, text="Resultado",
              style="Secao.Cartao.TLabel").pack(anchor="w")
    resultado = ttk.Label(cartao_resultado, style="Cartao.TLabel",
                          justify="left")
    resultado.pack(anchor="w", pady=(8, 0))

    campos = {}   # chave -> (caixa de texto, rótulo)

    def mostrar_campos(event=None):
        for widget in cartao_campos.winfo_children():
            widget.destroy()
        campos.clear()
        resultado.config(text=AGUARDANDO)

        _, lista_campos = operacoes[selecao.get()]
        for linha, (chave, rotulo) in enumerate(lista_campos):
            ttk.Label(cartao_campos, text=rotulo, style="Cartao.TLabel").grid(
                row=linha, column=0, sticky="w", padx=(0, 12), pady=5)
            entrada = ttk.Entry(cartao_campos, font=FONTE)
            entrada.grid(row=linha, column=1, sticky="ew", pady=5)
            campos[chave] = (entrada, rotulo)

        next(iter(campos.values()))[0].focus_set()

    def calcular(event=None):
        funcao, _ = operacoes[selecao.get()]
        try:
            valores = {
                chave: ler_numero(entrada.get(), chave, rotulo)
                for chave, (entrada, rotulo) in campos.items()
            }
            resultado.config(text=funcao(valores))
        except ValueError as erro:
            resultado.config(text=AGUARDANDO)
            messagebox.showerror("Erro de entrada", str(erro), parent=janela)

    def limpar():
        for entrada, _ in campos.values():
            entrada.delete(0, tk.END)
        resultado.config(text=AGUARDANDO)

    ttk.Button(barra, text="Calcular", command=calcular).grid(
        row=0, column=0, sticky="ew", padx=(0, 6))
    ttk.Button(barra, text="Limpar campos", style="Secundario.TButton",
               command=limpar).grid(row=0, column=1, sticky="ew", padx=(6, 0))

    selecao.bind("<<ComboboxSelected>>", mostrar_campos)
    janela.bind("<Return>", calcular)
    mostrar_campos()


def abrir_simulacao(root):
    janela = tk.Toplevel(root)
    configurar_janela(janela, "Simulação")


def criar_tela_inicial():
    root = tk.Tk()
    configurar_estilos(root)
    configurar_janela(root, "Mecânica dos Fluidos", altura=420)

    ttk.Label(root, text="Escolha uma opção:").pack(pady=(36, 12))

    botoes = [
        ("Básicos", lambda: abrir_calculadora(
            root, "Cálculos básicos", OPERACOES_BASICAS)),
        ("Bombas", lambda: abrir_calculadora(
            root, "Bombas", OPERACOES_BOMBAS)),
        ("Simulação", lambda: abrir_simulacao(root)),
    ]
    for texto, comando in botoes:
        ttk.Button(root, text=texto, width=24, command=comando).pack(pady=8)

    return root


if __name__ == "__main__":
    criar_tela_inicial().mainloop()