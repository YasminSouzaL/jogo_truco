import pygame
import sys
from truco_regras import TestDeck, CardCheck
from BaralhoDeTruco import Deck


class TrucoGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 20)
        self.player_names = []
        self.player_cards = {}
        self.current_screen = 'menu'
        self.input_name = ''
        self.input_box = pygame.Rect(100, 100, 200, 32)
        self.button_add_player = pygame.Rect(100, 200, 250, 50)
        self.button_start_game = pygame.Rect(100, 300, 200, 50)
        self.button_truco = pygame.Rect((500, 50), (100, 50))
        self.button_revange = pygame.Rect((500, 150), (100, 50))
        self.color_active = pygame.Color('lightskyblue')
        self.color_passive = pygame.Color('gray')
        self.color_button = pygame.Color('green')
        self.color_button_truco = pygame.Color('blue')
        self.active = False
        self.round_cards = {}
        self.player_scores = {}
        self.current_player_index = 0

    def add_player(self, player_name):
        print(f"Tentando adicionar jogador: {player_name}")
        if player_name and player_name not in self.player_names:
            self.player_names.append(player_name)
            self.round_cards[player_name] = []
            self.player_scores[player_name] = 0
            self.input_name = ''
        else:
            print(f"Erro: Jogador {player_name} já adicionado ou nome inválido")

    def remove_player(self, player_name):
        if player_name in self.player_names:
            self.player_names.remove(player_name)
        else:
            print(f"Erro: Jogador {player_name} não está na lista")

    def start_game(self):
        if len(self.player_names) >= 2:
            deck = Deck()
            deck.shuffle()
            self.player_cards = self.generate_player_cards(deck)
            self.current_screen = 'game'
        else:
            print("Erro: Não há jogadores suficientes")

    def generate_player_cards(self, deck):
        player_cards = {}
        for player in self.player_names:
            player_cards[player] = deck.deal_hand(3)
        TestDeck(player_cards)
        return player_cards

    def show_cards(self):
        self.screen.fill((240, 255, 255))
        y_offset = 100
        card_width = 100
        card_height = 140
        padding = 10

        for player_name in self.player_names:
            cards = self.player_cards[player_name]
            x_offset = 10
            for card in cards:
                card_text = f"{card.value} de {card.suit}"
                pygame.draw.rect(self.screen, (255, 255, 255), (x_offset, y_offset, card_width, card_height))
                pygame.draw.rect(self.screen, (0, 0, 0), (x_offset, y_offset, card_width, card_height), 2)

                text_surface = self.font_small.render(card_text, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(x_offset + card_width / 2, y_offset + card_height / 2))
                self.screen.blit(text_surface, text_rect)

                x_offset += card_width + padding

            y_offset += card_height + 2 * padding

        pygame.draw.rect(self.screen, self.color_button_truco, self.button_truco)
        self.draw_text('Truco', self.font, (255, 255, 255), self.button_truco.x + 7, self.button_truco.y + 15)

        pygame.display.flip()

    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.current_screen == 'menu':
                        if self.input_box.collidepoint(event.pos):
                            self.active = True
                        else:
                            self.active = False
                        if self.button_add_player.collidepoint(event.pos):
                            self.add_player(self.input_name)
                        if self.button_start_game.collidepoint(event.pos):
                            self.start_game()
                    elif self.current_screen == 'game':
                        if self.button_truco.collidepoint(event.pos):
                            self.declare_winner(self.player_names[self.current_player_index])
                        self.handle_card_click(event.pos)
                    elif self.current_screen == 'scores':
                        self.current_screen = 'game'
                        pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, 800, 600))
                        self.draw_text('TRUCO', self.font, (255, 0, 0), 100, 100)
                        self.show_cards()
                        self.start_game()  # Restart the game for a new round
                elif event.type == pygame.KEYDOWN:
                    if self.active:
                        if event.key == pygame.K_RETURN:
                            self.add_player(self.input_name)
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_name = self.input_name[:-1]
                        else:
                            self.input_name += event.unicode

            self.screen.fill((30, 30, 30))
            if self.current_screen == 'menu':
                self.draw_text('Jogador:', self.font, (240, 255, 255), 100, 50)
                self.draw_text(self.input_name, self.font, (255, 255, 255), self.input_box.x + 5, self.input_box.y + 5)
                pygame.draw.rect(self.screen, self.color_active if self.active else self.color_passive, self.input_box,
                                 3)
                pygame.draw.rect(self.screen, self.color_button, self.button_add_player)
                self.draw_text('Adicionar Jogador', self.font, (255, 255, 255), self.button_add_player.x + 20,
                               self.button_add_player.y + 15)
                pygame.draw.rect(self.screen, self.color_button, self.button_start_game)
                self.draw_text('Iniciar Jogo', self.font, (255, 255, 255), self.button_start_game.x + 8,
                               self.button_start_game.y + 12)
            elif self.current_screen == 'game':
                self.show_cards()
            elif self.current_screen == 'scores':
                self.show_scores()

            pygame.display.flip()
            self.clock.tick(60)

    def handle_card_click(self, pos):
        y_offset = 100
        for player_name in self.player_names:
            cards = self.player_cards[player_name]
            x_offset = 10
            for i, card in enumerate(cards):
                card_rect = pygame.Rect(x_offset, y_offset + 30, 100, 150)
                if card_rect.collidepoint(pos):
                    if player_name == self.player_names[self.current_player_index]:
                        self.play_card(i)
                        return
                x_offset += 110
            y_offset += 200

    def play_card(self, card_index):
        player_name = self.player_names[self.current_player_index]
        if 0 <= card_index < len(self.player_cards[player_name]):
            card = self.player_cards[player_name].pop(card_index)
            self.round_cards[player_name].append(card)
            self.show_cards()
            print(f"{player_name} jogou a carta {card}")
            if all(len(cards) == 3 for cards in self.round_cards.values()):  # Checa se todos os jogadores jogaram suas 3 cartas
                self.calculate_scores()

            self.current_player_index = (self.current_player_index + 1) % len(self.player_names)
        else:
            print(f"Índice de carta {card_index} inválido para o jogador {player_name}")

    def calculate_scores(self):
        print("Calculando pontuações...")
        card_check = CardCheck(self.round_cards)
        round_winner = card_check.determine_round_winner()

        if round_winner:
            self.player_scores[round_winner] += 1  # Supondo que o vencedor da rodada ganha 1 ponto
            print(f"{round_winner} ganhou a rodada e agora tem {self.player_scores[round_winner]} pontos.")
            if self.check_winner(round_winner):
                self.current_screen = 'winner'
                self.show_winner(round_winner)
                return

        self.round_cards = {player: [] for player in self.player_names}  # Reset para próxima rodada
        self.current_screen = 'scores'
        self.show_scores()

    def check_winner(self, player_name):
        return self.player_scores[player_name] >= 3


    def show_scores(self):
        self.screen.fill((255, 255, 255))
        y_offset = 100
        self.draw_text('Pontuações:', self.font, (255, 0, 0), 100, 50)
        for player_name, score in self.player_scores.items():
            self.draw_text(f"{player_name}: {score}", self.font, (255, 0, 0), 100, y_offset)
            y_offset += 40
        self.draw_text('Clique para continuar', self.font_small, (255, 0, 0), 100, y_offset + 20)
        pygame.display.flip()

    def declare_winner(self, winner_name):
        self.screen.fill((255, 255, 255))
        #Desenha um círculo azul no centro da tela
        circle_color = (0, 0, 255)  # Blue circle
        circle_thickness = 5  # 5 pixels thick

        pygame.draw.circle(self.screen, circle_color, (400, 300), 100, circle_thickness)

        # Desenha o nome do vencedor no centro do círculo
        text_surface = self.font.render(winner_name, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(400, 300))
        self.screen.blit(text_surface, text_rect)

        #Criar a perguntar se quer aumentar a aposta
        self.draw_text('Quer aumentar a aposta?', self.font, (255, 0, 0), 100, 100)
        pygame.draw.rect(self.screen, self.color_button_truco, self.button_revange)

        self.draw_text('Truco', self.font, (255, 255, 255), self.button_truco.x + 7, self.button_truco.y + 15)

        pygame.display.flip()
        pygame.time.wait(4000)

    def show_winner(self, winner_name):
        self.screen.fill((255, 255, 255))
        self.draw_text(f'{winner_name} venceu o jogo!', self.font, (255, 0, 0), 100, 100)
        # Mostra as pontuações finais
        y_offset = 200
        self.draw_text('Pontuações finais:', self.font, (255, 0, 0), 100, y_offset)
        for player_name, score in self.player_scores.items():
            self.draw_text(f"{player_name}: {score}", self.font, (255, 0, 0), 100, y_offset + 40)
            y_offset += 40

        #Emoji a lado
        trophy = pygame.image.load('trophy.png')
        trophy = pygame.transform.scale(trophy, (310, 300))
        self.screen.blit(trophy, (500, 100))

        pygame.display.flip()
        pygame.time.wait(9000)  # Espera 9 segundos antes de encerrar o jogo
        pygame.quit()
        sys.exit()

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))


if __name__ == '__main__':
    game = TrucoGame()
    game.game_loop()
