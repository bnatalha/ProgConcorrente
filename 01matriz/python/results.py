# %%
import matplotlib.pyplot as plt
from numpy import sqrt 

dimensoes = ["4", "8", "16", "32", "64", "128", "256", "1024", "2048"]

arquivo = open('metrics/C4_times.txt', "r")
concorrente = []
for linha in arquivo:
    linha = linha.strip()  
    concorrente.append((linha))
concorrente.pop(0)
arquivo.close()


arquivo = open('metrics/S4_times.txt', "r")
sequencial = []
for linha in arquivo:
    linha = linha.strip()  
    sequencial.append((linha))
sequencial.pop(0)
arquivo.close()


int_concorrente = list(map(float, concorrente))
int_sequencial = list(map(float, sequencial))

media_times_c = sum(int_concorrente)/len(int_concorrente)
media_times_s = sum(int_sequencial)/len(int_sequencial)

somatorio = 0.0

for tempo in int_concorrente:
    variante = (tempo - media_times_c) ** 2
    #print("variante: ", variante)
    
    somatorio += variante
    
desvio_padrao_c = sqrt((1/20) * (somatorio))

#for tempo in int_concorrente:
    #variante = (tempo - media_times_s) ** 2
    #somatorio += variante

#desvio_padrao_s = sqrt((1/20) * (somatorio))

    

print("Algoritmo concorrente 4x4")

print("Resultados : ", int_concorrente)

print("maior tempo: ", max(int_concorrente))

print("menor tempo: ", min(int_concorrente))

print("Tempo medio: %.4f" % media_times_c)

print("Desvio padrao: ", desvio_padrao_c)

print("")

print("Algoritmo sequencial 4x4")

print("Resultados : ", int_sequencial)

print("maior tempo: ", max(int_sequencial))

print("menor tempo: ", min(int_sequencial))

print("Tempo medio: %.4f" % media_times_s)

#print("Desvio padrao: ", desvio_padrao_s)

#grafico 

grupos = ['Sequencial', 'Concorrente']
valores = [media_times_s, media_times_c]
plt.bar(grupos, valores)
plt.show()

# %%