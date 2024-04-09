from ast import literal_eval as eval_input
from truco_game import  Player, Pair
from truco_regras import TestGame  # Importando a classe Game do truco_test

def play_player(player, match):
    while True:
        print("\nVez de " + player.player_name + "\n")

        indexes = []
        for index, card in enumerate(player.hand.cards):
            indexes.append(index + 1)
            print(str(index + 1) + " - " + str(card))
        
        card = input("\nEscolha o número correspondente à carta que deseja jogar: ")
        
        try:
            card = int(card)
            if 0 < card <= len(indexes):
                player.throw_card(match=match, card_position=card)
                break
            else:
                print("Entrada inválida.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

if __name__ == '__main__':
    print("\t\nAIKE TRUCO\n")
    print("\n \t\t O jogo comecou! \n")
    
    continue_game = True
    game = TestGame()  # Instanciando a classe Game do truco_test

    # Criando instâncias de jogadores
    player1 = Player("Emilie")
    player2 = Player("Italo")
    player3 = Player("Attany")
    player4 = Player("Keli")

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
