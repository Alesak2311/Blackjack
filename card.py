import pygame

card_asset = {
    "blank_card": pygame.image.load("sprites/blank-card.png"),
    "heart": pygame.transform.scale(pygame.image.load("sprites/heart.png"), (38, 38)),
    "diamond": pygame.transform.scale(pygame.image.load("sprites/diamond.png"), (38, 38)),
    "club": pygame.transform.scale(pygame.image.load("sprites/club.png"), (38, 38)),
    "spade": pygame.transform.scale(pygame.image.load("sprites/spade.png"), (38, 38))
}


class Card:
    COLORS = ("DIAMONDS", "HEARTS", "SPADES", "CLUBS")
    NAMES = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "JACK", "QUEEN", "KING", "ACE")
    # 
    # NAMES = ("3", )
    DECKS_IN_SHOE = 1
    shoe = []

    def __init__(self, name, color, value, _sprite):
        self.name = name
        self.color = color
        self.value = value
        self.sprite = _sprite

    @staticmethod
    def get_sprite(_asset, color, name):
        red_color = (255, 0, 0)
        black_color = (0, 0, 0)
        card_font = pygame.font.SysFont("consolas", 44)

        output = _asset["blank_card"].copy()
        if color == "DIAMONDS":
            font_color = red_color
            card_symbol = _asset["diamond"]
        elif color == "HEARTS":
            font_color = red_color
            card_symbol = _asset["heart"]
        elif color == "SPADES":
            font_color = black_color
            card_symbol = _asset["spade"]
        else:
            font_color = black_color
            card_symbol = _asset["club"]

        if name in ("JACK", "QUEEN", "KING", "ACE"):
            _text = card_font.render(name[0], True, font_color)
        else:
            _text = card_font.render(name, True, font_color)

        text_w = _text.get_width()
        text_h = _text.get_height()

        output.blit(_text, (10, 5))
        output.blit(_text, (90 - text_w, 145 - text_h))

        output.blit(card_symbol, (100 - 45, 8))
        output.blit(card_symbol, (5, 147 - text_h))

        return output

    @classmethod
    def shuffle_cards(cls):
        for deck in range(cls.DECKS_IN_SHOE):
            for color in cls.COLORS:
                for name in cls.NAMES:
                    if name == "ACE":
                        value = 11
                    elif name == "JACK" or name == "QUEEN" or name == "KING":
                        value = 10
                    else:
                        value = int(name)
                    img = Card.get_sprite(card_asset, color, name)
                    cls.shoe.append(Card(name, color, value, img))

    