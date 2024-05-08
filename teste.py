class TrucoJogarCartas:
def __init__(self, master, Game, player_names, player_cards):
    if player_names:
        self.master = master
        master.title("Truco Game - Jogar Cartas")

        self.game = Game
        self.deck = Game.deck
        self.player_names = player_names

        self.player_cards = player_cards

        self.label_players = tk.Label(master, text="Cartas de cada jogador:", font=("times", 15), fg="red")
        self.label_players.pack()

        self.listbox_players = tk.Listbox(master)
        self.listbox_players.pack()

        self.show_cards()  # Call show_cards before binding the event

        self.spinbox = tk.Spinbox(master, from_=1, to=3, width=55, font=("times", 15))
        self.spinbox.pack()

        self.play_button = tk.Button(master, text="Jogar Carta", command=self.play_player)
        self.play_button.pack()
    else:
        print("Nenhum jogador adicionado")

    def generate_player_cards(self):
        # Assuming each player gets 3 cards
        player_cards = {}
        for player in self.player_names:
            player_cards[player] = [self.deck.draw_card() for _ in range(3)]
        return player_cards

    def show_cards(self, player_name):
        cards = self.player_cards[player_name]
        for card in cards:
            print(card)


''' Esse metodo é chamado quando o jogador clica em uma carta para jogar, a partir do Spinbox 
que contém as cartas do jogador.'''


def show_cards(self):
    self.listbox_players.delete(0, tk.END)
    for player_index in range(len(self.player_names)):
        if player_index >= len(self.player_cards):
            continue
        player_name = self.player_names[player_index]
        self.listbox_players.insert(tk.END, f"Cartas de {player_name}:")
        cards = self.player_cards[player_index]
        for card in cards:
            self.listbox_players.insert(tk.END, card)
        # Add a check to see if the cards are being added
        if not cards:
            print(f"No cards for player {player_name}")


'''Ese metodo é chamado quando o jogador clica no botão "Jogar Carta" para jogar uma carta.
O jogador seleciona a carta que deseja jogar a partir do Spinbox que contém as cartas do jogador.'''


def play_player(self):
    if self.listbox_players.curselection():  # Check if a card is selected
        player_index = self.listbox_players.curselection()[0]
        player_name = self.player_names[player_index]
        card_index = self.spinbox.get()
        card = self.player_cards[player_index][int(card_index) - 1]
        print(f"Jogador {player_name} jogou a carta {card}")
        self.player_cards[player_index].remove(card)
        self.show_cards()
        if len(self.player_cards[player_index]) == 0:
            print(f"Jogador {player_name} não tem mais cartas")
            self.player_names.remove(player_name)
            self.player_cards.pop(player_index)
            self.show_cards()
            if len(self.player_names) == 1:
                print(f"Jogador {self.player_names[0]} ganhou o jogo!")
                self.master.withdraw()
                cartas_screen = tk.Toplevel(self.master)
                app = TrucoJogarCartas(cartas_screen, self.player_names, self.player_cards)
            else:
                print("Próximo jogador")
        else:
            print(f"Próximo jogador")
    else:
        print("Selecione uma carta para jogar.")
        return