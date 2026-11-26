import tkinter as tk
from tkinter import ttk, messagebox


# ==========================================
# FUNÇÕES DE CÁLCULO
# ==========================================



def calcular_vazao(volume, tempo_min):
    # Q = V / t  (tempo convertido de min para s)
    if tempo_min == 0:
        raise ValueError("O tempo não pode ser zero.")
    return volume / (tempo_min * 60)


def calcular_velocidade(tempo_ini, tempo_fin, pos_ini, pos_fin):
    # v = Δs / Δt  (tempos em min, convertidos para s)
    espaco = pos_fin - pos_ini
    tempo = (tempo_fin - tempo_ini) * 60
    if tempo == 0:
        raise ValueError("A variação de tempo não pode ser zero.")
    return espaco, tempo, espaco / tempo


def calcular_perda_carga(f, L, D, v, g=9.81):
    # Darcy-Weisbach: hf = f * (L / D) * v² / (2g)
    if D == 0:
        raise ValueError("O diâmetro não pode ser zero.")
    return f * (L / D) * (v ** 2) / (2 * g)


def calcular_reynolds(densidade, v, D, viscosidade):
    # Re = ρ * v * D / μ
    if viscosidade == 0:
        raise ValueError("A viscosidade não pode ser zero.")
    return densidade * v * D / viscosidade

def potencia_bombafun(vazao, altura, densidade=1000, rendimento=1.0, g=9.81):
    return (densidade * g * vazao * altura) / rendimento
# ==========================================
# JANELA PRINCIPAL
# ==========================================

root = tk.Tk()
root.title("Mecânica dos Fluidos")
root.geometry("550x620")
root.minsize(550, 620)
root.configure(bg="#FAFCFF")


# ==========================================
# TELA INICIAL
# ==========================================

def tela_inicial():

    titulo = tk.Label(
        root,
        text="CALCULADORA DE MECÂNICA DOS FLUIDOS",
        font=("Arial", 15, "bold"),
        bg="#EAF0F6",
        fg="#17365D"
    )
    titulo.pack(pady=30)

    tk.Label(
        root,
        text="Bem-vindo ao sistema!",
        font=("Arial", 13),
        bg="#EAF0F6"
    ).pack(pady=15)

    tk.Button(
        root,
        text="basicos",
        font=("Arial", 12, "bold"),
        bg="#17365D",
        fg="white",
        width=20,
        command=abrir_calculadora
    ).pack(pady=30)

    tk.Button(
            root,
            text="bombas",
            font=("Arial", 12, "bold"),
            bg="#17365D",
            fg="white",
            width=20,
            command=abrir_calculadora_3
        ).pack(pady=45)

    tk.Button(
                root,
                text="Simulaçao",
                font=("Arial", 12, "bold"),
                bg="#17365D",
                fg="white",
                width=20,
                command=abrir_calculadora_2
            ).pack(pady=50)


# ==========================================
# SEGUNDA JANELA - MENU ORIGINAL
# ==========================================

def abrir_calculadora():

    janela = tk.Toplevel(root)
    janela.title("Calculadora de Mecânica dos Fluidos")
    janela.geometry("550x620")
    janela.minsize(550, 620)
    janela.configure(bg="#EAF0F6")

    titulo = tk.Label(
        janela,
        text="CALCULADORA DE MECÂNICA DOS FLUIDOS",
        font=("Arial", 15, "bold"),
        bg="#EAF0F6",
        fg="#17365D"
    )
    titulo.pack(pady=20)

    # MENU ORIGINAL

    frame_menu = tk.Frame(janela, bg="#EAF0F6")
    frame_menu.pack(pady=10)

    tk.Label(
        frame_menu,
        text="Selecione a operação:",
        font=("Arial", 11, "bold"),
        bg="#EAF0F6"
    ).pack()

    operacoes = [
        "Vazão",
        "Velocidade média",
        "Perda de carga distribuída",
        "Número de Reynolds"
    ]

    selecao = ttk.Combobox(
        frame_menu,
        values=operacoes,
        state="readonly",
        width=35,
        font=("Arial", 11)
    )

    selecao.pack(pady=10)
    selecao.current(0)

    # CAMPOS

    frame_campos = tk.Frame(janela, bg="#EAF0F6")
    frame_campos.pack(pady=10)

    campos = {}

    # RESULTADOS

    frame_resultado = tk.LabelFrame(
        janela,
        text="Resultado da operação",
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#17365D",
        padx=15,
        pady=15
    )

    frame_resultado.pack(fill="both", padx=30, pady=10)

    resultado_label = tk.Label(
        frame_resultado,
        text="Aguardando cálculo...",
        font=("Arial", 11),
        bg="white",
        fg="#222222",
        justify="left"
    )

    resultado_label.pack(anchor="w")

    # ======================================
    # CRIAR CAMPOS
    # ======================================

    def limpar_campos():

        for widget in frame_campos.winfo_children():
            widget.destroy()

        campos.clear()

    def criar_campo(nome, texto):

        tk.Label(
            frame_campos,
            text=texto,
            font=("Arial", 10),
            bg="#EAF0F6"
        ).pack(anchor="w", pady=(8, 2))

        entrada = ttk.Entry(
            frame_campos,
            width=40,
            font=("Arial", 11)
        )

        entrada.pack(pady=2)

        campos[nome] = entrada

    # ======================================
    # MOSTRAR CAMPOS
    # ======================================

    def mostrar_campos(event=None):

        limpar_campos()

        operacao = selecao.get()

        if operacao == "Vazão":

            criar_campo("volume", "Volume do fluido (m³):")
            criar_campo("tempo", "Tempo de vazão (min):")

        elif operacao == "Velocidade média":

            criar_campo("tempo_ini", "Tempo inicial (min):")
            criar_campo("tempo_fin", "Tempo final (min):")
            criar_campo("pos_ini", "Posição inicial (m):")
            criar_campo("pos_fin", "Posição final (m):")

        elif operacao == "Perda de carga distribuída":

            criar_campo("atrito", "Fator de atrito:")
            criar_campo("comprimento", "Comprimento da tubulação (m):")
            criar_campo("diametro", "Diâmetro interno (m):")
            criar_campo("velocidade", "Velocidade média (m/s):")

        elif operacao == "Número de Reynolds":

            criar_campo("densidade", "Densidade do fluido (kg/m³):")
            criar_campo("velocidade", "Velocidade média (m/s):")
            criar_campo("diametro", "Diâmetro do tubo (m):")
            criar_campo("viscosidade", "Viscosidade dinâmica (Pa.s):")

    selecao.bind(
        "<<ComboboxSelected>>",
        mostrar_campos
    )

    # ======================================
    # CALCULAR
    # ======================================

    def calcular():

        try:

            def valor(nome):
                return float(
                    campos[nome].get().replace(",", ".")
                )

            operacao = selecao.get()

            if operacao == "Vazão":

                volume = valor("volume")
                tempo = valor("tempo")

                q = calcular_vazao(volume, tempo)

                mensagem = (
                    f"VAZÃO DO FLUIDO\n\n"
                    f"Volume: {volume} m³\n"
                    f"Tempo: {tempo} min\n\n"
                    f"Vazão: {q:.6f} m³/s"
                )

            elif operacao == "Velocidade média":

                ti = valor("tempo_ini")
                tf = valor("tempo_fin")
                pi = valor("pos_ini")
                pf = valor("pos_fin")

                espaco, tempo, velocidade = calcular_velocidade(
                    ti, tf, pi, pf
                )

                mensagem = (
                    f"VELOCIDADE MÉDIA\n\n"
                    f"Variação de espaço: {espaco} m\n"
                    f"Variação de tempo: {tempo} s\n\n"
                    f"Velocidade média: {velocidade:.4f} m/s"
                )

            elif operacao == "Perda de carga distribuída":

                f = valor("atrito")
                L = valor("comprimento")
                D = valor("diametro")
                v = valor("velocidade")

                perda = calcular_perda_carga(f, L, D, v)

                mensagem = (
                    f"PERDA DE CARGA DISTRIBUÍDA\n\n"
                    f"Comprimento: {L} m\n"
                    f"Diâmetro: {D} m\n\n"
                    f"Perda de carga: {perda:.4f} m"
                )

            elif operacao == "Número de Reynolds":

                d = valor("densidade")
                v = valor("velocidade")
                D = valor("diametro")
                mi = valor("viscosidade")

                re = calcular_reynolds(d, v, D, mi)

                if re < 2300:
                    regime = "Laminar"
                elif re < 4000:
                    regime = "Transição"
                else:
                    regime = "Turbulento"

                mensagem = (
                    f"NÚMERO DE REYNOLDS\n\n"
                    f"Reynolds: {re:.2f}\n\n"
                    f"Regime: {regime}"
                )

            resultado_label.config(text=mensagem)

        except ValueError as erro:

            messagebox.showerror(
                "Erro de entrada",
                str(erro) or "Digite valores numéricos válidos.",
                parent=janela
            )

    # ======================================
    # BOTÕES
    # ======================================

    tk.Button(
        janela,
        text="CALCULAR",
        font=("Arial", 12, "bold"),
        bg="#17365D",
        fg="white",
        width=20,
        command=calcular
    ).pack(pady=15)

    def limpar():

        for entrada in campos.values():
            entrada.delete(0, tk.END)

        resultado_label.config(
            text="Aguardando cálculo..."
        )

    tk.Button(
        janela,
        text="LIMPAR CAMPOS",
        font=("Arial", 10),
        bg="#AAB7C4",
        width=20,
        command=limpar
    ).pack(pady=5)

    # MOSTRAR PRIMEIRA OPERAÇÃO

    mostrar_campos()


# ==========================================
# SEGUNDA FUNÇÃO (NOME ALTERADO)
# ==========================================

def abrir_calculadora_2():

    janela = tk.Toplevel(root)
    janela.title("Calculadora de Mecânica dos Fluidos")
    janela.geometry("550x620")
    janela.minsize(550, 620)
    janela.configure(bg="#EAF0F6")

    titulo = tk.Label(
        janela,
        text="CALCULADORA DE MECÂNICA DOS FLUIDOS",
        font=("Arial", 15, "bold"),
        bg="#EAF0F6",
        fg="#17365D"
    )
    titulo.pack(pady=20)

    # MENU ORIGINAL

    frame_menu = tk.Frame(janela, bg="#EAF0F6")
    frame_menu.pack(pady=10)

    tk.Label(
        frame_menu,
        text="Selecione a operação:",
        font=("Arial", 11, "bold"),
        bg="#EAF0F6"
    ).pack()

    operacoes = [
        "Vazão",
        "Velocidade média",
        "Perda de carga distribuída",
        "Número de Reynolds"
    ]

    selecao = ttk.Combobox(
        frame_menu,
        values=operacoes,
        state="readonly",
        width=35,
        font=("Arial", 11)
    )

    selecao.pack(pady=10)
    selecao.current(0)

    # CAMPOS

    frame_campos = tk.Frame(janela, bg="#EAF0F6")
    frame_campos.pack(pady=10)

    campos = {}

    # RESULTADOS

    frame_resultado = tk.LabelFrame(
        janela,
        text="Resultado da operação",
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#17365D",
        padx=15,
        pady=15
    )

    frame_resultado.pack(fill="both", padx=30, pady=10)

    resultado_label = tk.Label(
        frame_resultado,
        text="Aguardando cálculo...",
        font=("Arial", 11),
        bg="white",
        fg="#222222",
        justify="left"
    )

    resultado_label.pack(anchor="w")

    # ======================================
    # CRIAR CAMPOS
    # ======================================

    def limpar_campos():

        for widget in frame_campos.winfo_children():
            widget.destroy()

        campos.clear()

    def criar_campo(nome, texto):

        tk.Label(
            frame_campos,
            text=texto,
            font=("Arial", 10),
            bg="#EAF0F6"
        ).pack(anchor="w", pady=(8, 2))

        entrada = ttk.Entry(
            frame_campos,
            width=40,
            font=("Arial", 11)
        )

        entrada.pack(pady=2)

        campos[nome] = entrada

    # ======================================
    # MOSTRAR CAMPOS
    # ======================================

    def mostrar_campos(event=None):

        limpar_campos()

        operacao = selecao.get()

        if operacao == "Vazão":

            criar_campo("volume", "Volume do fluido (m³):")
            criar_campo("tempo", "Tempo de vazão (min):")

        elif operacao == "Velocidade média":

            criar_campo("tempo_ini", "Tempo inicial (min):")
            criar_campo("tempo_fin", "Tempo final (min):")
            criar_campo("pos_ini", "Posição inicial (m):")
            criar_campo("pos_fin", "Posição final (m):")

        elif operacao == "Perda de carga distribuída":

            criar_campo("atrito", "Fator de atrito:")
            criar_campo("comprimento", "Comprimento da tubulação (m):")
            criar_campo("diametro", "Diâmetro interno (m):")
            criar_campo("velocidade", "Velocidade média (m/s):")

        elif operacao == "Número de Reynolds":

            criar_campo("densidade", "Densidade do fluido (kg/m³):")
            criar_campo("velocidade", "Velocidade média (m/s):")
            criar_campo("diametro", "Diâmetro do tubo (m):")
            criar_campo("viscosidade", "Viscosidade dinâmica (Pa.s):")

    selecao.bind(
        "<<ComboboxSelected>>",
        mostrar_campos
    )

    # ======================================
    # CALCULAR
    # ======================================

    def calcular():

        try:

            def valor(nome):
                return float(
                    campos[nome].get().replace(",", ".")
                )

            operacao = selecao.get()

            if operacao == "Vazão":

                volume = valor("volume")
                tempo = valor("tempo")

                q = potencia_bombafun(volume, tempo)

                mensagem = (
                    f"VAZÃO DO FLUIDO\n\n"
                    f"Volume: {volume} m³\n"
                    f"Tempo: {tempo} min\n\n"
                    f"Vazão: {q:.6f} m³/s"
                )

            elif operacao == "Velocidade média":

                ti = valor("tempo_ini")
                tf = valor("tempo_fin")
                pi = valor("pos_ini")
                pf = valor("pos_fin")

                espaco, tempo, velocidade = calcular_velocidade(
                    ti, tf, pi, pf
                )

                mensagem = (
                    f"VELOCIDADE MÉDIA\n\n"
                    f"Variação de espaço: {espaco} m\n"
                    f"Variação de tempo: {tempo} s\n\n"
                    f"Velocidade média: {velocidade:.4f} m/s"
                )

            elif operacao == "Perda de carga distribuída":

                f = valor("atrito")
                L = valor("comprimento")
                D = valor("diametro")
                v = valor("velocidade")

                perda = calcular_perda_carga(f, L, D, v)

                mensagem = (
                    f"PERDA DE CARGA DISTRIBUÍDA\n\n"
                    f"Comprimento: {L} m\n"
                    f"Diâmetro: {D} m\n\n"
                    f"Perda de carga: {perda:.4f} m"
                )

            elif operacao == "Número de Reynolds":

                d = valor("densidade")
                v = valor("velocidade")
                D = valor("diametro")
                mi = valor("viscosidade")

                re = calcular_reynolds(d, v, D, mi)

                if re < 2300:
                    regime = "Laminar"
                elif re < 4000:
                    regime = "Transição"
                else:
                    regime = "Turbulento"

                mensagem = (
                    f"NÚMERO DE REYNOLDS\n\n"
                    f"Reynolds: {re:.2f}\n\n"
                    f"Regime: {regime}"
                )

            resultado_label.config(text=mensagem)

        except ValueError as erro:

            messagebox.showerror(
                "Erro de entrada",
                str(erro) or "Digite valores numéricos válidos.",
                parent=janela
            )

    # ======================================
    # BOTÕES
    # ======================================

    tk.Button(
        janela,
        text="CALCULAR",
        font=("Arial", 12, "bold"),
        bg="#17365D",
        fg="white",
        width=20,
        command=calcular
    ).pack(pady=15)

    def limpar():

        for entrada in campos.values():
            entrada.delete(0, tk.END)

        resultado_label.config(
            text="Aguardando cálculo..."
        )

    tk.Button(
        janela,
        text="LIMPAR CAMPOS",
        font=("Arial", 10),
        bg="#AAB7C4",
        width=20,
        command=limpar
    ).pack(pady=5)

    # MOSTRAR PRIMEIRA OPERAÇÃO

    mostrar_campos()


def abrir_calculadora_3():

    G = 9.81        # aceleração da gravidade (m/s²)
    RHO = 1000      # densidade da água (kg/m³)

    janela = tk.Toplevel(root)
    janela.title("Calculadora de bombas")
    janela.geometry("550x620")
    janela.minsize(550, 620)
    janela.configure(bg="#EAF0F6")

    titulo = tk.Label(
        janela,
        text="CALCULADORA DE BOMBAS",
        font=("Arial", 15, "bold"),
        bg="#EAF0F6",
        fg="#17365D"
    )
    titulo.pack(pady=20)

    # MENU ORIGINAL

    frame_menu = tk.Frame(janela, bg="#EAF0F6")
    frame_menu.pack(pady=10)

    tk.Label(
        frame_menu,
        text="Selecione o tipo de bomba:",
        font=("Arial", 11, "bold"),
        bg="#EAF0F6"
    ).pack()

    operacoes = [
        "potência da bomba",
        "Altura manométrica total",
        "vazão da bomba",
        "consumo de energia elétrica"
    ]

    selecao = ttk.Combobox(
        frame_menu,
        values=operacoes,
        state="readonly",
        width=35,
        font=("Arial", 11)
    )

    selecao.pack(pady=10)
    selecao.current(0)

    # CAMPOS

    frame_campos = tk.Frame(janela, bg="#EAF0F6")
    frame_campos.pack(pady=10)

    campos = {}

    # RESULTADOS

    frame_resultado = tk.LabelFrame(
        janela,
        text="Resultado da operação",
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#17365D",
        padx=15,
        pady=15
    )

    frame_resultado.pack(fill="both", padx=30, pady=10)

    resultado_label = tk.Label(
        frame_resultado,
        text="Aguardando cálculo...",
        font=("Arial", 11),
        bg="white",
        fg="#222222",
        justify="left"
    )

    resultado_label.pack(anchor="w")

    # ======================================
    # CRIAR CAMPOS
    # ======================================

    def limpar_campos():

        for widget in frame_campos.winfo_children():
            widget.destroy()

        campos.clear()

    def criar_campo(nome, texto):

        tk.Label(
            frame_campos,
            text=texto,
            font=("Arial", 10),
            bg="#EAF0F6"
        ).pack(anchor="w", pady=(8, 2))

        entrada = ttk.Entry(
            frame_campos,
            width=40,
            font=("Arial", 11)
        )

        entrada.pack(pady=2)

        campos[nome] = entrada

    # ======================================
    # MOSTRAR CAMPOS
    # ======================================

    def mostrar_campos(event=None):

        limpar_campos()
        resultado_label.config(text="Aguardando cálculo...")

        operacao = selecao.get()

        if operacao == "potência da bomba":

            criar_campo("vazao", "Vazão da bomba (m³/h):")
            criar_campo("altura", "Altura manométrica total - HMT (m):")
            criar_campo("rendimento", "Rendimento da bomba (%):")

        elif operacao == "Altura manométrica total":

            criar_campo("h_sucao", "Altura de sucção (m):")
            criar_campo("h_recalque", "Altura de recalque (m):")
            criar_campo("perda_sucao", "Perda de carga na sucção (m):")
            criar_campo("perda_recalque", "Perda de carga no recalque (m):")

        elif operacao == "vazão da bomba":

            criar_campo("potencia", "Potência da bomba (kW):")
            criar_campo("altura", "Altura manométrica total - HMT (m):")
            criar_campo("rendimento", "Rendimento da bomba (%):")

        elif operacao == "consumo de energia elétrica":

            criar_campo("potencia", "Potência elétrica do motor (kW):")
            criar_campo("horas", "Horas de funcionamento por dia (h):")
            criar_campo("dias", "Número de dias:")
            criar_campo("tarifa", "Tarifa de energia (R$/kWh) - opcional:")

    selecao.bind(
        "<<ComboboxSelected>>",
        mostrar_campos
    )

    # ======================================
    # CÁLCULOS
    # ======================================

    def calcular():

        try:

            def valor(nome, rotulo, obrigatorio=True, positivo=True):

                texto = campos[nome].get().strip().replace(",", ".")

                if texto == "":
                    if obrigatorio:
                        raise ValueError(f"Preencha o campo: {rotulo}")
                    return 0.0

                try:
                    numero = float(texto)
                except ValueError:
                    raise ValueError(
                        f"Valor inválido no campo: {rotulo}"
                    )

                if positivo and numero <= 0:
                    raise ValueError(
                        f"O campo '{rotulo}' deve ser maior que zero."
                    )

                return numero

            def rendimento_decimal():

                r = valor("rendimento", "Rendimento")

                if r > 100:
                    raise ValueError(
                        "O rendimento deve estar entre 0 e 100%."
                    )

                return r / 100

            operacao = selecao.get()

            # ---------- POTÊNCIA DA BOMBA ----------
            if operacao == "potência da bomba":

                vazao_h = valor("vazao", "Vazão")
                altura = valor("altura", "HMT")
                eta = rendimento_decimal()

                q = vazao_h / 3600                      # m³/s
                potencia_w = RHO * G * q * altura / eta
                potencia_kw = potencia_w / 1000
                potencia_cv = potencia_w / 735.5

                mensagem = (
                    "POTÊNCIA DA BOMBA\n\n"
                    f"Vazão: {vazao_h:.2f} m³/h ({q:.5f} m³/s)\n"
                    f"HMT: {altura:.2f} m\n"
                    f"Rendimento: {eta * 100:.1f} %\n\n"
                    f"Potência: {potencia_w:.2f} W\n"
                    f"Potência: {potencia_kw:.3f} kW\n"
                    f"Potência: {potencia_cv:.3f} cv"
                )

            # ---------- ALTURA MANOMÉTRICA TOTAL ----------
            elif operacao == "Altura manométrica total":

                hs = valor("h_sucao", "Altura de sucção", positivo=False)
                hr = valor("h_recalque", "Altura de recalque")
                ps = valor("perda_sucao", "Perda na sucção",
                           obrigatorio=False, positivo=False)
                pr = valor("perda_recalque", "Perda no recalque",
                           obrigatorio=False, positivo=False)

                h_geometrica = hs + hr
                perdas = ps + pr
                hmt = h_geometrica + perdas

                mensagem = (
                    "ALTURA MANOMÉTRICA TOTAL\n\n"
                    f"Altura geométrica: {h_geometrica:.2f} m\n"
                    f"Perdas de carga totais: {perdas:.2f} m\n\n"
                    f"HMT: {hmt:.2f} m"
                )

            # ---------- VAZÃO DA BOMBA ----------
            elif operacao == "vazão da bomba":

                potencia_kw = valor("potencia", "Potência")
                altura = valor("altura", "HMT")
                eta = rendimento_decimal()

                q = (potencia_kw * 1000 * eta) / (RHO * G * altura)   # m³/s

                mensagem = (
                    "VAZÃO DA BOMBA\n\n"
                    f"Potência: {potencia_kw:.3f} kW\n"
                    f"HMT: {altura:.2f} m\n"
                    f"Rendimento: {eta * 100:.1f} %\n\n"
                    f"Vazão: {q:.5f} m³/s\n"
                    f"Vazão: {q * 3600:.2f} m³/h\n"
                    f"Vazão: {q * 1000:.2f} L/s"
                )

            # ---------- CONSUMO DE ENERGIA ELÉTRICA ----------
            elif operacao == "consumo de energia elétrica":

                potencia_kw = valor("potencia", "Potência")
                horas = valor("horas", "Horas por dia")
                dias = valor("dias", "Número de dias")
                tarifa = valor("tarifa", "Tarifa",
                               obrigatorio=False, positivo=False)

                if horas > 24:
                    raise ValueError(
                        "As horas por dia não podem passar de 24."
                    )

                energia = potencia_kw * horas * dias

                mensagem = (
                    "CONSUMO DE ENERGIA ELÉTRICA\n\n"
                    f"Potência: {potencia_kw:.3f} kW\n"
                    f"Tempo de operação: {horas * dias:.2f} h\n\n"
                    f"Consumo: {energia:.2f} kWh"
                )

                if tarifa > 0:
                    mensagem += f"\nCusto estimado: R$ {energia * tarifa:.2f}"

            resultado_label.config(text=mensagem)

        except ValueError as erro:

            messagebox.showerror(
                "Erro de entrada",
                str(erro) or "Digite valores numéricos válidos.",
                parent=janela
            )

    # ======================================
    # BOTÕES
    # ======================================

    tk.Button(
        janela,
        text="CALCULAR",
        font=("Arial", 12, "bold"),
        bg="#17365D",
        fg="white",
        width=20,
        command=calcular
    ).pack(pady=15)

    def limpar():

        for entrada in campos.values():
            entrada.delete(0, tk.END)

        resultado_label.config(
            text="Aguardando cálculo..."
        )

    tk.Button(
        janela,
        text="LIMPAR CAMPOS",
        font=("Arial", 10),
        bg="#AAB7C4",
        width=20,
        command=limpar
    ).pack(pady=5)

    # MOSTRAR PRIMEIRA OPERAÇÃO

    mostrar_campos()

# ==========================================
# INICIAR PROGRAMA
# ==========================================

tela_inicial()

root.mainloop()