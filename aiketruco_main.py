import tkinter as tk
from truco_game import Pair, Player, Hand, Match 
from truco_regras import TestGame, TestMatch


class TrucoJogador:
    def __init__(self, master):
        self.master = master
        master.title("Truco Game")

        self.player_names = []
        self.players = []

        self.player_name_label = tk.Label(master, text="Digite o nome dos jogadores (mínimo 2):", font=("times", 15), fg="red")
        self.player_name_label.pack()

        self.player_name_entry = tk.Entry(master)
        self.player_name_entry.pack()

        self.add_button = tk.Button(master, text="Adicionar Jogador", command=self.add_player)
        self.add_button.pack()

        self.remove_button = tk.Button(master, text="Remover Jogador", command=self.remove_player)
        self.remove_button.pack()

        self.player_list_label = tk.Label(master, text="Jogadores adicionados:", font=("times", 15), fg="red")
        self.player_list_label.pack()

        self.player_listbox = tk.Listbox(master)
        self.player_listbox.pack()

        self.start_button = tk.Button(master, text="Iniciar Jogo", command=self.start_game)
        self.start_button.pack()

    def add_player(self):
        player_name = self.player_name_entry.get()
        if player_name not in self.player_names:
            self.player_names.append(player_name)
            self.player_name_entry.delete(0, tk.END)
            self.player_listbox.insert(tk.END, player_name)
            print(f"Jogador {player_name} adicionado")
        else:
            print(f"O jogador {player_name} já está na lista.")
        player_name = self.player_name_entry.get()
        player = Player(player_name)
        self.players.append(player)

    def remove_player(self):
        player_name = self.player_name_entry.get()
        if player_name in self.player_names:
            self.player_names.remove(player_name)
            self.player_name_entry.delete(0, tk.END)
            self.show_players()
            print(f"Jogador {player_name} removido")
        else:
            print(f"Jogador {player_name} não encontrado")

    def show_players(self):
        self.player_listbox.delete(0, tk.END)
        for player in self.player_names:
            self.player_listbox.insert(tk.END, player)

    def start_game(self):
        if len(self.player_names) >= 2:
            self.players = [Player(name, Hand([])) for name in self.player_names]
            game = TestGame()
            self.play_game(game)
            self.master.destroy()
        else:
            print("É necessário adicionar pelo menos dois jogadores para iniciar o jogo.")

    def play_game(self, game):
        while True:
            match = game.current_match
            match = Match(game)

            for player in self.players:
                self.play_player(player, match)

            end_game = game.score[Pair.PAIR_ONE_ID] >= 12 or game.score[Pair.PAIR_TWO_ID] >= 12

    def play_player(self, player, match):
        print(f"Vez de {player.name} jogar.")
        print("Cartas disponíveis:")
        for i, card in enumerate(player.hand.cards):
            print(f"{i + 1}: {card}")
        card_index = int(input("Digite o número da carta que deseja jogar: ")) - 1
        card = player.hand.cards.pop(card_index)
        match.play_card(player, card)
        print(f"{player.name} jogou {card}.")

        if match.is_over():
            print("A rodada acabou.")
            print(f"Vencedor da rodada: {match.winner.name}")
            print("Placar da partida:")
            print(f"Equipe 1: {match.game.score[Pair.PAIR_ONE_ID]}")
            print(f"Equipe 2: {match.game.score[Pair.PAIR_TWO_ID]}")
        else:
            print("A rodada continua.")
            print(f"Vez do próximo jogador.")
        print()

class TrucoJogarCartas:
    def __init__(self, master, player_names):
        self.master = master
        master.title("Truco Game - Jogar Cartas")

        self.player_names = player_names
        self.players = []

        self.label_cards = tk.Label(master, text="Cartas de cada jogador:", font=("times", 15), fg="red")
        self.label_cards.pack()

        self.listbox_players = tk.Listbox(master)
        self.listbox_players.pack()

        self.show_cards()

    def show_cards(self):
        self.listbox_players.delete(0, tk.END)
        for player_name in self.player_names:
            self.listbox_players.insert(tk.END, f"Cartas de {player_name}:")
            cards = ["Carta 1", "Carta 2", "Carta 3"]
            for card in cards:
                self.listbox_players.insert(tk.END, card)


class TrucoCartas:
    def __init__(self, master, player_names):
        self.master = master
        master.title("Truco Game - Cartas")

        self.player_names = player_names
        self.players = []

        self.label_cards = tk.Label(master, text="Cartas de cada jogador:", font=("times", 15), fg="red")
        self.label_cards.pack()

        self.listbox_players = tk.Listbox(master)
        self.listbox_players.pack()

        self.show_cards()

    def show_cards(self):
        self.listbox_players.delete(0, tk.END)
        for player_name in self.player_names:
            self.listbox_players.insert(tk.END, f"Cartas de {player_name}:")
            cards = ["Carta 1", "Carta 2", "Carta 3"]
            for card in cards:
                self.listbox_players.insert(tk.END, card)

class TrucoRodadas:
    def __init__(self, master, player_names):
        self.master = master
        master.title("Truco Game - Rodadas")

        self.player_names = player_names
        self.players = []

        self.label_rounds = tk.Label(master, text="Rodadas de cada jogador:", font=("times", 15), fg="red")
        self.label_rounds.pack()

        self.listbox_players = tk.Listbox(master)
        self.listbox_players.pack()

        self.show_rounds()

    def show_rounds(self):
        self.listbox_players.delete(0, tk.END)
        for player_name in self.player_names:
            self.listbox_players.insert(tk.END, f"Rodadas de {player_name}:")
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

        self.label_score = tk.Label(master, text=f"Placar: {score[Pair.PAIR_ONE_ID]} x {score[Pair.PAIR_TWO_ID]}", font=("times", 15
), fg="red")
        self.label_score.pack()


if __name__ == "__main__":
    root = tk.Tk()
    my_gui = TrucoJogador(root)
    root.mainloop()

    root = tk.Tk()
    my_gui = TrucoJogarCartas(root, ["Jogador 1", "Jogador 2", "Jogador 3", "Jogador 4"])
    root.mainloop()

    root = tk.Tk()
    my_gui = TrucoCartas(root, ["Jogador 1", "Jogador 2", "Jogador 3", "Jogador 4"])
    root.mainloop()

    root = tk.Tk()
    my_gui = TrucoRodadas(root, ["Jogador 1", "Jogador 2", "Jogador 3", "Jogador 4"])
    root.mainloop()

    root = tk.Tk()
    my_gui = TrucoPlacar(root, [0, 0])
    root.mainloop()