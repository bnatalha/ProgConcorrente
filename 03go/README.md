# Atividade 3

Progama em Go que simula uma corrida de revezamento com 4 corredores.

### Compilando sem condição de corrida

O go fornece a capacidade de compilar um programa e identificar onde pode existir uma condição de corrida através da flag `-race`. Desta maneira, compilaremos o programa executando o comando:

```
go build -race main.go
```

### Como executar

Para executar o binário compilado no passo anterior, execute o comando
```
./main
```