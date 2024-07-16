import sys
import pygame
import os
from BaralhoDeTruco import Deck,Hand,TestDeck
pygame.init()

# Tamanhos dos botões
size_button = (180, 50)

# Cores RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (196, 213, 230)
RED = (125, 34, 34)
GREEN = (113, 146, 100)
BLUE = (5, 79, 119)
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
''' Imaqens de fundo  que estão sendo usadas no jogo'''
background_image = pygame.image.load("data/imagem/background.png")
background_image = pygame.transform.scale(background_image, (width, height))
win_image = pygame.image.load("data/imagem/wallpaper.png")
win_image = pygame.transform.scale(win_image, (width, height))
textbox = pygame.image.load("data/imagem/textbox.png")
textbox = pygame.transform.scale(textbox, (150, 40))

# Caixa de entrada
input_boxes = [pygame.Rect(170, 200, 300, 50), pygame.Rect(170, 300, 300, 50)]
active_boxes = [False, False]
box_colors = [GREY, GREY]
texts = ['', '']
screen = pygame.display.set_mode((width, height))
# Botões
add_button = pygame.Rect(100, 400, 200, 50)
remove_button = pygame.Rect(400, 400, 200, 50)
play_button = pygame.Rect(500, 200, 100, 50)
button_choose = pygame.Rect(500, 200, 100, 50)

def draw_text(text, rect, color, screen):
    text_surf = main_font.render(text, True, color)
    screen.blit(text_surf, (rect.x, rect.y - 30))

class Background:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path).convert()
        self.image = pygame.transform.smoothscale(self.image, (width, height))

    def draw_background(self):
        screen.blit(self.image, (0, 0))
        clock.tick(250)
class Buttons(pygame.sprite.Sprite):
    def __init__(self, text, size):
        super().__init__()

        self.image_up = pygame.image.load("data/imagem/button1.png").convert()
        self.image_down = pygame.image.load("data/imagem/button2.png").convert()

        self.image_up = pygame.transform.scale(self.image_up, size)
        self.image_down = pygame.transform.scale(self.image_down, size)

        self.image = self.image_up
        self.rect = self.image.get_rect()

        self.click = False

        self.font = pygame.font.SysFont('padrão', 50)
        self.text = text
        self.text_surface = None
        self.text_rect = None
        self.render_text()

    def render_text(self):
        self.text_surface = self.font.render(self.text, True, BLACK)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.image_up.blit(self.text_surface, self.text_rect)
        self.image_down.blit(self.text_surface, self.text_rect)
        clock.tick(FPS)

    def update(self):
        self.image = self.image_up if not self.click else self.image_down

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        # Centralizar o texto no botão
        self.text_rect.center = self.rect.center
        screen.blit(self.text_surface, self.text_rect)

    def print_display(self, pos):
        self.update()
        self.draw(screen)
        self.collision_point(pos)

    def collision_point(self, pos):
        if self.rect.collidepoint(pos):
            self.click = True
        else:
            self.click = False

    def up(self):
        self.click = False


class PlayerCreationScreen:
    def __init__(self):
        self.running = True
        self.player_names = []
        self.input_name = ''

    def draw_title(self):
        title_surf = main_font.render("Criar Jogador", True, RED)
        title_rect = title_surf.get_rect(center=(width // 2, 100))
        screen.blit(title_surf, title_rect)

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
        self.draw_title()
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
    '''
    Claase ScreenCard resposalvel por gerar as cartas para os jogadores
    '''

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
        self.points = {player: 0 for player in player_names}

    def adicionar_pontos(self, player, pontos):
        self.points[player] += pontos

    def get_pontos(self, player):
        return self.points.get(player, 0)

class Rodadas:
    '''
    Classe Rodadas responsavel por gerenciar as rodadas do jogo
    metodo run() é responsavel por rodar o jogo

    '''
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
                                    # Verifacar se acabou as cartas
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
        title_surf = main_font.render("Vencedor", True, RED)
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
        pygame.display.flip()

class ScreenSettings:
    def __init__(self):
        self.running = True

    def draw_title(self):
        title_surf = main_font.render("Configurações", True, RED)
        title_rect = title_surf.get_rect(center=(width // 2, 200))
        screen.blit(title_surf, title_rect)

    def draw_emoji(self):
        emoji = pygame.image.load("data/imagem/config.png")
        emoji = pygame.transform.scale(emoji, (100, 100))
        screen.blit(emoji, (width // 2, 300))

    def draw(self):
        screen.fill(WHITE)
        self.draw_title()
        self.draw_emoji()
        pygame.display.flip()

    def run(self):
        while self.running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        pygame.quit()
        sys.exit()