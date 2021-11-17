import pygame
from hand import PlayerHand

hand_asset = {
    "blank_card": pygame.image.load("sprites/blank-card.png"),
    "hand": pygame.image.load("sprites/hand.png"),
    "dealer_hand": pygame.image.load("sprites/dealer-hand.png"),
    "active_hand": pygame.image.load("sprites/active-hand.png")
}


class Player:
    def __init__(self, money):
        self.money = money
        self.hands = [PlayerHand()]
        self.bet = 0

    def draw(self, window, active):
        black_color = (0, 0, 0)
        font = pygame.font.SysFont("consolas", 20)

        win_h = window.get_height()

        for h, hand in enumerate(self.hands):
            hand_pos = (h * 150, win_h - 50)
            if h == active:
                window.blit(hand_asset["active_hand"], hand_pos)
            else:
                window.blit(hand_asset["hand"], hand_pos)

            score_readout = font.render(str(hand.score), True, black_color)
            window.blit(score_readout, (h * 150 + 10, win_h - 18))

            if hand.splittable:
                split_text = font.render('You can split this hand by pressing "F"', True, black_color)
                window.blit(split_text, (2, split_text.get_height() + 2))

            for c, card in enumerate(hand.cards_in_hand):
                card_pos = (h * 150 + 25, (win_h - 180) - c * 50)
                window.blit(card.sprite, card_pos)

    def count_score(self, _dealer_hand):
        for hand in self.hands:
            hand.winner = hand.score > _dealer_hand.score
