# Atividade 3 - Corrida de Revezamento

Progama em Go que simula uma corrida de revezamento com equipes. Por padrão, a corrida tem 4 equipes de 4 corredores, podendo ser modificado via linha de comando.

## Compilando sem condição de corrida

Go fornece a capacidade de compilar um programa e identificar onde pode existir uma condição de corrida através da flag `-race`. Desta maneira, compilaremos o programa executando o comando:

```
go build -race main.go
```

## Como executar

Para executar o binário compilado no passo anterior, execute o comando:
```
./main
```
É possível modificar a quantidade de equipes e/ou de corredores por equipe. Para isso:
```
./main E C
```
onde:
- `E` é um número natural > 0 e será o novo número de __equipes__ disputando a corrida;
- `C` é um número natural > 0 e será o novo número de __corredores por equipe__ disputando a corrida;