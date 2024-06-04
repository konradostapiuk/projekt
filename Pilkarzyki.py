import pygame

OKNO_SZER = 1024
OKNO_WYS = 900
FPS = 60

pygame.init()
okienko = pygame.display.set_mode((OKNO_SZER, OKNO_WYS), 0, 32)
pygame.display.set_caption("Piłkarzyki")
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
        
przycisk_graj = Przycisk((OKNO_SZER - 200) // 2 - 100, 300, "przycisk_graj2", 400, 150)
przycisk_zasady = Przycisk((OKNO_SZER - 200) // 2 - 100, 500, "przycisk_zasady2", 400, 150)
przycisk_wyjdz = Przycisk((OKNO_SZER - 200) // 2 - 100, 700, "przycisk_wyjdz2", 400, 150)

graj = True
while graj:
    for zdarzenie in pygame.event.get():
        if zdarzenie.type == pygame.QUIT:
            graj = False
         
    if przycisk_wyjdz.klik():
        graj = False


    okienko.blit(tlo, (0, 0))
    
    
    tytul_rect = tytul_image.get_rect(center=(OKNO_SZER // 2, 150))  
    okienko.blit(tytul_image, tytul_rect)
 
    przycisk_graj.wyswietl(okienko)
    przycisk_zasady.wyswietl(okienko)
    przycisk_wyjdz.wyswietl(okienko)
 
    pygame.display.update()
    zegarek.tick(FPS)
 
pygame.quit()
