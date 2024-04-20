
from Color import Color as palette_couleur
import pygame
from font_import import *
from Sylver_fonction_usuelle import *

class BoiteDialogPygame:
    
    def __init__(self,w : int = 400 ,h : int = 200 ,screen : pygame.Surface = None,fond_filedialong : palette_couleur  = palette_couleur().Gris_clair):
        self.longueur = w
        self.largeur = h
        self.longueur_btn = w/5
        self.largeur_btn = h/5
        self.fond_filedialong = fond_filedialong
        self.screen = screen
        self.icone_interrogation = pygame.transform.smoothscale(\
            pygame.image.load(os.path.join("Image","Icone_interrogation_filedialog.png"))
            ,(25,25))
        self.icone_exclamation = pygame.transform.smoothscale(\
            pygame.image.load(os.path.join("Image","mise-en-garde.png"))
            ,(25,25))
        
        
    def ask_yes_no(self,text : str ,dernier_ecran : pygame.Surface,color_text : tuple = (0,0,0)) -> bool:
        """Boite de dialogue permettant de posez une question fermer. Renvoie True pour oui, False pour non

        Args:
            text (str): texte à afficher
            dernier_ecran (pygame.Surface): fond de la boite de dialogue 
            color_text (tuple, optional): couleur du texte. Defaults to (0,0,0).

        Returns:
            bool: Reponse de l'utilisateur
        """
        self.screen.blit(dernier_ecran,(0,0))
        surface = pygame.Surface((self.longueur,self.largeur),pygame.SRCALPHA)
        longueur_surface, largeur_surface = surface.get_size()
        x_surface = self.screen.get_rect().w/2 - surface.get_width()/2
        y_surface = self.screen.get_rect().h/2 - surface.get_height()/2
        surface_case = pygame.Surface((self.longueur_btn,self.largeur_btn),pygame.SRCALPHA)
        longueur_btn,largeur_btn = surface_case.get_size()
        rect_btn_oui = pygame.Rect(x_surface + longueur_surface/2 - longueur_btn - 20, y_surface + largeur_surface - largeur_btn - 10,*surface_case.get_size())
        rect_btn_non = pygame.Rect(x_surface + longueur_surface/2 + 20, y_surface + largeur_surface - largeur_btn - 10,*surface_case.get_size())
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
            #creation de l'ombre arriere
            surface.fill((0,0,0,0))
            pygame.draw.rect(surface,palette_couleur().Noir,surface.get_rect(),0,35)
            self.screen.blit(surface,(x_surface + 5, y_surface+5))
            #creation logique fenetre
            surface.fill((0,0,0,0))
            pygame.draw.rect(surface,palette_couleur().Gris_clair,surface.get_rect(),0,35)
            pygame.draw.rect(surface,palette_couleur().Noir,surface.get_rect(),1,35)
            barre_noir.fill((0,0,0,0))
            pygame.draw.rect(barre_noir,palette_couleur().Noir,barre_noir.get_rect(),0,0,35,35,0,0)
            surface.blit(barre_noir,(0,0))
            mouse = pygame.mouse.get_pos()
            #evenement
            for event in pygame.event.get():
                if rect_btn_oui.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return True                
                elif rect_btn_non.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return None
            #affichage
            draw_text_(contener=surface,text = "SylverService",x = longueur_surface/2 - font('Arial',15,False).size("Sylver_service")[0]/2,
                      y = 5, color = (255,255,255), font="Arial")
            draw_text_(contener=surface,text = text,x = position_text,
                      y = largeur_surface/2 - hauteur_text/2, font = "Arial",size = taille_text,color=(255,)*3,center_multi_line=True)
            surface.blit(self.icone_interrogation,(20,10))
            self.screen.blit(surface,(x_surface, y_surface))            
            if rect_btn_oui.collidepoint(mouse):
                bord_case[0] = (255,)*3
            else:                
                bord_case[0] = palette_couleur().Noir_clair
            if rect_btn_non.collidepoint(mouse):
                bord_case[1] = (255,)*3
            else:                
                bord_case[1] = palette_couleur().Noir_clair                
            pygame.draw.rect(self.screen,palette_couleur().Noir_clair,rect_btn_oui,0,35)
            pygame.draw.rect(self.screen,bord_case[0],rect_btn_oui,1,35)
            pygame.draw.rect(self.screen,palette_couleur().Noir_clair,rect_btn_non,0,35)
            pygame.draw.rect(self.screen,bord_case[1],rect_btn_non,1,35)
            draw_text_(contener= self.screen,text = "OUI", x = rect_btn_oui.x + rect_btn_oui.w/2 - font(TNN,20,True).size("OUI")[0]/2, 
                      y = rect_btn_oui.y + rect_btn_oui.h/2 - font(TNN,20,True).size("OUI")[1]/2, color=(255,)*3,
                      font = TNN, importer= True,size = 20)
            draw_text_(contener= self.screen,text = "NON", x = rect_btn_non.x + rect_btn_non.w/2 - font(TNN,20,True).size("NON")[0]/2, 
                      y = rect_btn_non.y + rect_btn_non.h/2 - font(TNN,20,True).size("NON")[1]/2, color=(255,)*3,
                      font = TNN, importer= True,size = 20)
            pygame.display.update()
    
    def ask_yes_no_cancel(self,text : str ,dernier_ecran : pygame.Surface,color_text : tuple = (0,0,0)) -> bool:
        """Boite de dialogue permettant de poser une question fermé, Renvoie True pour oui, False pour non, None pour annuler

        Args:
            text (str): texte à afficher sur la FileDialog
            dernier_ecran (pygame.Surface): fond de la boite de dialogue
            color_text (tuple, optional): couleur du texte. Defaults to (0,0,0).

        Returns:
            bool: Reponse de l'utilisateur
        """
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
            surface.fill((0,0,0,0))
            pygame.draw.rect(surface,palette_couleur().Noir,surface.get_rect(),0,35)
            self.screen.blit(surface,(x_surface + 5, y_surface+5))
            #creation logique fenetre
            surface.fill((0,0,0,0))
            pygame.draw.rect(surface,palette_couleur().Gris_clair,surface.get_rect(),0,35)
            pygame.draw.rect(surface,palette_couleur().Noir,surface.get_rect(),1,35)

            barre_noir.fill((0,0,0,0))
            pygame.draw.rect(barre_noir,palette_couleur().Noir,barre_noir.get_rect(),0,0,35,35,0,0)
            surface.blit(barre_noir,(0,0))
            mouse = pygame.mouse.get_pos()
            #evenement
            for event in pygame.event.get():
                if rect_btn_oui.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return True                
                elif rect_btn_non.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return False
                elif rect_btn_annuler.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return None
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return None
            #affichage
            draw_text_(contener=surface,text = "SylverService",x = longueur_surface/2 - font('Arial',15,False).size("Sylver_service")[0]/2,
                      y = 5, color = (255,255,255), font="Arial")
            draw_text_(contener=surface,text = text,x = position_text,
                      y = largeur_surface/2 - hauteur_text/2, font = "Arial",size = taille_text,color=(255,)*3,center_multi_line=True)
            surface.blit(self.icone_interrogation,(20,10))
            self.screen.blit(surface,(x_surface, y_surface))
            i = 0
            for rect in all_rect:
                if rect.collidepoint(mouse):
                    bord_case[i] = (255,)*3
                else:                
                    bord_case[i] = palette_couleur().Noir_clair
                pygame.draw.rect(self.screen,palette_couleur().Noir_clair,rect,0,35)
                pygame.draw.rect(self.screen,bord_case[i],rect,1,35)
                draw_text_(contener= self.screen,text = texts[i], x = rect.x + rect.w/2 - font(TNN,sizes[i],True).size(texts[i])[0]/2, 
                      y = rect.y + rect.h/2 - font(TNN,sizes[i],True).size(texts[i])[1]/2, color=(255,)*3,
                      font = TNN, importer= True,size = sizes[i])
                i+=1          

            pygame.display.update()
            
    def message(self,text : str,dernier_ecran : pygame.Surface) -> None:
        """Fonction permettant d'afficher un message a l'écran, ne renvoie rien

        Args:
            text (str): texte a afficher
            dernier_ecran (pygame.Surface): fond de la boite de dialogue
        """
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
            print(hauteur_text)
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
            surface.fill((0,0,0,0))
            pygame.draw.rect(surface,palette_couleur().Noir,surface.get_rect(),0,35)
            self.screen.blit(surface,(x_surface + 5, y_surface+5))
            #creation logique fenetre
            surface.fill((0,0,0,0))
            pygame.draw.rect(surface,palette_couleur().Gris_clair,surface.get_rect(),0,35)
            pygame.draw.rect(surface,palette_couleur().Noir,surface.get_rect(),1,35)

            barre_noir.fill((0,0,0,0))
            pygame.draw.rect(barre_noir,palette_couleur().Noir,barre_noir.get_rect(),0,0,35,35,0,0)
            surface.blit(barre_noir,(0,0))
            mouse = pygame.mouse.get_pos()
            #evenement
            for event in pygame.event.get():
                if rect_btn_ok.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    affiche = False          
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    affiche = False
            #affichage
            draw_text_(contener=surface,text = "SylverService",x = longueur_surface/2 - font('Arial',15,False).size("Sylver_service")[0]/2,
                      y = 5, color = (255,255,255), font="Arial")
            draw_text_(contener=surface,text = text,x = position_text,
                      y = largeur_surface/2 - hauteur_text/2, font = "Arial",size = taille_text,color=(255,)*3,center_multi_line=True)
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
    screen.fill((0,0,0))
    draw_text_("Voici une demonstration des filedialog de SylverFiledialog",contener=screen,color=(255,255,255),center_multi_line=True)
    last_screen = screen.copy()
    dialog = BoiteDialogPygame(400,200,screen)
    rep = dialog.ask_yes_no("Boîte de dialogue pour oui ou non\nVous pouvez écrire sur plusieurs lignes en utilisant des '\\n'.",last_screen)
    print(rep)
    rep = dialog.message("Boîte de dialogue permettant d'afficher un message, une information, ce que vous voulez :)", last_screen)
    print(rep)
    rep = dialog.ask_yes_no_cancel("Boîte de dialogue pour oui, non ou annuler\nVous pouvez écrire sur plusieurs lignes en utilisant des '\\n'.",last_screen)
    print(rep)
    dialog.message("Les boîtes de dialogue de message tentent de s'adapter lorsque le texte est trop long, tandis que les boîtes de dialogue posant des questions se contentent de réduire la taille du texte.\n Ainsi, il est recommandé de ne pas inclure trop de texte dans les boîtes de questions.",last_screen)