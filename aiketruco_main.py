from ast import literal_eval as eval_input
from truco_game import Player, Pair, Hand
from truco_regras import TestGame  # Importando a classe Game do truco_test

def play_player(player, match):
    while True:
        print("\nVez de " + player.player_name + "\n")

        if player.hand is None:
            print("Erro: Mão do jogador não está inicializada.")
            return  # Exit the function if there's no hand

        indexes = []
        for index, card in enumerate(player.hand.cards):
            indexes.append(index + 1)
            print(str(index + 1) + " - " + str(card))

        while True:
            card = input("\nEscolha o número correspondente à carta que deseja jogar: ")

            try:
                card = int(card)
                if 0 < card <= len(indexes):
                    player.throw_card(match=match, card_position=card)
                    break
                else:
                    print("Erro: Número fora da faixa válida. Por favor, tente novamente.")
            except ValueError:
                print("Erro: Entrada inválida. Por favor, digite um número.")


if __name__ == '__main__':
    print("\t\nAIKE TRUCO\n")
    print("\n \t\t O jogo comecou! \n")
    
    continue_game = True
    game = TestGame()  # Instanciando a classe Game do truco_test

    # Criando instâncias de mãos para os jogadores
    hand1 = Hand([])
    hand2 = Hand([])
    hand3 = Hand([])
    hand4 = Hand([])

    # Criando instâncias de jogadores com mãos associadas
    player1 = Player("Emilie", hand1)
    player2 = Player("Italo", hand2)
    player3 = Player("Attany", hand3)
    player4 = Player("Keli", hand4)
         
    while continue_game:
        match = game.current_match
        play_player(player1, match)
        play_player(player2, match)
        play_player(player3, match)
        play_player(player4, match)

        end_game = game.score[Pair.PAIR_ONE_ID] >= 12 or game.score[Pair.PAIR_TWO_ID] >= 12

        if end_game:
            continue_game = False

    print("\t\t Fim do jogo!\n")
