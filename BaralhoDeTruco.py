import random

class Card:
    def __init__(self, suit, value):
        self._suit = suit
        self._value = value

    @property
    def suit(self):
        return self._suit

    @suit.setter
    def suit(self, value):
        self._suit = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return f'{self.value}_{self.suit}'

    def __repr__(self):
        return f'{self.value}_{self.suit}'


class Deck:
    CARDS_QUANTITY = 40
    _instance = None

    @staticmethod
    def get_instance():
        if Deck._instance is None:
            Deck._instance = Deck()
        return Deck._instance

    def __init__(self):
        self._cards = self.create_deck()
        self.shuffle()

    def create_deck(self):
        suits = ['Ouro', 'Copas', 'Espadas', 'Paus']
        values = ['4', '5', '6', '7', 'Q', 'J', 'K', 'As', '2', '3']
        deck = [Card(suit, value) for suit in suits for value in values]
        return deck

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, value):
        self._cards = value

    def shuffle(self):
        random.shuffle(self._cards)

    def deal(self, quantity):
        if len(self._cards) < quantity:
            self._cards = self.create_deck()
            self.shuffle()
        return [self._cards.pop(0) for _ in range(quantity)]

    def deal_hand(self, number_of_cards):
        if len(self._cards) < number_of_cards:
            self._cards = self.create_deck()
            self.shuffle()
        hand = self._cards[:number_of_cards]
        self._cards = self._cards[number_of_cards:]
        return hand


class Hand:
    def __init__(self, cards=None):
        self._cards = cards if cards else []

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, value):
        self._cards = value

    def add_card(self, card):
        self._cards.append(card)

    def throw_card(self, card_position=0):
        if 1 <= card_position <= len(self._cards):
            card_position -= 1
            card = self._cards[card_position]
            self.__remove_card(card)
        else:
            if not self._cards:
                raise Exception("Mão vazia")
            else:
                card = self._cards[0]
                self.__remove_card(card)
        return card

    def __remove_card(self, card):
        self._cards.remove(card)

    def __str__(self):
        return ", ".join(str(card) for card in self._cards)

    def deal_cards(self):
        deck = Deck.get_instance()
        self._cards = deck.deal(3)

    def winner(self):
        points = 0
        for card in self._cards:
            if card.value in ['7', 'A', '3']:
                points += 1
        return points

    def __gt__(self, other):
        return self.winner() > other.winner()

    def __lt__(self, other):
        return self.winner() < other.winner()

    def __eq__(self, other):
        return self.winner() == other.winner()


class Cardcheck:
    def __init__(self, round_cards):
        self._round_cards = round_cards
        self._card_ranking = {
            '4P': 14, '7O': 13, '7E': 12, '7C': 11, '3': 10, '2': 9,
            'A': 8, 'K': 7, 'J': 6, 'Q': 5, '7': 4, '6': 3, '5': 2, '4': 1
        }

    @property
    def round_cards(self):
        return self._round_cards

    @round_cards.setter
    def round_cards(self, value):
        self._round_cards = value

    @property
    def card_ranking(self):
        return self._card_ranking

    @card_ranking.setter
    def card_ranking(self, value):
        self._card_ranking = value

    def get_card_value(self, card):
        card_str = f"{card.value}{card.suit[0]}"
        return self._card_ranking.get(card_str, 0)

    def determine_round_winner(self):
        player_wins = {player: 0 for player in self._round_cards.keys()}
        for i in range(3):
            max_value = -1
            round_winner = None
            for player, cards in self._round_cards.items():
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
