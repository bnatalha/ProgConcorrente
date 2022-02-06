package main

import (
	"fmt"
	"math/rand"
	"sort"
	"time"
)

// estrutura para guardar as informações de um Corredor
type Corredor struct {
	tempo       time.Duration
	tempo_total time.Duration
	id          int
	time        int
}

type PorTempo []Corredor

func (a PorTempo) Len() int           { return len(a) }
func (a PorTempo) Less(i, j int) bool { return a[i].tempo_total < a[j].tempo_total }
func (a PorTempo) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }

const MAX_CORREDORES = 4 // total de corredores por time
const MAX_EQUIPES = 4    // total de times

func correr(id_corredor, id_equipe int, raia, chegada chan Corredor) {
	// espera o bastão chegar para começar a correr
	ultimo_corredor := <-raia

	// calcular tempo que será gasto na corrida
	seed := rand.NewSource(time.Now().UnixNano())
	random := rand.New(seed)
	tempo := time.Millisecond * time.Duration(random.Intn(100))

	// corre
	time.Sleep(tempo)

	tempo_total := tempo + ultimo_corredor.tempo_total
	corredor_atual := Corredor{tempo: tempo, id: id_corredor, time: id_equipe, tempo_total: tempo_total}
	fmt.Println("Corredor", id_corredor, "da equipe", id_equipe, "correu por", tempo, "\t TEMPO:", tempo_total)

	// fecha a pista para a equipe após o último corredor terminar de correr
	// ou manda o próximo corredor
	if MAX_CORREDORES == id_corredor {
		close(raia)
		chegada <- corredor_atual // notifica o canal da linha de chegada
		return
	} else {
		go correr(id_corredor+1, id_equipe, raia, chegada) // posiciona o próximo corredor
		raia <- corredor_atual                             // passa o bastão
	}
}

// simular a largada, deixando o bastão pronto para o primeiro
// corredor possa pegá-lo e começar a correr
func prepararBastao(raia chan Corredor) {
	raia <- Corredor{tempo_total: 0, tempo: 0}
}

func main() {

	// cada canal será uma raia para os corredores de uma equipe
	var raias [MAX_EQUIPES]chan Corredor
	for i := 0; i < MAX_EQUIPES; i++ {
		raias[i] = make(chan Corredor)
	}

	// canal responsável por notificar a chegada das equipes
	chegada := make(chan Corredor)

	// preparando os batões para que as equipes	possam largar
	for i := 0; i < MAX_EQUIPES; i++ {
		go prepararBastao(raias[i])
	}

	// ====================== LARGADA ==========================

	for i := 0; i < MAX_EQUIPES; i++ {
		go correr(1, i, raias[i], chegada)
	}

	var stats_finais []Corredor
	remainingTeams := MAX_EQUIPES
	for remainingTeams > 0 {
		t := <-chegada
		stats_finais = append(stats_finais, t)
		fmt.Println("Equipe", t.time, "\t==================CHEGADA==================\t", t.tempo_total)
		remainingTeams = remainingTeams - 1
	}

	// ====================== CHEGADA ==========================

	// ordena tempos e equipes
	sort.Sort(PorTempo(stats_finais))

	// imprime os resultados finais
	fmt.Print("\nEquipe ", stats_finais[0].time, ": ", stats_finais[0].tempo_total, "\tEQUIPE VENCEDORA")
	for i := 1; i < MAX_EQUIPES; i++ {
		fmt.Print("\nEquipe ", stats_finais[i].time, ": ", stats_finais[i].tempo_total)
	}
	fmt.Println()

}
