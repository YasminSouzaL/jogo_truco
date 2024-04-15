import tkinter as tk
from truco_game import Player, Game

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
