import pygame

OKNO_SZER = 1024
OKNO_WYS = 900
FPS = 60

pygame.init()
okienko = pygame.display.set_mode((OKNO_SZER, OKNO_WYS), 0, 32)
pygame.display.set_caption("Piwkorzyki")
zegarek = pygame.time.Clock()

tlo = pygame.image.load("tlo.png")

tytul_image = pygame.image.load("tytul.png")

class Przycisk:
    def __init__(self, x_cord, y_cord, file_name, new_width, new_height):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.button_image = pygame.image.load(f"{file_name}.png")
        self.button_image = pygame.transform.scale(self.button_image, (new_width, new_height))
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, new_width, new_height)
        
    def klik(self):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                return True
    
    def wyswietl(self, window):
        window.blit(self.button_image, (self.x_cord, self.y_cord))


przycisk_szer = 400
przycisk_wys = 120
odstepy_y = 30


tytul_y = 150
pierwszy_przycisk_y = tytul_y + 150  
odstepy_miedzy_przyciskami = przycisk_wys + odstepy_y


przycisk_graj = Przycisk((OKNO_SZER - przycisk_szer) // 2, pierwszy_przycisk_y, "przycisk_graj3", przycisk_szer, przycisk_wys)
przycisk_zasady = Przycisk((OKNO_SZER - przycisk_szer) // 2, pierwszy_przycisk_y + odstepy_miedzy_przyciskami, "przycisk_zasady3", przycisk_szer, przycisk_wys)
przycisk_ustawienia = Przycisk((OKNO_SZER - przycisk_szer) // 2, pierwszy_przycisk_y + 2 * odstepy_miedzy_przyciskami, "przycisk_ustawienia3", przycisk_szer, przycisk_wys)
przycisk_wyjdz = Przycisk((OKNO_SZER - przycisk_szer) // 2, pierwszy_przycisk_y + 3 * odstepy_miedzy_przyciskami, "przycisk_wyjdz3", przycisk_szer, przycisk_wys)


current_screen = "menu"

def pokaz_zasady(window):
    window.fill((0, 0, 0))  
    font = pygame.font.Font(None, 36)
    tekst = [
        "Zasady gry:",
        "1. Zasada 1",
        "2. Zasada 2",
        "3. Zasada 3",
        "Kliknij, aby wrócić do menu"
    ]
    for i, line in enumerate(tekst):
        rendered_text = font.render(line, True, (255, 255, 255))
        window.blit(rendered_text, (50, 50 + i * 40))


def pokaz_ustawienia(window):
    window.fill((0, 0, 0))  
    font = pygame.font.Font(None, 36)
    tekst = [
        "Ustawienia:",
        "1. Ustawienie 1",
        "2. Ustawienie 2",
        "3. Ustawienie 3",
        "Kliknij, aby wrócić do menu"
    ]
    for i, line in enumerate(tekst):
        rendered_text = font.render(line, True, (255, 255, 255))
        window.blit(rendered_text, (50, 50 + i * 40))

graj = True
while graj:
    for zdarzenie in pygame.event.get():
        if zdarzenie.type == pygame.QUIT:
            graj = False
        elif zdarzenie.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "menu":
                if przycisk_graj.klik():
                    pass  
                elif przycisk_zasady.klik():
                    current_screen = "zasady"
                elif przycisk_ustawienia.klik():
                    current_screen = "ustawienia"
                elif przycisk_wyjdz.klik():
                    graj = False
            elif current_screen in ["zasady", "ustawienia"]:
                current_screen = "menu"
    
    if current_screen == "menu":  
        okienko.blit(tlo, (0, 0))
        tytul_rect = tytul_image.get_rect(center=(OKNO_SZER // 2, tytul_y))  
        okienko.blit(tytul_image, tytul_rect)
        przycisk_graj.wyswietl(okienko)
        przycisk_zasady.wyswietl(okienko)
        przycisk_ustawienia.wyswietl(okienko)
        przycisk_wyjdz.wyswietl(okienko)
    elif current_screen == "zasady":
        pokaz_zasady(okienko)
    elif current_screen == "ustawienia":
        pokaz_ustawienia(okienko)
 
    pygame.display.update()
    zegarek.tick(FPS)
 
pygame.quit()
