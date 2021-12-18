## TODO:

### Programa

- Decidir a linguagem: Python
- Algoritmos:
  - sequencial
  - concorrente
- Entrada:
  - leitura de arquivos de entrada
    - `Aixi.txt` ou `Bixi.txt`
- Saída:
  - Formato e produção dos arquivos de saída `Cixi.txt`
  - Testes
  - **clockar** os tempos e registrar em um arquivo de saída (.csv?)
    - barra de progresso?
- Parâmetros do executável:
  - `$ <programa> i S`  
    - i: inteiro potencia de 2
    - S | C : Sequencial on Conconrente
- Experimentação:
  - registrar tempo máximo, mínimo e médio dos tempos nas `20` e desvio padrão.
  - criar script para automatizaros testes;
  - rodar script;
  - Calcular o Speedup (T_seq / T_co)

---

### Relatório
- alimentar o relatório com os resultados obtidos;
#### Metodologia
Indicar o método adotado para realizar os experimentos com as soluções e analisar
os resultados obtidos. Por exemplo, deverá ser apresentada a caracterização técnica do compu-
tador utilizado (processador, sistema operacional, quantidade de memória RAM), a linguagem
de programação e a versão do compilador empregados, os cenários considerados, entre outras in-
formações. Deverão também ser descritos qual o procedimento adotado para gerar os resultados,
como a comparação entre as soluções foi feita, etc.
#### Resultados
Apresentar os resultados obtidos na forma de um gráficos de linha e tabelas. Para
cada solução deverá ser apresentada uma tabela contendo os tempos mínimo, médio e máximo
obtidos para cada dimensão de matriz, além dos valores de desvio padrão. Por sua vez, os gráficos
de linha deverão exibir apenas os tempos médios obtidos nas execuções de cada solução.
#### Conclusões
Discutir os resultados, ou seja, o que foi possível concluir através dos resultados ob-
tidos através dos experimentos, incluindo uma análise do ganho de desempenho (speed-up).
