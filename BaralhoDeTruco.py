# -*- coding: utf-8 -*- 

import random

class Card:
    """ Representa a carta de baralho """
    def __init__(self, suit, value=None):
        self.suit = suit
        self.value = value

    def clone(self, value):
        return Card(self.suit, value)

    def __str__(self):
        suit = self.suit
        value = self.value
        if value == "A":
            value = "As"
        elif value == "K":
            value = "Rei"
        elif value == "Q":
            value = "Dama"
        elif value == "J":
            value = "Valete"

        return value + " de " + suit


class Deck:
    CARDS_QUANTITY = 40
    instance = None

    @staticmethod
    def get_instance():
        if Deck.instance is None:
            Deck.instance = Deck()
        return Deck.instance

    def __init__(self):
        self.cards = []
        self.__init_deck()
        self.cards = self.create_deck()

    def __init_deck(self):
        self.__create_cards("Copas")
        self.__create_cards("Ouros")
        self.__create_cards("Espadas")
        self.__create_cards("Paus")

    def __create_cards(self, suit):
        suit_card = Card(suit)
        self.cards.append(suit_card.clone("A"))
        self.cards.append(suit_card.clone("J"))
        self.cards.append(suit_card.clone("Q"))
        self.cards.append(suit_card.clone("K"))
        for number in range(2, 8):
            value = str(number)
            card = suit_card.clone(value)
            self.cards.append(card)

    def create_deck(self):
        suits = ['Ouros', 'Copas', 'Espadas', 'Paus']
        values = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
        deck = [Card(value, suit) for suit in suits for value in values]
        return deck

    def shuffle(self):
        random.shuffle(self.cards)

    def __check_deck(self):
        """ Check deck integrity """
        if len(self.cards) != self.CARDS_QUANTITY:
            raise Exception('Alguém está roubando e não devolveu todas as cartas!')

    def get_top_card(self):
        top_card = self.cards[0]
        # Remove it from pool
        self.cards.remove(top_card)
        return top_card

    def get_bottom_card(self):
        bottom_card = self.cards[-1]
        # Remove it from pool
        self.cards.remove(bottom_card)
        return bottom_card

    def keep_card(self, card):
        # Add the card back to the pool
        self.cards.append(card)

    def deal(self, quantity):
        cards = []
        for _ in range(quantity):
            cards.append(self.get_top_card())
        return cards

    def draw_card(self):
        if len(self.cards) == 0:
            self.shuffle()  # Reshuffle deck when empty (optional)
            return "Baralho vazio (Deck reshuffled)"  # Optional warning message
        return self.cards.pop()

    def deal_hand(self, number_of_cards):
        hand = self.cards[:number_of_cards]
        self.cards = self.cards[number_of_cards:]
        return hand


class Hand:
    """ Represents the player hand """

    def __init__(self, cards=None):
        if cards is None:
            cards = []
        self.cards = cards

    def add_card(self, card):
        self.cards.append(card)

    def throw_card(self, card_position=0):

        if 1 <= card_position <= len(self.cards):
            card_position -= 1
            card = self.cards[card_position]
            self.__remove_card(card)
        else:
            # Return the first card of the hand by default
            if not self.cards:
                raise Exception("Mão vazia")
            else:
                card = self.cards[0]
                self.__remove_card(card)

        return card

    def __remove_card(self, card):
        self.cards.remove(card)

    def __str__(self):
        cards_str = ""
        for card in self.cards:
            cards_str += str(card) + ", "
        return cards_str
    
    def deal_cards(self):
        deck = Deck.get_instance()
        self.cards = deck.deal(3)


class CardCheck:
    def __init__(self, round_cards):
        self.round_cards = round_cards
        self.card_ranking = {
            '4P': 14, '7O': 13, 'A': 12, '7E': 11, '3': 10, '2': 9,
            'K': 8, 'J': 7, 'Q': 6, '7C': 5, '6': 4, '5': 3, '4': 2
        }

    def get_card_value(self, card):
        # Converte o naipe e valor para uma string correspondente no ranking
        card_str = f"{card.value}{card.suit[0]}"
        return self.card_ranking.get(card_str, 0)

    def determine_round_winner(self):
        player_wins = {player: 0 for player in self.round_cards.keys()}

        for i in range(3):
            max_value = -1
            round_winner = None

            for player, cards in self.round_cards.items():
                card = cards[i]  # Cada jogador joga uma carta em cada mão
                card_value = self.get_card_value(card)
                if card_value > max_value:
                    max_value = card_value
                    round_winner = player

            if round_winner:
                player_wins[round_winner] += 1

        # O jogador que ganhar duas ou mais mãos vence a rodada
        round_winner = max(player_wins, key=player_wins.get)
        return round_winner

    def calculate_points(self, cards):
        points = 0
        for card in cards:
            points += self.get_card_value(card)
        return points


class Pair:
    """ Represents the pair """
    
    PAIR_ONE_ID = 'pair_one'
    PAIR_TWO_ID = 'pair_two'

    def __init__(self, id_pair, players):
        self.id_pair = id_pair
        self.players = players

    players = {}.fromkeys(['player1','player2'],'player')


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = hand = Hand([])

    def set_hand(self, hand):
        self.hand = hand

    def __str__(self):
        return self.name

class Match:

    def __init__(self, players):
        self.players = players
        self.round_cards = {Pair.PAIR_ONE_ID: [], Pair.PAIR_TWO_ID: []}
        self.winner = None

    def play_card(self, player, card):
        if player in self.players:
            self.round_cards[player].append(card)
        else:
            raise Exception("Jogador não pertence a partida")

    def is_over(self):
        return len(self.round_cards[Pair.PAIR_ONE_ID]) == 3 and len(self.round_cards[Pair.PAIR_TWO_ID]) == 3

    def check_winner(self):
        card_check = CardCheck(self.round_cards)
        self.winner = card_check.get_winner()

    def __str__(self):
        return f"Vencedor da rodada: {self.winner.name}"


class TestGame:
    def __init__(self):
        self.current_match = None
        self.score = {Pair.PAIR_ONE_ID: 0, Pair.PAIR_TWO_ID: 0}

    def start_match(self, players):
        self.current_match = Match(players)

    def end_match(self):
        self.current_match.check_winner()
        self.score[self.current_match.winner] += 1

    def __str__(self):
        return f"Placar da partida: Equipe 1: {self.score[Pair.PAIR_ONE_ID]}, Equipe 2: {self.score[Pair.PAIR_TWO_ID]}"


class Game:
    def __init__(self):
        self.players = []
        self.deck = Deck.get_instance()
        self.current_match = None
        self.score = {Pair.PAIR_ONE_ID: 0, Pair.PAIR_TWO_ID: 0}

    def start_match(self):
        self.current_match = Match(self.players)

    def end_match(self):
        self.current_match.check_winner()
        self.score[self.current_match.winner] += 1

    def __str__(self):
        return f"Placar da partida: Equipe 1: {self.score[Pair.PAIR_ONE_ID]}, Equipe 2: {self.score[Pair.PAIR_TWO_ID]}"


class Round:
    def __init__(self, players):
        self.players = players
        self.round_cards = {Pair.PAIR_ONE_ID: [], Pair.PAIR_TWO_ID: []}
        self.winner = None

    def play_card(self, player, card):
        if player in self.players:
            self.round_cards[player].append(card)
        else:
            raise Exception("Jogador não pertence a partida")

    def is_over(self):
        return len(self.round_cards[Pair.PAIR_ONE_ID]) == 3 and len(self.round_cards[Pair.PAIR_TWO_ID]) == 3

    def check_winner(self):
        card_check = CardCheck(self.round_cards)
        self.winner = card_check.get_winner()

    def __str__(self):
        return f"Vencedor da rodada: {self.winner.name}"


# MatchState, NormalMatch, TrucoMatch, SixMatch, NineMatch, TwelveMatch

class MatchState:
    def __init__(self, match):
        self.match = match

    def play_card(self, player, card):
        self.match.play_card(player, card)
        if self.match.is_over():
            self.match.check_winner()
            self.match.end_match()
            self.match = NormalMatch(self.match.players)
        return self.match


class NormalMatch(MatchState):
    def __init__(self, players):
        self.players = players
        self.round = Round(players)

    def play_card(self, player, card):
        self.round.play_card(player, card)
        if self.round.is_over():
            self.round.check_winner()
            self.match.end_match()
            self.match = NormalMatch(self.players)
        return self.match


class TrucoMatch(MatchState):
    def __init__(self, players):
        self.players = players
        self.round = Round(players)

    def play_card(self, player, card):
        self.round.play_card(player, card)
        if self.round.is_over():
            self.round.check_winner()
            self.match.end_match()
            self.match = NormalMatch(self.players)
        return self.match


class SixMatch(MatchState):
    def __init__(self, players):
        self.players = players
        self.round = Round(players)

    def play_card(self, player, card):
        self.round.play_card(player, card)
        if self.round.is_over():
            self.round.check_winner()
            self.match.end_match()
            self.match = NormalMatch(self.players)
        return self.match


class NineMatch(MatchState):
    def __init__(self, players):
        self.players = players
        self.round = Round(players)

    def play_card(self, player, card):
        self.round.play_card(player, card)
        if self.round.is_over():
            self.round.check_winner()
            self.match.end_match()
            self.match = NormalMatch(self.players)
        return self.match


class TwelveMatch(MatchState):
    def __init__(self, players):
        self.players = players
        self.round = Round(players)

    def play_card(self, player, card):
        self.round.play_card(player, card)
        if self.round.is_over():
            self.round.check_winner()
            self.match.end_match()
            self.match = NormalMatch(self.players)
        return self.match


