import tkinter as tk
from truco_game import Player, Game

class TrucoTela:
    def __init__(self, master):
        self.master = master
        master.title("Truco Game")

        self.player_names = []

        self.label = tk.Label(master,text="Digite os nomes dos jogadores:", font=("times", 15), fg="red")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.add_button = tk.Button(master, text="Adicionar Jogador", command=self.add_player)
        self.add_button.pack()

        self.start_button = tk.Button(master, text="Iniciar Jogo", command=self.start_game)
        self.start_button.pack()

    def add_player(self):
        player_name = self.entry.get()
        self.player_names.append(player_name)
        self.entry.delete(0, tk.END)
        print(f"Jogador {player_name} adicionado")

    def start_game(self):
        if len(self.player_names) >= 2:
            players = [Player(name) for name in self.player_names]
            game = Game(players)
            game.start()
            self.master.destroy()
        else:
            print("É necessário adicionar pelo menos dois jogadores para iniciar o jogo.")

def main():
    root = tk.Tk()
    app = TrucoTela(root)
    root.mainloop()

if __name__ == "__main__":
    main()
