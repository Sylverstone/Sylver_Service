import pygame,threading,time
from font_import import *
from Sylver_class_import import draw_text

class Animation:
    
    """Class permettant de generer une animation de chargement

        Args:
            screen (pygame.Surface): Surface sur laquelle l'animation est dessiner
            text_chargement (str, optional): Texte du chargement Defaults to "Chargement".
            id_ (int, optional): id representant si l'animation est situé dans un endroit bloquant ou non. Defaults to 1.
    """
    def __init__(self,screen : pygame.Surface,text_chargement : str = "Chargement",id_ : int = 1, color = (0,0,0),ombre = False,font_name = apple_titre,size_text = 18,importer = True):
        self.screen = screen
        self.texte = text_chargement
        self.running = True
        self.font = pygame.font.Font(font_name,size_text)
        self.nom_font = font_name
        self.size_text = size_text
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
        self.running = False
        self.id_ = 1