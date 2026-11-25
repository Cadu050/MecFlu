def vazaofun():
    volume = float(input("informe o volume de seu fluido em m³ (somente valor numérico):  "))
    tempo= float(input("informe o tempo de vazão em minutos:  "))
    vazao = volume/tempo 
    print(f"sua vazão em {tempo} min é de {vazao} m³/s.")

def velocidadefun():
    tempoini= float(input("informe o tempo inicial em minutos: "))
    tempofin= float(input("informe o tempo final em minutos: "))
    vartempo = tempofin - tempoini

    posini = float(input("informe a posicição inicial do fluido em m/s: "))
    posifi= float(input("informe a posicição final do fluido m/s : "))
    

    varespaco = posifi - posini 

    velocidademedia = varespaco/vartempo
    print(f"sua variação de tempo é {vartempo} min, e sua variação de espaço é de {varespaco} m/s, e sua velocidade média é de {velocidademedia} m/s")

def perdadecargafun():
      fatrito = float(input("informe o falor de atrito de seu escoamento:  "))
      comprimento = float(input("informe o comprimento da tubulação:  "))
      diametro = float(input("informe o diametro interno do tubo:  "))
      velocidadecarga = float(input("informe a velocidade média do escoamento:  "))
      acdagravidade = 9.81
      perdadecarga = fatrito * (comprimento / diametro) * (velocidadecarga**2 / acdagravidade* 2)
      print(f"sua Perda de Carga Distribuída é de {perdadecarga} metros. ")

def reynoldsfun():
     densidade = float(input("informe a densidade do fluido:  "))
     velocidaderey = float(input("informe a velocidade média do fluido:  "))
     diametrorey = float(input("informe o diâmetro do tubo:  "))
     viscosidade = float(input("informe a viscosidade dinâmica do fluido:  "))
     reynolds = (densidade * velocidaderey * diametrorey) / viscosidade
     print(f"seu número de reynolds é de {reynolds} Re.")



def usuario():
    while True:

     opcoes = ["velocidade (0)", "vazao (1)", "perda de carga (2)", "reynolds (3)"]
     for opt in opcoes:
        print(opt)
    
     escolha = int(input("o que você deseja calcular? digite o número referente a cima:   "))
     if escolha == 0:
        velocidadefun()
        continue

     if escolha == 1:
        vazaofun()
        continue

     if escolha == 2 :
         perdadecargafun()
         continue

     if escolha == 3:
         reynoldsfun()
     else:
        print("valor invalido, digite outro valor.")
        continue
        
       
     return print("fim da operação!!")

usuario()
        

    
    