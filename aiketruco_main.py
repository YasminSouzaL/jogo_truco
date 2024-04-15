from ast import literal_eval as eval_input
from truco_game import Match, Player, Pair, Hand, Card, Game,Match # Importando as classes Match, Player, Pair, Hand, Card e Game do truco_game
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
            card_input = input("\nEscolha o número correspondente à carta que deseja jogar: ")

            try:
                card = int(card_input)
                if 1 <= card <= len(indexes):
                    player.throw_card(match=match, card_position=card)
                    break
                else:
                    print("Erro: Número fora da faixa válida. Por favor, tente novamente.")
            except ValueError:
                print("Erro: Entrada inválida. Por favor, digite um número inteiro.")

        players = [player1, player2, player3, player4]
        for player in players:
            player.hand = None
        
    # Print the winner of the match
        print("\n" + match.winner.player_name + " venceu a rodada!\n")
        print("Placar: " + str(game.score[Pair.PAIR_ONE_ID]) + " x " + str(game.score[Pair.PAIR_TWO_ID]) + "\n")


if __name__ == '__main__':
    print("\t\nAIKE TRUCO\n")
    print("\n \t\t O jogo comecou! \n")
    
    continue_game = True
    game = TestGame()  # Instanciando a classe Game do truco_test

    # Adicione cartas à mão do jogador antes de iniciar o jogo
    hand1 = Hand([Card('4', 'Copas'), Card('5', 'Espadas'), Card('6', 'Ouros')])
    hand2 = Hand([Card('7', 'Copas'), Card('8', 'Espadas'), Card('9', 'Ouros')])
    hand3 = Hand([Card('10', 'Copas'), Card('J', 'Espadas'), Card('Q', 'Ouros')])
    hand4 = Hand([Card('K', 'Copas'), Card('A', 'Espadas'), Card('2', 'Ouros')])

    # Criando instâncias de jogadores com mãos associadas
    player1 = Player("Emilie", hand1)
    player2 = Player("Italo", hand2)
    player3 = Player("Attany", hand3)
    player4 = Player("Keli", hand4)

    while continue_game:
        match = game.current_match
        match = Match(game)  # Inicialize a instância de Match aqui
        play_player(player1, match)
        play_player(player2, match)
        play_player(player3, match)
        play_player(player4, match)

        end_game = game.score[Pair.PAIR_ONE_ID] >= 12 or game.score[Pair.PAIR_TWO_ID] >= 12

        if end_game:
            continue_game = False

    print("\t\t Fim do jogo!\n")
