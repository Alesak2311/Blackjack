import pygame
from sys import exit
from player import Player
from hand import PlayerHand, DealerHand
from tools import blit_text_center

pygame.font.init()
MAIN_FONT = pygame.font.SysFont("consolas", 20)

WIDTH = 1000
HEIGHT = 500

BG_COLOR = (55, 185, 30)
BLACK = (0, 0, 0)

asset = {
    "blank_card": pygame.image.load("sprites/blank-card.png"),
    "hand": pygame.image.load("sprites/hand.png"),
    "dealer_hand": pygame.image.load("sprites/dealer-hand.png"),
    "active_hand": pygame.image.load("sprites/active-hand.png"),
    "heart": pygame.transform.scale(pygame.image.load("sprites/heart.png"), (38, 38)),
    "diamond": pygame.transform.scale(pygame.image.load("sprites/diamond.png"), (38, 38)),
    "club": pygame.transform.scale(pygame.image.load("sprites/club.png"), (38, 38)),
    "spade": pygame.transform.scale(pygame.image.load("sprites/spade.png"), (38, 38))
}

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")

clock = pygame.time.Clock()


def draw(_player, _dealer_hand, _money, active=None):
    window.fill(BG_COLOR)

    _player.draw(window, active)

    _dealer_hand.draw(window)

    money_text = MAIN_FONT.render(f"Money: {_money}", True, BLACK)
    text_w = money_text.get_width()
    window.blit(money_text, (WIDTH - text_w, 0))

    pygame.display.update()


def choose_bet(_hand_list, _dealer_hand, _money):
    _bet = 100
    _cont = False
    while not _cont:
        clock.tick(15)

        draw(player, _dealer_hand, _money)

        blit_text_center(window, f"Choose your bet: {_bet}")

        for _event in pygame.event.get():
            if _event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if _event.type == pygame.KEYDOWN:
                _keys = pygame.key.get_pressed()

                if _keys[pygame.K_UP]:
                    if _bet < _money:
                        _bet += 100
                    break

                if _keys[pygame.K_DOWN]:
                    if _bet > 100:
                        _bet -= 100
                    break

                if _keys[pygame.K_SPACE]:
                    _cont = True
    return _bet


def player_loop(_hand_list):
    for active, _hand in enumerate(_hand_list):
        while not _hand.finished:
            clock.tick(15)

            draw(player, dealer_hand, player.money, active)
            _instr_text = MAIN_FONT.render('Press "SPACE" to get another card|Press "BACKSPACE" to finish hand',
                                           True, BLACK)
            window.blit(_instr_text, (2, 2))
            pygame.display.update()

            for _event in pygame.event.get():
                if _event.type == pygame.QUIT:
                    # _run = False
                    # _hand.finished = True
                    pygame.quit()
                    exit()

                if _event.type == pygame.KEYDOWN:
                    _keys = pygame.key.get_pressed()
                    if _keys[pygame.K_SPACE]:
                        _hand.draw_card()
                        break

                    if _keys[pygame.K_BACKSPACE]:
                        _hand.finished = True
                        draw(player, dealer_hand, player.money)
                        break

                    if _hand.splittable:
                        if _keys[pygame.K_f]:
                            _hand.split(_hand_list)
                            break

            if _hand.score > 21:
                _hand.score = 0
                _hand.finished = True


def dealer_plays(_player, _dealer_hand):
    _dealer_hand.hidden = False
    draw(_player, dealer_hand, player.money)
    while not _dealer_hand.finished:
        if _dealer_hand.score > 21:
            _dealer_hand.score = 0
            _dealer_hand.finished = True
            break
        if _dealer_hand.score > 16:
            _dealer_hand.finished = True
            break
        _dealer_hand.draw_card()
    draw(_player, dealer_hand, player.money)


player = Player(2000)

run = True
while run:
    dealer_hand = DealerHand()
    player.hands = [PlayerHand()]

    bet = choose_bet(player.hands, dealer_hand, player.money)

    draw(player, dealer_hand, player.money)

    dealer_hand.draw_card()
    dealer_hand.draw_card()
    player.hands[-1].draw_card()
    player.hands[-1].draw_card()

    draw(player, dealer_hand, player.money)

    # player loop
    player_loop(player.hands)

    # dealer plays
    dealer_plays(player, dealer_hand)

    # count score
    for h, hand in enumerate(player.hands):
        if hand.score > dealer_hand.score:
            hand.winner = "Winner"
            player.money += bet
        else:
            hand.winner = "Loser"
            player.money -= bet

        draw(player, dealer_hand, player.money)

        text = MAIN_FONT.render(hand.winner, True, BLACK)
        text.get_width()
        window.blit(text, (h*150 + 140 - text.get_width(), HEIGHT - 18))

        instr_text = MAIN_FONT.render('Press "SPACE" to play again', True, BLACK)
        window.blit(instr_text, (2, 2))
        pygame.display.update()

    cont = False
    while not cont:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    cont = True
                    break

    if player.money == 0:
        clock.tick(30)

        draw(player, dealer_hand, player.money)
        lose_text = MAIN_FONT.render(f"Game over with {player.money} money", True, BLACK)
        lose_text_w = lose_text.get_width()
        lose_text_h = lose_text.get_height()
        lose_text_pos = ((WIDTH - lose_text_w) / 2, (HEIGHT - lose_text_h) / 2)
        window.blit(lose_text, lose_text_pos)
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
