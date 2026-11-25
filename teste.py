
import tkinter as tk
from tkinter import ttk, messagebox


# -----------------------------
# FUNÇÕES DE CÁLCULO
# -----------------------------

def calcular_vazao(volume, tempo):
    if tempo <= 0:
        raise ValueError("O tempo deve ser maior que zero.")

    vazao = volume / (tempo * 60)
    return vazao


def calcular_velocidade(tempo_ini, tempo_fin, pos_ini, pos_fin):
    vartempo = (tempo_fin - tempo_ini) * 60

    if vartempo <= 0:
        raise ValueError("O tempo final deve ser maior que o inicial.")

    varespaco = pos_fin - pos_ini
    velocidade = varespaco / vartempo

    return varespaco, vartempo, velocidade


def calcular_perda_carga(fatrito, comprimento, diametro, velocidade):
    if diametro <= 0:
        raise ValueError("O diâmetro deve ser maior que zero.")

    gravidade = 9.81

    perda = fatrito * (comprimento / diametro) * (
        velocidade**2 / (2 * gravidade)
    )

    return perda


def calcular_reynolds(densidade, velocidade, diametro, viscosidade):
    if viscosidade <= 0:
        raise ValueError("A viscosidade deve ser maior que zero.")

    reynolds = (densidade * velocidade * diametro) / viscosidade

    return reynolds


# -----------------------------
# INTERFACE GRÁFICA
# -----------------------------

def janela2():
     janela = tk.Tk()
     janela.title("Calculadora de Mecânica dos Fluidos")
     janela.geometry("550x620")
     janela.minsize(550, 620)
     janela.configure(bg="#EAF0F6")


     # Título
     titulo = tk.Label(
     janela,
     text="CALCULADORA DE MECÂNICA DOS FLUIDOS",
     font=("Arial", 15, "bold"),
     bg="#EAF0F6",
     fg="#17365D"
     )
     titulo.pack(pady=20)


     # Seleção da operação
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


     # Área dos campos
     frame_campos = tk.Frame(janela, bg="#EAF0F6")
     frame_campos.pack(pady=10)

     campos = {}    


     def limpar_campos():
        for widget in frame_campos.winfo_children():
            widget.destroy()

            campos.clear()


     def criar_campo(nome, texto):
         label = tk.Label(
            frame_campos,
            text=texto,
            font=("Arial", 10),
            bg="#EAF0F6"
    )
         label.pack(anchor="w", pady=(8, 2))

         entrada = ttk.Entry(frame_campos, width=40, font=("Arial", 11))
         entrada.pack(pady=2)

         campos[nome] = entrada


# Mostrar os campos de acordo com a operação
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


            selecao.bind("<<ComboboxSelected>>", mostrar_campos)




            def calcular():
                 try:
                    operacao = selecao.get()

                 def valor(nome):
                    return float(campos[nome].get().replace(",", "."))

                    if operacao == "Vazão":
                        volume = valor("volume")
                        tempo = valor("tempo")

                        resultado = calcular_vazao(volume, tempo)

                        mensagem = (
                        f"VAZÃO DO FLUIDO\n\n"
                        f"Volume: {volume} m³\n"
                        f"Tempo: {tempo} minutos\n\n"
                        f"Vazão: {resultado:.6f} m³/s"
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
                    f"Diâmetro: {D} m\n"
                    f"Velocidade: {v} m/s\n\n"
                    f"Perda de carga: {perda:.4f} m"
                )

            elif operacao == "Número de Reynolds":
                densidade = valor("densidade")
                velocidade = valor("velocidade")
                diametro = valor("diametro")
                viscosidade = valor("viscosidade")

                re = calcular_reynolds(
                    densidade, velocidade, diametro, viscosidade
                )

                if re < 2300:
                    regime = "Laminar"
                elif re < 4000:
                    regime = "Transição"
                else:
                    regime = "Turbulento"

                mensagem = (
                    f"NÚMERO DE REYNOLDS\n\n"
                    f"Número de Reynolds: {re:.2f}\n\n"
                    f"Regime de escoamento: {regime}"
                )

            resultado_label.config(text=mensagem)

            except ValueError as erro:
            messagebox.showerror(
            "Erro de entrada",
            str(erro) if str(erro) else "Digite valores numéricos válidos."
        )

            except Exception:
            messagebox.showerror(
            "Erro",
            "Verifique se todos os campos foram preenchidos corretamente."
        )


# Botão calcular
            botao = tk.Button(
                janela,
                text="CALCULAR",
                font=("Arial", 12, "bold"),
                bg="#17365D",
                fg="white",
                width=20,
                command=calcular,
                cursor="hand2"
            )
            botao.pack(pady=20)


# Área de resultados
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


# Botão limpar
def limpar():
    for entrada in campos.values():
        entrada.delete(0, tk.END)

    resultado_label.config(text="Aguardando cálculo...")


botao_limpar = tk.Button(
    janela,
    text="LIMPAR CAMPOS",
    font=("Arial", 10),
    bg="#AAB7C4",
    fg="black",
    width=20,
    command=limpar
)
botao_limpar.pack(pady=10)

def login ():
     janela1 = tk.Tk()
     janela1.title("Calculadora de Mecânica dos Fluidos")
     janela1.geometry("550x620")
     janela1.minsize(550, 620)
     janela1.configure(bg="#EAF0F6")


# Título
     titulo1 = tk.Label(
     janela1,
     text="CALCULADORA DE MECÂNICA DOS FLUIDOS",
     font=("Arial", 15, "bold"),
     bg="#EAF0F6",
     fg="#17365D"
)
     titulo1.pack(pady=20)


# Seleção da operação
frame_menu = tk.Frame(janela, bg="#EAF0F6")
frame_menu.pack(pady=10)

tk.Label(
    frame_menu,
    text="Selecione a operação:",
    font=("Arial", 11, "bold"),
    bg="#EAF0F6"
).pack()

# Inicializar
login()

janela.mainloop()
