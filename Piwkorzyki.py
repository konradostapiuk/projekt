import pygame

OKNO_SZER = 1024
OKNO_WYS = 1024
FULLSCREEN_SZER = 1920
FULLSCREEN_WYS = 1080
FPS = 60

pygame.init()
okienko = pygame.display.set_mode((OKNO_SZER, OKNO_WYS), 0, 32)
pygame.display.set_caption("Piwkorzyki")
zegarek = pygame.time.Clock()

moja_czcionka = "pricedown bl.otf"

tlo = pygame.image.load("tlo.png")
tlo_fullscreen = pygame.image.load("tlo2.png")
tlo_zasady = pygame.image.load("tlo_zasady3.png")
tlo_zasady2 = pygame.image.load("tlo_zasady2.png")
tlo_ustawienia = pygame.image.load("tlo_ustawienia.png")
tlo_ustawienia2 = pygame.image.load("tlo_ustawienia2.png")


tytul_image = pygame.image.load("tytul2.png")


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
        Przycisk((i_szerokosc - przycisk_szer) // 2, przyciski_y + odstep_y, "przycisk_zasady3", przycisk_szer, przycisk_wys),
        Przycisk((i_szerokosc - przycisk_szer) // 2, przyciski_y + 2 * odstep_y, "przycisk_ustawienia3", przycisk_szer, przycisk_wys),
        Przycisk((i_szerokosc - przycisk_szer) // 2, przyciski_y + 3 * odstep_y, "przycisk_wyjdz3", przycisk_szer, przycisk_wys),
    ]
#def ustawienia_przyciski_po_grze(i_szerokosc, odstep_y, przycisk_szer, przycisk_wys):
    # tutaj dodac img przycisku wyjdz do menu Przycisk((i_szerokosc - przycisk_szer) // 2, przyciski_y, "przycisk_wyjdzdomenu" ,przycisk_szer, przycisk_wys),
    # tutaj dodac img przycisku zagraj ponownie Przycisk((i_szerokosc - przycisk_szer) // 2, przyciski_y, "przycisk_zagrajponownie" ,przycisk_szer, przycisk_wys)

przycisk_szer = 400
przycisk_wys = 120
odstepy_y = 30
tytul_y = 150
full_screen = False

przyciski_menu = ustawienia_przyciski(OKNO_SZER, odstepy_y + przycisk_wys, przycisk_szer, przycisk_wys)

przycisk_pelny_ekran = Przycisk((OKNO_SZER - 200) // 2, (OKNO_WYS - 80) // 2, "fullscreen", 200, 200)

current_screen = "menu"
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

def pokaz_zasady(window):
    window.blit(tlo_zasady, (0, 0))
    tytul_font = pygame.font.Font(moja_czcionka, 100)
    zasady_tytul_text = "ZASADY:"
    zasady_tytul = tytul_font.render(zasady_tytul_text, True, (255, 255, 255))  
    zasady_tytul_rect = zasady_tytul.get_rect(center=(OKNO_SZER // 2, 80))
    window.blit(zasady_tytul, zasady_tytul_rect)
    
    font = pygame.font.Font(moja_czcionka, 24)  
    tekst = [
        "Gra dla dwóch graczy rozgrywana na boisku o wymiarach 10x8 kratek z bramkami o szerokości dwóch kratek kształt boiska przedstawiono na ilustracji poniżej",
        "Celem gry jest umieszczenie w bramce przeciwnika wirtualnej piłki, która początkowo znajduje się na środku boiska, a w kolejnych ruchach jest przemieszczana pomiędzy sąsiednimi przecięciami kratek. W jednym ruchu piłka może być przemieszczona na jedno z ośmiu sąsiednich pól (poziomo, pionowo lub po ukosie) i w wyniku przemieszczenia pozycja początkowa jest łączona odcinkiem z pozycją końcową.",
        "Golem będziemy również nazywać sytuację, w której jeden z graczy zostanie zablokowany, czyli nie będzie miał ani jednej możliwości ruchu",
        "Piłka nie może przemieszczać się wzdłuż brzegu boiska ani po odcinkach, po których już wcześniej się przemieszczała, może jednak się od nich odbijać: jeśli w pozycji końcowej znajdował się przed wykonaniem ruchu koniec odcinka lub brzeg boiska, to po wykonaniu ruchu gracz wykonuje kolejny.",
        "Gra kończy się gdy jeden z graczy zdobędzie wymaganą liczbę goli, która ustalana jest przed rozpoczęciem meczu.",
    ]
    
    y_offset = 200
    line_height = font.get_linesize()  
    paragraph_spacing = 40 
    for paragraph in tekst:
        lines = wrap_text(paragraph, font, OKNO_SZER - 100)
        for line in lines:
            rendered_text = font.render(line, True, (255, 255, 255))  
            window.blit(rendered_text, (OKNO_SZER // 2 - rendered_text.get_width() // 2, y_offset))
            y_offset += line_height
        y_offset += paragraph_spacing  
    
    powrot_text = font.render("Kliknij, aby wrócić do menu", True, (255, 255, 255))
    window.blit(powrot_text, (OKNO_SZER // 2 - powrot_text.get_width() // 2, OKNO_WYS - 100))

def pokaz_zasady_fullscreen(window):
    window.blit(tlo_zasady2, (0, 0))
    tytul_font = pygame.font.Font(moja_czcionka, 150)
    zasady_tytul_text = "ZASADY:"
    zasady_tytul = tytul_font.render(zasady_tytul_text, True, (255, 255, 255)) 
    zasady_tytul_rect = zasady_tytul.get_rect(center=(FULLSCREEN_SZER // 2, 80))
    window.blit(zasady_tytul, zasady_tytul_rect)

    font = pygame.font.Font(moja_czcionka, 35)  
    tekst = [
        "Gra dla dwóch graczy rozgrywana na boisku o wymiarach 10x8 kratek z bramkami o szerokości dwóch kratek kształt boiska przedstawiono na ilustracji poniżej",
        "Celem gry jest umieszczenie w bramce przeciwnika wirtualnej piłki, która początkowo znajduje się na środku boiska, a w kolejnych ruchach jest przemieszczana pomiędzy sąsiednimi przecięciami kratek. W jednym ruchu piłka może być przemieszczona na jedno z ośmiu sąsiednich pól (poziomo, pionowo lub po ukosie) i w wyniku przemieszczenia pozycja początkowa jest łączona odcinkiem z pozycją końcową.",
        "Golem będziemy również nazywać sytuację, w której jeden z graczy zostanie zablokowany, czyli nie będzie miał ani jednej możliwości ruchu",
        "Piłka nie może przemieszczać się wzdłuż brzegu boiska ani po odcinkach, po których już wcześniej się przemieszczała, może jednak się od nich odbijać: jeśli w pozycji końcowej znajdował się przed wykonaniem ruchu koniec odcinka lub brzeg boiska, to po wykonaniu ruchu gracz wykonuje kolejny.",
        "Gra kończy się gdy jeden z graczy zdobędzie wymaganą liczbę goli, która ustalana jest przed rozpoczęciem meczu.",
    ]

    y_offset = FULLSCREEN_WYS // 5
    line_height = font.get_linesize()  
    paragraph_spacing = 50  
    for paragraph in tekst:
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
    
    przycisk_pelny_ekran.skaluj(300, 300)
    przycisk_pelny_ekran.x_cord = (FULLSCREEN_SZER - 300) // 2
    przycisk_pelny_ekran.y_cord = (FULLSCREEN_WYS - 300) // 2
    przycisk_pelny_ekran.wyswietl(window)

    napis = font.render("FULLSCREEN", True, (255, 255, 255))
    window.blit(napis, ((FULLSCREEN_SZER - napis.get_width()) // 2, (FULLSCREEN_WYS) // 2 - 250))

    powrot_text = font.render("Kliknij, aby wrócić do menu", True, (255, 255, 255))
    window.blit(powrot_text, (FULLSCREEN_SZER // 2 - powrot_text.get_width() // 2, FULLSCREEN_WYS - 150))

def pokaz_menu(window):
    window.blit(tlo, (0, 0))
    tytul_rect = tytul_image.get_rect(center=(OKNO_SZER // 2, tytul_y))
    window.blit(tytul_image, tytul_rect)
    for przycisk in przyciski_menu:
        przycisk.wyswietl(window)

def pokaz_menu_fullscreen(window):
    window.blit(tlo_fullscreen, (0, 0))
    tytul_image_fs = pygame.transform.scale(tytul_image, (FULLSCREEN_SZER // 2, FULLSCREEN_WYS // 8))
    tytul_rect = tytul_image_fs.get_rect(center=(FULLSCREEN_SZER // 2, FULLSCREEN_WYS // 8))
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
