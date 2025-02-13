#ce fichier ne peut pas pas être inclut dans sylver_service.py, pour des raisons que j'ignore fortement.
import pygame,os
from Class.Color import Color
from Class.Animation import Animation
from Sylver_filedialog import BoiteDialogPygame

pygame.init()
pygame.mixer.init()
pygame.display.init()
pygame.font.init()
pygame.key.set_repeat(750,50)  


resolution = pygame.display.Info()
width = resolution.current_w
height = resolution.current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN | pygame.SCALED | pygame.HWSURFACE | pygame.DOUBLEBUF )

taille_origine = pygame.display.Info()
w_origine = taille_origine.current_w
h_origine = taille_origine.current_h
rect_screen = screen.get_rect()
#palette de couleur qui regroupe toute les couleurs de l'app
palette_couleur = Color()
dialog = BoiteDialogPygame(screen = screen,contour = 1,filtre_blanc=True,base_title="SylverService",echap_destroy_windows=True)
#class animation qui servira a declencher des chargement de deux maniere, soit a des periodes bloquante ou non
animation_chargement = Animation(screen,color = (255,)*3,ombre = True, W = w_origine)
animation_mise_en_ligne = Animation(screen, text_chargement="Mise en ligne",color = (255,)*3,ombre=True,W = w_origine)
animation_connection = Animation(screen, text_chargement = "Connection",color = (255,)*3,ombre = True,W = w_origine)
animation_ouverture = Animation(screen, text_chargement = "Ouverture", color = (255,)*3,ombre=True,W = w_origine)
animation_update = Animation(screen, text_chargement="Mise à jour",color = (255,)*3,ombre=True,W = w_origine)
animation_demarrage_application = Animation(screen,color = (255,255,255), text_chargement="Sylver.service",W = w_origine)
fond_ecran =  palette_couleur.Gris
Clock = pygame.time.Clock()
taille_icone = (50,50)
size_for_title = 72
#preparation imag
rect_goback = pygame.Rect(5,5,*taille_icone)
image_retour = pygame.image.load(os.path.join("Image","Icone_retour.png"))
image_retour = pygame.transform.smoothscale(image_retour,(rect_goback.w,rect_goback.h))
surface_status_co = pygame.Surface((50,50), pygame.SRCALPHA)
surface_status_co.fill((0,0,0,0))
pos_surface_status_co = (w_origine-10,h_origine-10)
fond_nav = pygame.Surface((w_origine,100))
