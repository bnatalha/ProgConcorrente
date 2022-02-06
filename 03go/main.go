package main

import (
	"fmt"
	"math/rand"
	"time"
)

// estrutura para guardar as informações de um corredor
type corredor struct {
	duracao time.Duration
	id      int
	time    int
}

const MAX_CORREDORES = 4

func run(id_corredor, id_time int, raia chan corredor, chegada chan int) {
	// tempo percorrido
	seed := rand.NewSource(time.Now().UnixNano())
	random := rand.New(seed)
	duracao := time.Second * time.Duration(random.Intn(5))
	// duracao := time.Millisecond * time.Duration(random.Intn(100))

	time.Sleep(duracao)
	fmt.Print("Corredor ", id_corredor, " do time ", id_time, " correu por ", duracao)

	raia <- corredor{duracao: duracao, id: id_corredor, time: id_time}

	// fecha a pista para a equipe após o último corredor terminar de correr
	if MAX_CORREDORES == id_corredor {
		close(raia)
		chegada <- id_time // notifica o canal da linha de chegada
		return
	} else {
		go run(id_corredor+1, id_time, raia, chegada) // lança o próximo corredor
	}
}

func main() {

	// cada canal receberá as informações de uma equipe
	raia1 := make(chan corredor)
	raia2 := make(chan corredor)
	chegada := make(chan int) // canal responsável por notificar se todas as esquipes cruzaram a chegada

	go func() {
		run(1, 1, raia1, chegada)
	}()
	go func() {
		run(1, 2, raia2, chegada)
	}()

	tempo1 := time.Duration(0)
	tempo2 := time.Duration(0)
	menorTempo := time.Duration(0)
	remainingTeams := 2
	for remainingTeams > 0 {
		select {
		case c, ok := <-raia1:
			if ok {
				tempo1 = tempo1 + c.duracao
				fmt.Println("\tTEMPO TOTAL:", tempo1)
			}
		case c, ok := <-raia2:
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

	// calculando equipe que correu mais rápido
	menorTempo = tempo1
	vencedor := 1
	if tempo1 > tempo2 {
		menorTempo = tempo2
		vencedor = 2
	}

	fmt.Println("\nEquipe", vencedor, "venceu com", menorTempo)
}
