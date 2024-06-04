import pygame

OKNO_SZER = 1024
OKNO_WYS = 900
FULLSCREEN_SZER = 1920
FULLSCREEN_WYS = 1080
FPS = 60

pygame.init()
okienko = pygame.display.set_mode((OKNO_SZER, OKNO_WYS), 0, 32)
pygame.display.set_caption("Piwkorzyki")
zegarek = pygame.time.Clock()

tlo = pygame.image.load("tlo.png")
tlo_fullscreen = pygame.image.load("tlo2.png")

tytul_image = pygame.image.load("tytul2.png")
zasady_tytul_image = pygame.image.load("zasady_tytul2.png")
ustawienia_tytul_image = pygame.image.load("ustawienia_tytul2.png")

class Przycisk:
    def __init__(self, x_cord, y_cord, file_name, new_width, new_height):
        self.initial_x = x_cord
        self.initial_y = y_cord
        self.initial_width = new_width
        self.initial_height = new_height
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
    
    def skaluj(self, new_width, new_height):
        self.button_image = pygame.transform.scale(self.button_image, (new_width, new_height))
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, new_width, new_height)
        
    def resetuj(self):
        self.x_cord = self.initial_x
        self.y_cord = self.initial_y
        self.skaluj(self.initial_width, self.initial_height)

def ustawienia_przyciski(i_szerokosc, odstep_y, przycisk_szer, przycisk_wys):
    przyciski_y = tytul_y + 150
    return [
        Przycisk((i_szerokosc - przycisk_szer) // 2, przyciski_y, "przycisk_graj3", przycisk_szer, przycisk_wys),
        Przycisk((i_szerokosc - przycisk_szer) // 2, przyciski_y + odstep_y, "przycisk_zasady3", przycisk_szer, przycisk_wys),
        Przycisk((i_szerokosc - przycisk_szer) // 2, przyciski_y + 2 * odstep_y, "przycisk_ustawienia3", przycisk_szer, przycisk_wys),
        Przycisk((i_szerokosc - przycisk_szer) // 2, przyciski_y + 3 * odstep_y, "przycisk_wyjdz3", przycisk_szer, przycisk_wys),
    ]

przycisk_szer = 400
przycisk_wys = 120
odstepy_y = 30
tytul_y = 150
full_screen = False

przyciski_menu = ustawienia_przyciski(OKNO_SZER, odstepy_y + przycisk_wys, przycisk_szer, przycisk_wys)

przycisk_pelny_ekran = Przycisk((OKNO_SZER - 200) // 2, (OKNO_WYS - 80) // 2, "fullscreen", 200, 200)

current_screen = "menu"

def pokaz_zasady(window):
    window.blit(tlo, (0, 0))
    zasady_tytul_rect = zasady_tytul_image.get_rect(center=(OKNO_SZER // 2, 50))
    window.blit(zasady_tytul_image, zasady_tytul_rect)
    
    font = pygame.font.Font(None, 36)
    tekst = [
        "1. Zasada 1",
        "2. Zasada 2",
        "3. Zasada 3",
    ]
    for i, line in enumerate(tekst):
        rendered_text = font.render(line, True, (255, 255, 255))
        window.blit(rendered_text, (50, 150 + i * 40))
    
    powrot_text = font.render("Kliknij, aby wrócić do menu", True, (255, 255, 255))
    window.blit(powrot_text, (OKNO_SZER // 2 - powrot_text.get_width() // 2, OKNO_WYS - 40))

def pokaz_zasady_fullscreen(window):
    window.blit(tlo_fullscreen, (0, 0))
    zasady_tytul_image_fs = pygame.transform.scale(zasady_tytul_image, (FULLSCREEN_SZER // 2, FULLSCREEN_WYS // 10))
    zasady_tytul_rect = zasady_tytul_image_fs.get_rect(center=(FULLSCREEN_SZER // 2, FULLSCREEN_WYS // 10))
    window.blit(zasady_tytul_image_fs, zasady_tytul_rect)

    font = pygame.font.Font(None, 72)
    tekst = [
        "1. Zasada 1",
        "2. Zasada 2",
        "3. Zasada 3",
    ]
    for i, line in enumerate(tekst):
        rendered_text = font.render(line, True, (255, 255, 255))
        window.blit(rendered_text, (FULLSCREEN_SZER // 4, FULLSCREEN_WYS // 4 + i * 80))
    
    powrot_text = font.render("Kliknij, aby wrócić do menu", True, (255, 255, 255))
    window.blit(powrot_text, (FULLSCREEN_SZER // 2 - powrot_text.get_width() // 2, FULLSCREEN_WYS - 100))

def pokaz_ustawienia(window):
    window.blit(tlo, (0, 0))
    ustawienia_tytul_rect = ustawienia_tytul_image.get_rect(center=(OKNO_SZER // 2, 50))
    window.blit(ustawienia_tytul_image, ustawienia_tytul_rect)
    
    font = pygame.font.Font(None, 36)
    tekst = [
        ""
    ]
    for i, line in enumerate(tekst):
        rendered_text = font.render(line, True, (255, 255, 255))
        window.blit(rendered_text, (50, 150 + i * 40))
    
    przycisk_pelny_ekran.wyswietl(window)
    
    napis = font.render("FULLSCREEN", True, (255, 255, 255))
    window.blit(napis, ((OKNO_SZER - napis.get_width()) // 2, (OKNO_WYS - 80) // 2 + 90))

    powrot_text = font.render("Kliknij, aby wrócić do menu", True, (255, 255, 255))
    window.blit(powrot_text, (OKNO_SZER // 2 - powrot_text.get_width() // 2, OKNO_WYS - 40))

def pokaz_ustawienia_fullscreen(window):
    window.blit(tlo_fullscreen, (0, 0))
    ustawienia_tytul_image_fs = pygame.transform.scale(ustawienia_tytul_image, (FULLSCREEN_SZER // 2, FULLSCREEN_WYS // 10))
    ustawienia_tytul_rect = ustawienia_tytul_image_fs.get_rect(center=(FULLSCREEN_SZER // 2, FULLSCREEN_WYS // 10))
    window.blit(ustawienia_tytul_image_fs, ustawienia_tytul_rect)
    
    font = pygame.font.Font(None, 72)
    tekst = [
        ""
    ]
    for i, line in enumerate(tekst):
        rendered_text = font.render(line, True, (255, 255, 255))
        window.blit(rendered_text, (FULLSCREEN_SZER // 4, FULLSCREEN_WYS // 4 + i * 80))
    
    przycisk_pelny_ekran.skaluj(300, 300)
    przycisk_pelny_ekran.x_cord = (FULLSCREEN_SZER - 300) // 2
    przycisk_pelny_ekran.y_cord = (FULLSCREEN_WYS - 300) // 2
    przycisk_pelny_ekran.wyswietl(window)

    napis = font.render("FULLSCREEN", True, (255, 255, 255))
    window.blit(napis, ((FULLSCREEN_SZER - napis.get_width()) // 2, (FULLSCREEN_WYS - 300) // 2 + 350))

    powrot_text = font.render("Kliknij, aby wrócić do menu", True, (255, 255, 255))
    window.blit(powrot_text, (FULLSCREEN_SZER // 2 - powrot_text.get_width() // 2, FULLSCREEN_WYS - 100))

def pokaz_menu(window):
    window.blit(tlo, (0, 0))
    tytul_rect = tytul_image.get_rect(center=(OKNO_SZER // 2, tytul_y))
    window.blit(tytul_image, tytul_rect)
    for przycisk in przyciski_menu:
        przycisk.wyswietl(window)

def pokaz_menu_fullscreen(window):
    window.blit(tlo_fullscreen, (0, 0))
    tytul_image_fs = pygame.transform.scale(tytul_image, (FULLSCREEN_SZER // 2, FULLSCREEN_WYS // 10))
    tytul_rect = tytul_image_fs.get_rect(center=(FULLSCREEN_SZER // 2, FULLSCREEN_WYS // 10))
    window.blit(tytul_image_fs, tytul_rect)
    for przycisk in przyciski_menu:
        przycisk.wyswietl(window)

graj = True
while graj:
    for zdarzenie in pygame.event.get():
        if zdarzenie.type == pygame.QUIT:
            graj = False
        elif zdarzenie.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "menu":
                if przyciski_menu[0].klik():
                    pass  
                elif przyciski_menu[1].klik():
                    current_screen = "zasady"
                elif przyciski_menu[2].klik():
                    current_screen = "ustawienia"
                elif przyciski_menu[3].klik():
                    graj = False
            elif current_screen == "ustawienia":
                if przycisk_pelny_ekran.klik():
                    if not full_screen:
                        okienko = pygame.display.set_mode((FULLSCREEN_SZER, FULLSCREEN_WYS), pygame.FULLSCREEN)
                        przyciski_menu = ustawienia_przyciski(FULLSCREEN_SZER, odstepy_y + przycisk_wys, przycisk_szer * 1.5, przycisk_wys * 1.5)
                        przycisk_pelny_ekran.skaluj(300, 300)
                        przycisk_pelny_ekran.x_cord = (FULLSCREEN_SZER - 300) // 2
                        przycisk_pelny_ekran.y_cord = (FULLSCREEN_WYS - 300) // 2
                        full_screen = True
                    else:
                        okienko = pygame.display.set_mode((OKNO_SZER, OKNO_WYS), 0, 32)
                        przyciski_menu = ustawienia_przyciski(OKNO_SZER, odstepy_y + przycisk_wys, przycisk_szer, przycisk_wys)
                        przycisk_pelny_ekran.resetuj()
                        full_screen = False
                else:
                    current_screen = "menu"
            elif current_screen == "zasady":
                current_screen = "menu"
    
    if current_screen == "menu":  
        if full_screen:
            pokaz_menu_fullscreen(okienko)
        else:
            pokaz_menu(okienko)
    elif current_screen == "zasady":
        if full_screen:
            pokaz_zasady_fullscreen(okienko)
        else:
            pokaz_zasady(okienko)
    elif current_screen == "ustawienia":
        if full_screen:
            pokaz_ustawienia_fullscreen(okienko)
        else:
            pokaz_ustawienia(okienko)
 
    pygame.display.update()
    zegarek.tick(FPS)
 
pygame.quit()
