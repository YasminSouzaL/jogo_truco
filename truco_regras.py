import pytest
from truco_game import Card, Deck, Hand, CardCheck, Player, Pair, Game, Match, Round, MatchState, NormalMatch, TrucoMatch, SixMatch, NineMatch, TwelveMatch

@pytest.fixture
def deck():
    Deck.instance = None
    return Deck.get_instance()

@pytest.fixture
def game():
    pairs = []

    game = TestGame(pairs)
    
    return game

class TestCard:
    
    @pytest.fixture
    def card(self):
        return Card("Copas", "3")

    def test_card_clone(self, card):
        new_card = card.clone("J")
        assert new_card.suit == card.suit
        assert new_card.value == "J"


class TestDeck:

    NUMBER_OF_CARDS_IN_TRUCO = 40

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

    def test_shuffle_without_a_card(self, deck):
        bottom_card = deck.get_bottom_card()
        try:
            deck.shuffle()
            shuffled = True
        except Exception:
            shuffled = False
        assert not shuffled


class TestHand:

    @pytest.fixture
    def hand(self, deck):
        cards = []
        for i in range(1, 4):
            cards.append(deck.get_bottom_card())
        return Hand(cards)

    @pytest.fixture
    def fixed_hand(self):
        self.card1 = Card("Espadas", "A")
        self.card2 = self.card1.clone("3")
        self.card3 = self.card1.clone("2")
        cards = []
        cards.append(self.card1)
        cards.append(self.card2)
        cards.append(self.card3)
        return Hand(cards)

    def test_throw_one_card(self, hand):
        assert len(hand.cards) == 3
        hand.throw_card()
        assert len(hand.cards) == 2

    def test_throw_two_card(self, hand):
        assert len(hand.cards) == 3
        hand.throw_card()
        hand.throw_card()
        assert len(hand.cards) == 1

    def test_throw_three_card(self, hand):  
        assert len(hand.cards) == 3
        hand.throw_card()
        hand.throw_card()
        hand.throw_card()
        assert len(hand.cards) == 0


    def test_throw_first_card(self, fixed_hand):
        fixed_hand.throw_card(1)
        assert self.card1 not in fixed_hand.cards

    def test_throw_second_card(self, fixed_hand):
        fixed_hand.throw_card(2)
        assert self.card2 not in fixed_hand.cards

    def test_throw_third_card(self, fixed_hand):
        fixed_hand.throw_card(3)
        assert self.card3 not in fixed_hand.cards

    def test_throw_card_on_position_out_of_range(self, fixed_hand):
        fixed_hand.throw_card(10)
        assert self.card1 not in fixed_hand.cards

    def test_throw_first_then_second_card(self, fixed_hand):
        fixed_hand.throw_card(1)
        assert self.card1 not in fixed_hand.cards
        fixed_hand.throw_card(2)
        assert self.card3 not in fixed_hand.cards

    def test_throw_first_then_third_card(self, fixed_hand):
        fixed_hand.throw_card(1)
        assert self.card1 not in fixed_hand.cards
        fixed_hand.throw_card(3)
        assert self.card2 not in fixed_hand.cards

    def test_throw_second_then_first_card(self, fixed_hand):
        fixed_hand.throw_card(2)
        assert self.card2 not in fixed_hand.cards
        fixed_hand.throw_card(1)
        assert self.card1 not in fixed_hand.cards

    def test_throw_second_then_third_card(self, fixed_hand):
        fixed_hand.throw_card(2)
        assert self.card2 not in fixed_hand.cards
        fixed_hand.throw_card(3)
        assert self.card1 not in fixed_hand.cards

    def test_throw_third_then_second_card(self, fixed_hand):
        fixed_hand.throw_card(3)
        assert self.card3 not in fixed_hand.cards
        fixed_hand.throw_card(2)
        assert self.card2 not in fixed_hand.cards

    def test_throw_third_then_first_card(self, fixed_hand):
        fixed_hand.throw_card(3)
        assert self.card3 not in fixed_hand.cards
        fixed_hand.throw_card(1)
        assert self.card1 not in fixed_hand.cards

class TestCardCheck:

    @pytest.fixture
    def suits(self):
        cards = {}
        cards['spades'] = Card("Espadas")
        cards['clubs'] = Card("Paus")
        cards['hearts'] = Card("Copas")
        cards['diamonds'] = Card("Ouros")

        return cards

    @pytest.fixture
    def shackles(self, suits):
        hearts = suits['hearts'].clone("7")
        zap = suits['clubs'].clone("4")
        diamonds = suits['diamonds'].clone("7")
        ace_of_spades = suits['spades'].clone("A")
        
        shackles = []
        shackles.append(zap)
        shackles.append(hearts)
        shackles.append(diamonds)
        shackles.append(ace_of_spades)
        
        return shackles

    def get_winner_on_card_check(self, pair_one, pair_two):
        round_cards = {'pair_one': pair_one, 'pair_two':pair_two}
        card_check = CardCheck(round_cards)
        result = card_check.get_winner()
        return result

    def test_card_check_with_all_shackles(self, shackles):
        
        pair_one = [shackles[0], shackles[3]]
        pair_two = [shackles[1], shackles[2]]
        
        expected = 'pair_one'
        result = self.get_winner_on_card_check(pair_one, pair_two)

        assert result == 'pair_one'

    def test_card_check_with_one_shackle_on_each_pair(self, shackles, suits):
        normal_card = suits['spades'].clone("3")
        pair_one = [shackles[1], normal_card]
        pair_two = [shackles[3], normal_card] 

        expected = 'pair_one'
        result = self.get_winner_on_card_check(pair_one, pair_two)

        assert result == 'pair_one'

    def test_card_check_without_shackles(self, suits):
        card1 = suits['spades'].clone("3") 
        card2 = suits['clubs'].clone("J") 
        card3 = suits['diamonds'].clone("2") 
        card4 = suits['hearts'].clone("A") 
        
        pair_one = [card1, card2]
        pair_two = [card3, card4] 

        expected = 'pair_one'
        result = self.get_winner_on_card_check(pair_one, pair_two)

        assert result == 'pair_one'

class TestRound:

    @pytest.fixture
    def round(self, game):
        match = Match(game)
        round = Round(match)

        return round

    def test_add_round_card(self, round):
        player = round.match.game.pairs[0].players['player1']
        card = Card("Paus", "4")
        round.add_round_card(player, card)
        result = round.round_cards
        expected = {player: card}

        assert result == expected

    def add_round_cards_to_players(self, round):
        player = round.match.game.pairs[0].players['player1']
        card = Card("Paus", "4")
        round.add_round_card(player, card)

        player = round.match.game.pairs[0].players['player2']
        card = Card("Espadas", "A")
        round.add_round_card(player, card)

        player = round.match.game.pairs[1].players['player1']
        card = Card("Copas", "7")
        round.add_round_card(player, card)

        player = round.match.game.pairs[1].players['player2']
        card = Card("Ouros", "7")
        round.add_round_card(player, card)
        
    def test_end_round(self, round):
        self.add_round_cards_to_players(round)
        result_winner = round.end_round()
        expected_winner = 'pair_one'

        assert result_winner is expected_winner
class TestGame:
    def __init__(self, players):
        self.players  = players
        self.score = {Pair.PAIR_ONE_ID: 0, Pair.PAIR_TWO_ID: 0}
        self.current_match = None  # Initialize current_match in the constructor
        
    def start_match(self):
        match = Match(self.players)
        return match

    def test_start_match(self):  # Remove "game" argument, as it's not used
        self.start_match()  # Call start_match to initiate a match
        assert self.current_match is not None  # Assert that a match object is created

    def test_end_match(self):
        self.start_match()  # Start the match
        self.end_match()  # End the match
        assert self.current_match is None

    def end_match(self):
        self.current_match = None
    
    def is_over(self):
        return self.score[Pair.PAIR_ONE_ID] >= 12 or self.score[Pair.PAIR_TWO_ID] >= 12


class TestMatch:

    @pytest.fixture
    def match(self, game):
        match = Match(game)

        return match

    def test_start_match(self, match, deck):
        match.start_match()        
        assert len(deck.cards) == (40 - 12)

    def test_end_current_round(self, match):
        TestRound().add_round_cards_to_players(match.current_round)
        match.end_current_round()
        assert len(match.rounds) == 1
        TestRound().add_round_cards_to_players(match.current_round)
        match.end_current_round()
        assert len(match.rounds) == 2

    def test_normal_match_raise_match(self, match):
        
        normalMatch = NormalMatch(match)
        normalMatch.raise_match()
        result_points = match.state.get_points()
        expected = 3

        assert result_points == expected

    def test_truco_match_raise_match(self, match):
        
        trucoMatch = TrucoMatch(match)
        trucoMatch.raise_match()
        result_points = match.state.get_points()
        expected = 6

        assert result_points == expected

    def test_six_match_raise_match(self, match):
        
        sixMatch = SixMatch(match)
        sixMatch.raise_match()
        result_points = match.state.get_points()
        expected = 9

        assert result_points == expected

    def test_nine_match_raise_match(self, match):
        
        nineMatch = NineMatch(match)
        nineMatch.raise_match()
        result_points = match.state.get_points()
        expected = 12

        assert result_points == expected

    def test_twelve_match_raise_match(self, match):
        with pytest.raises(Exception):        
            twelveMatch = TwelveMatch(match)
            twelveMatch.raise_match()
            result_points = match.state.get_points()

class TestPair:
        @pytest.fixture
        def pair(self):
            pair = Pair("pair_one", "player1", "player2")
    
            return pair
    
        def test_get_points(self, pair):
            pair.points = 5
            result = pair.get_points()
            expected = 5
    
            assert result == expected
    
        def test_get_points_with_no_points(self, pair):
            result = pair.get_points()
            expected = 0
    
            assert result == expected
    
        def test_get_points_with_negative_points(self, pair):
            pair.points = -5
            result = pair.get_points()
            expected = 0
    
            assert result == expected
    
        def test_get_points_with_points_greater_than_twelve(self, pair):
            pair.points = 15
            result = pair.get_points()
            expected = 12
    
            assert result == expected
    
        def test_get_points_with_points_equal_to_twelve(self, pair):
            pair.points = 12
            result = pair.get_points()
            expected = 12
    
            assert result == expected
    
        def test_get_points_with_points_less_than_twelve(self, pair):
            pair.points = 10
            result = pair.get_points()
            expected = 10
    
            assert result == expected


    