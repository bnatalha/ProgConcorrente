package main

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

type corredor struct {
	duracao time.Duration
	id      int
	time    int
}

var groupCorrida sync.WaitGroup

const CORREDORES = 4

func run(id_corredor, id_time int, pista chan corredor, chegada chan int) {
	// tempo percorrido
	seed := rand.NewSource(time.Now().UnixNano())
	random := rand.New(seed)
	duracao := time.Second * time.Duration(random.Intn(5))
	// duracao := time.Millisecond * time.Duration(random.Intn(100))

	time.Sleep(duracao)
	fmt.Print("Corredor ", id_corredor, " do time ", id_time, " correu por ", duracao)

	pista <- corredor{duracao: duracao, id: id_corredor, time: id_time}

	if CORREDORES == id_corredor {
		close(pista)
		chegada <- id_time
		return
	} else {
		go run(id_corredor+1, id_time, pista, chegada)
	}
}

func main() {
	pista1 := make(chan corredor)
	pista2 := make(chan corredor)
	chegada := make(chan int)

	go func() {
		run(1, 1, pista1, chegada)
	}()
	go func() {
		run(1, 2, pista2, chegada)
	}()

	tempo1 := time.Duration(0)
	tempo2 := time.Duration(0)
	menorTempo := time.Duration(0)
	remainingTeams := 2
	for remainingTeams > 0 {
		select {
		case c, ok := <-pista1:
			if ok {
				tempo1 = tempo1 + c.duracao
				fmt.Println("\tTEMPO TOTAL:", tempo1)
			}
		case c, ok := <-pista2:
			if ok {
				tempo2 = tempo2 + c.duracao
				fmt.Println("\tTEMPO TOTAL:", tempo2)
			}
		case t := <-chegada:
			tempo := time.Duration(0)
			if t == 1 {
				tempo = tempo1
			} else {
				tempo = tempo2
			}
			fmt.Println("Tempo final do time", t, tempo)
			remainingTeams = remainingTeams - 1
		}

	}

	menorTempo = tempo1
	vencedor := 1
	if tempo1 > tempo2 {
		menorTempo = tempo2
		vencedor = 2
	}

	fmt.Println("\nEquipe", vencedor, "venceu com", menorTempo)
	// fmt.Println("Tempo final percorrido 1:", tempo1)
	// fmt.Println("Tempo final percorrido 2:", tempo2)
}
