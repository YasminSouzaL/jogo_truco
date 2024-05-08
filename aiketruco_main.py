# Author : Yasmin Souza-8764
import tkinter as tk
from random import shuffle
from tkinter import Listbox

from truco_regras import TestDeck
from truco_game import Deck
class TrucoJogador:
    # Classe para a tela de adicionar e remover jogadores e ir para a tela de jogar cartas
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)

        master.title("Truco Game - Jogadores")
        self.players = []

        self.label = tk.Label(master, text="Digite os nomes dos jogadores:", font=("times", 15), fg="red")
        self.label.pack()

        self.player_name_entry = tk.Entry(master)
        self.player_name_entry.pack()

        self.add_button = tk.Button(master, text="Adicionar Jogador", command=self.add_player)
        self.add_button.pack()

        self.remove_button = tk.Button(master, text="Remover Jogador", command=self.remove_player)
        self.remove_button.pack()

        self.label_players = tk.Label(master, text="Jogadores adicionados:", font=("times", 15), fg="red")
        self.label_players.pack()

        self.player_listbox = tk.Listbox(master)
        self.player_listbox.pack()

        self.start_button = tk.Button(master, text="Iniciar Jogo", command=self.start_game)
        self.start_button.pack()

        self.entry = tk.Entry(self.frame)
        self.entry.pack()

        self.player_names = []
        self.player_cards = []

    def add_player(self):
        player_name = self.player_name_entry.get()
        if player_name not in self.player_names:
            self.player_names.append(player_name)
            self.player_name_entry.delete(0, tk.END)
            self.show_players()
            print(f"Jogador {player_name} adicionado")
        else:
            print(f"Jogador {player_name} já adicionado")

    def remove_player(self):
        player_name = self.player_name_entry.get()
        if player_name in self.player_names:
            self.player_names.remove(player_name)
            self.player_name_entry.delete(0, tk.END)
            self.show_players()
            print(f"Jogador {player_name} removido")
        else:
            print(f"Jogador {player_name} não está na lista")

    def show_players(self):
        self.player_listbox.delete(0, tk.END)
        for player in self.player_names:
            self.player_listbox.insert(tk.END, player)

    def start_game(self):
        if len(self.player_names) >= 2:
            self.master.withdraw()
            cartas_screen = tk.Toplevel(self.master)
            app = TrucoJogarCartas(cartas_screen, self, self.player_names)
        else:
            print("Adicione pelo menos 2 jogadores")

def on_card_select(event):
    print("on_card_select called")  # Add this line
    widget = event.widget
    selection = widget.curselection()
    if selection:  # Check if the selection is not empty
        index = int(selection[0])
        # Rest of your code
    else:
        print("No item selected")

class TrucoJogarCartas:

    # Classe para a tela de jogar cartas
    def __init__(self, master, previous_screen, player_names, player_cards=None):
        self.master = master
        self.previous_screen = previous_screen
        self.player_names = player_names
        self.deck = Deck()
        self.deck.shuffle()
        self.player_cards = self.generate_player_cards()

        master.title("Truco Game - Jogar Cartas")

        self.label_players = tk.Label(master, text="Cartas de cada jogador:", font=("times", 15), fg="red")
        self.label_players.pack()

        self.listbox_players = tk.Listbox(master)
        self.listbox_players.pack()

        self.show_cards()  # Call show_cards before binding the event

        self.spinbox = tk.Spinbox(master, from_=1, to=3, width=55, font=("times", 15))
        self.spinbox.pack()

        self.play_button = tk.Button(master, text="Jogar Carta", command=self.play_player)
        self.play_button.pack()

    def generate_player_cards(self):
        # Assuming each player gets 3 cards
        player_cards = {}
        for player in self.player_names:
            player_cards[player] = [self.deck.draw_card() for _ in range(3)]
        return player_cards

    def show_cards(self):
        self.listbox_players.delete(0, tk.END)
        for player_name in self.player_names:
            self.listbox_players.insert(tk.END, f"Cartas de {player_name}:")
            cards = self.player_cards[player_name]  # Use player_name instead of player_index
            for card in cards:
                self.listbox_players.insert(tk.END, card)
            # Add a check to see if the cards are being added
            if not cards:
                print(f"Sem cartas para o jogador {player_name}")

    def play_player(self):
        if self.listbox_players.curselection():  # Check if a card is selected
            player_index = self.listbox_players.curselection()[0]
            player_name = self.player_names[player_index]
            card_index = self.spinbox.get()
            card = self.player_cards[player_index][int(card_index) - 1]
            print(f"Jogador {player_name} jogou a carta {card}")
            self.player_cards[player_index].remove(card)


if __name__ == "__main__":
    root = tk.Tk()
    my_gui = TrucoJogador(root)
    root.mainloop()