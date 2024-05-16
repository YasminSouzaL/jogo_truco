# -*- coding: utf-8 -*- 

import random

class Card:
    """Prototype class for Card"""
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
    """ Represents the card check """
    SHACKLES = {'zap': Card("Paus", "4"),
                'hearts': Card("Copas", "7"),
                'diamonds': Card("Ouros", "7"),
                'ace_of_spades': Card("Espadas", "A")
                }

    CARDS_VALUES = {
        '3': 10,
        '2': 9,
        'A': 8,
        'K': 7,
        'J': 6,
        'Q': 5,
        '7': 4,
        '6': 3,
        '5': 2,
        '4': 1
    }

    def __init__(self, round_cards):
        self.round_cards = round_cards
        self.winner = self.check_winner_round()

    def get_winner(self):
        return self.winner

    def calculate_scores(self):
        # Initialize or check keys here if necessary
        card_check = CardCheck(self.round_cards)
        # Continue with the rest of the logic to calculate scores

    def check_winner_round(self):
        winners_pairs = []

        pair_one_winner = self.check_shackles(self.round_cards.get(Pair.PAIR_ONE_ID, []))
        winners_pairs.append(pair_one_winner)
        pair_two_winner = self.check_shackles(self.round_cards.get(Pair.PAIR_TWO_ID, []))
        winners_pairs.append(pair_two_winner)

        if 'pair_one' not in self.round_cards:
            self.round_cards['pair_one'] = []
        if 'pair_two' not in self.round_cards:
            self.round_cards['pair_two'] = []

        winner_card = self.check_shackles(winners_pairs)
        if winner_card in self.round_cards[Pair.PAIR_ONE_ID]:
            winner = Pair.PAIR_ONE_ID
        else:
            winner = Pair.PAIR_TWO_ID
        return winner

    def check_shackles(self, cards):
        if len(cards) < 2:
            return None

        fst_card_is_shackle = self.check_if_is_shackle(cards[0])
        snd_card_is_shackle = self.check_if_is_shackle(cards[1])
        if fst_card_is_shackle and snd_card_is_shackle:
            winner_card = self.get_shackle_winner(cards)
        elif not snd_card_is_shackle and fst_card_is_shackle:
            winner_card = cards[0]
        elif not fst_card_is_shackle and snd_card_is_shackle:
            winner_card = cards[1]
        else:
            winner_card = self.get_winner_without_shackles(cards)

        return winner_card

    def check_if_is_shackle(self, card):
        if card is None:
            return False

        zap = card.value == self.SHACKLES['zap'].value and card.suit == self.SHACKLES['zap'].suit
        hearts = card.value == self.SHACKLES['hearts'].value and card.suit == self.SHACKLES['hearts'].suit
        diamonds = card.value == self.SHACKLES['diamonds'].value and card.suit == self.SHACKLES['diamonds'].suit
        ace_of_spades = card.value == self.SHACKLES['ace_of_spades'].value and card.suit == self.SHACKLES[
            'ace_of_spades'].suit

        return zap or hearts or diamonds or ace_of_spades

    def get_winner_without_shackles(self, cards):
        if not cards or len(cards) < 2 or cards[0] is None or cards[1] is None:
            return None
        first_card = cards[0].value
        second_card = cards[1].value
        if self.CARDS_VALUES[first_card] > self.CARDS_VALUES[second_card]:
            winner_card = cards[0]
        else:
            winner_card = cards[1]

        return winner_card

    def get_shackle_winner(self, cards):
        if not cards or len(cards) < 2:
            return None

        first_card_shackle = self.get_shackle(cards[0])
        second_card_shackle = self.get_shackle(cards[1])

        if self.CARDS_VALUES[first_card_shackle] > self.CARDS_VALUES[second_card_shackle]:
            winner_card = cards[0]
        else:
            winner_card = cards[1]

        return winner_card

    def get_shackle(self, card):
        if card.value == self.SHACKLES['zap'].value and card.suit == self.SHACKLES['zap'].suit:
            return self.SHACKLES['zap'].value
        elif card.value == self.SHACKLES['hearts'].value and card.suit == self.SHACKLES['hearts'].suit:
            return self.SHACKLES['hearts'].value
        elif card.value == self.SHACKLES['diamonds'].value and card.suit == self.SHACKLES['diamonds'].suit:
            return self.SHACKLES['diamonds'].value
        elif card.value == self.SHACKLES['ace_of_spades'].value and card.suit == self.SHACKLES['ace_of_spades'].suit:
            return self.SHACKLES['ace_of_spades'].value
        else:
            raise Exception("Carta não é uma manilha")

    def calculate_points(self, cards):
        if len(cards) < 3:
            return 0

        return (self.CARDS_VALUES.get(cards[0].value, 0) +
                self.CARDS_VALUES.get(cards[1].value, 0) +
                self.CARDS_VALUES.get(cards[2].value, 0))


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
    
#MatchState, NormalMatch, TrucoMatch, SixMatch, NineMatch, TwelveMatch

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