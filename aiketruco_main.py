#Author : Yasmin Souza-8764
import tkinter as tk
from truco_game import Pair, Hand, Player, Match, Game
from truco_regras import TestGame
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
            print(f"Jogador {player_name} não encontrado")

    def show_players(self):
        self.player_listbox.delete(0, tk.END)
        for player in self.player_names:
            self.player_listbox.insert(tk.END, player)

    def start_game(self, test=False, player_names=None, player_cards=None):
        if test:
            test_game = TestGame(player_names, player_cards)
            test_game.play()
        else:
            if len(self.player_names) < 2:
                print("Adicione pelo menos 2 jogadores para iniciar o jogo.")
                return

            self.master.withdraw()
            cartas_screen = tk.Toplevel(self.master)
            app = TrucoJogarCartas(cartas_screen, self.player_names, self.player_cards)
    

class TrucoJogarCartas:
    def __init__(self, master, player_names, player_cards):
        self.master = master
        master.title("Truco Game - Jogar Cartas")

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
            if player_index < len(self.player_cards):  # Adicione esta linha
                self.listbox_players.insert(tk.END, f"Cartas de {player_name}:")
                cards = self.player_cards[player_index]
                for card in cards:
                    self.listbox_players.insert(tk.END, card)
        self.listbox_players.bind("<Double-Button-1>", self.play_player)
        self.listbox_players.pack()

    def on_card_select(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print('You selected item %d: "%s"' % (index, value))

    def play_player(self):
        player_index = self.listbox_players.curselection()[0]
        player_name = self.player_names[player_index]
        card_index = int(self.spinbox.get()) - 1
        card = self.player_cards[player_index][card_index]
        print(f"{player_name} jogou a carta {card}")
        self.player_cards[player_index].remove(card)
        self.show_cards()
        if len(self.player_cards[player_index]) == 0:
            print(f"O jogador {player_name} não tem mais cartas.")
            self.player_names.remove(player_name)
            self.player_cards.pop(player_index)
            self.show_cards()
            if len(self.player_names) == 1:
                print(f"O jogador {self.player_names[0]} venceu o jogo.")
                self.master.destroy()
                return
        print(f"Próximo jogador: {self.player_names[0]}")
        self.listbox_players.selection_clear(0, tk.END)
        self.spinbox.delete(0, tk.END)
        self.spinbox.insert(0, 1)

if __name__ == "__main__":
    root = tk.Tk()
    my_gui = TrucoJogador(root)
    root.mainloop()

