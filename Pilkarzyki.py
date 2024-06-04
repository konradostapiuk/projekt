import pygame

OKNO_SZER = 800
OKNO_WYS = 800
FPS = 60
 
TŁO = (9, 145, 13)

pygame.init()
okienko = pygame.display.set_mode((OKNO_SZER, OKNO_WYS), 0, 32)
pygame.display.set_caption("Piłkarzyki")
zegarek = pygame.time.Clock()

#tworzenie klasy 'przycisk' do menu.
class Przycisk:
    def __init__(self, x_cord, y_cord, file_name):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.button_image = pygame.image.load(f"{file_name}.png")
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.button_image.get_width(), self.button_image.get_height())
        
    def klik(self):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                return True
    
    def wyswietl(self, window):
        window.blit(self.button_image, (self.x_cord, self.y_cord))
     
#przyciski w menu głównym
przycisk_graj = Przycisk((OKNO_SZER-366)/2 - 80, 50, "przycisk_graj")
przycisk_zasady = Przycisk((OKNO_SZER-366)/2 - 80, 300, "przycisk_zasady")
przycisk_wyjdz = Przycisk((OKNO_SZER-366)/2 - 80, 550, "przycisk_wyjdz")

graj = True
while graj:
    for zdarzenie in pygame.event.get():
        if zdarzenie.type == pygame.QUIT:
            graj = False
         
    if przycisk_wyjdz.klik():
        graj = False

 
    okienko.fill(TŁO)
 
    przycisk_graj.wyswietl(okienko)
    przycisk_zasady.wyswietl(okienko)
    przycisk_wyjdz.wyswietl(okienko)
 
    pygame.display.update()
    zegarek.tick(FPS)
 
pygame.quit()
