from card import Card
from random import randrange
import pygame

hand_asset = {
    "blank_card": pygame.image.load("sprites/blank-card.png"),
    "hand": pygame.image.load("sprites/hand.png"),
    "dealer_hand": pygame.image.load("sprites/dealer-hand.png"),
    "active_hand": pygame.image.load("sprites/active-hand.png")
}


class Hand:
    def __init__(self):
        self.cards_in_hand = []
        self.score = 0
        self.num_of_aces = 0
        self.finished = False

    def count_score(self):
        self.score = 0
        self.num_of_aces = 0

        for card in self.cards_in_hand:
            self.score += card.value
            if card.name == "ACE":
                self.num_of_aces += 1

        while self.score > 21 and self.num_of_aces > 0:
            self.score -= 10
            self.num_of_aces -= 1

    def draw_card(self):
        if len(Card.shoe) == 0:
            Card.shuffle_cards()
        drawn_card = Card.shoe.pop(randrange(len(Card.shoe)))
        self.cards_in_hand.append(drawn_card)
        self.count_score()


class PlayerHand(Hand):
    def __init__(self):
        super().__init__()
        self.winner = None
        self.splittable = None

    def count_score(self):
        super().count_score()

        self.splittable = False

        if len(self.cards_in_hand) >= 2:
            if self.cards_in_hand[-1].name == self.cards_in_hand[-2].name:
                self.splittable = True

    def split(self, _hand_list):
        new_hand = PlayerHand()
        new_hand.cards_in_hand.append(self.cards_in_hand.pop())

        new_hand.count_score()
        self.count_score()

        _hand_list.append(new_hand)


class DealerHand(Hand):
    def __init__(self):
        super().__init__()
        self.hidden = True
        
    def draw(self, window):
        win_w = window.get_width()
        win_h = window.get_height()

        font = pygame.font.SysFont("consolas", 20)
        black_color = (0, 0, 0)
        
        window.blit(hand_asset["dealer_hand"], (win_w - 150, win_h - 50))

        for c, card in enumerate(self.cards_in_hand):
            if c == 1 and self.hidden:
                window.blit(hand_asset["blank_card"], (win_w - 125, (win_h - 180) - c * 50))
                break
            window.blit(card.sprite, (win_w - 125, (win_h - 180) - c * 50))

        if not self.hidden:
            d_score_readout = font.render(str(self.score), True, black_color)
            window.blit(d_score_readout, (win_w - 140, win_h - 18))
