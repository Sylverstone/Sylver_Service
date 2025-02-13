import pygame,threading,time
from font_import import *

def font(font_name,size,importer = False):
    if not importer:
        return pygame.font.SysFont(font_name,size)
    return pygame.font.Font(font_name,size)

def verification_size(contenaire : pygame.Rect, nom_font : pygame.font, size : int, texte : str,importer : bool = True, id = 0):
    """Fonction récursive permettant de reduire la taille d'un texte si il est trop grand

    Args:
        contenaire (pygame.Rect): Rect que le texte ne doit pas dépasser
        nom_font (pygame.font): nom de la police utilisée
        size (int): taille du texte original
        texte (str): texte a afficher
    """
    if id == 0:
        if contenaire.w <= font(nom_font,size,importer).size(texte)[0]:
            size -= 2
            return verification_size(contenaire,nom_font,size,texte,importer)
        else:
            return size

def draw_text(text, font = "Comic Sans Ms", color = (0,0,0), x = 0, y = 0,reference_center_x = None,contener = None,size = 20,importer = False, center_multi_line_y = False, ombre = False,center_multi_line = False):
    """Fonction affichant un texte a l'écran

    Args:
        text (str): texte a afficher
        font (str, optional): nom de la police a afficher. Defaults to "Comic Sans Ms".
        color (tuple, optional): couleur du texte a afficher. Defaults to (0,0,0).
        x (int, optional): position en x du texte a afficher. Defaults to 0.
        y (int, optional): position en y du texte a afficher. Defaults to 0.
        reference_center_x (pygame.Surface, optional): Surface sur laquelle le texte doit être centré en x. Defaults to None.
        contener (pygame.Surface, optional): Surface sur laquelle le texte doit être afficher. Defaults to screen.
        size (int, optional): taille du texte a afficher. Defaults to 20.
        importer (bool, optional): Variable indiquant si la varible n'est pas native a pygame ou non. Defaults to False.
        center_multi_line_y (bool, optional): Variable indiquant si le texte est centrer en y (pour les textes avec \\n). Defaults to False.
        ombre (bool, optional): Variable indiquant si le texte doit comporter une ombre. Defaults to False.
        center_multi_line (bool, optional): Variable indiquant si le texte est centrer en x (pour les textes avec \\n). Defaults to False.
    """
    
    text = str(text) #transformer le texte en str 
    all_text = text.split("\n")
    if not importer:
        font_ = pygame.font.SysFont(font, size)
    else:
        font_ = pygame.font.Font(font,size)
    #boucle pour afficher tout les textes de all_text
    
    for enum,text in enumerate(all_text):
        if center_multi_line:
            if reference_center_x==None:
                x = contener.get_rect()[2]/2 - font_.size(text)[0]/2
            else:
                x = reference_center_x.get_rect()[2]/2 - font_.size(text)[0]/2
        if center_multi_line_y:
            y = contener.get_rect()[3]/2 - font_.size(text)[1] * len(all_text)/2
        if ombre:
            text_ = font_.render(str(text), True, (0,0,0))            
            contener.blit(text_, (x+1,y+(size+2)*enum))
        text_ = font_.render(str(text), True, color)
        contener.blit(text_, (x,y+(size + 2)*enum))
        
class Animation:
    
    """Class permettant de generer une animation de chargement

        ## Args:
            * screen (pygame.Surface): Surface sur laquelle l'animation est dessiner
            * text_chargement (str, optional): Texte du chargement Defaults to "Chargement".
            * id_ (int, optional): id representant si l'animation est situé dans un endroit bloquant ou non. Defaults to 1.
    """
    def __init__(self,screen : pygame.Surface,text_chargement : str = "Chargement",id_ : int = 1, color = (0,0,0),ombre = False,font_name = apple_titre,size_text = 18,importer = True,W = None):
        self.screen = screen
        self.texte = text_chargement
        self.running = True
        self.size_text = verification_size(pygame.Rect(0,0,W/16,0),font_name,22,self.texte,True)
        self.font = pygame.font.Font(font_name,self.size_text)
        self.nom_font = font_name        
        self.id_ = id_
        self.nb_point = 0
        self.color = color
        self.importer = importer
        self.ombre = ombre
        
    def start_anime(self,last_screen,delay = 0):
        """Fonction démarrant une animation dans une situation bloquante
            (situation bloquant : le chargement se fait en parallèle du code)
        Args:
            last_screen (pygame.Surface): Dernier écran a afficher
            fond_ecran (list): Fond de l'ecran
            delay(int,optional) : delay représente le temp qu'il faut attendre avant de forcer l'arret de l'animation
        """
        print("début animation chargement")
        self.running = 1
        self.id_ = 0
        th = threading.Thread(target=self.animate, args=(None,last_screen, "",delay),daemon=True)
        th.start()
        
    def animate(self,fond_ecran : list,last_screen : pygame.Surface= None,ajout_decriture :str = None, delay = 0):
        """Fonction permettant d'animer l'animation

        Args:
            fond_ecran (list): couleur du fond de l'ecran
            last_screen (pygame.Surface, optional): Dernier ecran a afficher. Defaults to None.
            ajout_decriture (str, optional): Ajout de texte . Defaults to None.
            delay(int,optional) : delay représente le temp qu'il faut attendre avant de forcer l'arret de l'animation
        """
        screen = self.screen
        if self.id_ == 1:
            self.nb_point += 0.05
            point = "."*((int(self.nb_point) %4))    
            rect_a_update = pygame.Rect(screen.get_rect()[2]/2 - self.font.size(self.texte)[0]/2,screen.get_rect()[3] - 80,200,
                                        50)                                            
            screen.fill(fond_ecran,rect_a_update)            
            draw_text(self.texte + point +"\n"+ajout_decriture,center_multi_line=True,
                      size = self.size_text,font = self.nom_font,
                      y = screen.get_rect()[3] - 2*self.font.size(self.texte + point)[1],contener=screen,
                      color = self.color,
                      importer=self.importer, ombre = self.ombre)
        else:
            print("chargement started")
            
            
            pygame.display.update()
            debut = time.time()
            while self.running:
                self.nb_point += 1
                point = "."*((int(self.nb_point) %4))                                                
                rect_a_update = pygame.Rect(screen.get_rect()[2]/2 - self.font.size(self.texte)[0]/2 - 200,screen.get_rect()[3] - 60,600,300)
                screen.blit(last_screen,(0,0)) 
                actu = time.time() - debut
                if delay == 0:
                    if actu >= 6:
                        ajout_texte = "Pardon pour l'attente"
                        
                    else:
                        ajout_texte = ""
                else:
                    ajout_texte = ""
                    if actu >= delay:
                        self.stop_anime()
                taille_second_texte = self.font.size(ajout_texte)[1]
                taille_premier_texte = self.font.size(self.texte)[1]
                draw_text(self.texte + point + "\n" + ajout_texte,
                          center_multi_line= True,size = self.size_text,
                          font= self.nom_font,y = screen.get_rect()[3]-taille_second_texte-taille_premier_texte - 5,
                          contener=screen,color=self.color,
                          importer=self.importer,ombre = self.ombre)
                pygame.display.update(rect_a_update)
                pygame.time.delay(250)
            print("chargement ended")
            
    def stop_anime(self):
        """Fonction permettant d'arreter une animation qui a été démarrer dans une situation bloquante"""
        print("fin animation chargement")
        self.running = False
        self.id_ = 1