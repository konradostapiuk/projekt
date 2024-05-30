import pygame

OKNO_SZER = 800
OKNO_WYS = 950
FPS = 60
 
TŁO = (9, 145, 13)

pygame.init()
okienko = pygame.display.set_mode((OKNO_SZER, OKNO_WYS), 0, 32)
pygame.display.set_caption("Piłkarzyki")
zegarek = pygame.time.Clock()
 
graj = True
while graj:
    for zdarzenie in pygame.event.get():
        if zdarzenie.type == pygame.QUIT:
            graj = False
 
    okienko.fill(TŁO)
 
    pygame.display.update()
    zegarek.tick(FPS)
 
pygame.quit()
