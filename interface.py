import math
import tkinter as tk
from tkinter import ttk, messagebox
import calculos
import simulacao

# ==========================================
# APARÊNCIA (altere aqui para mudar todas as telas)
# ==========================================

AZUL = "#17365D"
AZUL_CLARO = "#24518A"
FUNDO = "#F0F4F8"
BRANCO = "#FFFFFF"
TEXTO = "#222222"
CINZA = "#D5DDE6"

FONTE = ("Segoe UI", 12)
FONTE_NEGRITO = ("Segoe UI", 12, "bold")
FONTE_TITULO = ("Segoe UI", 14, "bold")

AGUARDANDO = "Preencha os campos e clique em Calcular."
AGUARDANDO_SIMULACAO = ("Marque as variáveis que você possui, preencha os valores "
                        "e clique em Calcular.")
TUDO = "Tudo o que for possível calcular"


def configurar_estilos(root):
    estilo = ttk.Style(root)
    estilo.theme_use("clam")

    estilo.configure("TFrame", background=FUNDO)
    estilo.configure("Cartao.TFrame", background=BRANCO)
    estilo.configure("TLabel", background=FUNDO, foreground=TEXTO, font=FONTE)
    estilo.configure("Cartao.TLabel", background=BRANCO)
    estilo.configure("Secao.Cartao.TLabel", foreground=AZUL, font=FONTE_NEGRITO)

    estilo.configure("TButton", font=FONTE_NEGRITO, padding=12, borderwidth=0,
                     background=AZUL, foreground=BRANCO)
    estilo.map("TButton", background=[("active", AZUL_CLARO)])
    estilo.configure("Secundario.TButton", background=CINZA, foreground=AZUL)
    estilo.map("Secundario.TButton", background=[("active", "#C3CEDA")])

    estilo.configure("Cartao.TCheckbutton", background=BRANCO, font=FONTE)
    estilo.map("Cartao.TCheckbutton", background=[("active", BRANCO)])

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
        v["vazao"], v["altura"], v["rendimento"], v["densidade"])
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
        v["potencia"], v["altura"], v["rendimento"], v["densidade"])
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
    "Vazão pela tubulação": (lambda v: f"Vazão: {numero_auto(calculos.calcular_vazao_tubo(v['diametro'], v['velocidade']))} m³/h", [("diametro", "Diâmetro interno (m)"), ("velocidade", "Velocidade (m/s)")]),
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
        ("densidade", "Densidade (kg/m³)"),
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
        ("densidade", "Densidade (kg/m³)"),
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
        valor = float(texto)
        if not math.isfinite(valor):
            raise ValueError()
        return valor
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
            if chave == "densidade" and operacoes is OPERACOES_BOMBAS:
                entrada.insert(0, "1000")
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


def numero_auto(valor):
    """Escolhe as casas decimais conforme o tamanho do número."""
    if valor == 0:
        return "0"
    if abs(valor) < 1e-5:
        return f"{valor:.3e}".replace(".", ",")
    casas = 2 if abs(valor) >= 1000 else 4 if abs(valor) >= 1 else 6
    return numero(valor, casas)


def formatar_simulacao(res):
    """Transforma o resultado de simulacao.resolver() em texto."""
    valores, calculadas, alvo = res["valores"], res["calculadas"], res["alvo"]
    rotulos = simulacao.ROTULOS

    def linha(chave):
        return (f"• {rotulos[chave]} = {numero_auto(valores[chave])}"
                f"   [{calculadas[chave].equacao}]")

    def lista_de(chaves):
        return ", ".join(rotulos[c] for c in chaves)

    texto = []

    if alvo is not None and res["alvo_informado"]:
        texto.append(f"{rotulos[alvo]}: você já informou este valor "
                     f"({numero_auto(valores[alvo])}).")

    elif alvo is not None and alvo in calculadas:
        texto.append(linha(alvo))
        outras = [c for c in calculadas if c != alvo]
        if outras:
            texto.append("\nTambém calculado no caminho:")
            texto += [linha(c) for c in outras]

    elif alvo is not None:
        texto.append(f"Não foi possível calcular: {rotulos[alvo]}.")
        if res["alternativas"]:
            texto.append("\nFaltou informar:")
            for i, faltam in enumerate(res["alternativas"], start=1):
                prefixo = f"Opção {i}: " if len(res["alternativas"]) > 1 else ""
                texto.append(f"• {prefixo}{lista_de(faltam)}")
            texto.append("(Dica: se você já tem alguma dessas variáveis, "
                         "marque-a na lista.)")

    else:
        if calculadas:
            texto.append(f"Variáveis calculadas ({len(calculadas)}):")
            texto += [linha(c) for c in calculadas]
        else:
            texto.append("Não foi possível resolver nenhuma conta com as "
                         "variáveis marcadas.")
        if res["parciais"]:
            texto.append("\nEquações que ficaram incompletas:")
            for equacao, faltam, opcoes in res["parciais"]:
                plural = "variável" if faltam == 1 else "variáveis"
                texto.append(f"• {equacao}: falta(m) {faltam} {plural} "
                             f"entre: {lista_de(opcoes)}")

    if "reynolds" in valores and alvo in (None, "reynolds"):
        texto.append(f"\nRegime de escoamento: "
                     f"{calculos.classificar_regime(valores['reynolds'])}")

    if res["assumidas"]:
        texto.append(f"\nConsiderei 0 (campo opcional): {lista_de(res['assumidas'])}.")

    if res["erros"]:
        texto.append("\nAtenção - conta não resolvida por valor inválido:")
        texto += [f"• {erro}" for erro in res["erros"]]

    if res.get("conflitos"):
        texto.insert(0, "ATENÇÃO: dados contraditórios. Resultados provisórios.\n" + "\n".join(res["conflitos"]) + "\n")
    texto.append("\nValores informados:")
    texto.extend(f"• {rotulos[c]} = {numero_auto(v)}" for c, v in valores.items() if c not in calculadas)
    return "\n".join(texto)


def abrir_simulacao(root):
    janela = tk.Toplevel(root)
    configurar_janela(janela, "Simulação", largura=800, altura=740)

    # --- O que o usuário quer calcular ---
    cartao_alvo = criar_cartao(janela)
    ttk.Label(cartao_alvo, text="Quero calcular",
              style="Secao.Cartao.TLabel").grid(row=0, column=0, sticky="w")
    alvo = ttk.Combobox(cartao_alvo, values=[TUDO, *simulacao.ROTULOS.values()],
                        state="readonly", font=FONTE)
    alvo.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(6, 0))
    alvo.current(0)

    # --- Resultado e botões (fixos embaixo) ---
    cartao_resultado = ttk.Frame(janela, style="Cartao.TFrame", padding=16)
    cartao_resultado.pack(side="bottom", fill="x", padx=24, pady=(16, 16))
    ttk.Label(cartao_resultado, text="Resultado",
              style="Secao.Cartao.TLabel").pack(anchor="w")
    caixa = tk.Text(cartao_resultado, height=8, wrap="word", font=FONTE,
                    bg=BRANCO, fg=TEXTO, relief="flat", highlightthickness=0)
    rolagem_resultado = ttk.Scrollbar(cartao_resultado, orient="vertical",
                                      command=caixa.yview)
    caixa.configure(yscrollcommand=rolagem_resultado.set)
    rolagem_resultado.pack(side="right", fill="y")
    caixa.pack(side="left", fill="both", expand=True, pady=(8, 0))

    def mostrar(texto):
        caixa.config(state="normal")
        caixa.delete("1.0", tk.END)
        caixa.insert("1.0", texto)
        caixa.config(state="disabled")

    barra = ttk.Frame(janela)
    barra.pack(side="bottom", fill="x", padx=24, pady=(16, 0))
    barra.columnconfigure((0, 1), weight=1, uniform="botoes")

    ttk.Button(barra, text="Copiar resultado", style="Secundario.TButton", command=lambda: (janela.clipboard_clear(), janela.clipboard_append(caixa.get("1.0", "end-1c")))).grid(row=0, column=2, padx=(8, 0))
    ttk.Label(janela, text="Marque apenas dados conhecidos. Para água, informe densidade 1000 kg/m³.\nPerdas desconhecidas ficam em branco; marque zero apenas se desprezíveis.", justify="left", wraplength=650).pack(fill="x", padx=24, pady=(8, 0))
    # --- Check list rolável ---
    area_lista = ttk.Frame(janela)
    area_lista.pack(fill="both", expand=True, padx=24, pady=(16, 0))
    tela = tk.Canvas(area_lista, bg=BRANCO, highlightthickness=0)
    rolagem = ttk.Scrollbar(area_lista, orient="vertical", command=tela.yview)
    tela.configure(yscrollcommand=rolagem.set)
    rolagem.pack(side="right", fill="y")
    tela.pack(side="left", fill="both", expand=True)

    lista = ttk.Frame(tela, style="Cartao.TFrame", padding=16)
    lista.columnconfigure(0, weight=1)
    id_lista = tela.create_window((0, 0), window=lista, anchor="nw")
    lista.bind("<Configure>",
               lambda e: tela.configure(scrollregion=tela.bbox("all")))
    tela.bind("<Configure>",
              lambda e: tela.itemconfigure(id_lista, width=e.width))

    linhas = {}   # chave -> (marcada?, caixa de texto, rótulo)

    def alternar(chave):
        marcada, entrada, _ = linhas[chave]
        if marcada.get():
            entrada.config(state="normal")
            entrada.focus_set()
        else:
            entrada.delete(0, tk.END)
            entrada.config(state="disabled")

    linha = 0
    for grupo, variaveis in simulacao.GRUPOS.items():
        ttk.Label(lista, text=grupo, style="Secao.Cartao.TLabel").grid(
            row=linha, column=0, columnspan=2, sticky="w",
            pady=(0 if linha == 0 else 14, 4))
        linha += 1
        for chave, rotulo in variaveis:
            marcada = tk.BooleanVar(value=False)
            ttk.Checkbutton(lista, text=rotulo, variable=marcada,
                            style="Cartao.TCheckbutton",
                            command=lambda c=chave: alternar(c)).grid(
                row=linha, column=0, sticky="w", pady=3)
            entrada = ttk.Entry(lista, font=FONTE, width=14, state="disabled")
            entrada.grid(row=linha, column=1, sticky="e", pady=3)
            linhas[chave] = (marcada, entrada, rotulo)
            linha += 1

    def rolar(event):
        sobe = event.num == 4 or event.delta > 0
        tela.yview_scroll(-1 if sobe else 1, "units")

    for widget in (tela, lista, *lista.winfo_children()):
        widget.bind("<MouseWheel>", rolar)
        widget.bind("<Button-4>", rolar)   # Linux
        widget.bind("<Button-5>", rolar)

    rotulo_para_chave = {r: c for c, r in simulacao.ROTULOS.items()}

    def calcular(event=None):
        try:
            # chave=None: aqui um campo marcado e vazio sempre é erro
            informadas = {
                chave: ler_numero(entrada.get(), None, rotulo)
                for chave, (marcada, entrada, rotulo) in linhas.items()
                if marcada.get()
            }
            if not informadas:
                raise ValueError("Marque pelo menos uma variável que você possui.")
        except ValueError as erro:
            messagebox.showerror("Erro de entrada", str(erro), parent=janela)
            return

        escolhido = alvo.get()
        chave_alvo = None if escolhido == TUDO else rotulo_para_chave[escolhido]
        try:
            mostrar(formatar_simulacao(simulacao.resolver(informadas, chave_alvo)))
        except ValueError as erro:
            mostrar(str(erro))
            messagebox.showerror("Dados inválidos", str(erro), parent=janela)

    def limpar():
        for chave, (marcada, _, _) in linhas.items():
            marcada.set(False)
            alternar(chave)
        alvo.current(0)
        mostrar(AGUARDANDO_SIMULACAO)

    ttk.Button(barra, text="Calcular", command=calcular).grid(
        row=0, column=0, sticky="ew", padx=(0, 6))
    ttk.Button(barra, text="Limpar tudo", style="Secundario.TButton",
               command=limpar).grid(row=0, column=1, sticky="ew", padx=(6, 0))

    janela.bind("<Return>", calcular)
    mostrar(AGUARDANDO_SIMULACAO)


def criar_tela_inicial():
    root = tk.Tk()
    configurar_estilos(root)
    configurar_janela(root, "Mecânica dos Fluidos", altura=440)

    ttk.Label(root, text="Simule seu sistema ou faça cálculos individuais.").pack(pady=(36, 12))

    botoes = [
        ("Simulação", lambda: abrir_simulacao(root)),
        ("Básicos", lambda: abrir_calculadora(
            root, "Cálculos básicos", OPERACOES_BASICAS)),
        ("Bombas", lambda: abrir_calculadora(
            root, "Bombas", OPERACOES_BOMBAS)),
    ]
    for texto, comando in botoes:
        ttk.Button(root, text=texto, width=24, command=comando).pack(pady=8)

    return root


if __name__ == "__main__":
    criar_tela_inicial().mainloop()