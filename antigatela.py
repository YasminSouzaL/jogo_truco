import tkinter as tk
from truco_game import Match, Player, Pair, Hand, Card, Game, Match # Importando as classes Match, Player, Pair, Hand, Card e Game do truco_game
from truco_regras import TestGame, game  # Importando a classe Game do truco_test

'''Linha de janela de comando para rodar o programa:

TrucoJogador: python aiketruco_main.py
TrucoCartas: python aiketruco_main.py cartas
TrucoRodadas: python aiketruco_main.py rodadas
TrucoPlacar: python aiketruco_main.py placar

'''

class TrucoJogador:
    def __init__(self, master):
        self.master = master
        master.title("Truco Game")

        self.player_names = []
        self.players = []  # Lista para armazenar os jogadores

        self.label = tk.Label(master, text="Digite os nomes dos jogadores (mínimo 2):", font=("times", 15), fg="red")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.add_button = tk.Button(master, text="Adicionar Jogador", command=self.add_player)
        self.add_button.pack()

        self.remove_button = tk.Button(master, text="Remover Jogador", command=self.remove_player)
        self.remove_button.pack()

        self.label_players = tk.Label(master, text="Jogadores adicionados:", font=("times", 15), fg="red")
        self.label_players.pack()

        self.listbox_players = tk.Listbox(master)
        self.listbox_players.pack()

        self.start_button = tk.Button(master, text="Iniciar Jogo", command=self.start_game)
        self.start_button.pack()

    def add_player(self):
        player_name = self.entry.get()
        if player_name not in self.player_names:
            self.player_names.append(player_name)
            self.entry.delete(0, tk.END)
            self.listbox_players.insert(tk.END, player_name)  
            print(f"Jogador {player_name} adicionado")
        else:
            print(f"O jogador {player_name} já está na lista.")

    def remove_player(self):
        player_name = self.entry.get()
        if player_name in self.player_names:
            self.player_names.remove(player_name)
            self.entry.delete(0, tk.END)
            self.show_players()
            print(f"Jogador {player_name} removido")
        else:
            print(f"Jogador {player_name} não encontrado")

    def show_players(self):
        self.listbox_players.delete(0, tk.END)
        for player in self.player_names:
            self.listbox_players.insert(tk.END, player)

    def start_game(self):
        if len(self.player_names) >= 2:
            self.players = [Player(name, Hand([])) for name in self.player_names]  # Passa uma mão vazia para cada jogador
            game = TestGame()  # Instanciando a classe Game do truco_test
            self.play_game(game)
            self.master.destroy()
        else:
            print("É necessário adicionar pelo menos dois jogadores para iniciar o jogo.")


    def play_game(self, game):
        while True:
            match = game.current_match
            match = Match(game)  # Inicialize a instância de Match aqui
            for player in self.players:
                self.play_player(player, match)

            end_game = game.score[Pair.PAIR_ONE_ID] >= 12 or game.score[Pair.PAIR_TWO_ID] >= 12

            if end_game:
                break

        print("\t\t Fim do jogo!\n")
        print("Placar final: " + str(game.score[Pair.PAIR_ONE_ID]) + " x " + str(game.score[Pair.PAIR_TWO_ID]) + "\n")

    def play_player(self, player, match):
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
                if card_input.isdigit():
                    card_index = int(card_input) - 1  # Subtraia 1 porque os índices da lista começam em 0
                    if 0 <= card_index < len(player.hand.cards):
                        # O número está dentro do intervalo válido, saia do loop
                        break
                print("Erro: Número fora da faixa válida. Por favor, tente novamente.")

                players = self.players
            for player in players:
                player.hand = None

            print("\n" + match.winner.player_name + " venceu a rodada!\n")
            print("Placar: " + str(game.score[Pair.PAIR_ONE_ID]) + " x " + str(game.score[Pair.PAIR_TWO_ID]) + "\n")

class TrucoJogarCartas:
    def __init__(self, master, player_names):
        self.master = master
        master.title("Truco Game - Jogar Cartas")

        self.player_names = player_names
        self.players = []  # Lista para armazenar os jogadores

        self.label_cards = tk.Label(master, text="Cartas de cada jogador:", font=("times", 15), fg="red")
        self.label_cards.pack()

        self.listbox_players = tk.Listbox(master)
        self.listbox_players.pack()

        self.show_cards()

    def show_cards(self):
        self.listbox_players.delete(0, tk.END)
        for player_name in self.player_names:
            self.listbox_players.insert(tk.END, f"Cartas de {player_name}:")
            # Simulando cartas aleatórias para cada jogador
            cards = ["Carta 1", "Carta 2", "Carta 3"]
            for card in cards:
                self.listbox_players.insert(tk.END, card)


class TrucoCartas:
    def __init__(self, master, player_names):
        self.master = master
        master.title("Truco Game - Cartas")

        self.player_names = player_names
        self.players = []  # Lista para armazenar os jogadores

        self.label_cards = tk.Label(master, text="Cartas de cada jogador:", font=("times", 15), fg="red")
        self.label_cards.pack()

        self.listbox_players = tk.Listbox(master)
        self.listbox_players.pack()

        self.show_cards()

    def show_cards(self):
        self.listbox_players.delete(0, tk.END)
        for player_name in self.player_names:
            self.listbox_players.insert(tk.END, f"Cartas de {player_name}:")
            # Simulando cartas aleatórias para cada jogador
            cards = ["Carta 1", "Carta 2", "Carta 3"]
            for card in cards:
                self.listbox_players.insert(tk.END, card)

class TrucoRodadas:
    def __init__(self, master, player_names):
        self.master = master
        master.title("Truco Game - Rodadas")

        self.player_names = player_names
        self.players = []  # Lista para armazenar os jogadores

        self.label_rounds = tk.Label(master, text="Rodadas de cada jogador:", font=("times", 15), fg="red")
        self.label_rounds.pack()

        self.listbox_players = tk.Listbox(master)
        self.listbox_players.pack()

        self.show_rounds()

    def show_rounds(self):
        self.listbox_players.delete(0, tk.END)
        for player_name in self.player_names:
            self.listbox_players.insert(tk.END, f"Rodadas de {player_name}:")
            # Simulando rodadas aleatórias para cada jogador
            rounds = ["Rodada 1", "Rodada 2", "Rodada 3"]
            for round in rounds:
                self.listbox_players.insert(tk.END, round)


class TrucoPlacar:
    def __init__(self, master, score):
        self.master = master
        master.title("Truco Game - Placar")

        self.score = score

        self.label_score = tk.Label(master, text="Placar:", font=("times", 15), fg="red")
        self.label_score.pack()

        self.label_score = tk.Label(master, text=f"Placar: {score[Pair.PAIR_ONE_ID]} x {score[Pair.PAIR_TWO_ID]}", font=("times", 15), fg="red")
        self.label_score.pack()



'''Linha de janela de comando para rodar o programa:

TrucoJogador: python aiketruco_main.py
TrucoJogarCartas: python aiketruco_main.py cartas
TrucoCartas: python aiketruco_main.py cartas
TrucoRodadas: python aiketruco_main.py rodadas
TrucoPlacar: python aiketruco_main.py placar

'''

def main():
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "cartas":
            player_names = ["Jogador 1", "Jogador 2", "Jogador 3", "Jogador 4"]
            root = tk.Tk()
            my_gui = TrucoCartas(root, player_names)
            root.mainloop()
        elif sys.argv[1] == "rodadas":
            player_names = ["Jogador 1", "Jogador 2", "Jogador 3", "Jogador 4"]
            root = tk.Tk()
            my_gui = TrucoRodadas(root, player_names)
            root.mainloop()
        elif sys.argv[1] == "placar":
            score = [6, 9]
            root = tk.Tk()
            my_gui = TrucoPlacar(root, score)
            root.mainloop()
    else:
        root = tk.Tk()
        my_gui = TrucoJogador(root)
        root.mainloop()
if __name__ == "__main__":
    main()
