from ast import literal_eval as eval_input
from truco_game import Card, Deck, Hand, CardCheck, Player, Pair, Game, Match, Round, MatchState, NormalMatch, TrucoMatch, SixMatch, NineMatch, TwelveMatch
from truco_regras import Game, TestGame  # Importando a classe Game do truco_test

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
    while continue_game:
        match = game.current_match
        
        for _ in range(3):  # Cada jogador joga três cartas por rodada
            play_player(Player, match)
            
        end_game = game.score[Pair.PAIR_ONE_ID] >= 12 or game.score[Pair.PAIR_TWO_ID] >= 12
        if end_game:
            continue_game = False

    print("\t\t Fim do jogo!\n")
