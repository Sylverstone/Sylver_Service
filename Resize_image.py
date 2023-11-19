from typing import Tuple
import pygame

from Sylver_class_import import User

pygame.init()

class AnnuleCropPhoto(Exception):
    def __init__(self, what) -> None:
        self.what = what
        super().__init__(self.what)
      
      
def draw_text(text, font = "Comic Sans Ms", color = (0,0,0), x = 0, y = 0,contener = None,size = 20,importer = False, ombre = False):
    """
        dessiner un texte a une position donné
        :param 1: text qu'on veut dessiner
        :param 2: font qu'utilise le texte
        :param 3: couleur du texte
        :param 4: coordonne x ou le dessiner
        :param 5: coordonne y ou le dessiner
        :CU: arg 1 est un str, arg 2 est de type font.FONT ou font.SysFont, arg 3 est un rbg, arg 4 et 5 sont des int
    """
    if not importer:
        font_ = pygame.font.SysFont(font, size)
    else:
        font_ = pygame.font.Font(font,size)
    if ombre:
        text_ = font_.render(str(text), True, (0,0,0))
        contener.blit(text_, (x+1,y+1))
    text_ = font_.render(str(text), True, color)
    contener.blit(text_, (x,y)) 
     
class resizeImage:
    def __init__(self,chemin):
        self.chemin = chemin
        
    @staticmethod
    def rendre_transparent(image : pygame.Surface,rect):
        start_x = rect[0] + rect[2]/2
        start_y = rect[1] + rect[3]/2
        size=(rect[2], rect[3])
        for y in range(image.get_height()):
            for x in range(image.get_width()):
                if (x - start_x)**2 + (y - start_y)**2 > (size[0]/2)**2:  # Si le pixel est en dehors de l'ellipse (equation de cercle)
                    image.set_at((x,y),(0,0,0,0))
        return image
                      
    def try_to_resize(self,screen : pygame.Surface) -> Tuple[pygame.Surface,pygame.Rect,pygame.Surface]:
        """créé une mini surface où l'utilisteur pourras selectionner la partie de son image qu'il veut en photo de profil

        Args:
            screen (pygame.Surface): surface ou afficher la mini surface pour crop

        Raises:
            Renvoie AnnuleCropPhoto dans le cas ou l'utilisateur n'a pas achevé sa manoeuvre

        Returns:
            Tuple[pygame.Surface,pygame.Rect,pygame.Surface]: renvoie la surface ou est mise l'image crop, le rect de l'ellipse qui a permit de crop l'image, et l'image qui a été utilsé et resize
        """
        resolution = pygame.display.Info()
        width = resolution.current_w
        height = resolution.current_h
        image = pygame.image.load(self.chemin).convert_alpha()
        old_width, old_height = image.get_size()
        # Définir la nouvelle largeur (ou hauteur)
        new_width = 500
        # Calculer la nouvelle hauteur (ou largeur) pour conserver le rapport d'aspect (produit en croix)
        new_height = int(old_height * new_width / old_width)
        # Redimensionner l'image
        image = pygame.transform.smoothscale(image, (new_width,new_height))
        screen_ = pygame.Surface((image.get_size()[0], image.get_size()[1]))
        pos = (width/2 - screen_.get_rect().w/2, 200)
        L = screen_.get_rect()[3]
        l = screen_.get_rect()[2]
        continuer = True
        mouse_click = False
        can_affiche = False
        new_image = image.copy()
        size = (200,200)
        start_x = start_y = 0
        rect = pygame.Rect(start_x - size[0]/2,start_y - size[0]/2,*size)

        def verif_sortie(rect : pygame.Rect):
            scr = screen_.get_rect()
            if rect.left < 0:
                rect.left = scr.left
            if rect.top < 0:
                rect.top = scr.top
            if rect.bottom > L:
                rect.bottom = scr.bottom
            if rect.right > l:
                rect.right = scr.right
            return rect
        
        def gerer_souris(start_x,start_y):
            if start_x < size[0]/2:
                start_x = 0 + size[0]/2
            if start_y < size[0]/2:
                start_y = 0 + size[0]/2
            if start_x > screen_.get_rect().right - size[0]/2:
                start_x = screen_.get_rect().right - size[0]/2
            if start_y > screen_.get_rect().bottom - size[0]/2:
                start_y = screen_.get_rect().bottom - size[0]/2
            return start_x,start_y
        text = "Bouger votre souris pour faire deplacer le cercle, appuyer sur 'c' pour valider, ou 'q','Echap' pour quitter"
        font = pygame.font.SysFont("Arial",40)
        draw_text(text = text, contener= screen,
                  x = width/2 - font.size(text)[0]/2, y = 20, font = "Arial",size=40)   
        while continuer:
            mouse = pygame.mouse.get_pos()
            mouse = (mouse[0] - pos[0],mouse[1] - pos[1])
            screen_.blit(image,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continuer = False
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_q or event.key == pygame.K_ESCAPE):
                    continuer = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                    #technique pour sauvegarder: enregistrer le rect de l'image en base de données. puis a chaque fois que l'user se connect ducoup on re rend transparent son image avec la bonne ellipse et bonne formule puis on met le blit en surf3 avec le bon rect
                    new_image = self.rendre_transparent(image,rect)
                    surf2 = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)
                    surf3 = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)
                    can_affiche = True
        
            start_x = mouse[0] 
            start_y = mouse[1]
            rect = pygame.Rect(start_x - size[0]/2,start_y - size[0]/2,*size)
            verif_sortie(rect)
            start_x,start_y = gerer_souris(start_x,start_y)
            
            pygame.draw.ellipse(screen_,(0,0,0),rect,2)
            if can_affiche:
                pygame.draw.ellipse(surf2, (255, 255, 255), (0,0,*size))
                surf3.blit(surf2, (0, 0))
                surf3.fill((0,0,0,0))
                surf3.blit(new_image, (0, 0),rect)
                continuer = False
            screen.blit(screen_,pos)
            pygame.display.flip()
        if not can_affiche:
            raise AnnuleCropPhoto("Vous avez abandonné le choix de photo de profil :(")
        return surf3,rect,image
    
    
if __name__ == "__main__":
    resolution = pygame.display.Info()
    width = resolution.current_w
    height = resolution.current_h
    screen = pygame.display.set_mode((width, height - 20), pygame.FULLSCREEN | pygame.SCALED | pygame.HWSURFACE | pygame.DOUBLEBUF)
    continuer = True
    resize_finish = False
    while continuer:
        screen.fill((255,0,0))
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    continuer = False
            if event.type == pygame.QUIT:
                continuer = False
        
        if not resize_finish:
            path = User.get_file()[0]
            image = resizeImage(path)
            image,rect_ellipse,img = image.try_to_resize(screen)
            image = pygame.transform.smoothscale(image, (125,125))
            resize_finish = True
        screen.blit(image,(mouse[0] - 125/2,mouse[1] - 125/2))
        pygame.display.flip()
pygame.quit()