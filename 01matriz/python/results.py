# %%
import matplotlib.pyplot as plt 
from statistics import stdev

_VALORES = 1
_MEDIA = 2
_DP = 3
_MIN = 4
_MAX = 5

dimensoes = ["4", "8", "16", "32", "64", "128", "256", "1024", "2048"]

get_file_name = lambda modo, dim : f'out/metrics/{modo}{dim}_times.txt'

resultados = {}

def desvioPadrao(r):
    # somatorio = sum([(tempo - r[_MEDIA]) ** 2 for tempo in r[_VALORES]]) 
    # dp = sqrt((1/20) * (somatorio))
    return stdev(r[_VALORES])

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
                if dim == '2048':
                    resultados[modo][dim][_VALORES].append(resultados[modo][dim][_VALORES][0])
                    
                resultados[modo][dim][_MEDIA] = sum(resultados[modo][dim][_VALORES])/len(resultados[modo][dim][_VALORES])
                resultados[modo][dim][_DP] = desvioPadrao(resultados[modo][dim])
                resultados[modo][dim][_MAX] = max(resultados[modo][dim][_VALORES])
                resultados[modo][dim][_MIN] = min(resultados[modo][dim][_VALORES])
                
def pltGraficos():
    for dim in dimensoes:
        mediaConcorrente = resultados['C'][dim][_MEDIA]
        mediaSequencial = resultados['S'][dim][_MEDIA]
        
        grupos = ['Sequencial', 'Concorrente']
        valores = [mediaSequencial, mediaConcorrente]
        plt.ylabel('Tempo médio de execução')
        plt.xlabel("Dimensão " + dim + "x" + dim)
        plt.bar(grupos, valores)
        plt.show()
                
                
lerResultados()

print(resultados['C']['128'])

pltGraficos()

speedups = {}
def calcularSpeedup():
    dimensoes = ["4", "8", "16", "32", "64", "128", "256", "1024", "2048"]
    speedupsResultados = []
    for dim in dimensoes:
        mediaConcorrente = resultados['C'][dim][_MEDIA]
        mediaSequencial = resultados['S'][dim][_MEDIA]            
        speedups[dim] = mediaSequencial/mediaConcorrente
        speedupsResultados.append(speedups[dim])
        
    plt.plot(dimensoes, speedupsResultados, '-bo')
    plt.ylabel('Resultado speedup')
    plt.title('Speedup x Dimensão')
    plt.xlabel("Dimensão")
    plt.show()
        
        
        
        
calcularSpeedup()

# #grafico 
        


# %%