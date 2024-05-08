import tkinter as tk


class TrucoJogador:
    def __init__(self, master):
        self.master = master
        master.title("Truco Game - Jogadores")

        self.player_names = []
        self.players = []  # Lista para armazenar os jogadores

        self.label = tk.Label(master, text="Digite os nomes dos jogadores:", font=("times", 15), fg="red")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.add_button = tk.Button(master, text="Adicionar Jogador", command=self.add_player)
        self.add_button.pack()

        # Botão para remover jogador
        self.remove_button = tk.Button(master, text="Remover Jogador", command=self.remove_player)
        self.remove_button.pack()

        self.label_players = tk.Label(master, text="Jogadores adicionados:", font=("times", 15), fg="red")
        self.label_players.pack()

        self.listbox_players = tk.Listbox(master)
        self.listbox_players.pack()

        self.start_button = tk.Button(master, text="Continuar para Cartas", command=self.open_cartas_screen)
        self.start_button.pack()

    def add_player(self):
        player_name = self.entry.get()
        self.player_names.append(player_name)
        self.entry.delete(0, tk.END)
        self.listbox_players.insert(tk.END, player_name)  # Adiciona o jogador à lista de jogadores exibidos
        print(f"Jogador {player_name} adicionado")

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

    def open_cartas_screen(self):
        if len(self.player_names) >= 2:
            cartas_screen = tk.Toplevel(self.master)
            app = TrucoCartas(cartas_screen, self.player_names)
        else:
            print("É necessário adicionar pelo menos dois jogadores para continuar.")


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


def main():
    root = tk.Tk()
    app = TrucoJogador(root)
    root.mainloop()


if __name__ == "__main__":
    main()

'''
class TrucoCartas:
    
    def __init__(self, master, player_names):
        self.window = tk.Tk()
        self.spinbox = tk.Spinbox(self.window, from_=1, to=10)
        self.spinbox.pack()
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
                
    def play_player(self, player, match):
        print(f"Vez de {player.name} jogar.")
        print("Cartas disponíveis:")
        for i, card in enumerate(player.hand.cards):
            print(f"{i + 1}: {card}")
        self.window.mainloop()
        card_index = int(self.spinbox.get()) - 1
        if not player.hand.cards or card_index >= len(player.hand.cards) or card_index < 0:
            print("Número de carta inválido.")
            return
        card = player.hand.cards.pop(card_index)
        match.play_card(player, card)
        print(f"{player.name} jogou {card}.")
        print()

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
    def __init__(self, master, score, player_names):
        self.master = master
        self.score = score
        self.player_names = player_names
        self.players = [Player(name) for name in self.player_names]
        master.title("Truco Game - Placar")

    def start_game(self):
        self.players = [Player(name) for name in self.player_names]
        game = TestGame()

        













class TrucoJogarCartas:
    def __init__(self, master, player_names):
        self.master = master
        master.title("Truco Game - Jogar Cartas")

        self.player_names = player_names
        self.players = []

        self.label_players = tk.Label(master, text="Cartas de cada jogador:", font=("times", 15), fg="red")
        self.label_players.pack()

        self.listbox_players = tk.Listbox(master)
        self.listbox_players.pack()

        self.show_cards()

        self.spinbox = tk.Spinbox(master, from_=1, to=3, width=55, font=("times", 15))
        self.spinbox.pack()

        self.play_button = tk.Button(master, text="Jogar Carta", command=self.play_player)
        self.play_button.pack()
    
    def show_cards(self):
        self.listbox_players.delete(0, tk.END)
        for player_name in self.player_names:
            self.listbox_players.insert(tk.END, f"Cartas de {player_name}:")
            cards = ["Carta 1", "Carta 2", "Carta 3"]
            for card in cards:
                self.listbox_players.insert(tk.END, card)

    def play_player(self):
        player_index = int(self.spinbox.get()) - 1
        if player_index < 0 or player_index >= len(self.players):
            print("Jogador inválido.")
            return
        player_name = self.player_names[player_index]
        print(f"Carta jogada pelo jogador {player_name}.")

'''

'''
class TrucoRodadas:
    def __init__(self, master, player_names, player_cards):
        self.master = master
        master.title("Truco Game - Rodadas")

        self.player_names = player_names
        self.player_cards = player_cards

        self.label_players = tk.Label(master, text="Cartas de cada jogador:", font=("times", 15), fg="red")
        self.label_players.pack()

        self.listbox_players = tk.Listbox(master)
        self.listbox_players.pack()

        self.show_cards()

        self.spinbox = tk.Spinbox(master, from_=1, to=3, width=55, font=("times", 15))
        self.spinbox.pack()

        self.play_button = tk.Button(master, text="Jogar Carta", command=self.play_player)
        self.play_button.pack()
    
    def show_cards(self):
        self.listbox_players.delete(0, tk.END)
        for player_name in self.player_names:
            player_index = self.player_names.index(player_name)
            if player_index < len(self.player_cards):  
                self.listbox_players.insert(tk.END, f"Cartas de {player_name}:")
                cards = self.player_cards[player_index]
                for card in cards:
                    self.listbox_players.insert(tk.END, card)
        
    def play_player(self):
        if self.listbox_players.curselection() == ():  
            print("Selecione uma carta para jogar.")
            return

        player_index = int(self.spinbox.get()) - 1
        if player_index < 0 or player_index >= len(self.player_names):
            print("Jogador inválido.")
            return

        # Armazena informações da carta selecionada em uma variável separada
        selected_card_index = self.listbox_players.curselection()[0]
        selected_card_text = self.listbox_players.get(selected_card_index)

        # Mostra a carta selecionada e o jogador que jogou a carta
        print(f"Jogador {self.player_names[player_index]} jogou a carta {selected_card_text}")

        # A caixa de listagem após remover a carta jogada
        self.listbox_players.delete(selected_card_index)
        self.show_cards()

'''
