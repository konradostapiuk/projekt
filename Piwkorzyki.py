# Import niezbędnych rzeczy
import pygame
import sys
import math
import numpy as np
from pygame.locals import *
import random

# Rozmiary okna menu
OKNO_SZER = 1024
OKNO_WYS = 1024
FULLSCREEN_SZER = 1920
FULLSCREEN_WYS = 1080
FPS = 60

# Rozmiary planszy
BOARD_WIDTH = 15
BOARD_HEIGHT = 10
CELL_SIZE = 70

# Rozmiary okna
WINDOW_WIDTH = BOARD_WIDTH * CELL_SIZE
WINDOW_HEIGHT = BOARD_HEIGHT * CELL_SIZE

# Stworzenie okna
pygame.init()
okienko = pygame.display.set_mode((OKNO_SZER, OKNO_WYS), 0, 32)
pygame.display.set_caption("Piwkorzyki")
zegarek = pygame.time.Clock()

# Czcionka
moja_czcionka = "pricedown bl.otf"
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Wyciszenie gry wyłączone przy otwieraniu aplikacji
wyciszenie = False

# Załadowanie wszystkich potrzebnych teł, obiektów graficznych etc.
tlo = pygame.image.load("tlo.png")
tlo_fullscreen = pygame.image.load("tlo2.png")
tlo_zasady = pygame.image.load("tlo_zasady.png")
tlo_zasady2 = pygame.transform.scale(tlo_zasady, (1920, 1080))
tlo_ustawienia = pygame.image.load("tlo_ustawienia.png")
tlo_ustawienia2 = pygame.transform.scale(tlo_ustawienia, (1920, 1080))
tlo_pauza = pygame.image.load("tlo_pauza.jpg")
tlo_pauza = pygame.transform.scale(tlo_pauza, (WINDOW_WIDTH, WINDOW_HEIGHT+50))
tytul_image = pygame.image.load("tytul2.png")
tlo_koniec = pygame.image.load("piwa.jpg")
tlo_koniec = pygame.transform.scale(tlo_koniec, (400, 300))
tlo_intro = pygame.image.load("intro.png")
tlo_wybor = pygame.image.load("tlo_wybor.png")
tlo_wybor2 = pygame.transform.scale(tlo_wybor, (1920,1080))
ball_images = [
    'pilka.png',
    'pilka2.png',
    'pilka3.png',
    'pilka4.png',
    'pilka5.png',
    'pilka6.png',
    'pilka7.png',
    'pilka8.png'
]

# Dźwięki
uderzenie_sfx = pygame.mixer.Sound("uderzenie.mp3")
intro_sfx = pygame.mixer.Sound("intro.mp3")
gol_sfx = pygame.mixer.Sound("gol.mp3")
piosenka_sfx = pygame.mixer.Sound("piosenka.mp3")

# Definiowanie kolorów
BIALY = (255, 255, 255)
CZARNY = (0, 0, 0)
CZERWONY = (255, 0, 0)
NIEBIESKI = (0, 0, 255)
ZIELONY = (0, 255, 0)

# Włączenie ekranu startowego
def intro() -> None:
    intro_active = True
    intro_sfx.play()
    while intro_active:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                intro_active = False
                pygame.mixer.stop()
                
        okienko.blit(tlo_intro, (0, 0))
        intro_text = small_font.render("Gra zawiera obrazy wygenerowane przy pomocy sztucznej inteligencji.", True, BIALY)
        intro_text_rect = intro_text.get_rect(center=(OKNO_SZER / 2, OKNO_WYS - 100))
        okienko.blit(intro_text, intro_text_rect)
        skip_text = small_font.render('Kliknij dwukrotnie, aby wejść do gry.', True, BIALY)
        skip_text_rect = skip_text.get_rect(center=(OKNO_SZER / 2, OKNO_WYS - 50))
        okienko.blit(skip_text, skip_text_rect)

        pygame.display.flip()


        
# Utworzenie klasy przycisków        
class Przycisk:
    def __init__(self, x_cord:int, y_cord:int, file_name:str, new_width:int, new_height:int) -> None:
        self.initial_x = x_cord
        self.initial_y = y_cord
        self.initial_width = new_width
        self.initial_height = new_height
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.button_image = pygame.image.load(f"{file_name}.png")
        self.hovered_button_image = pygame.image.load(f"{file_name}_podswietlony.png")
        self.button_image = pygame.transform.scale(self.button_image, (new_width, new_height))
        self.hovered_button_image = pygame.transform.scale(self.hovered_button_image, (new_width, new_height))
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, new_width, new_height)
    # Reakcja przycisku na kliknięcie    
    def klik(self) -> bool:
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                return True
    # Wyświetlenie przycisku na ekranie
    def wyswietl(self, window:pygame.surface.Surface) -> None:
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            window.blit(self.hovered_button_image, (self.x_cord, self.y_cord))
        else:
            window.blit(self.button_image, (self.x_cord, self.y_cord))
    # Przeskalowanie przycisku (głównie do trybu fullscreen)
    def skaluj(self, new_width:int, new_height:int) -> None:
        self.button_image = pygame.transform.scale(self.button_image, (new_width, new_height))
        self.hovered_button_image = pygame.transform.scale(self.hovered_button_image, (new_width, new_height))
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, new_width, new_height)
        
    def resetuj(self) -> None:
        self.x_cord = self.initial_x
        self.y_cord = self.initial_y
        self.skaluj(self.initial_width, self.initial_height)

# Załadowanie przycisków w menu głównym
def ustawienia_przyciski(i_szerokosc:int, odstep_y:int, przycisk_szer:int, przycisk_wys:int) -> list:
    przyciski_y = tytul_y + 150
    return [
        Przycisk((i_szerokosc - przycisk_szer) // 2, przyciski_y, "przycisk_graj3", przycisk_szer, przycisk_wys),
        Przycisk((i_szerokosc - przycisk_szer) // 2, przyciski_y + odstep_y+35, "przycisk_zasady3", przycisk_szer, przycisk_wys),
        Przycisk((i_szerokosc - przycisk_szer) // 2, przyciski_y + 2 * odstep_y+70, "przycisk_ustawienia3", przycisk_szer, przycisk_wys),
        Przycisk((i_szerokosc - przycisk_szer) // 2, przyciski_y + 3 * odstep_y+105, "przycisk_wyjdz3", przycisk_szer, przycisk_wys),
    ]

# Załadowanie przycisków w menu wyboru
def ustawienia_przyciski_wybor(i_szerokosc:int, odstep_y:int, przycisk_szer:int, przycisk_wys:int) -> list:
    przyciski_y = tytul_y + 150
    return [
        Przycisk((i_szerokosc - przycisk_szer) // 2, przyciski_y, "przycisk_wybor1", przycisk_szer, przycisk_wys),
        Przycisk((i_szerokosc - przycisk_szer) // 2, przyciski_y + odstep_y+35, "przycisk_wybor2", przycisk_szer, przycisk_wys),
        Przycisk((i_szerokosc - przycisk_szer) // 2, przyciski_y + 2 * odstep_y+70, "przycisk_wybor3", przycisk_szer, przycisk_wys),
        Przycisk((i_szerokosc - przycisk_szer) // 2, przyciski_y + 3 * odstep_y+105, "przycisk_wyjdz3", przycisk_szer, przycisk_wys),
    ]

# Załadowanie przycisków podczas pauzy w rozgrywce
def ustawienia_przyciski_pauza(i_szerokosc:int, odstep_y:int, przycisk_szer:int, przycisk_wys:int) -> list:
    przyciski_y = tytul_y + 30
    return [
        Przycisk((i_szerokosc - przycisk_szer//2+180) // 2, przyciski_y + odstep_y + 75, "przycisk_wyjdz3", przycisk_szer, przycisk_wys),
    ]

# Parametry przycisków (wielkóść, odstępy pomiędzy następnymi przyciskami)
przycisk_szer = 400
przycisk_wys = 120
odstepy_y = 30
tytul_y = 150
full_screen = False

przyciski_menu = ustawienia_przyciski(OKNO_SZER, odstepy_y + przycisk_wys, przycisk_szer, przycisk_wys)
przycisk_pelny_ekran = Przycisk((OKNO_SZER - 200) // 2, (OKNO_WYS - 450) // 2, "fullscreen", 200, 200)
przycisk_glos = Przycisk((OKNO_SZER - 150) // 2, (OKNO_WYS + 200) // 2, "glos", 150, 150)
przycisk_wyciszony = Przycisk((OKNO_SZER - 150) // 2, (OKNO_WYS + 200) // 2, "wyciszony", 150, 150)
przyciski_pauza = ustawienia_przyciski_pauza(OKNO_SZER, odstepy_y + przycisk_wys, przycisk_szer, przycisk_wys)
przyciski_wybor = ustawienia_przyciski_wybor(OKNO_SZER, odstepy_y + przycisk_wys, przycisk_szer, przycisk_wys)

# Wyświetlenie menu głównego
def pokaz_menu(window:pygame.surface.Surface) -> None:
    window.blit(tlo, (0, 0))
    tytul_rect = tytul_image.get_rect(center=(OKNO_SZER // 2, tytul_y))
    window.blit(tytul_image, tytul_rect)
    for przycisk in przyciski_menu:
        przycisk.wyswietl(window)

# Wyświetlenie menu głównego w trybie fullscreen       
def pokaz_menu_fullscreen(window:pygame.surface.Surface) -> None:
    window.blit(tlo_fullscreen, (0, 0))
    tytul_image_fs = pygame.transform.scale(tytul_image, (FULLSCREEN_SZER // 2, FULLSCREEN_WYS // 8))
    tytul_rect = tytul_image_fs.get_rect(center=(FULLSCREEN_SZER // 2, FULLSCREEN_WYS // 8))
    window.blit(tytul_image_fs, tytul_rect)
    for przycisk in przyciski_menu:
        przycisk.wyswietl(window)

# Stworzenie main
def main() -> None:
    intro()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                running = False       
        pokaz_menu(okienko)
if __name__ == '__main__':
    main()

# Edycja tekstu
def wrap_text(text:str, font:pygame.font.Font, max_width:int) -> list:
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    return lines
        
# Zasady
tekst_zasad = [
    "Piwkorzyki, to gra dla dwóch graczy rozgrywana na boisku o wymiarach 15x10 kratek, z bramkami o szerokości dwóch kratek",
    "Celem gry jest umieszczenie w bramce przeciwnika wirtualnej piłki (zdobycie gola), która początkowo znajduje się na środku boiska, a w kolejnych ruchach jest przemieszczana pomiędzy sąsiednimi przecięciami kratek. W jednym ruchu piłka może być przemieszczona na jedno z ośmiu sąsiednich pól (poziomo, pionowo lub po ukosie). W wyniku przemieszczenia pozycja początkowa jest łączona odcinkiem z pozycją końcową.",
    "Golem nazywamy również taką sytuację, w której przeciwnik zostanie zablokowany, czyli nie będzie miał ani jednej możliwości ruchu.",
    "Piłka nie może przemieszczać się wzdłuż brzegu boiska ani po odcinkach, po których już wcześniej się przemieszczała, może jednak się od nich odbijać.",
    "Gra kończy się gdy jeden z graczy zdobędzie dwa gole.",
    "Umieszczenie piłki w swojej bramce skutkuje golem dla przeciwnika.",
]
        
# Wyświetlenie zasad
def pokaz_zasady(window:pygame.surface.Surface) -> None:
    window.blit(tlo_zasady, (0, 0))
    tytul_font = pygame.font.Font(moja_czcionka, 120)
    zasady_tytul_text = "ZASADY:"
    zasady_tytul = tytul_font.render(zasady_tytul_text, True, (255, 255, 255))  
    zasady_tytul_rect = zasady_tytul.get_rect(center=(OKNO_SZER // 2, 80))
    window.blit(zasady_tytul, zasady_tytul_rect)
    
    font = pygame.font.Font(moja_czcionka, 26)  
    y_offset = 200
    line_height = font.get_linesize()  
    paragraph_spacing = 40 
    for paragraph in tekst_zasad:
        lines = wrap_text(paragraph, font, OKNO_SZER - 100)
        for line in lines:
            rendered_text = font.render(line, True, (255, 255, 255))  
            window.blit(rendered_text, (OKNO_SZER // 2 - rendered_text.get_width() // 2, y_offset))
            y_offset += line_height
        y_offset += paragraph_spacing  
    
    powrot_text = font.render("Kliknij, aby wrócić do menu", True, (255, 255, 255))
    window.blit(powrot_text, (OKNO_SZER // 2 - powrot_text.get_width() // 2, OKNO_WYS - 100))

# Wyświetlenie zasad w trybie fullscreen
def pokaz_zasady_fullscreen(window:pygame.surface.Surface) -> None:
    window.blit(tlo_zasady2, (0, 0))
    tytul_font = pygame.font.Font(moja_czcionka, 150)
    zasady_tytul_text = "ZASADY:"
    zasady_tytul = tytul_font.render(zasady_tytul_text, True, (255, 255, 255)) 
    zasady_tytul_rect = zasady_tytul.get_rect(center=(FULLSCREEN_SZER // 2, 80))
    window.blit(zasady_tytul, zasady_tytul_rect)

    font = pygame.font.Font(moja_czcionka, 35)  
    y_offset = FULLSCREEN_WYS // 5
    line_height = font.get_linesize()  
    paragraph_spacing = 50  
    for paragraph in tekst_zasad:
        lines = wrap_text(paragraph, font, FULLSCREEN_SZER - 100)
        for line in lines:
            rendered_text = font.render(line, True, (255, 255, 255))  
            window.blit(rendered_text, (FULLSCREEN_SZER // 2 - rendered_text.get_width() // 2, y_offset))
            y_offset += line_height
        y_offset += paragraph_spacing  
    
    powrot_text = font.render("Kliknij, aby wrócić do menu", True, (255, 255, 255))
    window.blit(powrot_text, (FULLSCREEN_SZER // 2 - powrot_text.get_width() // 2, FULLSCREEN_WYS - 50))

# Wyświetlenie ustawień
def pokaz_ustawienia(window:pygame.surface.Surface) -> None:
    window.blit(tlo_ustawienia, (0, 0))
    tytul_font = pygame.font.Font(moja_czcionka, 100)
    ustawienia_tytul_text = "USTAWIENIA:"
    ustawienia_tytul = tytul_font.render(ustawienia_tytul_text, True, BIALY)
    ustawienia_tytul_rect = ustawienia_tytul.get_rect(center=(OKNO_SZER // 2, 80))
    window.blit(ustawienia_tytul, ustawienia_tytul_rect)
    font = pygame.font.Font(moja_czcionka, 45)
    tekst = [
        ""
    ]
    for i, line in enumerate(tekst):
        rendered_text = font.render(line, True, BIALY)
        window.blit(rendered_text, (50, 150 + i * 40))
    
    przycisk_glos.x_cord = (OKNO_SZER - 150) // 2
    przycisk_glos.y_cord = (OKNO_WYS + 200) // 2
    przycisk_wyciszony.x_cord = (OKNO_SZER - 150) // 2
    przycisk_wyciszony.y_cord = (OKNO_WYS + 200) // 2
    
    przycisk_pelny_ekran.wyswietl(window)
    if wyciszenie==False:
        przycisk_glos.wyswietl(window)
    else:
        przycisk_wyciszony.wyswietl(window)
    
    napis = font.render("FULLSCREEN", True, BIALY)
    window.blit(napis, ((OKNO_SZER - napis.get_width()) // 2, (OKNO_WYS) // 2 - 290))
    napis2 = font.render("GŁOS", True, BIALY)
    window.blit(napis2, ((OKNO_SZER - napis2.get_width()) // 2, (OKNO_WYS+50) // 2))

    powrot_text = font.render("Kliknij, aby wrócić do menu", True, BIALY)
    window.blit(powrot_text, (OKNO_SZER // 2 - powrot_text.get_width() // 2, OKNO_WYS - 100))

# Wyświetlenie ustawień w trybie fullscreen
def pokaz_ustawienia_fullscreen(window:pygame.surface.Surface) -> None:
    window.blit(tlo_ustawienia2, (0, 0))
    tytul_font = pygame.font.Font(moja_czcionka, 150)
    ustawienia_tytul_text = "USTAWIENIA:"
    ustawienia_tytul = tytul_font.render(ustawienia_tytul_text, True, BIALY)
    ustawienia_tytul_rect = ustawienia_tytul.get_rect(center=(FULLSCREEN_SZER // 2, 80))
    window.blit(ustawienia_tytul, ustawienia_tytul_rect)
    font = pygame.font.Font(moja_czcionka, 72)
    tekst = [
             
             ""]
    for i, line in enumerate(tekst):
        rendered_text = font.render(line, True, BIALY)
        window.blit(rendered_text, (FULLSCREEN_SZER // 4, FULLSCREEN_WYS // 4 + i * 80))
        
    przycisk_pelny_ekran.skaluj(200,200)
    przycisk_pelny_ekran.x_cord = (FULLSCREEN_SZER - 200) // 2
    przycisk_pelny_ekran.y_cord = (FULLSCREEN_WYS - 400) // 2
    przycisk_glos.skaluj(150,150)
    przycisk_glos.x_cord = (FULLSCREEN_SZER - 150) // 2
    przycisk_glos.y_cord = (FULLSCREEN_WYS + 300) // 2
    przycisk_wyciszony.skaluj(150,150)
    przycisk_wyciszony.x_cord = (FULLSCREEN_SZER - 150) // 2
    przycisk_wyciszony.y_cord = (FULLSCREEN_WYS + 300) // 2
    
    przycisk_pelny_ekran.wyswietl(window)
    if wyciszenie==False:
        przycisk_glos.wyswietl(window)
    else:
        przycisk_wyciszony.wyswietl(window)

    napis = font.render("FULLSCREEN", True, BIALY)
    window.blit(napis, ((FULLSCREEN_SZER - napis.get_width()) // 2, (FULLSCREEN_WYS) // 2 - 300))
    napis2 = font.render("GłOS", True, BIALY)
    window.blit(napis2, ((FULLSCREEN_SZER - napis2.get_width()) // 2, (FULLSCREEN_WYS) // 2 + 50))
    powrot_text = font.render("Kliknij, aby wrócić do menu", True, BIALY)
    window.blit(powrot_text, (FULLSCREEN_SZER // 2 - powrot_text.get_width() // 2, FULLSCREEN_WYS - 150))

# Wyświetlenie menu wyboru        
def pokaz_wybor(window:pygame.surface.Surface) -> None:
    window.blit(tlo_wybor, (0, 0))
    wybor_font = pygame.font.Font(moja_czcionka, 100)
    wybor_tytul_text = "WYBIERZ DŁUGOŚĆ GRY:"
    wybor_tytul = wybor_font.render(wybor_tytul_text, True, BIALY)
    wybor_tytul_rect = wybor_tytul.get_rect(center=(OKNO_SZER // 2, 80))
    window.blit(wybor_tytul, wybor_tytul_rect)
    for przycisk in przyciski_wybor:
        przycisk.wyswietl(window)

# Wyświetlenie menu wyboru w trybie fullscreen        
def pokaz_wybor_fullscreen(window:pygame.surface.Surface) -> None:
    window.blit(tlo_wybor2, (0, 0))
    wybor_font = pygame.font.Font(moja_czcionka, 150)
    wybor_tytul_text = "WYBIERZ DŁUGOŚĆ GRY:"
    wybor_tytul = wybor_font.render(wybor_tytul_text, True, BIALY)
    wybor_tytul_rect = wybor_tytul.get_rect(center=(FULLSCREEN_SZER // 2, 80))
    window.blit(wybor_tytul, wybor_tytul_rect)
    for przycisk in przyciski_wybor:
        przycisk.wyswietl(window)
    
#Utworzenie klasy gry
class Game:
    def __init__(self) -> None :
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT+50))
        pygame.display.set_caption('Piwkorzyki')
        self.clock = pygame.time.Clock()
        self.initGame()
        self.paused = False
        self.game_over = False
        self.additional_move = False
        self.load_images()
        self.resetGame()
        self.ball_path = [(BOARD_HEIGHT // 2, BOARD_WIDTH // 2)]

# Załadowanie interfejsu graficznego okna rozgrywki
    def load_images(self) -> None:
        # Losowy wybór piłki spośród 8 możliwych przez funkcję random
        selected_ball = random.choice(ball_images)
        self.pilka_image = pygame.image.load(selected_ball)
        self.pilka_image = pygame.transform.scale(self.pilka_image, (CELL_SIZE, CELL_SIZE))
        self.bramka_image = pygame.image.load("bramka.jpg")
        self.bramka_image = pygame.transform.scale(self.bramka_image, (CELL_SIZE, 2*CELL_SIZE))
        self.bramka0_image = pygame.image.load("bramka0.jpg")
        self.bramka0_image = pygame.transform.scale(self.bramka0_image, (CELL_SIZE, 2*CELL_SIZE))
        
    def initGame(self) -> None:
        self.board = np.zeros((BOARD_HEIGHT, BOARD_WIDTH), dtype=int)
        self.lines = np.zeros((BOARD_HEIGHT, BOARD_WIDTH, 8), dtype=bool)
        self.ball_pos = (BOARD_HEIGHT // 2, BOARD_WIDTH // 2)
        self.player_turn = 1
        self.scores = {1: 0, 2: 0}

# Załadowanie boiska
    def drawBoard(self) -> None:
        self.screen.fill(BIALY)
        board_rect = pygame.Rect(0, 0, BOARD_WIDTH * CELL_SIZE, BOARD_HEIGHT * CELL_SIZE)
        boisko_image = pygame.image.load('boisko.jpeg')
        boisko_image = pygame.transform.scale(boisko_image, (BOARD_WIDTH * CELL_SIZE, BOARD_HEIGHT * CELL_SIZE))
        self.screen.blit(boisko_image, (0, 0))
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                    pygame.draw.rect(self.screen, CZARNY, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
        left_goal_pos = ((BOARD_HEIGHT // 2)-1, 0)
        self.screen.blit(self.bramka0_image, (left_goal_pos[1] * CELL_SIZE, left_goal_pos[0] * CELL_SIZE))
        right_goal_pos = ((BOARD_HEIGHT // 2)-1, BOARD_WIDTH - 1)
        self.screen.blit(self.bramka_image, (right_goal_pos[1] * CELL_SIZE, right_goal_pos[0] * CELL_SIZE))
        
        font = pygame.font.SysFont(None, 30)
        score_text1 = font.render(f"Gracz 1: {self.scores[1]}", True, CZARNY)
        score_rect = score_text1.get_rect(center=(0.1*WINDOW_WIDTH, WINDOW_HEIGHT+25))
        self.screen.blit(score_text1, score_rect)
        
        score_text2 = font.render(f"Gracz 2: {self.scores[2]}", True, CZARNY)
        score_rect = score_text2.get_rect(center=(0.9*WINDOW_WIDTH, WINDOW_HEIGHT+25))
        self.screen.blit(score_text2, score_rect)

        font = pygame.font.SysFont(None, 30)
        if self.player_turn == 1:
            text = font.render(f"Player {self.player_turn} turn (-->)", True, CZARNY)
        else:
            text = font.render(f"Player {self.player_turn} turn (<--)", True, CZARNY)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT + 25))
        self.screen.blit(text, text_rect)
        
# Ekran pauzy
    def MenuPauza(self) -> None:
        self.screen.blit(tlo_pauza, (0, 0))
        font = pygame.font.Font(None, 150)
        font2 = pygame.font.Font(moja_czcionka, 30)
        text = font.render("PAUZA", True, CZARNY)
        text2 = font2.render("Naciśnij klawisz 'ESC', aby powrócić do gry.", True, CZARNY)
        text_rect = text.get_rect(midtop=(WINDOW_WIDTH // 2, 50))
        text2_rect = text2.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT ))
        self.screen.blit(text, text_rect)
        self.screen.blit(text2, text2_rect)
        for przycisk in przyciski_pauza:
            przycisk.wyswietl(self.screen)
        pygame.display.flip()

# Zasady prawidłowego ruchu   
    def isValidMove(self, pos:tuple) -> bool:
        y, x = pos
        direction = self.getDirection(self.ball_pos, pos)
        if direction is None:
            print("Nieprawidłowy kierunek ruchu dla piłki")
            return False
        if abs(self.ball_pos[0] - y) > 1 or abs(self.ball_pos[1] - x) > 1:
            print("Nieprawidłowa odległość ruchu dla piłki")
            return False
        if self.lines[self.ball_pos[0], self.ball_pos[1], direction] or \
            self.lines[y, x, (direction + 4) % 8]:
                print(f"Linia w kierunku {direction} jest już narysowana")
                return False
        return True
    
    def getDirection(self, start:tuple, end:tuple) -> bool:
        dy, dx = end[0] - start[0], end[1] - start[1]
        if dy == -1 and dx == -1:
            return 0
        elif dy == -1 and dx == 0:
            return 1
        elif dy == -1 and dx == 1:
            return 2
        elif dy == 0 and dx == 1:
            return 3
        elif dy == 1 and dx == 1:
            return 4
        elif dy == 1 and dx == 0:
            return 5
        elif dy == 1 and dx == -1:
            return 6
        elif dy == 0 and dx == -1:
            return 7
        else:
            return None
        
# Sprawdzenie czy gracz ma możliwosc wykonania ruchu
    def hasAvailableMoves(self) -> bool:
        y, x = self.ball_pos
        directions = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
        for direction in directions:
            ny, nx = y + direction[0], x + direction[1]
            if 0 <= ny < BOARD_HEIGHT and 0 <= nx < BOARD_WIDTH:
                direction_index = self.getDirection(self.ball_pos, (ny, nx))
                opposite_direction_index = (direction_index + 4) % 8
                if direction_index is not None and \
                    not self.lines[y, x, direction_index] and \
                        not self.lines[ny, nx, opposite_direction_index]:
                            return True
    
# Oddanie gola przeciwnikowi za brak możliwosci ruchu
    def scoreForOpponent(self) -> None:
        self.player_turn = 3 - self.player_turn  # Przełączanie tury gracza
        print(f"Player {self.player_turn} scores due to no available moves!")
        self.scores[self.player_turn] += 1
        if not wyciszenie:
            gol_sfx.play()
        self.lines.fill(False)
        self.ball_pos = (BOARD_HEIGHT // 2, BOARD_WIDTH // 2)
        self.ball_path = [self.ball_pos]
        if self.scores[self.player_turn] >= GOALS_TO_WIN:
            self.endGame(self.player_turn)
            
# Mechanika ruszania piłką
    def moveBall(self, pos:tuple) -> None:
        if not (0 <= pos[0] < BOARD_HEIGHT and 0 <= pos[1] < BOARD_WIDTH):
            print(f"Pozycja {pos} jest poza zakresem")
            return
        direction = self.getDirection(self.ball_pos, pos)
        if direction is None:
            print("Nieprawidłowy kierunek ruchu dla moveBall")
            return
        if self.isValidMove(pos):
            self.lines[self.ball_pos[0], self.ball_pos[1], direction] = True
            self.ball_pos = pos
            self.ball_path.append(pos)
            print(f"Moved ball to {pos}")
            if self.checkGoal():
                print("Goal scored!")
                self.lines.fill(False)
                self.ball_path = [(BOARD_HEIGHT // 2, BOARD_WIDTH // 2)]
                self.ball_pos = (BOARD_HEIGHT // 2, BOARD_WIDTH // 2)
                self.player_turn = 3 - self.player_turn  # Przełączanie tury gracza
            else:
                if not self.hasAvailableMoves():
                    self.scoreForOpponent()
# Sprawdzenie, czy padł gol
    def checkGoal(self) -> bool:
        if self.ball_pos[1] == 0:  # Piłka w lewej bramce
            if self.ball_pos[0] in range((BOARD_HEIGHT - 2) // 2, (BOARD_HEIGHT + 2) // 2):
                if self.player_turn == 2:  # Tylko gracz 2 może zdobyć bramkę w lewej bramce
                    print(f"Player {self.player_turn} scores!")
                    self.scores[self.player_turn] += 1
                    if not wyciszenie:
                        gol_sfx.play()
                    self.lines.fill(False)
                    self.ball_path = [self.ball_pos]
                    self.ball_pos = (BOARD_HEIGHT // 2, BOARD_WIDTH // 2)
                    self.lines[self.ball_pos[0], self.ball_pos[1], self.getDirection(self.ball_pos, self.ball_path[-1])] = True
                    if self.scores[self.player_turn] >= GOALS_TO_WIN:
                        self.endGame(self.player_turn)
                    return True
                else:
                    print("Gracz numer 1 próbował strzelić samobója, punkt dla przeciwnika")
                    self.scores[3 - self.player_turn] += 1  # Przeciwnik zdobywa punkt
                    if not wyciszenie:
                        gol_sfx.play()
                    self.ball_pos = (BOARD_HEIGHT // 2, BOARD_WIDTH // 2)
                    self.ball_path = [self.ball_pos]
                    if self.scores[3-self.player_turn] >= GOALS_TO_WIN:
                        self.endGame(3-self.player_turn)
                    self.lines.fill(False)
                    return False
        elif self.ball_pos[1] == BOARD_WIDTH - 1:  # Piłka w prawej bramce
            if self.ball_pos[0] in range((BOARD_HEIGHT - 2) // 2, (BOARD_HEIGHT + 2) // 2):
                if self.player_turn == 1:  # Tylko gracz 1 może zdobyć bramkę w prawej bramce
                    print(f"Player {self.player_turn} scores!")
                    self.scores[self.player_turn] += 1
                    if not wyciszenie:
                        gol_sfx.play()
                    self.lines.fill(False)
                    self.ball_path = [self.ball_pos]
                    self.ball_pos = (BOARD_HEIGHT // 2, BOARD_WIDTH // 2)
                    self.lines[self.ball_pos[0], self.ball_pos[1], self.getDirection(self.ball_pos, self.ball_path[-1])] = True
                    if self.scores[self.player_turn] >= GOALS_TO_WIN:
                        self.endGame(self.player_turn)
                    return True
                else:
                    print("Gracz numer 2 próbował strzelić samobója, punkt dla przeciwnika")
                    self.scores[3 - self.player_turn] += 1  # Przeciwnik zdobywa punkt
                    if not wyciszenie:
                        gol_sfx.play()
                    self.ball_pos = (BOARD_HEIGHT // 2, BOARD_WIDTH // 2)
                    self.ball_path = [self.ball_pos]
                    if self.scores[3-self.player_turn] >= GOALS_TO_WIN:
                        self.endGame(3-self.player_turn)
                    self.lines.fill(False)
                    return False
        return False
    def resetGame(self) -> None:
        self.initGame()
        self.ball_path = [self.ball_pos]
        self.game_over = False

# Ekran tuż po zakończeniu rozgrywki
    def endGame(self, winner) -> None:
        if not wyciszenie:
            piosenka_sfx.play()
        self.screen.fill(CZARNY)
        self.screen.blit(tlo_koniec, (WINDOW_WIDTH // 2 - 200, 120))
        self.game_over = True
        self.scores = {1: 0, 2: 0}  # Reset scores
        font = pygame.font.Font(None, 150)
        font2 = pygame.font.Font(None, 50)
        text = font.render("KONIEC GRY!", True, BIALY)
        text2 = font2.render(f"Gracz {winner} dostaje piwo!", True, BIALY)
        text3 = font2.render("Naciśnij 'R', aby zagrać ponownie.", True, BIALY)
        text4 = font2.render("Naciśnij 'Q', aby zakończyć.", True, BIALY)

        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 8))
        text2_rect = text2.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT *2 // 3 + 20))
        text3_rect = text3.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 7 // 8))
        text4_rect = text4.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 7 // 8 + 60))

        self.screen.blit(text, text_rect)
        self.screen.blit(text2, text2_rect)
        self.screen.blit(text3, text3_rect)
        self.screen.blit(text4, text4_rect)
        self.screen.blit
        pygame.display.flip()
    
# Rysowanie przebytej drogi przez piłkę
    def drawBallPath(self) -> None:
        for i in range(1, len(self.ball_path)):
            start = self.ball_path[i - 1]
            end = self.ball_path[i]
            start_pos = (start[1] * CELL_SIZE + CELL_SIZE // 2, start[0] * CELL_SIZE + CELL_SIZE // 2)
            end_pos = (end[1] * CELL_SIZE + CELL_SIZE // 2, end[0] * CELL_SIZE + CELL_SIZE // 2)
            pygame.draw.line(self.screen, CZARNY, start_pos, end_pos, 3)  # Draw the line
            self.drawArrow(start_pos, end_pos)
     
    def drawArrow(self, start_pos:tuple, end_pos:tuple) -> None:
        angle = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])
        arrow_length = 10
        arrow_angle = math.pi / 6
        arrow_point1 = (
            end_pos[0] - arrow_length * math.cos(angle - arrow_angle),
            end_pos[1] - arrow_length * math.sin(angle - arrow_angle)
        )
        arrow_point2 = (
            end_pos[0] - arrow_length * math.cos(angle + arrow_angle),
            end_pos[1] - arrow_length * math.sin(angle + arrow_angle)
        )
        pygame.draw.polygon(self.screen, CZARNY, [end_pos, arrow_point1, arrow_point2])
        
# Działanie okna z rozgrywką
    def run(self) -> None:
        running = True
        current_screen = "menu"
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_r and self.game_over:
                        pygame.mixer.stop()
                        self.resetGame()
                        self.game_over = False
                    elif event.key == pygame.K_q and self.game_over:
                        running = False
                        
                if not self.paused and not self.game_over:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            x = event.pos[0] // CELL_SIZE
                            y = event.pos[1] // CELL_SIZE
                            if 0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT:
                                if self.isValidMove((y, x)):
                                    self.moveBall((y, x))
                                    if not wyciszenie:
                                        uderzenie_sfx.play()
                                    self.player_turn = 3 - self.player_turn  # Przełączanie tury gracza

                                    
            if self.paused:
                self.MenuPauza()
                if przyciski_pauza[0].klik():
                    pygame.quit()
                    pokaz_menu(okienko)
            elif not self.game_over:
                self.drawBoard()
                ball_screen_pos = (
                    self.ball_pos[1] * CELL_SIZE,  # x
                    self.ball_pos[0] * CELL_SIZE   # y
                )
                self.screen.blit(self.pilka_image, ball_screen_pos)
                self.drawBallPath()

            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()
current_screen = "menu"

# Działanie przycisków menu głównego        
graj = True
while graj:
    for zdarzenie in pygame.event.get():
        if zdarzenie.type == pygame.QUIT:
            graj = False
        elif zdarzenie.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "menu":
                if przyciski_menu[0].klik():
                    current_screen = "wybor"  
                elif przyciski_menu[1].klik():
                    current_screen = "zasady"
                elif przyciski_menu[2].klik():
                    current_screen = "ustawienia"
                elif przyciski_menu[3].klik():
                    graj = False
            elif current_screen == "ustawienia":
                if przycisk_glos.klik():
                    wyciszenie = not wyciszenie
                elif przycisk_pelny_ekran.klik():
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
                        przycisk_glos.resetuj()
                        przycisk_wyciszony.resetuj()
                        full_screen = False
                else:
                    current_screen = "menu"
            elif current_screen == "zasady":
                current_screen = "menu"
            elif current_screen == "wybor":
                if przyciski_wybor[0].klik():  
                    GOALS_TO_WIN = 1
                    current_screen = "gra"
                if przyciski_wybor[1].klik():  
                    GOALS_TO_WIN = 2
                    current_screen = "gra"
                elif przyciski_wybor[2].klik():  
                    GOALS_TO_WIN = 3
                    current_screen = "gra"
                elif przyciski_wybor[3].klik():
                    current_screen = "menu"
            elif current_screen == "gra":
                game = Game()
                game.run()   
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
    elif current_screen == "wybor":
        if full_screen:
            pokaz_wybor_fullscreen(okienko)
        else:
            pokaz_wybor(okienko)
    pygame.display.flip()
    zegarek.tick(FPS)
# Koniec programu
pygame.quit()
