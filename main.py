import tkinter as tk
from tkinter import ttk, messagebox

from calculos import *
# ==================================================
# CONFIGURAÇÕES (somente interface)
# ==================================================

# Cores
COR_FUNDO = "#EAF0F6"
COR_PRINCIPAL = "#17365D"
COR_PRINCIPAL_HOVER = "#24508A"
COR_SECUNDARIA = "#AAB7C4"
COR_SECUNDARIA_HOVER = "#95A4B3"
COR_TEXTO = "#222222"
COR_TEXTO_SUAVE = "#6B7785"
COR_BRANCO = "#FFFFFF"
COR_BORDA = "#C5D1DD"

# Fontes
FONTE_TITULO = ("Arial", 15, "bold")
FONTE_SUBTITULO = ("Arial", 10)
FONTE_NORMAL = ("Arial", 12)
FONTE_BOTAO = ("Arial", 12, "bold")
FONTE_NOTA = ("Arial", 10, "italic")
FONTE_CATEGORIA = ("Arial", 10, "bold")

# Janela
TAMANHO_JANELA = "480x620"
TAMANHO_MINIMO = (480, 620)

# ==================================================
# CLASSE PRINCIPAL
# ==================================================

class CalculadoraFluidos:

    def __init__(self, root):

        self.root = root

        self.root.title("Mecânica dos Fluidos")
        self.root.geometry(TAMANHO_JANELA)
        self.root.minsize(*TAMANHO_MINIMO)
        self.root.configure(bg=COR_FUNDO)
        self.configurar_estilo()
        self.tela_inicial()

    # ==================================================
    # ESTILO
    # ==================================================

    def configurar_estilo(self):

        estilo = ttk.Style()
        estilo.theme_use("clam")

        # Campos de texto
        estilo.configure(
            "TEntry",
            font=FONTE_NORMAL,
            padding=6,
            fieldbackground=COR_BRANCO,
            foreground=COR_TEXTO,
            bordercolor=COR_BORDA,
            lightcolor=COR_BORDA,
            darkcolor=COR_BORDA
        )

        estilo.map(
            "TEntry",
            bordercolor=[("focus", COR_PRINCIPAL)],
            lightcolor=[("focus", COR_PRINCIPAL)],
            darkcolor=[("focus", COR_PRINCIPAL)]
        )

        # Lista de operações
        estilo.configure(
            "TCombobox",
            font=FONTE_NORMAL,
            padding=6,
            fieldbackground=COR_BRANCO,
            background=COR_SECUNDARIA,
            foreground=COR_TEXTO,
            arrowcolor=COR_PRINCIPAL,
            bordercolor=COR_BORDA,
            lightcolor=COR_BORDA,
            darkcolor=COR_BORDA
        )

        estilo.map(
            "TCombobox",
            fieldbackground=[("readonly", COR_BRANCO)],
            foreground=[("readonly", COR_TEXTO)],
            bordercolor=[("focus", COR_PRINCIPAL)]
        )

        # Lista suspensa do combobox
        self.root.option_add("*TCombobox*Listbox.font", FONTE_NORMAL)
        self.root.option_add("*TCombobox*Listbox.selectBackground", COR_PRINCIPAL)
        self.root.option_add("*TCombobox*Listbox.selectForeground", COR_BRANCO)

    # ==================================================
    # COMPONENTES REUTILIZÁVEIS
    # ==================================================

    def criar_cabecalho(self, pai, subtitulo=None):

        faixa = tk.Frame(pai, bg=COR_PRINCIPAL)
        faixa.pack(fill="x")

        tk.Label(
            faixa,
            text="CALCULADORA DE MECÂNICA DOS FLUIDOS",
            font=FONTE_TITULO,
            bg=COR_PRINCIPAL,
            fg=COR_BRANCO
        ).pack(pady=(22, 4 if subtitulo else 22))

        if subtitulo:
            tk.Label(
                faixa,
                text=subtitulo,
                font=FONTE_SUBTITULO,
                bg=COR_PRINCIPAL,
                fg=COR_SECUNDARIA
            ).pack(pady=(0, 18))

    def criar_janela(self, titulo):

        janela = tk.Toplevel(self.root)

        janela.title(titulo)
        janela.geometry(TAMANHO_JANELA)
        janela.minsize(*TAMANHO_MINIMO)
        janela.configure(bg=COR_FUNDO)

        self.criar_cabecalho(janela, titulo)

        return janela

    def criar_botao(self, pai, texto, comando, cor=COR_PRINCIPAL):

        principal = cor == COR_PRINCIPAL
        cor_hover = COR_PRINCIPAL_HOVER if principal else COR_SECUNDARIA_HOVER
        cor_texto = COR_BRANCO if principal else COR_TEXTO

        botao = tk.Button(
            pai,
            text=texto,
            font=FONTE_BOTAO,
            bg=cor,
            fg=cor_texto,
            activebackground=cor_hover,
            activeforeground=cor_texto,
            relief="flat",
            bd=0,
            pady=8,
            width=22,
            command=comando,
            cursor="hand2"
        )
  
        botao.bind("<Enter>", lambda e: botao.config(bg=cor_hover))
        botao.bind("<Leave>", lambda e: botao.config(bg=cor))

        return botao

    def criar_menu(self, pai, titulo, apoio, botoes, voltar=None):

        tk.Label(
            pai,
            text=titulo,
            font=("Arial", 13),
            bg=COR_FUNDO,
            fg=COR_TEXTO
        ).pack(pady=(30, 5))

        tk.Label(
            pai,
            text=apoio,
            font=FONTE_SUBTITULO,
            bg=COR_FUNDO,
            fg=COR_TEXTO_SUAVE
        ).pack()

        frame_botoes = tk.Frame(pai, bg=COR_FUNDO)
        frame_botoes.pack(pady=25)

        for texto, comando in botoes:
            self.criar_botao(frame_botoes, texto, comando).pack(pady=12)

        if voltar:
            self.criar_botao(
                frame_botoes,
                "VOLTAR",
                voltar,
                COR_SECUNDARIA
            ).pack(pady=(24, 12))

    def criar_area_rolavel(self, pai):

        moldura = tk.Frame(pai, bg=COR_FUNDO)
        moldura.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            moldura,
            bg=COR_BRANCO,
            highlightthickness=1,
            highlightbackground=COR_BORDA
        )

        barra = ttk.Scrollbar(moldura, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=barra.set)

        barra.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        interno = tk.Frame(canvas, bg=COR_BRANCO)
        janela_interna = canvas.create_window((0, 0), window=interno, anchor="nw")

        # Ajusta a área rolável ao conteúdo e a largura ao canvas
        interno.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfigure(janela_interna, width=e.width)
        )

        # Roda do mouse (Windows/macOS e Linux)
        def rolar(evento):

            if not canvas.winfo_exists():
                return

            if evento.num == 4 or evento.delta > 0:
                canvas.yview_scroll(-1, "units")
            else:
                canvas.yview_scroll(1, "units")

        topo = pai.winfo_toplevel()
        topo.bind("<MouseWheel>", rolar)
        topo.bind("<Button-4>", rolar)
        topo.bind("<Button-5>", rolar)

        return interno

    # ==================================================
    # TELA INICIAL
    # ==================================================

    def tela_inicial(self):

        self.criar_cabecalho(self.root, "Cálculos e simulações para escoamentos")

        self.criar_menu(
            self.root,
            "Bem-vindo ao sistema!",
            "Escolha uma das áreas abaixo para começar.",
            [
                ("BÁSICOS", self.abrir_basicos),
                ("BOMBAS", self.abrir_bombas),
                ("SIMULAÇÃO", self.abrir_simulacao),
            ]
        )

    # ==================================================
    # SEÇÃO BÁSICOS
    # ==================================================

    def abrir_basicos(self):

        janela = self.criar_janela("Cálculos Básicos")

        # MENU

        frame_menu = tk.Frame(janela, bg=COR_FUNDO)
        frame_menu.pack(pady=(18, 5))

        tk.Label(
            frame_menu,
            text="Selecione a operação:",
            font=FONTE_NORMAL,
            bg=COR_FUNDO,
            fg=COR_TEXTO
        ).pack()

        selecao = ttk.Combobox(
            frame_menu,
            values=list(OPERACOES),
            state="readonly",
            width=35,
            font=FONTE_NORMAL
        )

        selecao.pack(pady=8)
        selecao.current(0)

        # CAMPOS

        frame_campos = tk.Frame(janela, bg=COR_FUNDO)
        frame_campos.pack(pady=5)

        campos = {}

        # RESULTADO

        frame_resultado = tk.LabelFrame(
            janela,
            text=" Resultado da operação ",
            font=FONTE_NORMAL,
            bg=COR_BRANCO,
            fg=COR_PRINCIPAL,
            bd=1,
            relief="solid",
            highlightthickness=0,
            padx=15,
            pady=12
        )

        frame_resultado.pack(fill="x", padx=40, pady=12)

        resultado = tk.Label(
            frame_resultado,
            text="Aguardando cálculo...",
            font=FONTE_NORMAL,
            bg=COR_BRANCO,
            fg=COR_TEXTO,
            justify="left",
            anchor="nw",
            height=7 
        )

        resultado.pack(fill="x")

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
                bg=COR_FUNDO,
                fg=COR_TEXTO
            ).pack(anchor="w", pady=(7, 2))

            entrada = ttk.Entry(frame_campos, width=40, font=FONTE_NORMAL)
            entrada.pack(pady=2)

            campos[nome] = entrada

        # ------------------------------------------
        # MOSTRAR CAMPOS (vindos de calculos.OPERACOES)
        # ------------------------------------------

        def mostrar_campos(event=None):

            limpar_campos()

            for nome, texto in OPERACOES[selecao.get()]["campos"]:
                criar_campo(nome, texto)

            resultado.config(text="Aguardando cálculo...")

        selecao.bind("<<ComboboxSelected>>", mostrar_campos)

        # ------------------------------------------
        # CALCULAR
        # ------------------------------------------

        def ler_valor(entrada):

            try:
                return float(entrada.get().replace(",", "."))

            except ValueError:
                raise ValueError("Digite valores numéricos válidos.")

        def calcular():

            try:
                valores = {
                    nome: ler_valor(entrada)
                    for nome, entrada in campos.items()
                }

                resultado.config(
                    text=executar_operacao(selecao.get(), valores)
                )

            except ValueError as erro:

                messagebox.showerror(
                    "Erro de entrada",
                    str(erro),
                    parent=janela
                )

        def limpar():

            for entrada in campos.values():
                entrada.delete(0, tk.END)

            resultado.config(text="Aguardando cálculo...")

        # ------------------------------------------
        # BOTÕES
        # ------------------------------------------

        self.criar_botao(janela, "CALCULAR", calcular).pack(pady=(8, 8))

        self.criar_botao(
            janela,
            "LIMPAR CAMPOS",
            limpar,
            COR_SECUNDARIA
        ).pack(pady=(0, 15))

        # Enter também calcula
        janela.bind("<Return>", lambda e: calcular())

        mostrar_campos()

    # ==================================================
    # SEÇÃO BOMBAS
    # ==================================================


    def abrir_bombas(self):

        janela = self.criar_janela("Cálculos de Bombas")

        

    # ==================================================
    # SEÇÃO SIMULAÇÃO
    # ==================================================

    def abrir_simulacao(self):

        janela = self.criar_janela("Simulação")

        conteudo = tk.Frame(janela, bg=COR_FUNDO)
        conteudo.pack(fill="both", expand=True, padx=30, pady=(15, 15))

# ==================================================
# INICIALIZAÇÃO DO PROGRAMA
# ==================================================

if __name__ == "__main__":

    root = tk.Tk()
    app = CalculadoraFluidos(root)
    root.mainloop()