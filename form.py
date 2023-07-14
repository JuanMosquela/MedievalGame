import pygame
from button import Button


class TextInput:
    def __init__(self, x, y, width, height, max_length):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.font = pygame.font.SysFont("white", 50)
        self.max_length = max_length
        self.min_characters = 4
        self.done = False
        self.accept_button = Button("Accept", (255,255,255), (255,255,255))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < self.max_length:
                    self.text += event.unicode

    def check_button_click(self, event):


        if event.type == pygame.MOUSEBUTTONDOWN:           
            

            if self.accept_button.rect.collidepoint(event.pos[0] - self.accept_button.button_x, event.pos[1] - self.accept_button.button_y ) and len(self.text) >= self.min_characters:
                self.done = True
                # Realiza la acción deseada cuando se presiona el botón "Accept"
                # Por ejemplo, puedes imprimir el texto ingresado por el usuario
                print("Texto ingresado:", self.text)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        rendered_text = self.font.render(self.text, True, (255, 255, 255))

        self.accept_button.draw(screen)

        screen.blit(rendered_text, (self.rect.x + 5, self.rect.y + 5))
