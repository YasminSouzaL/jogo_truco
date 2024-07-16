import pygame
import sys
import os
from BaralhoDeTruco import Deck, Hand, TestDeck

# Inicialização do Pygame
pygame.init()

# Tamanhos dos botões
size_button = (180, 50)

# Cores RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (196, 213, 230)
RED = (125, 34, 34)
GREEN = (113, 146, 100)
BLUE = (0, 0, 128)
REDClaro = (255, 107, 102)
VerdeClaro = (153, 255, 102)

# Fonte
pygame.font.init()
main_font = pygame.font.Font("data/font/DS-DIGIB.TTF", 32)
custom_font = pygame.font.Font("data/font/stocky.ttf", 32)
button_font = pygame.font.Font(None, 36)

# Configurações da tela
logo = pygame.image.load("data/imagem/logo.png")
height = 550
width = 750
pygame.display.set_caption('JOGO DE TRUCO!!!!')
pygame.display.set_icon(logo)

clock = pygame.time.Clock()
FPS = 45

# Imagens
background_image = pygame.image.load("data/imagem/background.png")
background_image = pygame.transform.scale(background_image, (width, height))

win_image = pygame.image.load("data/imagem/wallpaper.png")
win_image = pygame.transform.scale(win_image, (width, height))

textbox = pygame.image.load("data/imagem/textbox.png")
textbox = pygame.transform.scale(textbox, (300, 50))

# Caixa de entrada
input_boxes = [pygame.Rect(170, 200, 300, 50)]
active_boxes = [False]
box_colors = [GREY]
texts = ['']
screen = pygame.display.set_mode((width, height))

# Botões
add_button = pygame.Rect(100, 400, 200, 50)
remove_button = pygame.Rect(400, 400, 200, 50)
play_button = pygame.Rect(500, 200, 100, 50)
button_choose = pygame.Rect(500, 200, 100, 50)

# Carregar imagens das cartas
card_images = {}


def draw_title():
    title_surf = main_font.render("Criar Jogador", True, RED)
    title_rect = title_surf.get_rect(center=(width // 2, 100))
    screen.blit(title_surf, title_rect)


class PlayerCreationScreen:
    def __init__(self):
        self.running = True
        self.player_names = []
        self.input_name = ''

    def draw_text(self, text, font, color, x, y):
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))
        screen.blit(text_surf, text_rect)

    def draw_input(self):
        # Desenha a caixa de entrada de texto
        self.draw_text('Jogador:', main_font, BLACK, 100, 225)
        self.draw_text(self.input_name, main_font, BLACK, 300, 225)
        pygame.draw.rect(screen, box_colors[0], input_boxes[0], 2)

    def draw_buttons(self):
        # Desenha os botões
        pygame.draw.rect(screen, GREEN, add_button)
        pygame.draw.rect(screen, RED, remove_button)
        self.draw_text('Adicionar', button_font, BLACK, add_button.centerx, add_button.centery)
        self.draw_text('Remover', button_font, BLACK, remove_button.centerx, remove_button.centery)

    def draw(self):
        # Desenha a tela
        screen.blit(background_image, (0, 0))
        draw_title()
        self.draw_input()
        self.draw_buttons()
        pygame.display.flip()

    def add_player(self, player_name):
        print(f"Adicionado jogador: {player_name}")
        if player_name and player_name not in self.player_names:
            self.player_names.append(player_name)
            self.input_name = ''

    def remove_player(self):
        if self.player_names:
            self.player_names.pop()
        self.input_name = ''

    def run(self):
        self.running = True
        while self.running:
            screen.fill(WHITE)
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if add_button.collidepoint(event.pos):
                        self.add_player(self.input_name)
                    if remove_button.collidepoint(event.pos):
                        self.remove_player()
                    for i, box in enumerate(input_boxes):
                        if box.collidepoint(event.pos):
                            active_boxes[i] = not active_boxes[i]
                        else:
                            active_boxes[i] = False
                        box_colors[i] = RED if active_boxes[i] else GREY
                if event.type == pygame.KEYDOWN:
                    if active_boxes[0]:
                        if event.key == pygame.K_BACKSPACE:
                            self.input_name = self.input_name[:-1]
                        else:
                            if len(self.input_name) < 10:
                                self.input_name += event.unicode

            if len(self.player_names) >= 2:
                self.running = False


class ScreenCard:
    # Classe que controla a tela de cartas
    def __init__(self):
        self.running = True
        self.deck = Deck()
        self.player_names = []
        self.player_cards = {}
        self.cards_drawn = False
        self.card_width = 80
        self.card_height = 120
        self.card_images = self.load_card_images()

    def draw_title(self):
        title_surf = main_font.render("Cartas", True, RED)
        title_rect = title_surf.get_rect(center=(width // 2, 50))
        screen.blit(title_surf, title_rect)

    def checkplayer(self):
        if len(self.player_names) >= 2:
            self.deck.shuffle()
            self.player_cards = self.generate_player_cards()
            print("Cartas geradas para os jogadores:", self.player_cards)
            return True
        else:
            print("Não há jogadores suficientes.")
            return False

    def generate_player_cards(self):
        player_cards = {}
        for player in self.player_names:
            player_cards[player] = self.deck.deal_hand(3)
        TestDeck(player_cards)
        return player_cards

    def draw_text(self, text, font, color, x, y):
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))
        screen.blit(text_surf, text_rect)

    def load_card_images(self):
        pygame.init()  # Inicializa todos os módulos do pygame
        suits = ['Copas', 'Espadas', 'Paus', 'Ouro']
        values = ['4', '5', '6', '7', 'Q', 'J', 'K', 'As', '2', '3']
        base_path = "Data/imagem/card"
        card_images = {}  # Inicializa o dicionário de imagens
        for suit in suits:
            for value in values:
                card_name = f"{value}_{suit}.png"
                card_path = os.path.join(base_path, card_name)
                if os.path.exists(card_path):
                    try:
                        card_image = pygame.image.load(card_path)
                        card_image = pygame.transform.scale(card_image, (
                            self.card_width, self.card_height))  # Redimensiona a imagem
                        card_images[f"{value}_{suit}"] = card_image
                    except pygame.error as e:
                        print(f"Erro ao carregar a imagem: {card_path}. Erro: {e}")
                else:
                    print(f"Arquivo não encontrado: {card_path}")

        return card_images

    def draw_cards(self):
        x = 75
        y = 95
        for player, cards in self.player_cards.items():
            self.draw_text(player, main_font, BLACK, x + 100, y - 30)
            for card in cards:
                card_name = str(card)
                if card_name in self.card_images:
                    card_image = self.card_images[card_name]
                    screen.blit(card_image, (x, y))
                else:
                    # Desenha um retângulo caso a imagem não seja encontrada
                    card_rect = pygame.Rect(x, y, self.card_width, self.card_height)
                    pygame.draw.rect(screen, REDClaro, card_rect)
                x += 100
            x = 50
            y += 210

    def button_play(self):
        pygame.draw.rect(screen, GREY, play_button)
        self.draw_text('Jogar', main_font, BLACK, 550, 225)

    def draw(self):
        screen.fill(WHITE)
        self.draw_title()
        self.draw_cards()
        self.button_play()
        pygame.display.flip()

    def run(self):
        print("Running ScreenCard")
        if self.checkplayer():
            self.running = True
            while self.running:
                self.draw()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if play_button.collidepoint(event.pos):
                            self.cards_drawn = True
                            self.running = False
                        if remove_button.collidepoint(event.pos):
                            self.running = False


class Pontuacao:
    def __init__(self, player_names):
        self.points = {name: 0 for name in player_names}

    def adicionar_pontos(self, player, pontos):
        if player in self.points:
            self.points[player] += pontos
        else:
            raise KeyError(f"Jogador {player} não encontrado na pontuação")

    def get_pontos(self, player):
        if player in self.points:
            return self.points[player]
        else:
            raise KeyError(f"Jogador {player} não encontrado na pontuação")


class Rodadas:
    def __init__(self):
        self.players = None
        self.deck = Deck()
        self.hand = Hand()
        self.running = True
        self.player_names = []
        self.player_cards = {}
        self.current_round = 1
        self.selected_cards = {}
        self.round_cards = []
        self.card_width = 170
        self.card_height = 140
        self.current_player_index = 0
        self.round_winners = []
        self.winner = None
        self.truco_called = False
        self.pontuacao = None
        self.card_images = ScreenCard().card_images

    def draw_title(self):
        title_surf = main_font.render("Rodadas", True, RED)
        title_rect = title_surf.get_rect(center=(width // 2, 50))
        screen.blit(title_surf, title_rect)

    def draw_text(self, text, font, color, x, y):
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))
        screen.blit(text_surf, text_rect)

    def draw_players(self):
        y = 400
        for player in self.player_names:
            points = self.pontuacao.get_pontos(player)
            self.draw_text(f"{player} - {points} pontos", main_font, BLACK, 150, y)
            y += 50

    def draw_truco_button(self):
        truco_button = pygame.Rect(550, 400, 150, 50)
        pygame.draw.rect(screen, RED, truco_button)
        self.draw_text('TRUCO', button_font, WHITE, truco_button.centerx, truco_button.centery)
        return truco_button

    def draw_cards(self, player):
        x = 100
        y = 140
        for card in self.player_cards[player]:
            card_image = self.card_images[str(card)]
            card_rect = card_image.get_rect(topleft=(x, y))
            screen.blit(card_image, card_rect)
            self.round_cards.append((card_rect, card))
            x += self.card_width
        x += 200

    def draw(self):
        screen.blit(background_image, (0, 0))
        screen.fill(WHITE)
        self.draw_title()
        current_player = self.player_names[self.current_player_index]
        self.draw_text(f"Vez de {current_player}", main_font, BLACK, 300, 100)
        self.draw_cards(current_player)
        self.draw_players()
        truco_button = self.draw_truco_button()
        pygame.display.flip()
        return truco_button

    def hand_winner(self, card1, card2):
        hand = Hand()
        hand.add_card(card1)
        hand.add_card(card2)
        print(f"Vencedor da rodada: {hand.winner()}")

    def check_round_winner(self):
        if len(self.selected_cards) == len(self.player_names):
            print(f"Cartas jogadas na rodada: {self.selected_cards}")
            winning_card = None
            round_winner = None
            for player, card in self.selected_cards.items():
                if winning_card is None or card.value > winning_card.value:
                    winning_card = card
                    round_winner = player
            self.round_winners.append(round_winner)
            print(f"Ganhador da rodada: {round_winner}")

    def check_game_winner(self):
        player_points = {player: self.pontuacao.get_pontos(player) for player in self.player_names}
        max_points = max(player_points.values())
        for player, points in player_points.items():
            if points >= 12:
                self.winner = player
                break
        return self.winner

    def handle_truco(self):
        self.truco_called = True
        print("Truco foi chamado!")
        if self.truco_called:
            self.pontuacao.adicionar_pontos(self.player_names[self.current_player_index], 3)
            self.current_player_index = (self.current_player_index + 1) % len(self.player_names)
            self.selected_cards = {player: [] for player in self.player_names}
            self.truco_called = False

    def run(self):
        self.running = True
        self.selected_cards = {player: [] for player in self.player_names}  # Inicializar com listas vazias
        self.pontuacao = Pontuacao(self.player_names)
        while self.running:
            self.round_cards = []
            truco_button = self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if truco_button.collidepoint(event.pos):
                        self.handle_truco()
                    else:
                        for card_rect, card in self.round_cards:
                            if card_rect.collidepoint(event.pos):
                                current_player = self.player_names[self.current_player_index]
                                self.selected_cards[current_player] = card
                                self.player_cards[current_player].remove(card)
                                self.current_player_index = (self.current_player_index + 1) % len(self.player_names)
                                if all(self.selected_cards.values()):
                                    self.check_round_winner()
                                    round_winner = self.round_winners[-1]
                                    self.pontuacao.adicionar_pontos(round_winner, 2 if self.truco_called else 1)
                                    self.current_round += 1
                                    self.selected_cards = {player: [] for player in
                                                           self.player_names}  # Redefinir listas vazias
                                    self.current_player_index = 0
                                    self.truco_called = False
                                    #Verifacar se acabou as cartas
                                    if all(len(cards) == 0 for cards in self.player_cards.values()):
                                        print("Acabaram as cartas")
                                        for player in self.player_names:
                                            pontos_faltando = 12 - self.pontuacao.get_pontos(player)
                                            print(f"Jogador {player} precisa de {pontos_faltando} pontos para ganhar")
                                        # Chamar mais cartas para os jogadores e voltar para a rodada
                                        screen_card_instance = ScreenCard()
                                        screen_card_instance.player_names = self.player_names
                                        self.player_cards = screen_card_instance.generate_player_cards()
                                break
                    if self.check_game_winner():
                        self.running = False


class Winner:
    def __init__(self):
        self.running = True
        self.winner = None

    def draw_title(self):
        title_surf = custom_font.render("Vencedor", True, RED)
        title_rect = title_surf.get_rect(center=(width // 2, 50))
        screen.blit(title_surf, title_rect)

    def draw_text(self, text, font, color, x, y):
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))
        screen.blit(text_surf, text_rect)

    def draw_square(self, x, y, width, height, color):
        pygame.draw.rect(screen, color, (x - width // 2, y - height // 2, width, height))

    def draw(self):
        screen.blit(win_image, (0, 0))
        self.draw_title()
        self.draw_square(width // 2, height // 2, 300, 100, VerdeClaro)
        self.draw_text(f"O vencedor foi: {self.winner}", main_font, BLACK, width // 2, height // 2)
        print(f"O vencedor foi: {self.winner}")
        pygame.display.flip()


class Game:
    def __init__(self):
        self.running = True
        self.current_screen = "PlayerCreation"
        self.player_creation = PlayerCreationScreen()
        self.screen_card = ScreenCard()
        self.rodadas = Rodadas()
        self.winner = Winner()

    def switch_screen(self):
        print(f"Switching screen from {self.current_screen}")
        if self.current_screen == "PlayerCreation":
            if len(self.player_creation.player_names) >= 2:
                self.current_screen = "ScreenCard"
                self.screen_card.player_names = self.player_creation.player_names
                print("Switched to ScreenCard")
        elif self.current_screen == "ScreenCard":
            self.current_screen = "Rodadas"
            self.rodadas.player_names = self.screen_card.player_names
            self.rodadas.player_cards = self.screen_card.player_cards
            self.rodadas.selected_cards = {player: [] for player in self.rodadas.player_names}
            print("Switched to Rodadas")
        elif self.current_screen == "Rodadas":
            self.current_screen = "Winner"
            self.winner.winner = self.rodadas.winner
            print("Switched to Winner")
        elif self.current_screen == "Winner":
            self.running = False
            print("Game ended.")

    def run(self):
        while self.running:
            if self.current_screen == "PlayerCreation":
                self.player_creation.run()
                self.switch_screen()
            elif self.current_screen == "ScreenCard":
                self.screen_card.run()
                self.switch_screen()
            elif self.current_screen == "Rodadas":
                self.rodadas.run()
                self.switch_screen()
            elif self.current_screen == "Winner":
                self.winner.draw()
                pygame.time.wait(5000)  # Espera 5 segundos antes de encerrar
                self.running = False


game = Game()
game.run()
