package main

import (
	"fmt"
	"math/rand"
	"os"
	"sort"
	"strconv"
	"time"
)

var MAX_CORREDORES = 4 // total de corredores por time
var MAX_EQUIPES = 4    // total de times

// estrutura para guardar as informações de um corredor ao
// longo da corrida
type Corredor struct {
	tempo                  time.Duration
	tempo_acumulado_equipe time.Duration
	id                     int
	equipe                 int
}

// estrutura para ordenar os dados dos corredores pelo tempo total
type PorTempo []Corredor

func (a PorTempo) Len() int { return len(a) }
func (a PorTempo) Less(i, j int) bool {
	return a[i].tempo_acumulado_equipe < a[j].tempo_acumulado_equipe
}
func (a PorTempo) Swap(i, j int) { a[i], a[j] = a[j], a[i] }

// seta a quantidade de corredores e equipes caso o usuário
// tenha passado mais argumentos na hora da execução do programa
func prepararEquipes(args []string) {
	if len(args) > 0 {
		equipes, err := strconv.Atoi(args[0])
		if err == nil && equipes > 0 {
			fmt.Printf("equipes=%d\n", equipes)
			MAX_EQUIPES = equipes
		}
		if len(args) > 1 {
			corredores, err := strconv.Atoi(args[1])
			if err == nil && corredores > 0 {
				fmt.Printf("corredores=%d\n", corredores)
				MAX_CORREDORES = corredores
			}
		}
	}
}

// função que simula as ações do corredor;
// espera e recebe o bastão, corre e passa o bastão a diante caso a equipe ainda
// não tenha lançado todos os corredores
func correr(id_corredor, id_equipe int, raia, chegada chan Corredor) {
	// espera o bastão chegar para começar a correr
	ultimo_corredor := <-raia

	// calcular tempo que será gasto na corrida
	seed := rand.NewSource(time.Now().UnixNano())
	random := rand.New(seed)
	tempo := time.Millisecond * time.Duration(random.Intn(100))

	// corre
	time.Sleep(tempo)

	tempo_total := tempo + ultimo_corredor.tempo_acumulado_equipe
	corredor_atual := Corredor{
		tempo:                  tempo,
		id:                     id_corredor,
		equipe:                 id_equipe,
		tempo_acumulado_equipe: tempo_total}
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

// simular a largada, deixando o bastão pronto para que o primeiro
// corredor possa pegá-lo e começar a correr
func prepararBastao(raia chan Corredor) {
	raia <- Corredor{tempo_acumulado_equipe: 0, tempo: 0}
}

func main() {
	argsSemPrograma := os.Args[1:]
	prepararEquipes(argsSemPrograma)

	// cada canal será uma raia para os corredores de uma equipe
	var raias []chan Corredor
	for i := 0; i < MAX_EQUIPES; i++ {
		raias = append(raias, make(chan Corredor))
	}

	// canal responsável por notificar a chegada das equipes
	chegada := make(chan Corredor)

	// preparando os batões para que as equipes possam largar
	for i := 0; i < MAX_EQUIPES; i++ {
		go prepararBastao(raias[i])
	}

	// ====================== LARGADA ==========================
	fmt.Println("\t==================LARGADA==================\t")

	for i := 0; i < MAX_EQUIPES; i++ {
		go correr(1, i, raias[i], chegada)
	}

	var resultados []Corredor
	equipesRestantes := MAX_EQUIPES
	for equipesRestantes > 0 {
		corredor := <-chegada
		resultados = append(resultados, corredor)
		fmt.Println("\t==================CHEGADA==================\t", "Equipe", corredor.equipe, corredor.tempo_acumulado_equipe)
		equipesRestantes = equipesRestantes - 1
	}

	// ====================== CHEGADA ==========================

	// ordena tempos e equipes
	sort.Sort(PorTempo(resultados))

	// imprime os resultados finais
	fmt.Print("\nEquipe ", resultados[0].equipe, ": ", resultados[0].tempo_acumulado_equipe, "\tEQUIPE VENCEDORA")
	for i := 1; i < MAX_EQUIPES; i++ {
		fmt.Print("\nEquipe ", resultados[i].equipe, ": ", resultados[i].tempo_acumulado_equipe)
	}
	fmt.Println()

}
