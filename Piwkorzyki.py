import pygame
import sys
import numpy as np
from pygame.locals import *

OKNO_SZER = 1024
OKNO_WYS = 1024
FULLSCREEN_SZER = 1920
FULLSCREEN_WYS = 1080
FPS = 60

# Rozmiary planszy
BOARD_WIDTH = 15
BOARD_HEIGHT = 10
CELL_SIZE = 60

# Rozmiary okna
WINDOW_WIDTH = BOARD_WIDTH * CELL_SIZE
WINDOW_HEIGHT = BOARD_HEIGHT * CELL_SIZE

pygame.init()
okienko = pygame.display.set_mode((OKNO_SZER, OKNO_WYS), 0, 32)
pygame.display.set_caption("Piwkorzyki")
zegarek = pygame.time.Clock()

moja_czcionka = "pricedown bl.otf"
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

tlo = pygame.image.load("tlo.png")
tlo_fullscreen = pygame.image.load("tlo2.png")
tlo_zasady = pygame.image.load("tlo_zasady2.png")
tlo_ustawienia = pygame.image.load("tlo_ustawienia.png")
tlo_ustawienia2 = pygame.image.load("tlo_ustawienia2.png")
tlo_pauza = pygame.image.load("tlo_pauza.jpg")
tlo_pauza = pygame.transform.scale(tlo_pauza, (WINDOW_WIDTH, WINDOW_HEIGHT+50))
tytul_image = pygame.image.load("tytul2.png")
pilka_image = pygame.image.load("pilka.jpg")
tlo_koniec = pygame.image.load("piwa.jpg")
tlo_koniec = pygame.transform.scale(tlo_koniec, (400, 300))

black = (0, 0, 0)
white = (255, 255, 255)

def intro():
    intro_active = True
    while intro_active:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                intro_active = False

        okienko.fill(black)
        intro_text = font.render('Intro Screen', True, white)
        text_rect = intro_text.get_rect(center=(OKNO_SZER / 2, OKNO_WYS / 2))
        okienko.blit(intro_text, text_rect)

        skip_text = small_font.render('Kliknij dwukrotnie, aby pominąć.', True, white)
        skip_text_rect = skip_text.get_rect(center=(OKNO_SZER / 2, OKNO_WYS - 50))
        okienko.blit(skip_text, skip_text_rect)

        pygame.display.update()
        
        
        
class Przycisk:
    def __init__(self, x_cord, y_cord, file_name, new_width, new_height):

    
    
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
        
    def klik(self):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                return True
    
    def wyswietl(self, window):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            window.blit(self.hovered_button_image, (self.x_cord, self.y_cord))
        else:
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
        Przycisk((i_szerokosc - przycisk_szer) // 2, przyciski_y + odstep_y+35, "przycisk_zasady3", przycisk_szer, przycisk_wys),
        Przycisk((i_szerokosc - przycisk_szer) // 2, przyciski_y + 2 * odstep_y+70, "przycisk_ustawienia3", przycisk_szer, przycisk_wys),
        Przycisk((i_szerokosc - przycisk_szer) // 2, przyciski_y + 3 * odstep_y+105, "przycisk_wyjdz3", przycisk_szer, przycisk_wys),
    ]

def ustawienia_przyciski_pauza(i_szerokosc, odstep_y, przycisk_szer, przycisk_wys):
    przyciski_y = tytul_y + 30
    return [
        Przycisk((i_szerokosc - przycisk_szer//2) // 2, przyciski_y, "przycisk_zasady3", przycisk_szer, przycisk_wys),
        Przycisk((i_szerokosc - przycisk_szer//2) // 2, przyciski_y + odstep_y+35, "przycisk_wyjdz3", przycisk_szer, przycisk_wys),
    ]

    #def ustawienia_przyciski_po_grze(i_szerokosc, odstep_y, przycisk_szer, przycisk_wys):
    # tutaj dodac img przycisku wyjdz do menu Przycisk((i_szerokosc - przycisk_szer) // 2, przyciski_y, "przycisk_wyjdzdomenu",
    # przycisk_szer, przycisk_wys),
    # tutaj dodac img przycisku zagraj ponownie Przycisk((i_szerokosc - przycisk_szer) // 2, przyciski_y,
    # "przycisk_zagrajponownie" ,przycisk_szer, przycisk_wys)

przycisk_szer = 400
przycisk_wys = 120
odstepy_y = 30
tytul_y = 150
full_screen = False

przyciski_menu = ustawienia_przyciski(OKNO_SZER, odstepy_y + przycisk_wys, przycisk_szer, przycisk_wys)

przycisk_pelny_ekran = Przycisk((OKNO_SZER - 200) // 2, (OKNO_WYS - 80) // 2, "fullscreen", 200, 200)

przyciski_pauza = ustawienia_przyciski_pauza(OKNO_SZER, odstepy_y + przycisk_wys, przycisk_szer, przycisk_wys)


def pokaz_menu(window):
    window.blit(tlo, (0, 0))
    tytul_rect = tytul_image.get_rect(center=(OKNO_SZER // 2, tytul_y))
    window.blit(tytul_image, tytul_rect)
    for przycisk in przyciski_menu:
        przycisk.wyswietl(window)

def main():
    intro()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                running = False       
        pokaz_menu(okienko)


if __name__ == '__main__':
    main()
    
def wrap_text(text, font, max_width):
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
tekst_zasad = [
    "Piwkorzyki, to gra dla dwóch graczy rozgrywana na boisku o wymiarach 15x10 kratek, z bramkami o szerokości dwóch kratek",
    "Celem gry jest umieszczenie w bramce przeciwnika wirtualnej piłki (zdobycie gola), która początkowo znajduje się na środku boiska, a w kolejnych ruchach jest przemieszczana pomiędzy sąsiednimi przecięciami kratek. W jednym ruchu piłka może być przemieszczona na jedno z ośmiu sąsiednich pól (poziomo, pionowo lub po ukosie). W wyniku przemieszczenia pozycja początkowa jest łączona odcinkiem z pozycją końcową.",
    "Golem nazywamy również taką sytuację, w której jeden z graczy zostanie zablokowany, czyli nie będzie miał ani jednej możliwości ruchu.",
    "Piłka nie może przemieszczać się wzdłuż brzegu boiska ani po odcinkach, po których już wcześniej się przemieszczała, może jednak się od nich odbijać.",
    "Gra kończy się gdy jeden z graczy zdobędzie wymaganą liczbę goli, która ustalana jest przed rozpoczęciem meczu.",
]

def pokaz_zasady(window):
    window.blit(tlo_zasady, (0, 0))
    tytul_font = pygame.font.Font(moja_czcionka, 100)
    zasady_tytul_text = "ZASADY:"
    zasady_tytul = tytul_font.render(zasady_tytul_text, True, (255, 255, 255))  
    zasady_tytul_rect = zasady_tytul.get_rect(center=(OKNO_SZER // 2, 80))
    window.blit(zasady_tytul, zasady_tytul_rect)
    
    font = pygame.font.Font(moja_czcionka, 24)  
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

def pokaz_zasady_fullscreen(window):
    window.blit(tlo_zasady, (0, 0))
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
    window.blit(powrot_text, (FULLSCREEN_SZER // 2 - powrot_text.get_width() // 2, FULLSCREEN_WYS - 100))


def pokaz_ustawienia(window):
    window.blit(tlo_ustawienia, (0, 0))
    tytul_font = pygame.font.Font(moja_czcionka, 100)
    ustawienia_tytul_text = "USTAWIENIA:"
    ustawienia_tytul = tytul_font.render(ustawienia_tytul_text, True, (255, 255, 255))
    ustawienia_tytul_rect = ustawienia_tytul.get_rect(center=(OKNO_SZER // 2, 80))
    window.blit(ustawienia_tytul, ustawienia_tytul_rect)
    font = pygame.font.Font(moja_czcionka, 45)
    tekst = [
        ""
    ]
    for i, line in enumerate(tekst):
        rendered_text = font.render(line, True, (255, 255, 255))
        window.blit(rendered_text, (50, 150 + i * 40))
    
    przycisk_pelny_ekran.wyswietl(window)
    
    napis = font.render("FULLSCREEN", True, (255, 255, 255))
    window.blit(napis, ((OKNO_SZER - napis.get_width()) // 2, (OKNO_WYS) // 2 - 90))

    powrot_text = font.render("Kliknij, aby wrócić do menu", True, (255, 255, 255))
    window.blit(powrot_text, (OKNO_SZER // 2 - powrot_text.get_width() // 2, OKNO_WYS - 100))

def pokaz_ustawienia_fullscreen(window):
    window.blit(tlo_ustawienia2, (0, 0))
    tytul_font = pygame.font.Font(moja_czcionka, 150)
    ustawienia_tytul_text = "USTAWIENIA:"
    ustawienia_tytul = tytul_font.render(ustawienia_tytul_text, True, (255, 255, 255))
    ustawienia_tytul_rect = ustawienia_tytul.get_rect(center=(FULLSCREEN_SZER // 2, 80))
    window.blit(ustawienia_tytul, ustawienia_tytul_rect)
    
    font = pygame.font.Font(moja_czcionka, 72)
    tekst = [
             
             ""]
    for i, line in enumerate(tekst):
        rendered_text = font.render(line, True, (255, 255, 255))
        window.blit(rendered_text, (FULLSCREEN_SZER // 4, FULLSCREEN_WYS // 4 + i * 80))
    
    przycisk_pelny_ekran.skaluj(300,300)
    przycisk_pelny_ekran.x_cord = (FULLSCREEN_SZER - 300) // 2
    przycisk_pelny_ekran.y_cord = (FULLSCREEN_WYS - 300) // 2
    przycisk_pelny_ekran.wyswietl(window)

    napis = font.render("FULLSCREEN", True, (255, 255, 255))
    window.blit(napis, ((FULLSCREEN_SZER - napis.get_width()) // 2, (FULLSCREEN_WYS) // 2 - 250))

    powrot_text = font.render("Kliknij, aby wrócić do menu", True, (255, 255, 255))
    window.blit(powrot_text, (FULLSCREEN_SZER // 2 - powrot_text.get_width() // 2, FULLSCREEN_WYS - 150))


def pokaz_menu_fullscreen(window):
    window.blit(tlo_fullscreen, (0, 0))
    tytul_image_fs = pygame.transform.scale(tytul_image, (FULLSCREEN_SZER // 2, FULLSCREEN_WYS // 8))
    tytul_rect = tytul_image_fs.get_rect(center=(FULLSCREEN_SZER // 2, FULLSCREEN_WYS // 8))
    window.blit(tytul_image_fs, tytul_rect)
    for przycisk in przyciski_menu:
        przycisk.wyswietl(window)
    
# Definiowanie kolorów
BIALY = (255, 255, 255)
CZARNY = (0, 0, 0)
CZERWONY = (255, 0, 0)
NIEBIESKI = (0, 0, 255)
ZIELONY = (0, 255, 0)

GOALS_TO_WIN = 1

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT+50))
        pygame.display.set_caption('Piłkarzyki')
        self.clock = pygame.time.Clock()
        self.initGame()
        self.paused = False
        self.game_over = False
        self.additional_move = False
        self.load_images()
        self.resetGame()

    def load_images(self):
        self.pilka_image = pygame.image.load("pilka.jpg")
        self.pilka_image = pygame.transform.scale(self.pilka_image, (CELL_SIZE, CELL_SIZE))
        
    def initGame(self):
        self.board = np.zeros((BOARD_HEIGHT, BOARD_WIDTH), dtype=int)
        self.lines = np.zeros((BOARD_HEIGHT, BOARD_WIDTH, 8), dtype=bool)
        self.ball_pos = (BOARD_HEIGHT // 2, BOARD_WIDTH // 2)
        self.player_turn = 1
        self.highlighted_cells = [(BOARD_HEIGHT//2-1, BOARD_WIDTH-1), (BOARD_HEIGHT//2,BOARD_WIDTH-1),(BOARD_HEIGHT//2-1, 0),(BOARD_HEIGHT//2, 0)]
        self.scores = {1: 0, 2: 0}
    
    def drawBoard(self):
        self.screen.fill(BIALY)
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                if (row, col) in self.highlighted_cells:
                    pygame.draw.rect(self.screen, NIEBIESKI, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(self.screen, CZARNY, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        font = pygame.font.SysFont(None, 30)
        text = font.render(f"Player {self.player_turn} turn", True, CZARNY)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT + 25))
        self.screen.blit(text, text_rect)

    def MenuPauza(self):
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
        pygame.display.update()
        
    def isValidMove(self, pos):
        y, x = pos
        direction = self.getDirection(self.ball_pos, pos)
        if direction is None:
            print("Nieprawidłowy kierunek ruchu dla piłki")
            return False
        if abs(self.ball_pos[0] - y) > 1 or abs(self.ball_pos[1] - x) > 1:
            print("Nieprawidłowa odległość ruchu dla piłki")
            return False
        if self.lines[self.ball_pos[0], self.ball_pos[1], direction]:
            print(f"Linia w kierunku {direction} jest już narysowana")
            return False
        return True
    
    def getDirection(self, start, end):
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

    def moveBall(self, pos):
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
            print(f"Moved ball to {pos}")
        if not self.checkGoal():
            if self.ball_pos[1] in [0, BOARD_WIDTH - 1] and \
                self.ball_pos[0] in range((BOARD_HEIGHT - 2) // 2, (BOARD_HEIGHT + 2) // 2):
                    self.ball_pos = (BOARD_HEIGHT // 2, BOARD_WIDTH // 2)
                    print("Goal scored!")
    
    def checkGoal(self):
        if self.ball_pos[1] == 0:  # Piłka w lewej bramce
            if self.ball_pos[0] in range((BOARD_HEIGHT - 2) // 2, (BOARD_HEIGHT + 2) // 2):
                if self.player_turn == 2:  # Tylko gracz 2 może zdobyć bramkę w lewej bramce
                    print(f"Player {self.player_turn} scores!")
                    self.scores[self.player_turn] += 1
                    if self.scores[self.player_turn] >= GOALS_TO_WIN:
                        self.additional_move = False
                        self.endGame(self.player_turn)
                        return True
                else:
                    print("Gracz numer 1 próbował strzelić samobója, piłka wraca na środek boiska")
                    self.ball_pos = (BOARD_HEIGHT // 2, BOARD_WIDTH // 2)
                    self.additional_move = False  # Resetowanie dodatkowego ruchu przy samobóju
                    return False
        elif self.ball_pos[1] == BOARD_WIDTH - 1:  # Piłka w prawej bramce
            if self.ball_pos[0] in range((BOARD_HEIGHT - 2) // 2, (BOARD_HEIGHT + 2) // 2):
                if self.player_turn == 1:  # Tylko gracz 1 może zdobyć bramkę w prawej bramce
                    print(f"Player {self.player_turn} scores!")
                    self.scores[self.player_turn] += 1
                    if self.scores[self.player_turn] >= GOALS_TO_WIN:
                        self.additional_move = False
                        self.endGame(self.player_turn)
                        return True
                else:
                    print("Gracz numer 2 próbował strzelić samobója, piłka wraca na środek boiska")
                    self.ball_pos = (BOARD_HEIGHT // 2, BOARD_WIDTH // 2)
                    self.additional_move = False  # Resetowanie dodatkowego ruchu przy samobóju
                    return False
        return False
    def resetGame(self):
        self.initGame()
        self.game_over = False
    
    def endGame(self, winner):
        self.screen.fill(CZARNY)
        self.screen.blit(tlo_koniec, (250, 120))
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
        pygame.display.update()

    def run(self):
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
                                    if not self.additional_move:
                                        self.player_turn = 3 - self.player_turn  # Przełączanie tury gracza
                                    else:
                                        print(f"Player {self.player_turn} gets an additional move.")
                                        self.additional_move = False
                                        self.player_turn = 3-self.player_turn  # Resetowanie dodatkowego ruchu

                                    
            if self.paused:
                self.MenuPauza()
                if przyciski_pauza[0].klik():
                    current_screen == "zasady"
                    pokaz_zasady(okienko)
                elif przyciski_pauza[1].klik():
                    running = False

            elif not self.game_over:
                self.drawBoard()
                ball_screen_pos = (
                    self.ball_pos[1] * CELL_SIZE,  # x
                    self.ball_pos[0] * CELL_SIZE   # y
                )
                self.screen.blit(self.pilka_image, ball_screen_pos)

            pygame.display.update()
            self.clock.tick(30)
        pygame.quit()
current_screen = "menu"
   
graj = True
while graj:
    for zdarzenie in pygame.event.get():
        if zdarzenie.type == pygame.QUIT:
            graj = False
        elif zdarzenie.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "menu":
                if przyciski_menu[0].klik():
                    current_screen = "gra"  
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
    elif current_screen == "gra":
        game = Game()
        game.run()
 
    pygame.display.update()
    zegarek.tick(FPS)
 
pygame.quit()
