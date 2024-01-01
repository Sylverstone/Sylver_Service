from typing import Tuple
import pygame,tkinter.filedialog
pygame.init()

#Egalement un mini-projet git

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
        """renvoie une image avec les pixels transparents pour les pixels de l'ellipse

            args :
            image (pygame.Surface): l'image a modifier
            rect (pygame.Rect): rectangle de l'ellipse
        """
        start_x = rect[0] + rect[2]/2
        start_y = rect[1] + rect[3]/2
        size=(rect[2], rect[3])
        for y in range(image.get_height()):
            for x in range(image.get_width()):
                if (x - start_x)**2 + (y - start_y)**2 > (size[0]/2)**2:  # Si le pixel est en dehors de l'ellipse (equation de cercle)
                    image.set_at((x,y),(0,0,0,0))
        return image
                      
    def try_to_resize(self,screen : pygame.Surface) -> Tuple[pygame.Surface,pygame.Rect,pygame.Surface]:
        """créé une mini surface où l'utilisteur pourras selectionner la partie d'une image qu'il souhaite

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
        #processus suspect de resize de l'image (fonctionne mal pour les images portraits)
        
        old_width, old_height = image.get_size()
        # Définir la nouvelle largeur (ou hauteur)
        new_width = 500
        # Calculer la nouvelle hauteur (ou largeur) pour conserver le rapport d'aspect (produit en croix)
        new_height = int(old_height * new_width / old_width)
        # Redimensionner l'image
        image = pygame.transform.smoothscale(image, (new_width,new_height))
        #fin processus suspect
        screen_ = pygame.Surface((image.get_size()[0], image.get_size()[1]))
        pos = (width/2 - screen_.get_rect().w/2, 200) #position de où l'image va être mise
        rect_screen = pygame.Rect(*pos,screen_.get_width(),screen_.get_height())
        L = screen_.get_rect()[3] #Largeur
        l = screen_.get_rect()[2] #Longueur
        continuer = True
        can_affiche = False
        new_image = image.copy()
        size = [200,200] #taille original du carré qui continient le cercle, vous pouvez la changer
        start_x = start_y = 0
        rect = pygame.Rect(start_x - size[0]/2,start_y - size[0]/2,*size)

        def verif_sortie(rect : pygame.Rect):
            """Verifie si le Rect sort sort du screen, le repositionne si oui

            Args:
                rect (pygame.Rect): Rect ciblé

            Returns:
                Pygame.Rect: Return le rect ciblé avec ces nouvelles positions
            """
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
        
        def gerer_souris(start_x : float,start_y :float):
            """Transforme la position de la souris en position relative a screen_

            Args:
                start_x (float): Coordonné x de la souris
                start_y (float): Coordonné y de de la souris

            Returns:
                Tuple(float,float): Coordonnés x et y relative a screen_ de la souris
            """
            if start_x < size[0]/2:
                start_x = 0 + size[0]/2
            if start_y < size[0]/2:
                start_y = 0 + size[0]/2
            if start_x > screen_.get_rect().right - size[0]/2:
                start_x = screen_.get_rect().right - size[0]/2
            if start_y > screen_.get_rect().bottom - size[0]/2:
                start_y = screen_.get_rect().bottom - size[0]/2
            return start_x,start_y
        
        
        while continuer:
            mouse = pygame.mouse.get_pos()
            mouse = (mouse[0] - pos[0],mouse[1] - pos[1])
            screen_.blit(image,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continuer = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if size[0] + 20 < new_height: 
                            size[0] += 20
                            size[1] += 20
                    elif event.key == pygame.K_DOWN:
                        if size[0] - 20 > 60: #vous pouvez changer cette taille minimum, meme la retirez
                            size[0] -= 20
                            size[1] -= 20
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                    if size[0] + 20 < new_height: 
                            size[0] += 20
                            size[1] += 20
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                    if size[0] - 20 > 120: #vous pouvez changer cette taille minimum, meme la retirez
                            size[0] -= 20
                            size[1] -= 20
                    
                if (event.type == pygame.KEYDOWN and (event.key == pygame.K_q or event.key == pygame.K_ESCAPE)) :
                    continuer = False
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_c) or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) :
                    new_image = self.rendre_transparent(image,rect)
                    #créé les surfaces qui vont servir a designer une image ronde
                    surf2 = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)
                    surf3 = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)
                    can_affiche = True
        
            start_x = mouse[0] 
            start_y = mouse[1]
            rect = pygame.Rect(start_x - size[0]/2,start_y - size[0]/2,*size)
            verif_sortie(rect)
            start_x,start_y = gerer_souris(start_x,start_y)
            
            pygame.draw.ellipse(screen_,(255,0,0),rect,2)
            if can_affiche:
                pygame.draw.ellipse(surf2, (255, 255, 255), (0,0,*size))
                surf3.blit(surf2, (0, 0))
                surf3.fill((0,0,0,0))
                surf3.blit(new_image, (0, 0),rect)
                continuer = False
            screen.blit(screen_,pos)
            pygame.display.update(rect_screen)
        if not can_affiche:
            raise AnnuleCropPhoto("Vous avez abandonné le choix de photo de profil :(")
        return surf3,rect,image
    
    
if __name__ == "__main__":
    #simulationd de l'integrer dans votre code pygame
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
            path = tkinter.filedialog.askopenfilename(filetypes=[("*","*.png"),("*","*.jpg")])
            image = resizeImage(path)
            image,rect_ellipse,img = image.try_to_resize(screen)
            image = pygame.transform.smoothscale(image, (125,125)) #mettez la taille du l'ellipse que vous souhaitez
            resize_finish = True
        screen.blit(image,(mouse[0] - 125/2,mouse[1] - 125/2)) #mettez les tailles que vous voulez a la place des 2 125
        pygame.display.flip()
pygame.quit()