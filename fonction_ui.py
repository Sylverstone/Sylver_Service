from typing import Tuple
import pygame,os,io
from Class.User import User
from font_import import *
from Color import Color

import Sylver_filedialog
palette_couleur = Color()
def draw_text(text, font = "Comic Sans Ms", color = (0,0,0), x = 0, y = 0,reference_center_x = None,contener = None,size = 20,importer = False, center_multi_line_y = False, ombre = False,center_multi_line = False):
    """Fonction affichant un texte a l'écran

    Args:
        text (str): texte a image_userr
        font (str, optional): nom de la police a image_userr. Defaults to "Comic Sans Ms".
        color (tuple, optional): couleur du texte a image_userr. Defaults to (0,0,0).
        x (int, optional): position en x du texte a image_userr. Defaults to 0.
        y (int, optional): position en y du texte a image_userr. Defaults to 0.
        reference_center_x (pygame.Surface, optional): Surface sur laquelle le texte doit être centré en x. Defaults to None.
        contener (pygame.Surface, optional): Surface sur laquelle le texte doit être image_userr. Defaults to screen.
        size (int, optional): taille du texte a image_userr. Defaults to 20.
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
    #boucle pour image_userr tout les textes de all_text
    
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
            texte (str): texte a image_userr
        """
        if id == 0:
            if contenaire.w <= font(nom_font,size,importer).size(texte)[0]:
                size -= 2
                return verification_size(contenaire,nom_font,size,texte,importer)
            else:
                return size       
 
def make_line(text : str,font : pygame.font,size_max : int):
    """Fonction permettant de faire le coupage d'un texte par rapport a son contenaire,
    renvoie le nombre de ligne du texte et ses zones de coupages en plus de sa hauteur

    # Args:
        text (str): text que l'on choisi
        font (pygame.font): la police attribué a ce text
        size_max (int): la taille maximum a ne pas depasser

    # Returns:
        (list,int,float): Renvoie la liste de coupages des caractères, renvoie le nombre de ligne qu'occupe le texte, renvoie la hauteur qu'occupe le texte
    
    * Liste de coupages : liste comportant les indices où une nouvelle ligne commence pour le texte
    """
    coupage = [0]
    line = 1
    start = 0
    i = 0
    while i < len(text):
        size = font.size(text[start:i])[0]
        if size + 5 > size_max:
            w = -1
            while text[start:i][w] != " " and abs(w) < len(text[start:i]):
                w -= 1
            if abs(w) == len(text[start:i]):
                #dans le cas ou il n'y a pas d'espace avant le mot
                w = -1
            i += w #i recule jusqua la position de l'espace, pour eviter de couper un mot
            start = i
            coupage.append(start)
            line+=1
        elif text[start:i][-1:] == "\n": #i recule jusqua la position de l'espace, pour eviter de couper un mot
            start = i
            coupage.append(start)
            line+=1
        i+=1
    y = 0
    for i in range(line):
        y = font.size(text)[1] + font.size(text)[1] * i
    return coupage,line,y

def make_line_n(text : str,font : pygame.font,size_max : int):
    """Fonction permettant de faire le coupage d'un texte par rapport a son contenaire,
    dans cette version de make_line, des \n sont ajouter au texte

    # Args:
        text (str): text que l'on choisi
        font (pygame.font): la police attribué a ce text
        size_max (int): la taille maximum a ne pas depasser

    # Returns:
        (list,int,float): Renvoie la liste de coupages des caractères, renvoie le nombre de ligne qu'occupe le texte, renvoie la hauteur qu'occupe le texte
    
    * Liste de coupages : liste comportant les indices où une nouvelle ligne commence pour le texte
    """
    line = 1
    start = 0
    i = 0
    while i < len(text):
        size = font.size(text[start:i])[0]
        if size + 20 > size_max:
            
            w = -1
            while text[start:i][w] != " " and abs(w) < len(text[start:i]):
                w -= 1
            if abs(w) == len(text[start:i]):
                #dans le cas ou il n'y a pas d'espace avant le mot
                w = -1
            i += w #i recule jusqua la position de l'espace, pour eviter de couper un mot
            start = i
            line+=1
            text = text[0:i] + "\n" + text[i:]
        elif text[start:i][-1:] == "\n":
            line += 1
            start = i
        i+=1            
    
    y = font.size(text)[1] + font.size(text)[1] * (line-1)
    return text,line,y

def calcul_height(text, all_text : list,font : pygame.font):
    """Fonction permettant de calculer la taille de plusieur text

    Args:
        text (str): Le texte étudié en total
        all_text (list): chaque ligne du texte
        font (pygame.font): la police attribué au texte

    Returns:
        float: hauteur du texte
    """
    return font.size(text)[1] * len(all_text)
    
    
def draw_line(line :int,coupage : list,text :str,size : int,contener : pygame.Surface,font : str ,fontz : pygame.font,importer : bool = True,x : float=0,y : float=0):
    """Fonction permmettant d'image_userr un texte contenant plusieurs ligne grace a son coupage de texte

    Args:
        line (int): nombre de line utilisé
        coupage (list): Liste précisant les coupures du texte
        text (str): text que l'on ecrit
        size (int): la taille du texte
        contener (pygame.Surface): la surface sur laquel on ecrit le texte
        font (str): le nom de la font
        fontz (pygame.font): la font du texte
        importer (bool, optional): Indique si la font est une font importer Defaults to True.
        x (float, optional): Position x. Defaults to 0.
        y (float, optional): Position y. Defaults to 0.
    """
    back_x = x
    for i in range(line):
        start = coupage[i]
        if i != line - 1:
            limite = coupage[i+1]
        else:
            limite = len(text)
        if back_x == True:
            x = contener.get_width()/2 - fontz.size(f"{text[start:limite]}")[0]/2
        y = y + fontz.size(text)[1] * i
        draw_text(contener = contener, x = x,
                y = y,
                text = f"{text[start:limite]}",
                size = size, importer = importer, font = font)   

def decoupe_text(coupage : list ,line : int,text_info : str) :
    """Decouper un texte selon son coupage en le mettant dans une liste

    Args:
        coupage (list): liste contenant toute les coupure du texte
        line (int): nombre de ligne du texte
        text_info (str): text utilisé
    Returns:
        list : Represente toutes les lignes du texte
    """
    all_text = []
    for i in range(line):
        start = coupage[i]
        try:
            limite = coupage[i+1]
        except:
            limite = len(text_info)
        all_text.append(text_info[start:limite].strip())
    return all_text


def affiche_photo_profil(last_screen,screen,w_origine,h_origine,photo_deja_charger,palette_couleur,Photo_pp_tiers = False,pseudo = None):
    """Fonction permettant d'image_userr la photo de profil de l'utilisateur ou d'un utilisateur
    
    Args:
        last_screen (pygame.Surface): Dernier écran a image_userr
        Photo_pp_tiers (bool): Si False, c'est que c'est la photo de profil de l'utilisateur qu'il faut, sinon c'est celle d'un utilisateur tiers
    """
    screen.blit(last_screen,(0,0))
    go_back = False
    continuer = True
    surface_photo = pygame.Surface((w_origine/3 + 40 ,h_origine/2 + 40),pygame.SRCALPHA)
    if Photo_pp_tiers == False:
        photo_pp = pygame.image.load(os.path.join("image_user","photo_profil_user.png"))
    else:
        photo_pp = pygame.image.load(io.BytesIO(photo_deja_charger[pseudo][0]))
    dimension_photo_pp = photo_pp.get_size()
    width,height = dimension_photo_pp
    new_width = surface_photo.get_width() - 40
    new_height = new_width*height/width
    while new_height > surface_photo.get_height() - 40:
        new_width -= 20
        new_height = new_width*height/width
    photo_pp = pygame.transform.smoothscale(photo_pp,(new_width,new_height))
    position_photo_pp = (surface_photo.get_width()/2 - new_width/2,surface_photo.get_height()/2 - new_height/2)
    position_surface_photo_pp = (w_origine/2 - surface_photo.get_width()/2,h_origine/2 - surface_photo.get_height()/2)
    text = "Belle photo de profil ;)"
    size = 20
    blanc = (255,) *3
    draw_text(text,apple_titre,blanc,w_origine/2 - font(apple_titre,20,True).size(text)[0]/2,h_origine - font(apple_titre,20,True).size(text)[1] - 10,
            size = size,importer = True,ombre = True,contener=screen)
    fond_semi_colorer(screen,(255,) * 3)
    while continuer and not go_back:
        
        pygame.time.Clock().tick(120)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                go_back = True
        surface_photo.fill((0,0,0,0))
        pygame.draw.rect(surface_photo,palette_couleur.Noir,(0,0,*surface_photo.get_size()),0,60)
        surface_photo.blit(photo_pp,position_photo_pp)
        screen.blit(surface_photo,position_surface_photo_pp)
        pygame.display.flip()
    return continuer
        
def title(text, size = 72, color = (255,) * 3,importer = True, y = 5,screen : pygame.Surface = None):
    """Fonction permettant de mettre un titre

    Args:
        text (str): Texte en titre
        size (str, optional): taille du texte. Defaults to size_for_title.
        color (list, optional): couleur du texte. Defaults to blanc.
        importer (bool, optional): Indique si la police est importer ou non. Defaults to True.
    """
    font_ = font(chivo_titre,size,True)
    w_origine = screen.get_size()[0]
    draw_text(text, size = size,color = palette_couleur.Bleu, x = (w_origine/2 - font_.size(text)[0]/2), y = y,importer = importer, font = chivo_titre,contener=screen)
    
    
def input_popup(w_origine : int, h_origine : int, screen : pygame.Surface, dialog):
    """Fonction permettant d'afficher une input en popup

    Returns:
        bool | str: retourne False si l'input n'a pas été validez, le texte de l'input sinon
    """
    
    pygame.display.flip()
    sous_container = pygame.Surface((w_origine/3,h_origine/3), pygame.SRCALPHA)
    rect_container = pygame.Rect(w_origine/2 - sous_container.get_width()/2, h_origine/2 - sous_container.get_height()/2,sous_container.get_width(),sous_container.get_height())
    width = sous_container.get_width()
    
    height = sous_container.get_height()
    container = pygame.Surface((width - 40,height - 40), pygame.SRCALPHA)
    barre_input = pygame.Surface((3,30))
    active_input = False
    text_input = ""
    max_input = 50
    rect_quit = pygame.Rect(15,10,30,30)
    image_retour = pygame.image.load("Image/Icone_retour.png")
    image_retour = pygame.transform.smoothscale(image_retour,(rect_quit.w,rect_quit.h))
    font_paragraphe = apple_titre

    rect_quit_absolute = pygame.Rect(rect_container.x + 20 + rect_quit.x, rect_container.y + 20 + rect_quit.y, 30,30)
    text_titre = "Ecrivez le nom de votre tuto"
    taille_titre = verification_size(pygame.Rect(0,0,sous_container.get_width() - 90,0),chivo_titre,30,text_titre,True)
    text_active = "Input désactivé"
    color_input = palette_couleur.Bleu
    cancel = False
    finished = False
    taille_input = 25
    width_input = container.get_width()/2
    height_input = 50
    rect_input = pygame.Rect(container.get_width()/2 - width_input/2,
                            container.get_height()/2 - height_input/2,
                            width_input, height_input)
    surf_glissante = pygame.Surface((3000,rect_input.h),pygame.SRCALPHA)
    pos_x = 0
    coupage = False
    surface_ecriture = pygame.Surface((rect_input.w,rect_input.h),pygame.SRCALPHA) #surface
    position_cursor = 0
    while not (cancel or finished):
        pygame.time.Clock().tick(120)
        sous_container.fill((0,0,0,0))
        barre_input.fill((0,0,0))
        mouse = pygame.mouse.get_pos()
        rect_input_absolute = pygame.Rect(rect_container.x + width/2 - (width/2)/2,
                                        rect_container.y + height/2 - 50/2,
                                width/2,
                                50)
        #
        for event in pygame.event.get():
            if rect_input_absolute.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                active_input = not active_input
                color_input = palette_couleur.Noir if active_input else palette_couleur.Bleu
                text_active = "Input activé" if active_input else "Input désactivé"
            if rect_quit_absolute.collidepoint(mouse):
                if  event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    cancel = True
            if active_input:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        position_cursor -= 1
                        if pos_x + x_cursor <= 40:
                            pos_x += 20
                        
                        if abs(position_cursor) >= len(text_input):
                            position_cursor = -len(text_input)
                            pos_x = 0
                    if event.key == pygame.K_RIGHT:
                        if pos_x + x_cursor >= width_input - 40:
                            pos_x -= 20
                        position_cursor += 1 
                        if position_cursor >= 0:
                            position_cursor = 0
                    if event.key == pygame.K_RETURN:
                        rep_user = dialog.ask_yes_no_cancel(f"Voici le nom du tuto que vous avez rentrez : \n '{text_input}'",last_screen)
                        if rep_user:
                            finished = True
                        
                    elif event.key == pygame.K_SPACE and len(text_input) < max_input:
                        text_input = text_input[:len(text_input) + position_cursor] + " " + text_input[len(text_input) + position_cursor:]
                        if font(font_paragraphe,taille_input,True).size(text_input)[0] >= rect_input.w:
                            pos_x -= font(font_paragraphe,taille_input,True).size(" ")[0]
                        else:
                            pos_x = 0
                    elif event.key == pygame.K_BACKSPACE:
                        if len(text_input) > 0 and position_cursor != -(len(text_input)):
                            last_key = text_input[-1]
                            text_input = text_input[:len(text_input) + position_cursor][:-1] + text_input[len(text_input) + position_cursor:]
                            if coupage:
                                pos_x +=  font(font_paragraphe,taille_input,True).size(last_key)[0]
                        else:
                            pos_x = 0
                    else:
                        if len(text_input) < max_input:
                            if event.unicode.isprintable() and event.unicode != "":
                                text_input = text_input[:len(text_input) + position_cursor] + event.unicode + text_input[len(text_input) + position_cursor:]
                                if coupage:
                                    pos_x -= font(font_paragraphe,taille_input,True).size(event.unicode)[0]
                    if font(font_paragraphe,taille_input,True).size(text_input)[0] > rect_input.w - 30:
                        coupage = True
                    else:
                        coupage = False
                        pos_x = 0
                            
        
        #fond
        surface_ecriture.fill((0,0,0,0))
        surf_glissante.fill((0,0,0,0))
        pygame.draw.rect(sous_container,palette_couleur.Noir,sous_container.get_rect(),0,50)
        pygame.draw.rect(container,palette_couleur.Gris_clair,container.get_rect(),0,50)
        pygame.draw.rect(surface_ecriture,color_input,(0,0,rect_input.w,rect_input.h),1)
    
        blanc = (255,) * 3
        draw_text(contener = container, text = text_titre,font = chivo_titre, size = taille_titre, x = (width-40)/2 - font(chivo_titre,taille_titre,True).size(text_titre)[0]/2,
                y = 10,importer = True,color = blanc)
        draw_text(contener = container, text = text_active, font = chivo_titre, size = 18, x = (width-40)/2 - font(chivo_titre,18,True).size(text_active)[0]/2,
                y = (height-40) - 30, importer = True, color = blanc, ombre = True)
        draw_text(text_input, x = 5, y = 10 , font = font_paragraphe, size = taille_input,importer = True,contener = surf_glissante)
        x_cursor,y_cursor =(5 + font(font_paragraphe,taille_input,True).size(text_input[:len(text_input) + position_cursor])[0], 10 + font(font_paragraphe,taille_input,True).size(text_input)[1]/2 - 15)
        #pos_x + x_cursor = position dans l'input de la barre
        if active_input:
            surf_glissante.blit(barre_input,(x_cursor,y_cursor))
        surface_ecriture.blit(surf_glissante,(pos_x,0))
        container.blit(surface_ecriture,rect_input)
        container.blit(image_retour,rect_quit)
        sous_container.blit(container,(20,20))
        screen.blit(sous_container,(rect_container.x,rect_container.y))
        pygame.display.update(rect_container)
        last_screen = screen.copy()
       
    if finished:
        return text_input.strip()
    
    return False

def handleEscape(ev : pygame.event.Event,screen : pygame.Surface,last_screen : pygame.Surface) -> bool:
    rep = False
    if ev.type == pygame.KEYDOWN:
        if ev.key == pygame.K_ESCAPE:
            rep = User.confirm_close(screen,last_screen)
    return rep


def fond_semi_colorer(screen : pygame.Surface, color : Tuple[int],alpha : int = 90):
    
    surface_blanc_transparent = pygame.Surface((screen.get_width(), screen.get_height()),pygame.SRCALPHA)
    surface_blanc_transparent.fill((*color,alpha))
    screen.blit(surface_blanc_transparent,(0,0))