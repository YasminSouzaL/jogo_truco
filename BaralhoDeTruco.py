import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f'{self.value}_{self.suit}'

    def __repr__(self):
        return f'{self.value}_{self.suit}'
class Deck:
    CARDS_QUANTITY = 40
    instance = None

    @staticmethod
    def get_instance():
        if Deck.instance is None:
            Deck.instance = Deck()
        return Deck.instance

    def __init__(self):
        self.cards = self.create_deck()

    def create_deck(self):
        suits = ['Ouro', 'Copas', 'Espadas', 'Paus']
        values = ['4', '5', '6', '7', 'Q', 'J', 'K', 'As', '2', '3']
        deck = [Card(suit, value) for suit in suits for value in values]
        return deck

    def shuffle(self):
        random.shuffle(self.cards)

    def __check_deck(self):
        """ Check deck integrity """
        if len(self.cards) != self.CARDS_QUANTITY:
            raise Exception('Alguém está roubando e não devolveu todas as cartas!')

    def get_top_card(self):
        top_card = self.cards.pop(0)
        return top_card

    def get_bottom_card(self):
        bottom_card = self.cards.pop(-1)
        return bottom_card

    def keep_card(self, card):
        self.cards.append(card)

    def deal(self, quantity):
        return [self.cards.pop(0) for _ in range(quantity)]

    def draw_card(self):
        if not self.cards:
            self.cards = self.create_deck()
            self.shuffle()
        return self.cards.pop()

    def deal_hand(self, number_of_cards):
        hand = self.cards[:number_of_cards]
        self.cards = self.cards[number_of_cards:]
        return hand

    def draw(self):
        return self.cards.pop()

class Hand:
    def __init__(self, cards=None):
        self.cards = cards if cards else []

    def add_card(self, card):
        self.cards.append(card)

    def throw_card(self, card_position=0):
        if 1 <= card_position <= len(self.cards):
            card_position -= 1
            card = self.cards[card_position]
            self.__remove_card(card)
        else:
            if not self.cards:
                raise Exception("Mão vazia")
            else:
                card = self.cards[0]
                self.__remove_card(card)
        return card

    def __remove_card(self, card):
        self.cards.remove(card)

    def __str__(self):
        return ", ".join(str(card) for card in self.cards)

    def deal_cards(self):
        deck = Deck.get_instance()
        self.cards = deck.deal(3)

    def winner(self):
        points = 0
        for card in self.cards:
            if card.value in ['7', 'A', '3']:
                points += 1
        return points

    def __gt__(self, other):
        return self.winner() > other.winner()

    def __lt__(self, other):
        return self.winner() < other.winner()

    def __eq__(self, other):
        return self.winner() == other.winner()

class CardCheck:
    def __init__(self, round_cards):
        self.round_cards = round_cards
        self.card_ranking = {
            '4O': 14, '7C': 13, '7E': 12, '7P': 11, '3': 10, '2': 9,
            'A': 8, 'K': 7, 'J': 6, 'Q': 5, '7': 4, '6': 3, '5': 2, '4': 1
        }

    def get_card_value(self, card):
        card_str = f"{card.value[0]}{card.suit[0]}"
        return self.card_ranking.get(card_str, 0)

    def determine_round_winner(self):
        player_wins = {player: 0 for player in self.round_cards.keys()}
        for i in range(3):
            max_value = -1
            round_winner = None
            for player, cards in self.round_cards.items():
                card = cards[i]
                card_value = self.get_card_value(card)
                if card_value > max_value:
                    max_value = card_value
                    round_winner = player

            if round_winner:
                player_wins[round_winner] += 1

        round_winner = max(player_wins, key=player_wins.get)
        return round_winner

    def calculate_points(self, cards):
        return sum(self.get_card_value(card) for card in cards)


class TestDeck:
    NUMBER_OF_CARDS_IN_TRUCO = 40

    def __init__(self, player_cards):
        self.player_cards = player_cards

    def test_deck_initialization(self, deck):
        assert len(deck.cards) == self.NUMBER_OF_CARDS_IN_TRUCO

    def test_get_top_card(self, deck):
        top_card = deck.cards[0]
        assert deck.get_top_card() == top_card
        assert len(deck.cards) == (self.NUMBER_OF_CARDS_IN_TRUCO - 1)

    def test_get_bottom_card(self, deck):
        bottom_card = deck.cards[len(deck.cards) - 1]
        assert deck.get_bottom_card() == bottom_card
        assert len(deck.cards) == (self.NUMBER_OF_CARDS_IN_TRUCO - 1)

    def test_keep_card(self, deck):
        bottom_card = deck.get_bottom_card()
        assert len(deck.cards) == (self.NUMBER_OF_CARDS_IN_TRUCO - 1)
        deck.keep_card(bottom_card)
        assert len(deck.cards) == self.NUMBER_OF_CARDS_IN_TRUCO

    def test_shuffle(self, deck):
        try:
            deck.shuffle()
            shuffled = True
        except Exception:
            shuffled = False
        assert shuffled

    '''
    Testa se a mão tem naipe repetido; se sim, retorna as cartas para o deck e lida novamente.
    '''
    def check_deck(self, deck):
        deck = Deck.get_instance()
        hand = Hand()
        hand.deal_cards()
        suits = [card.suit for card in hand.cards]
        while len(set(suits)) < len(suits):
            for card in hand.cards:
                deck.keep_card(card)
            hand.deal_cards()
            suits = [card.suit for card in hand.cards]
        return hand

    def test_shuffle_without_a_card(self, deck):
        bottom_card = deck.get_bottom_card()
        try:
            deck.shuffle()
            shuffled = True
        except Exception:
            shuffled = False
        assert not shuffled

class Cardcheck:
    def __init__(self, round_cards):
        self.round_cards = round_cards
        self.card_ranking = {
            '4P': 14, '7O': 13, '7E': 12, '7C': 11, '3': 10, '2': 9,
            'A': 8, 'K': 7, 'J': 6, 'Q': 5, '7': 4, '6': 3, '5': 2, '4': 1
        }

    def get_card_value(self, card):
        card_str = f"{card.value}{card.suit[0]}"
        return self.card_ranking.get(card_str, 0)

    def determine_round_winner(self):
        player_wins = {player: 0 for player in self.round_cards.keys()}
        for i in range(3):
            max_value = -1
            round_winner = None
            for player, cards in self.round_cards.items():
                card = cards[i]
                card_value = self.get_card_value(card)
                if card_value > max_value:
                    max_value = card_value
                    round_winner = player

            if round_winner:
                player_wins[round_winner] += 1

        round_winner = max(player_wins, key=player_wins.get)
        return round_winner

    def calculate_points(self, cards):
        return sum(self.get_card_value(card) for card in cards)

    def check_card(self, card1, card2):
        return self.get_card_value(card1) > self.get_card_value(card2)