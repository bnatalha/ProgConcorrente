# %%
import matplotlib.pyplot as plt
from numpy import sqrt 

_VALORES = 1
_MEDIA = 2
_DP = 3
_MIN = 4
_MAX = 5

dimensoes = ["4", "8", "16", "32", "64", "128", "256", "1024", "2048"]

get_file_name = lambda modo, dim : f'out/metrics/{modo}{dim}_times.txt'

resultados = {}

def desvioPadrao(r):
    somatorio = sum([(tempo - r[_MEDIA]) ** 2 for tempo in r[_VALORES]]) 
    dp = sqrt((1/20) * (somatorio))
    return dp

def lerResultados():
    for modo in ['C','S']:    
        resultados[modo]={}
        for dim in dimensoes:
            nomeArquivo = get_file_name(modo,dim)
            resultados[modo][dim] = {}
            with open(nomeArquivo, "r") as arquivo:
                tempos = []
                arquivo.readline()
                for linha in arquivo:
                    linha = linha.strip()  
                    tempos.append(linha)
                resultados[modo][dim][_VALORES] = list(map(float, tempos))
                resultados[modo][dim][_MEDIA] = sum(resultados[modo][dim][_VALORES])/len(resultados[modo][dim][_VALORES])
                resultados[modo][dim][_DP] = desvioPadrao(resultados[modo][dim])
                resultados[modo][dim][_MAX] = max(resultados[modo][dim][_VALORES])
                resultados[modo][dim][_MIN] = min(resultados[modo][dim][_VALORES])
                
                
lerResultados()

print(resultados['C']['128'])



    

# print("Algoritmo concorrente 4x4")

# print("Resultados : ", int_concorrente)

# print("maior tempo: ", max(int_concorrente))

# print("menor tempo: ", min(int_concorrente))

# print("Tempo medio: %.4f" % media_times_c)

# print("Desvio padrao: ", desvio_padrao_c)

# print("")

# print("Algoritmo sequencial 4x4")

# print("Resultados : ", int_sequencial)

# print("maior tempo: ", max(int_sequencial))

# print("menor tempo: ", min(int_sequencial))

# print("Tempo medio: %.4f" % media_times_s)

# #print("Desvio padrao: ", desvio_padrao_s)

# #grafico 

# grupos = ['Sequencial', 'Concorrente']
# valores = [media_times_s, media_times_c]
# plt.bar(grupos, valores)
# plt.show()

# %%