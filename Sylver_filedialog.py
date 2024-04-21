
from Color import Color as palette_couleur
import pygame
from font_import import *
from Sylver_fonction_usuelle import *

class BoiteDialogPygame:
    """
    # BoiteDialogPygame 
        la class permet d'afficher différente boîte de dialogues tel que des oui non, des oui non annuler
        ou bien encore de simple message. Vous pouvez personnalisé les dimensions de la boîte de dialogues, son apparence (contour)
        avec également d'autre option comme son titre de base ainsi que un arrière plan transparent blanc a son affichage

    ## Args:
        * w (int, optional): longueur de la Boite de dialogue. Defaults to 400.
        * h (int, optional): hauteur de la boite de dialogue. Defaults to 200.
        * screen (pygame.Surface, optional): surface sur laquelle est dessiné la boîte de dialogue (conseillez de mettre votre écran). Defaults to None.
        * contour (int, optional): epaisseur du contour de la boîte de dialogue. Defaults to 0.
        * filtre_blanc (bool, optional): Si True, un arrière plan semi-transparent sera présent à l'affichage des boîtes de dialogues. Defaults to False.
        * base_title (str, optional): Titre de base des boîtes de dialogues, il est personnalisable pour les différentes boites de dialogues, si vous ne le changez pas, base_title sera considéré par défaut comme titre de la boite dialogue. Defaults to "Information".
        * echap_destroy_windows (bool,optional): Si True, a l'appuie de la touche echap, peut-importe la fenêtre, elle se fermera (renvoie None forcément)
    """
    
    def __init__(self,w : int = 400 ,h : int = 200 ,screen : pygame.Surface = None,contour = 0, filtre_blanc = False,base_title = "Information",echap_destroy_windows = False):
        self.longueur = w
        self.largeur = h
        self.longueur_btn = w/5
        self.largeur_btn = h/5
        self.screen = screen
        self.icone_interrogation = pygame.transform.smoothscale(\
            pygame.image.load(os.path.join("Image","Icone_interrogation_filedialog.png"))
            ,(25,25))
        self.icone_exclamation = pygame.transform.smoothscale(\
            pygame.image.load(os.path.join("Image","mise-en-garde.png"))
            ,(25,25))
        self.contour = contour
        self.filtre_blanc = filtre_blanc
        self.base_title = base_title
        self.echap_destroy_windows = echap_destroy_windows
        
    def basic_setup(self,surface : pygame.Surface,dernier_ecran : pygame.Surface,x_surface :int,y_surface : int,barre_noir : pygame.Surface) -> None:
        """
        Fonction permettant d'afficher l'esthétique de la boite de dialogue ainsi que son fond

        ## Args:
            * surface (pygame.Surface): surface de la boite de dialogue
            * dernier_ecran (pygame.Surface): fond de la boite de dialogue
            * x_surface (int): position x de la boite de dialogue
            * y_surface (int): position y de la boite de dialogue
            * barre_noir (pygame.Surface): surface de la barre noir de la boite de dialogue
        """
        self.screen.blit(dernier_ecran,(0,0))
        if self.filtre_blanc != False:
                surface_blanc_transparent = pygame.Surface((self.screen.get_width(), self.screen.get_height()),pygame.SRCALPHA)
                surface_blanc_transparent.fill((255,255,255,90))
                self.screen.blit(surface_blanc_transparent,(0,0))
                print("blit")
        #creation de l'ombre arriere
        surface.fill((0,0,0,0))
        pygame.draw.rect(surface,palette_couleur().Noir,surface.get_rect(),0,35)
        self.screen.blit(surface,(x_surface + 5, y_surface+5))
        #creation logique fenetre
        surface.fill((0,0,0,0))
        pygame.draw.rect(surface,palette_couleur().Gris_clair,surface.get_rect(),0,35)
        if self.contour != 0:
            pygame.draw.rect(surface,palette_couleur().Noir,surface.get_rect(),self.contour,35)
        barre_noir.fill((0,0,0,0))
        pygame.draw.rect(barre_noir,palette_couleur().Noir,barre_noir.get_rect(),0,0,35,35,0,0)
        surface.blit(barre_noir,(0,0))
        
    @staticmethod
    def affichage_text_et_titre_fenetre(surface : pygame.Surface,title : str,longueur_surface : int,taille_text : int,text : str ,position_text : int,largeur_surface : int,hauteur_text : int) -> None:
        """Fonction permettant d'afficher le contenu texte de la boite de dialogue ainsi que son texte

        ## Args:
            * surface (pygame.Surface): Surface de la boite de dialogue
            * title (str): titre de la boite de dialogue
            * longueur_surface (int): longueur de la boite de dialogue
            * taille_text (int): taille du contenu (texte) de la boite de dialogue
            * text (str): contenu (texte) de la boite de dialogue
            * position_text (int): position x du contenu (texte) de la boite de dialogue 
            * largeur_surface (int): largeur de la boite de dialogue
            * hauteur_text (int): hauteur du contenu (texte) de la boite de dialogue 
        """
        draw_text_(contener=surface,text = title,x = longueur_surface/2 - font('Arial',15,False).size(title)[0]/2,
                      y = 5, color = (255,255,255), font="Arial")
        draw_text_(contener=surface,text = text,x = position_text,
                    y = largeur_surface/2 - hauteur_text/2, font = "Arial",size = taille_text,color=(255,)*3,center_multi_line=True)
        
    def affiche_case(self,all_rect : list,mouse : tuple,bord_case : list,texts : list) -> None:
        """Fonction permettant d'afficher les btn de la boite de dialogue

        ## Args:
            * all_rect (list): tous les rects des boutons de la boite de dialogue
            * mouse (tuple): coordonné de la souris (x,y)
            * bord_case (list): listes contenu les couleurs des bords des boutons
            * texts (list): listes contenant les textes affichés sur les bouton
        """
        i = 0
        for rect in all_rect:
            if rect.collidepoint(mouse):
                bord_case[i] = (255,)*3
            else:                
                bord_case[i] = palette_couleur().Noir_clair
            pygame.draw.rect(self.screen,palette_couleur().Noir_clair,rect,0,35)
            pygame.draw.rect(self.screen,bord_case[i],rect,1,35)
            draw_text_(contener= self.screen,text = texts[i], x = rect.x + rect.w/2 - font(TNN,17,True).size(texts[i])[0]/2, 
                    y = rect.y + rect.h/2 - font(TNN,17,True).size(texts[i])[1]/2, color=(255,)*3,
                    font = TNN, importer= True,size = 17)
            i+=1
            
    def ask_yes_no(self,text : str ,dernier_ecran : pygame.Surface,color_text : tuple = (0,0,0),title = "") -> bool | None:
        """Boite de dialogue permettant de posez une question fermer. Renvoie True pour oui, False pour non

        Args:
            * text (str): texte à afficher
            * dernier_ecran (pygame.Surface): fond de la boite de dialogue 
            * color_text (tuple, optional): couleur du texte. Defaults to (0,0,0).

        Returns:
            bool: Reponse de l'utilisateur
        """
        
        print(self.filtre_blanc)
        if title == "":
            title = self.base_title
        surface = pygame.Surface((self.longueur,self.largeur),pygame.SRCALPHA)
        longueur_surface, largeur_surface = surface.get_size()
        x_surface = self.screen.get_rect().w/2 - surface.get_width()/2
        y_surface = self.screen.get_rect().h/2 - surface.get_height()/2
        surface_case = pygame.Surface((self.longueur_btn,self.largeur_btn),pygame.SRCALPHA)
        longueur_btn,largeur_btn = surface_case.get_size()
        rect_btn_oui = pygame.Rect(x_surface + longueur_surface/2 - longueur_btn - 20, y_surface + largeur_surface - largeur_btn - 10,*surface_case.get_size())
        rect_btn_non = pygame.Rect(x_surface + longueur_surface/2 + 20, y_surface + largeur_surface - largeur_btn - 10,*surface_case.get_size())
        all_rect = [rect_btn_oui,rect_btn_non]
        texts = ["OUI","NON"]
        taille_text = 25
        text, ligne,hauteur_text = make_line_n(text,font("Arial",25,False),surface.get_width() - 40 )
        while hauteur_text >  rect_btn_non.top - y_surface - largeur_btn:
            taille_text -= 1
            text, ligne,hauteur_text = make_line_n(text,font("Arial",taille_text,False),surface.get_width() - 40)
        if font("Arial",25,False).size(text)[0] > surface.get_width():
            position_text = 0
        else:
            position_text = surface.get_width()/2 - font("Arial",25,False).size(text)[0]/2
        bord_case = [(255,255,255),(255,255,255),(255,255,255)]
        affiche = True
        reponse_user = None
        barre_noir = pygame.Surface((longueur_surface,40),pygame.SRCALPHA)
        while affiche:
            self.basic_setup(surface,dernier_ecran,x_surface,y_surface,barre_noir)
            mouse = pygame.mouse.get_pos()
            #evenement
            for event in pygame.event.get():
                if rect_btn_oui.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return True                
                elif rect_btn_non.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return False
                if self.echap_destroy_windows:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        return None
            #affichage
            BoiteDialogPygame.affichage_text_et_titre_fenetre(surface,title,longueur_surface,taille_text,text,position_text,largeur_surface,hauteur_text)
            surface.blit(self.icone_interrogation,(20,10))
            self.screen.blit(surface,(x_surface, y_surface))            
            self.affiche_case(all_rect,mouse,bord_case,texts)
            pygame.display.update()
    
    def ask_yes_no_cancel(self,text : str ,dernier_ecran : pygame.Surface,color_text : tuple = (0,0,0),title = "") -> bool | None:
        """Boite de dialogue permettant de poser une question fermé, Renvoie True pour oui, False pour non, None pour annuler

        Args:
            * text (str): texte à afficher sur la FileDialog
            * dernier_ecran (pygame.Surface): fond de la boite de dialogue
            * color_text (tuple, optional): couleur du texte. Defaults to (0,0,0).

        Returns:
            bool: Reponse de l'utilisateur
        """
        if title == "":
            title = self.base_title
        self.screen.blit(dernier_ecran,(0,0))
        surface = pygame.Surface((self.longueur,self.largeur),pygame.SRCALPHA)
        longueur_surface, largeur_surface = surface.get_size()
        x_surface = self.screen.get_rect().w/2 - surface.get_width()/2
        y_surface = self.screen.get_rect().h/2 - surface.get_height()/2
        surface_case = pygame.Surface((self.longueur_btn,self.largeur_btn),pygame.SRCALPHA)
        longueur_btn,largeur_btn = surface_case.get_size()
        rect_btn_non = pygame.Rect(x_surface + longueur_surface/2 - longueur_btn/2, y_surface + largeur_surface - largeur_btn - 10,*surface_case.get_size())
        rect_btn_oui = pygame.Rect(x_surface + longueur_surface/2 - longueur_btn/2 - longueur_btn - 20, y_surface + largeur_surface - largeur_btn - 10,*surface_case.get_size())
        rect_btn_annuler = pygame.Rect(x_surface + longueur_surface/2 - longueur_btn/2 + longueur_btn + 20, y_surface + largeur_surface - largeur_btn - 10,*surface_case.get_size())
        all_rect = [rect_btn_oui,rect_btn_non,rect_btn_annuler]
        taille_text = 25
        text, ligne,hauteur_text = make_line_n(text,font("Arial",25,False),surface.get_width() - 40 )
        while hauteur_text >  rect_btn_non.top - y_surface - largeur_btn:
            taille_text -= 1
            text, ligne,hauteur_text = make_line_n(text,font("Arial",taille_text,False),surface.get_width() - 40)
        if font("Arial",25,False).size(text)[0] > surface.get_width():
            position_text = 0
        else:
            position_text = surface.get_width()/2 - font("Arial",25,False).size(text)[0]/2
        bord_case = [(255,255,255),(255,255,255),(255,255,255)]
        texts = ["OUI","NON","ANNULER"]
        sizes = [20,20,17]
        affiche = True
        reponse_user = None
        barre_noir = pygame.Surface((longueur_surface,40),pygame.SRCALPHA)
        while affiche:
            #creation de l'ombre arriere
            self.basic_setup(surface,dernier_ecran,x_surface,y_surface,barre_noir)
            mouse = pygame.mouse.get_pos()
            #evenement
            for event in pygame.event.get():
                if rect_btn_oui.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return True                
                elif rect_btn_non.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return False
                elif rect_btn_annuler.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return None
                if self.echap_destroy_windows:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        return None
            #affichage
            BoiteDialogPygame.affichage_text_et_titre_fenetre(surface,title,longueur_surface,taille_text,text,position_text,largeur_surface,hauteur_text)
            surface.blit(self.icone_interrogation,(20,10))
            self.screen.blit(surface,(x_surface, y_surface))
            self.affiche_case(all_rect,mouse,bord_case,texts)       
            pygame.display.update()
            
    def message(self,text : str,dernier_ecran : pygame.Surface,title = "") -> None:
        """Fonction permettant d'afficher un message a l'écran, ne renvoie rien

        Args:
            * text (str): texte a afficher
            * dernier_ecran (pygame.Surface): fond de la boite de dialogue
        """
        if title == "":
            title = self.base_title
        self.screen.blit(dernier_ecran,(0,0))
        surface = pygame.Surface((self.longueur,self.largeur),pygame.SRCALPHA)
        longueur_surface, largeur_surface = surface.get_size()
        x_surface = self.screen.get_rect().w/2 - surface.get_width()/2
        y_surface = self.screen.get_rect().h/2 - surface.get_height()/2
        surface_case = pygame.Surface((self.longueur_btn,self.largeur_btn),pygame.SRCALPHA)
        longueur_btn,largeur_btn = surface_case.get_size()
        rect_btn_ok = pygame.Rect(x_surface + longueur_surface/2 - longueur_btn/2, y_surface + largeur_surface - largeur_btn - 10,*surface_case.get_size())
        taille_text = 25
        text_origine = text
        taille_surface = surface.get_width()
        text, ligne,hauteur_text = make_line_n(text_origine,font("Arial",25,False),surface.get_width() - 40 )
        taille_surface_max = 700
        while hauteur_text >  rect_btn_ok.top - y_surface - largeur_btn:
            taille_text -= 0.1
            taille_surface += 5
            if taille_surface > taille_surface_max:
                taille_surface = taille_surface_max
            text, ligne,hauteur_text = make_line_n(text_origine,font("Arial",int(taille_text),False),taille_surface)
        taille_text = int(taille_text)
        surface = pygame.Surface((taille_surface,self.largeur),pygame.SRCALPHA) 
        longueur_surface, largeur_surface = surface.get_size()
        x_surface = self.screen.get_rect().w/2 - surface.get_width()/2
        y_surface = self.screen.get_rect().h/2 - surface.get_height()/2
        if font("Arial",25,False).size(text)[0] > surface.get_width():
            position_text = 0
        else:
            position_text = surface.get_width()/2 - font("Arial",25,False).size(text)[0]/2
        bord_case = [(255,255,255),(255,255,255)]
        affiche = True
        reponse_user = None
        barre_noir = pygame.Surface((longueur_surface,40),pygame.SRCALPHA)
        while affiche:
            #creation de l'ombre arriere
            self.basic_setup(surface,dernier_ecran,x_surface,y_surface,barre_noir)
            mouse = pygame.mouse.get_pos()
            #evenement
            for event in pygame.event.get():
                if rect_btn_ok.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    affiche = False        
                if self.echap_destroy_windows:

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        affiche = False
            #affichage
            BoiteDialogPygame.affichage_text_et_titre_fenetre(surface,title,longueur_surface,taille_text,text,position_text,largeur_surface,hauteur_text)
            surface.blit(self.icone_exclamation,(20,10))
            self.screen.blit(surface,(x_surface, y_surface))            
            if rect_btn_ok.collidepoint(mouse):
                bord_case[0] = (255,)*3
            else:                
                bord_case[0] = palette_couleur().Noir_clair                          
            pygame.draw.rect(self.screen,palette_couleur().Noir_clair,rect_btn_ok,0,35)
            pygame.draw.rect(self.screen,bord_case[0],rect_btn_ok,1,35)
            draw_text_(contener= self.screen,text = "OK", x = rect_btn_ok.x + rect_btn_ok.w/2 - font(TNN,20,True).size("OK")[0]/2, 
                      y = rect_btn_ok.y + rect_btn_ok.h/2 - font(TNN,20,True).size("OK")[1]/2, color=(255,)*3,
                      font = TNN, importer= True,size = 20)
            pygame.display.update()
            
if __name__ == "__main__":   
    pygame.init()
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    screen.fill((106,110,255))
    draw_text_("Voici une demonstration des filedialog de SylverFiledialog",contener=screen,color=(255,255,255),center_multi_line=True)
    last_screen = screen.copy()
    dialog = BoiteDialogPygame(400,200,screen,1,True,echap_destroy_windows=True)
    rep = dialog.ask_yes_no("Boîte de dialogue pour oui ou non\nVous pouvez écrire sur plusieurs lignes en utilisant des '\\n'.",last_screen)
    rep = dialog.message("Boîte de dialogue permettant d'afficher un message, une information, ce que vous voulez :)", last_screen)
    rep = dialog.ask_yes_no_cancel("Boîte de dialogue pour oui, non ou annuler\nVous pouvez écrire sur plusieurs lignes en utilisant des '\\n'.",last_screen)
    dialog.message("Les boîtes de dialogue de message tentent de s'adapter lorsque le texte est trop long, tandis que les boîtes de dialogue posant des questions se contentent de réduire la taille du texte.\n Ainsi, il est recommandé de ne pas inclure trop de texte dans les boîtes de questions.",last_screen)