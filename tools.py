import pygame


def blit_text_center(window, text):
    font = pygame.font.SysFont("consolas", 20)
    black_color = (0, 0, 0)

    win_w = window.get_width()
    win_h = window.get_height()

    text = font.render(text, True, black_color)

    text_w = text.get_width()
    text_h = text.get_height()

    text_pos = (
        (win_w - text_w) / 2,
        (win_h - text_h) / 2
    )

    window.blit(text, text_pos)
    pygame.display.update()
