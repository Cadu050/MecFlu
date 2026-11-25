
import tkinter as tk
from tkinter import ttk, messagebox

# Importacao das funcoes de calculo
from calculos import (
    calcular_vazao,
    calcular_velocidade,
    calcular_perda_carga,
    calcular_reynolds,
    classificar_regime
)


# ==================================================
# CONFIGURACOES
# ==================================================

COR_FUNDO = "#EAF0F6"
COR_PRINCIPAL = "#17365D"
COR_SECUNDARIA = "#AAB7C4"
COR_TEXTO = "#222222"
COR_BRANCO = "#FFFFFF"

FONTE_TITULO = ("Arial", 15, "bold")
FONTE_NORMAL = ("Arial", 11)
FONTE_BOTAO = ("Arial", 12, "bold")


# ==================================================
# CLASSE PRINCIPAL
# ==================================================

class CalculadoraFluidos:

    def __init__(self, root):

        self.root = root

        self.root.title("Mecanica dos Fluidos")
        self.root.geometry("550x620")
        self.root.minsize(550, 620)
        self.root.configure(bg=COR_FUNDO)

        self.configurar_estilo()

        self.tela_inicial()

    # ==================================================
    # ESTILO
    # ==================================================

    def configurar_estilo(self):

        estilo = ttk.Style()

        estilo.theme_use("clam")

        estilo.configure(
            "TCombobox",
            font=FONTE_NORMAL,
            padding=5
        )

        estilo.configure(
            "TEntry",
            font=FONTE_NORMAL,
            padding=5
        )

    # ==================================================
    # CRIAR JANELAS
    # ==================================================

    def criar_janela(self, titulo):

        janela = tk.Toplevel(self.root)

        janela.title(titulo)
        janela.geometry("550x620")
        janela.minsize(550, 620)
        janela.configure(bg=COR_FUNDO)

        tk.Label(
            janela,
            text="CALCULADORA DE MECANICA DOS FLUIDOS",
            font=FONTE_TITULO,
            bg=COR_FUNDO,
            fg=COR_PRINCIPAL
        ).pack(pady=20)

        return janela

    # ==================================================
    # CRIAR BOTOES
    # ==================================================

    def criar_botao(self, pai, texto, comando, cor=COR_PRINCIPAL):

        return tk.Button(
            pai,
            text=texto,
            font=FONTE_BOTAO,
            bg=cor,
            fg=COR_BRANCO if cor == COR_PRINCIPAL else COR_TEXTO,
            width=22,
            command=comando,
            cursor="hand2"
        )

    # ==================================================
    # TELA INICIAL
    # ==================================================

    def tela_inicial(self):

        tk.Label(
            self.root,
            text="CALCULADORA DE MECANICA DOS FLUIDOS",
            font=FONTE_TITULO,
            bg=COR_FUNDO,
            fg=COR_PRINCIPAL
        ).pack(pady=35)

        tk.Label(
            self.root,
            text="Bem-vindo ao sistema!",
            font=("Arial", 13),
            bg=COR_FUNDO
        ).pack(pady=15)

        frame_botoes = tk.Frame(
            self.root,
            bg=COR_FUNDO
        )

        frame_botoes.pack(pady=25)

        self.criar_botao(
            frame_botoes,
            "BASICOS",
            self.abrir_basicos
        ).pack(pady=15)

        self.criar_botao(
            frame_botoes,
            "BOMBAS",
            self.abrir_bombas
        ).pack(pady=15)

        self.criar_botao(
            frame_botoes,
            "SIMULACAO",
            self.abrir_simulacao
        ).pack(pady=15)

    # ==================================================
    # SECAO BASICOS
    # ==================================================

    def abrir_basicos(self):

        janela = self.criar_janela("Calculos Basicos")

        # MENU

        frame_menu = tk.Frame(
            janela,
            bg=COR_FUNDO
        )

        frame_menu.pack(pady=10)

        tk.Label(
            frame_menu,
            text="Selecione a operacao:",
            font=FONTE_NORMAL,
            bg=COR_FUNDO
        ).pack()

        operacoes = [
            "Vazao",
            "Velocidade media",
            "Perda de carga distribuida",
            "Numero de Reynolds"
        ]

        selecao = ttk.Combobox(
            frame_menu,
            values=operacoes,
            state="readonly",
            width=35,
            font=FONTE_NORMAL
        )

        selecao.pack(pady=10)
        selecao.current(0)

        # CAMPOS

        frame_campos = tk.Frame(
            janela,
            bg=COR_FUNDO
        )

        frame_campos.pack(pady=10)

        campos = {}

        # RESULTADO

        frame_resultado = tk.LabelFrame(
            janela,
            text="Resultado da operacao",
            font=FONTE_NORMAL,
            bg=COR_BRANCO,
            fg=COR_PRINCIPAL,
            padx=15,
            pady=15
        )

        frame_resultado.pack(
            fill="both",
            padx=30,
            pady=10
        )

        resultado = tk.Label(
            frame_resultado,
            text="Aguardando calculo...",
            font=FONTE_NORMAL,
            bg=COR_BRANCO,
            fg=COR_TEXTO,
            justify="left"
        )

        resultado.pack(anchor="w")

        # ------------------------------------------
        # CRIAR E LIMPAR CAMPOS
        # ------------------------------------------

        def limpar_campos():

            for widget in frame_campos.winfo_children():
                widget.destroy()

            campos.clear()

        def criar_campo(nome, texto):

            tk.Label(
                frame_campos,
                text=texto,
                font=FONTE_NORMAL,
                bg=COR_FUNDO
            ).pack(anchor="w", pady=(8, 2))

            entrada = ttk.Entry(
                frame_campos,
                width=40,
                font=FONTE_NORMAL
            )

            entrada.pack(pady=2)

            campos[nome] = entrada

        # ------------------------------------------
        # MOSTRAR CAMPOS
        # ------------------------------------------

        def mostrar_campos(event=None):

            limpar_campos()

            operacao = selecao.get()

            if operacao == "Vazao":

                criar_campo("volume", "Volume do fluido (m³):")
                criar_campo("tempo", "Tempo de vazao (min):")

            elif operacao == "Velocidade media":

                criar_campo("tempo_ini", "Tempo inicial (min):")
                criar_campo("tempo_fin", "Tempo final (min):")
                criar_campo("pos_ini", "Posicao inicial (m):")
                criar_campo("pos_fin", "Posicao final (m):")

            elif operacao == "Perda de carga distribuida":

                criar_campo("atrito", "Fator de atrito:")
                criar_campo("comprimento", "Comprimento da tubulacao (m):")
                criar_campo("diametro", "Diametro interno (m):")
                criar_campo("velocidade", "Velocidade media (m/s):")

            elif operacao == "Numero de Reynolds":

                criar_campo("densidade", "Densidade do fluido (kg/m³):")
                criar_campo("velocidade", "Velocidade media (m/s):")
                criar_campo("diametro", "Diametro do tubo (m):")
                criar_campo("viscosidade", "Viscosidade dinamica (Pa.s):")

            resultado.config(text="Aguardando calculo...")

        selecao.bind(
            "<<ComboboxSelected>>",
            mostrar_campos
        )

        # ------------------------------------------
        # CALCULAR
        # ------------------------------------------

        def calcular():

            try:

                def valor(nome):

                    return float(
                        campos[nome].get().replace(",", ".")
                    )

                operacao = selecao.get()

                if operacao == "Vazao":

                    volume = valor("volume")
                    tempo = valor("tempo")

                    q = calcular_vazao(volume, tempo)

                    mensagem = (
                        "VAZAO DO FLUIDO\n\n"
                        f"Volume: {volume} m³\n"
                        f"Tempo: {tempo} min\n\n"
                        f"Vazao: {q:.6f} m³/s"
                    )

                elif operacao == "Velocidade media":

                    ti = valor("tempo_ini")
                    tf = valor("tempo_fin")
                    pi = valor("pos_ini")
                    pf = valor("pos_fin")

                    espaco, tempo, velocidade = calcular_velocidade(
                        ti, tf, pi, pf
                    )

                    mensagem = (
                        "VELOCIDADE MEDIA\n\n"
                        f"Variacao de espaco: {espaco} m\n"
                        f"Variacao de tempo: {tempo} s\n\n"
                        f"Velocidade media: {velocidade:.4f} m/s"
                    )

                elif operacao == "Perda de carga distribuida":

                    f = valor("atrito")
                    L = valor("comprimento")
                    D = valor("diametro")
                    v = valor("velocidade")

                    perda = calcular_perda_carga(f, L, D, v)

                    mensagem = (
                        "PERDA DE CARGA DISTRIBUIDA\n\n"
                        f"Comprimento: {L} m\n"
                        f"Diametro: {D} m\n\n"
                        f"Perda de carga: {perda:.4f} m"
                    )

                elif operacao == "Numero de Reynolds":

                    d = valor("densidade")
                    v = valor("velocidade")
                    D = valor("diametro")
                    mi = valor("viscosidade")

                    re = calcular_reynolds(d, v, D, mi)

                    regime = classificar_regime(re)

                    mensagem = (
                        "NUMERO DE REYNOLDS\n\n"
                        f"Reynolds: {re:.2f}\n\n"
                        f"Regime: {regime}"
                    )

                resultado.config(text=mensagem)

            except ValueError as erro:

                messagebox.showerror(
                    "Erro de entrada",
                    str(erro) or "Digite valores numericos validos.",
                    parent=janela
                )

        # ------------------------------------------
        # BOTOES
        # ------------------------------------------

        self.criar_botao(
            janela,
            "CALCULAR",
            calcular
        ).pack(pady=15)

        def limpar():

            for entrada in campos.values():
                entrada.delete(0, tk.END)

            resultado.config(
                text="Aguardando calculo..."
            )

        self.criar_botao(
            janela,
            "LIMPAR CAMPOS",
            limpar,
            COR_SECUNDARIA
        ).pack(pady=5)

        mostrar_campos()

    # ==================================================
    # SECAO BOMBAS
    # ==================================================

    def abrir_bombas(self):

        janela = self.criar_janela("Calculos de Bombas")

        tk.Label(
            janela,
            text="MODULO DE BOMBAS",
            font=("Arial", 14, "bold"),
            bg=COR_FUNDO,
            fg=COR_PRINCIPAL
        ).pack(pady=35)

        tk.Label(
            janela,
            text=(
                "Area destinada aos calculos de bombas.\n\n"
                "Futuramente serao adicionadas ferramentas\n"
                "para analise e dimensionamento de bombas."
            ),
            font=FONTE_NORMAL,
            bg=COR_FUNDO,
            fg=COR_TEXTO,
            justify="center"
        ).pack(pady=20)

        tk.Label(
            janela,
            text="Funcionalidades em desenvolvimento",
            font=("Arial", 10, "italic"),
            bg=COR_FUNDO,
            fg="#777777"
        ).pack(pady=20)

        self.criar_botao(
            janela,
            "VOLTAR",
            janela.destroy,
            COR_SECUNDARIA
        ).pack(pady=35)

    # ==================================================
    # SECAO SIMULACAO
    # ==================================================

    def abrir_simulacao(self):

        janela = self.criar_janela("Simulacao")

        tk.Label(
            janela,
            text="MODULO DE SIMULACAO",
            font=("Arial", 14, "bold"),
            bg=COR_FUNDO,
            fg=COR_PRINCIPAL
        ).pack(pady=35)

        tk.Label(
            janela,
            text=(
                "Area destinada as simulacoes de\n"
                "mecanica dos fluidos.\n\n"
                "Futuramente serao adicionadas ferramentas\n"
                "de visualizacao e analise de escoamentos."
            ),
            font=FONTE_NORMAL,
            bg=COR_FUNDO,
            fg=COR_TEXTO,
            justify="center"
        ).pack(pady=20)

        tk.Label(
            janela,
            text="Funcionalidades em desenvolvimento",
            font=("Arial", 10, "italic"),
            bg=COR_FUNDO,
            fg="#777777"
        ).pack(pady=20)

        self.criar_botao(
            janela,
            "VOLTAR",
            janela.destroy,
            COR_SECUNDARIA
        ).pack(pady=35)


# ==================================================
# INICIALIZACAO DO PROGRAMA
# ==================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = CalculadoraFluidos(root)

    root.mainloop()
