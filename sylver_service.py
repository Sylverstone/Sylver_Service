import pygame,os,datetime,sys,threading,keyboard,time,math,io,random,dotenv
from Sylver_class_import import Gerer_requete,User,status_connection
from Animation import Animation
from Color import Color
from Resize_image import AnnuleCropPhoto, resizeImage
from Sylver_filedialog import BoiteDialogPygame
from font_import import *
from Exception import *
from Sylver_fonction_usuelle import *
import webbrowser
import smtplib, ssl
from email.message import EmailMessage

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.mixer.init()
pygame.display.init()
pygame.font.init()
pygame.key.set_repeat(750,50)  
dotenv.load_dotenv()
print("debut app")

#reglage de l'ecran
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

Clock = pygame.time.Clock()
message_categorie_compte = "Choisir une catégorie de compte permettra a l'application\
de vous proposez une recherche par défaut a l'ouverture du menu. Afin d'en choisir\
une clickez sur les case ! Vous pourrez alors lire la description des catégories ici même :). (Vous avez la possibilité de scroll si vous ne voyez pas toute les categories) "
message_categorie_tuto = "Choisir une catégorie pour votre tuto vous permettra d'être référencer chez les utilisateurs ayant une catégorie de compte !\
    Egalement, vos tuto seront disponible dans la recherche par catégorie de votre catégorie.\
        Afin d'en choisir une clickez sur les case ! Vous pourrez alors lire la description des catégories ici même :). (Vous avez la possibilité de scroll si vous ne voyez pas toute les categories) "
taille_icone = (50,50)
#preparation imag
rect_goback = pygame.Rect(5,5,*taille_icone)
image_retour = pygame.image.load(os.path.join("Image","Icone_retour.png"))
image_retour = pygame.transform.smoothscale(image_retour,(rect_goback.w,rect_goback.h))

photo_deja_charger = {} #dict qui va repertorier les photos déjà charger afin de ne pas les recharger

    
def draw_text(text, font = "Comic Sans Ms", color = (0,0,0), x = 0, y = 0,reference_center_x = None,contener = screen,size = 20,importer = False, center_multi_line_y = False, ombre = False,center_multi_line = False):
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
        
def ecrire_tuto(user : User | None,pre_text = "",pre_titre = "",id_tuto_a_supprimer = None):  
    """Fonction permettant a l'utilisateur décrire son tuto, cette fonction est également utilisé pour permettre a l'utilisateur décrire
        un signalement

    Args:
        user (User | None): Class representant les données de l'utilisateur
    """
    global fond_nav
    global continuer
    barre_input = pygame.Surface((2,30))
    barre_input.fill(noir)
    font_paragraphe = apple_titre
    font20 = pygame.font.Font(font_paragraphe, 20)
    font40 = pygame.font.Font(font_paragraphe, 40)
    surf_valider = pygame.Surface((200,50), pygame.SRCALPHA)
    surf_titre = pygame.Surface((300,50),pygame.SRCALPHA)
    surf_glissant_titre = pygame.Surface((3000,surf_titre.get_height()), pygame.SRCALPHA)
    surf_valider.fill((0,0,0,0))
    s_width = surf_valider.get_width()
    s_height = surf_valider.get_height()
    rect_valider = surf_valider.get_rect(x=w_origine - s_width - 30,
                                        y = h_origine - s_height - 20)    
    surf_ecrit = pygame.Surface((w_origine - 40, h_origine - 300 ), pygame.SRCALPHA)
    surf_glissant_ecrit = pygame.Surface((surf_ecrit.get_width(),3000),pygame.SRCALPHA)
    rect_titre = pygame.Rect(20,120,surf_titre.get_width(),surf_titre.get_height())
    rect_surf_ecrit = pygame.Rect(20,200,surf_ecrit.get_width(),surf_ecrit.get_height())
    pos_x = 0
    pos_y_ecrit = 0
    dict_input = {
        "input_titre" : { "max" : 50,"x" : 10,"y" : rect_titre.h/2 - font(font_paragraphe,30,True).size("m")[1]/2,"surf" : surf_glissant_titre,"input" : ["Titre",],
                        "zone_ecrit" : 0,"can_do_multiple_lines" : False, "base" : "Titre", "active" : False,"rect" : rect_titre, "time": 0, "take_time" : False,
                        "coupage" : 0,"all_size" : 0,"can_write" : True},
        
        "input_text" : {"coupage" : 0, "max" : 4000,"x" : 20,"y" : 30 ,"surf" : surf_glissant_ecrit, "input" : ["Contenu",], "zone_ecrit" : 0,
                        "can_do_multiple_lines" : True,"can_write" : True, "base" : "Contenu", "all_size" : 0,"active" : False,"rect" : rect_surf_ecrit,"time": 0, "take_time" : False}
    }
    if pre_text:
        coupage,line,y = make_line(pre_text,font(font_paragraphe,30,True),surf_ecrit.get_width() - 20)
        text_decoupe = decoupe_text(coupage,line,pre_text)
        dict_input["input_text"]["input"] = text_decoupe
        dict_input["input_text"]["zone_ecrit"] = len(text_decoupe) - 1 
        dict_input["input_text"]["active"] = True
        caractere = 0
        for mot in text_decoupe:
            for c in mot:
                caractere += 1
        dict_input["input_text"]["all_size"] = caractere
        while pos_y_ecrit + y > surf_ecrit.get_height() - 40:
            pos_y_ecrit  -= 30
        dict_input["input_titre"]["input"] = [pre_titre,]
        dict_input["input_titre"]["all_size"] = len(pre_titre)
        while pos_x + font(font_paragraphe,30,True).size(pre_titre)[0] > surf_titre.get_width() - 30:
            pos_x -= 20
    base_input_text = dict_input["input_text"]["base"]
    base_input_titre = dict_input["input_titre"]["base"]
    a_ecrit = False
    
    go_back = False
    rect_a_ne_pas_depasser = rect_screen
    rect_a_ne_pas_depasser.w -= (image_retour.get_width() * 2)
    if user != None:
        texte_title = f"Ecrivez ici votre tutoriel {user.pseudo}"
        size_du_titre = verification_size(rect_a_ne_pas_depasser,chivo_titre,size_for_title,texte_title,True)
    else:
        texte_title = "Écrivez ici votre signalement"
        size_du_titre = verification_size(rect_a_ne_pas_depasser,chivo_titre,size_for_title,texte_title,True)
    #boucle principale
    cursor_ecriture = 0 # 0 signifi cursor a la fin du mot
    ecrit_en_plus = False
    while continuer:
        Clock.tick(120)
        screen.fill(fond_ecran)
        fond_nav.fill(palette_couleur.Noir)  
        mouse = pygame.mouse.get_pos()
        #boucle evenementielle
        for event in pygame.event.get():
            if rect_goback.collidepoint(mouse):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    go_back = True
            ### Validation de l'input => mettre le tuto en bdd ###
            if rect_valider.collidepoint(mouse):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if ''.join(dict_input["input_text"]["input"]) != base_input_text and ''.join(dict_input["input_titre"]["input"]) != base_input_titre:
                        all_input = [text + "\n" for text in dict_input["input_text"]["input"]]
                        dict_input["input_text"]["input"] = all_input
                        if user != None:                            
                            #.strip() utilisé pour supprimer les espaces au debut et a la fin
                            text_pour_tuto = ''.join(dict_input["input_text"]["input"])
                            text_pour_tuto = text_pour_tuto.strip()
                            titre = ''.join(dict_input["input_titre"]["input"])
                            titre = titre.strip()
                            try:
                                if user.categorie != None:
                                    rep = dialog.ask_yes_no_cancel(f"Souhaitez vous mettre a ce tuto la même catégorie que votre compte ? ({user.categorie})",last_screen)
                                else:
                                    rep = False
                                if  rep is False:
                                    categorie = interface_deroullante_categorie(last_screen,"Choisissez la catégorie de votre tuto",message_categorie_tuto)
                                elif rep is True:
                                    categorie = user.categorie
                                elif rep is None:
                                    categorie = None
                                if categorie != None:
                                    if dialog.ask_yes_no("Doit-on considerer votre tuto comme une demande de tuto / Annonce ?",last_screen):
                                        is_annonce = 1
                                    else:
                                        is_annonce = 0
                                    animation_mise_en_ligne.start_anime(last_screen)
                                    if not pre_text:
                                        user.save_tuto(None,text_pour_tuto,titre,categorie,is_annonce)
                                    else:
                                        user.modifier_tuto(None,text_pour_tuto,titre,categorie,is_annonce,id_tuto_a_supprimer)
                                    animation_mise_en_ligne.stop_anime()
                                    go_back = True 
                            except noConnection:
                                dialog.message("Une erreur de connexion a eu lieu !",last_screen,title="Erreur")
                                
                            except Exception as e:
                                dialog.message("Une erreur est survenue ! ", last_screen,title="Erreur")
                            else:
                                if not pre_text:
                                    if rep != None:
                                        dialog.message("Votre tuto a bien été mis en ligne ! ",last_screen)
                                else:
                                    if rep != None:
                                        dialog.message("Votre tuto a bien été modifié !",last_screen)
                        else:
                            #si user = None, c'est un signalement qui est écrit
                            #.strip() utilisé pour supprimer les espaces au debut et a la fin
                            text_pour_tuto = ' '.join(dict_input["input_text"]["input"])
                            text_pour_tuto = text_pour_tuto.strip()
                            titre = ''.join(dict_input["input_titre"]["input"])
                            titre = titre.strip()
                            animation_mise_en_ligne.start_anime(last_screen)
                            return text_pour_tuto, titre
                    else:
                        dialog.message("Votre Tuto est vide. Vous ne pouvez pas le valider tant qu'il est vide !",last_screen)
                        
            ################################### Logique de l'input #################################      
            for elt in dict_input.values():
                if elt["rect"].collidepoint(mouse): 
                    #si je fais avec mouse click le click est tjr detecter
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        elt["active"] = not elt["active"]
                        if elt["active"] == False and len(elt["input"]) == 1 and elt["input"][0] == "":
                            elt["input"][0] = elt["base"]
                        elif elt["active"] == True and len(elt["input"]) == 1 and elt["input"][0] == elt["base"]:
                            elt["input"][0] = ""
                        for elt2 in dict_input.values():
                            if elt2 != elt:
                                elt2["active"] = False
                                if len(elt2["input"]) == 1 and elt2["input"][0] == "":
                                    elt2["input"][0] = elt2["base"]                             
                        
                if elt["active"]:
                    if event.type == pygame.KEYDOWN:
                        len_input = len(elt["input"][elt["zone_ecrit"]])
                        #systeme de copié collé defaillant
                        """if event.key == pygame.K_v and event.mod & pygame.KMOD_CTRL:
                            text_pasted = pyperclip.paste()
                            cursor = 0
                            debut = 0
                            while cursor < len(text_pasted):
                                if font(font_paragraphe,30,True).size(elt["input"][elt["zone_ecrit"]] + text_pasted[debut:cursor])[0] > surf_ecrit.get_width() - 40:
                                    elt["input"][elt["zone_ecrit"]] += text_pasted[debut:cursor]
                                    elt["input"].append("")
                                    debut = cursor +1
                                    elt["zone_ecrit"] += 1
                                cursor += 1"""
                        if event.key == pygame.K_LEFT:
                            cursor_ecriture -= 1
                            if abs(cursor_ecriture) >= len(elt["input"][elt["zone_ecrit"]]):
                                if elt["zone_ecrit"] > 0:
                                    elt["zone_ecrit"] -= 1
                                    cursor_ecriture = 0
                                    print(elt["input"][elt["zone_ecrit"]])
                                else:
                                    cursor_ecriture = -len(elt["input"][elt["zone_ecrit"]])
                                
                        if event.key == pygame.K_RIGHT:
                            cursor_ecriture += 1
                            if cursor_ecriture >= 0:
                                if elt["zone_ecrit"] != len(elt["input"]) -1:
                                    elt["zone_ecrit"] += 1
                                    #elt["input"][elt["zone_ecrit"] - 1] += "\n"
                                    cursor_ecriture = -len(elt["input"][elt["zone_ecrit"]])
                                else:
                                    cursor_ecriture = 0
                                    
                        if event.key == pygame.K_UP and elt["can_do_multiple_lines"]:
                            #changer de zone d'ecriture vers le haut
                            elt["zone_ecrit"] -= 1 if elt["zone_ecrit"] > 0 else 0                     
                            if  elt["y"] * len(elt["input"]) + 40 > surf_ecrit.get_height():            
                                pos_y_ecrit += 30
                                if pos_y_ecrit >= 0:
                                    pos_y_ecrit = 0 
                                                        
                        elif event.key == pygame.K_SPACE and elt["can_write"]:
                            if len(''.join(elt["input"]).strip()) < elt["max"]:
                                a_ecrit= True
                                
                                elt["input"][elt["zone_ecrit"]] = elt["input"][elt["zone_ecrit"]][:len_input + cursor_ecriture] + " " + elt["input"][elt["zone_ecrit"]][len_input + cursor_ecriture:]
                                elt["all_size"] += 1
                                
                        elif event.key == pygame.K_BACKSPACE:
                            
                            if elt["input"][elt["zone_ecrit"]] != "":
                                element_retirer = elt["input"][elt["zone_ecrit"]][-1]
                                elt["input"][elt["zone_ecrit"]] = elt["input"][elt["zone_ecrit"]][:len_input +  cursor_ecriture][:-1] + elt["input"][elt["zone_ecrit"]][len_input +  cursor_ecriture:]
                                elt["all_size"] -= 1
                                if not elt["can_do_multiple_lines"]:
                                    pos_x += 0.5
                                    print(font(font_paragraphe,30,True).size(element_retirer)[0])
                                    if pos_x >= 0:
                                        pos_x = 0
                            else:
                                if elt["can_do_multiple_lines"]:
                                    if len(elt["input"]) > 1:
                                        #supprimer la ligne
                                        del(elt["input"][elt["zone_ecrit"]])
                                        elt["zone_ecrit"] -= 1 
                                        #  = True
                                        if elt["y"] * len(elt["input"]) + 40 > surf_ecrit.get_height():
                                            pos_y_ecrit += 30
                                            if pos_y_ecrit >= 0:
                                                pos_y_ecrit = 0
                                    else:
                                        pos_y_ecrit = 0   
                                else:
                                    
                                    pos_x = 0             
                                                    
                        elif (event.key == pygame.K_RETURN) and elt["can_do_multiple_lines"] and elt["can_write"] :
                            #elt["input"][elt["zone_ecrit"]] += "\n"
                            if cursor_ecriture != 0:
                                origine_input = elt["input"][elt["zone_ecrit"]]
                                elt["input"][elt["zone_ecrit"]] = elt["input"][elt["zone_ecrit"]][:cursor_ecriture]# + "\n"
                                
                                #ajouter une zone d'ecriture
                                elt["input"].insert(elt["zone_ecrit"] + 1,origine_input[cursor_ecriture:])
                            else:
                                #elt["input"][elt["zone_ecrit"]] += "\n"
                                elt["input"].insert(elt["zone_ecrit"] + 1,"")
                            elt["zone_ecrit"]+=1
                            elt["input"][elt["zone_ecrit"]] = elt["input"][elt["zone_ecrit"]].strip()
                            if elt["y"] * len(elt["input"]) + 40 > surf_ecrit.get_height():
                                add = font(font_paragraphe,30,True).size("m")[1]
                                pos_y_ecrit -= 30
                            cursor_ecriture = 0
                            
                        elif event.key == pygame.K_DOWN:
                            elt["zone_ecrit"] += 1 if elt["zone_ecrit"] < len(elt["input"]) -1 else 0
                            if elt["zone_ecrit"] < len(elt["input"]) -1:
                                if elt["y"] * len(elt["input"][:elt["zone_ecrit"]]) +40 > surf_ecrit.get_height():
                                    pos_y_ecrit -= 35 
                                    
                        elif event.key == pygame.K_ESCAPE:
                            pass
                        else:
                            if len(''.join(elt["input"]).strip())< elt["max"] and elt["can_write"]:
                                if event.unicode.isprintable() and event.unicode != "":
                                    a_ecrit = True
                                    elt["input"][elt["zone_ecrit"]] = elt["input"][elt["zone_ecrit"]][:len_input +  cursor_ecriture] + event.unicode + elt["input"][elt["zone_ecrit"]][len_input +  cursor_ecriture:]                                   
                                    elt["all_size"] += 1
                            
                        if len(elt["input"][elt["zone_ecrit"]]) > 0 and a_ecrit and elt["can_do_multiple_lines"]:
                            if font(font_paragraphe,30,True).size(elt["input"][elt["zone_ecrit"]])[0] >= surf_ecrit.get_width() - 40:
                                if elt["y"] * len(elt["input"]) + 40 < surf_ecrit.get_height():
                                    ecrit_en_plus = False    
                                    """elt["input"].append("")
                                    elt["zone_ecrit"] +=1"""
                                    dernier_mot = ""
                                    cursor = -1 
                                    while abs(cursor) <= len(elt["input"][elt["zone_ecrit"]]) and elt["input"][elt["zone_ecrit"]][cursor] != " " :
                                        cursor -= 1
                                    if abs(cursor) > len(elt["input"][elt["zone_ecrit"]]):
                                        dernier_mot = elt["input"][elt["zone_ecrit"]][-1]
                                        cursor =  -1
                                    else:
                                        dernier_mot = elt["input"][elt["zone_ecrit"]][cursor:].strip()

                                    elt["input"][elt["zone_ecrit"]] = elt["input"][elt["zone_ecrit"]][:cursor] 
                                    
                                    elt["input"].insert(elt["zone_ecrit"] + 1,"")
                                    elt["zone_ecrit"] += 1
                                    elt["input"][elt["zone_ecrit"]] += dernier_mot
                                    
                                    
                                else:
                                    ecrit_en_plus = True  
                                    add = font(font_paragraphe,30,True).size(event.unicode)[1]
                                    if event.key != pygame.K_BACKSPACE:
                                        pos_y_ecrit -= 30
                                        dernier_mot = ""
                                        cursor = -1 
                                        while abs(cursor) <= len(elt["input"][elt["zone_ecrit"]]) and elt["input"][elt["zone_ecrit"]][cursor] != " " :
                                            cursor -= 1
                                        if abs(cursor) > len(elt["input"][elt["zone_ecrit"]]):
                                            dernier_mot = elt["input"][elt["zone_ecrit"]][-1]
                                            cursor =  -1
                                        else:
                                            dernier_mot = elt["input"][elt["zone_ecrit"]][cursor:].strip()

                                        elt["input"][elt["zone_ecrit"]] = elt["input"][elt["zone_ecrit"]][:cursor]
                                        
                                        elt["input"].insert(elt["zone_ecrit"] + 1,"")
                                        elt["zone_ecrit"] += 1
                                        elt["input"][elt["zone_ecrit"]] += dernier_mot
                                    else:
                                        add = font(font_paragraphe,30,True).size(element_retirer)[1]
                                        pos_y_ecrit += 30
                            
                                    
                        elif elt["can_do_multiple_lines"] == False:
                            if len(''.join(elt["input"]).strip()) < elt["max"]:
                                if (font(font_paragraphe,30,True).size(elt["input"][elt["zone_ecrit"]])[0] >= surf_titre.get_width() - 20):
                                    add = font(font_paragraphe,30,True).size(event.unicode)[0]
                                    if event.key != pygame.K_BACKSPACE:
                                        pos_x -= add
                                    else:
                                        add = font(font_paragraphe,30,True).size(element_retirer)[0]
                                        pos_x += add
                        a_ecrit = False            
        surf_valider.fill((0,0,0,0))
        surf_titre.fill((0,0,0,0))
        surf_glissant_titre.fill((0,0,0,0))
        surf_glissant_ecrit.fill((0,0,0,0))
        pygame.draw.rect(surf_titre,blanc,(0,0,*surf_titre.get_size()),0,20)
        pygame.draw.rect(screen,palette_couleur.Gris_clair,(rect_titre[0] -10,
                                        rect_titre[1] -10
                                        ,surf_titre.get_width() + 20, surf_titre.get_height() +20),0,20)      
        surf_ecrit.fill((255,255,255,0))
        pygame.draw.rect(surf_ecrit,blanc,(0,0,surf_ecrit.get_width(),surf_ecrit.get_height()),0,20)
        pygame.draw.rect(screen,palette_couleur.Gris_clair,(rect_surf_ecrit[0]-10,rect_surf_ecrit[1]-10,surf_ecrit.get_width() + 20,surf_ecrit.get_height() +20),0,20)
        color_valider = palette_couleur.Bleu if  rect_valider.collidepoint(mouse) else (0,0,0)
        pygame.draw.rect(surf_valider,color_valider,(0,0,*rect_valider[2:4]),1,20)
        draw_text(text = "Valider", contener = surf_valider,x= s_width/2 - font40.size("valider")[0]/2, color = color_valider,font = font_paragraphe, importer=True, size = 40)       
        for keys,elt in dict_input.items():
            for enum,i in enumerate(elt["input"]):
                #ecrire tout les lignes dans all_input
                if keys == "input_titre":
                    add = 1
                else:
                    
                    add = 0
                draw_text(i,importer=True,size = 30,contener=elt["surf"], x = elt["x"], y = elt["y"]*(enum+add), font=font_paragraphe)
            if elt["active"]:
                add = 1 if keys == "input_titre" else 0
                len_text = len(elt["input"][elt["zone_ecrit"]])
                text_tuto = elt["input"][elt["zone_ecrit"]]
                elt["surf"].blit(barre_input, (elt["x"] + font(font_paragraphe,30,True).size(text_tuto[:len_text + cursor_ecriture])[0], 2 + elt["y"] * (elt["zone_ecrit"]+add))) #le y le met a la position du texte adapter en fonction de zone_ecrit
        surf_ecrit.blit(surf_glissant_ecrit,(0,pos_y_ecrit))
        surf_titre.blit(surf_glissant_titre,(pos_x,0))
        screen.blit(surf_titre,(rect_titre[0],rect_titre[1]))
        screen.blit(surf_valider,(rect_valider[0],rect_valider[1]))
        screen.blit(surf_ecrit,(rect_surf_ecrit[0],rect_surf_ecrit[1]))
        screen.blit(fond_nav,(0,0))
        screen.blit(image_retour,rect_goback) 
        if user != None:
            title(texte_title,size = size_du_titre)
        else:
            title("Écrivez ici votre signalement",size = size_du_titre)
        if go_back:
            break
        screen.blit(surface_status_co,pos_surface_status_co)
        last_screen = screen.copy()
        pygame.display.flip()
    

def trait(x : float,y : float ,longueur : float ,surf : pygame.Surface,epaisseur = 2):
    """Fonction permettant de dessiner un trait
    Args:
        x (float): position x du trait
        y (float): position y du trait
        longueur (float): longueur du trait a dessiner
        surf (pygame.Surface): Surface sur laquelle est dessinée le trait
        epaisseur (int, optional): epaisseur du trait. Defaults to 3.
    """
    pygame.draw.rect(surf,(0,0,0),(x,y,longueur,epaisseur))      


def interface_deroullante_categorie(last_screen,message1 = "Choisissez votre catégorie de compte",message2 = message_categorie_compte):
    """Fonction permettant a l'utilisateur de choisir sa catégorie

    Args:
        last_screen (pygame.Surface): Dernier écran à afficher
        message1 (str, optional): message de consigne à ajouter. Defaults to "Choisissez votre catégorie de compte".
        message2 (str, optional): message de description à ajouter. Defaults to message_categorie_compte.

    Returns:
        _type_: _description_
    """    
    rect_go_back = pygame.Rect(5,5,30,30)
    texte = message1
    texte_infos_categorie = message2
    
    liste_categorie = {}
    for i in range(len(recup_categorie)):
        liste_categorie[recup_categorie[i][0]] = recup_categorie[i][1].replace("\r","").replace("\n","")
    nom_categorie = [nom for nom in liste_categorie.keys()]
    surface_categorie = pygame.Surface((w_origine/3,h_origine/2), pygame.SRCALPHA)
    surface_ecriture_categorie = pygame.Surface((surface_categorie.get_width() - 200,h_origine/2),pygame.SRCALPHA)
    height = h_origine/2
    taille_totale = surface_ecriture_categorie.get_width() + 20 + surface_categorie.get_width()
    rect_surf_categorie = pygame.Rect(w_origine/2 - taille_totale/2,h_origine/2 - height/2,surface_categorie.get_width(),surface_categorie.get_height())
    x_base = w_origine/2 -taille_totale/2
    y_base = h_origine/2 -height/2
    ecart = 20
    font_paragraphe = apple_titre
    rect_case_categorie = pygame.Rect(0,0,surface_categorie.get_width(),20)
    rect_case_categorie.h = 75
    case_max_visu = surface_categorie.get_height()/(75 + ecart)
    surface_glissante = pygame.Surface((surface_categorie.get_width(),(rect_case_categorie.h + ecart)*len(recup_categorie)), pygame.SRCALPHA)
    all_rect_case_rel = []
    all_rect_case_abs = []
    all_coupage_line_y= {}
    size_text = [30,]* len(recup_categorie)

    i = 0
    for key, value in liste_categorie.items():
        coupage,line,y = make_line(value,font(font_paragraphe,size_text[i],True),surface_ecriture_categorie.get_width())
        while y >= surface_categorie.get_height() - 40:
            size_text[i] -= 2
            coupage,line,y = make_line(value,font(font_paragraphe,size_text[i],True),surface_ecriture_categorie.get_width())
        all_text = decoupe_text(coupage,line,value)
        all_coupage_line_y[key] = {"coupage":coupage, "line":line,"y":y,"liste_texte" : all_text}
        i+=1
        
    for i in range(len(liste_categorie)):
            pos_x = rect_case_categorie.x
            pos_y = rect_case_categorie.y + (rect_case_categorie.h +ecart) *i
            rect = pygame.Rect(x_base + pos_x,y_base+pos_y,rect_case_categorie.w,rect_case_categorie.h)
            all_rect_case_abs.append(rect.copy())
            rect.x -= x_base
            rect.y -= y_base
            all_rect_case_rel.append(rect)
            
    size_base = 30
    coupage_base,line_base_,y_base = make_line(texte_infos_categorie,font(font_paragraphe,size_base,True),surface_ecriture_categorie.get_width())
    while y_base >= surface_ecriture_categorie.get_height() - 60:
        size_base -= 2
        coupage_base,line_base_,y_base = make_line(texte_infos_categorie,font(font_paragraphe,size_base,True),surface_ecriture_categorie.get_width())
    all_text_base = decoupe_text(coupage_base,line_base_,texte_infos_categorie)
    Categorie_choisi = None
    go_back = False
    pos_y_surf_glissante = 0
    while continuer:
        Clock.tick(120)

        screen.blit(last_screen,(0,0))
        draw_text(texte, color = blanc, x = w_origine/2 -  font(font_paragraphe,20,True).size(texte)[0]/2, y = h_origine-  font(font_paragraphe,20,True).size(texte)[1],
                font = font_paragraphe, importer = True)
        surface_categorie.fill((0,0,0,0))
        #pygame.draw.rect(surface_categorie,palette_couleur.Noir,(0,0,*surface_categorie.get_size()),0,20)
        surface_ecriture_categorie.fill((0,0,0,0))
        pygame.draw.rect(surface_ecriture_categorie,palette_couleur.Noir,(0,0,*surface_ecriture_categorie.get_size()),0,20)
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            i = 0
            for rect in all_rect_case_abs:
                if rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    Categorie_choisi = nom_categorie[i]
                    go_back = True
                i += 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                go_back = True
        
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 5) or (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN):
                pos_y_surf_glissante -= 20
                add = -20
            
                if abs(pos_y_surf_glissante) >= surface_glissante.get_height() - (rect_case_categorie.h + ecart)*(case_max_visu):
                    pos_y_surf_glissante += 20
                    add  = 0
                i = 0
                for rect in all_rect_case_abs:
                    rect.y += add
                    i+=1
            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 4) or (event.type == pygame.KEYDOWN and event.key == pygame.K_UP):
                if pos_y_surf_glissante < 0:
                    pos_y_surf_glissante += 20
                    for rect in all_rect_case_abs:
                        rect.y += 20
                        
        for i in range(len(liste_categorie)):
            pos_x = rect_case_categorie.w/2 - font(TNN,40,True).size(nom_categorie[i])[0]/2
            pos_y = rect_case_categorie.y + (rect_case_categorie.h +ecart) *i
            pygame.draw.rect(surface_glissante,palette_couleur.Noir,all_rect_case_rel[i])
            draw_text(nom_categorie[i], x = pos_x, y = pos_y + rect_case_categorie.h/2 - font(TNN,40,True).size(nom_categorie[i])[1]/2, color = palette_couleur.Bleu, contener = surface_glissante,
                    font = TNN, importer = True, size = 40,ombre = True)
        aucun_affichage = True
        for z,rect in enumerate(all_rect_case_abs):
            if rect.collidepoint(mouse):
                aucun_affichage = False
                size = verification_size(pygame.Rect(0,0,surface_ecriture_categorie.get_width(),0),TNN,30,nom_categorie[z],True)
                draw_text(nom_categorie[z],ombre = True,size = size, x = surface_ecriture_categorie.get_width()/2 - font(TNN,size,True).size(nom_categorie[z])[0]/2, y = 10, color = palette_couleur.Bleu_clair, contener = surface_ecriture_categorie, font = TNN, importer = True)
                categorie = nom_categorie[z]
                """draw_line(all_coupage_line_y[categorie]["line"],all_coupage_line_y[categorie]["coupage"],liste_categorie[categorie],20,contener = surface_ecriture_categorie,
                        font = font_paragraphe, fontz = font(font_paragraphe,20,True),importer = True,y = 30)"""
                for i in range(len(all_coupage_line_y[categorie]["liste_texte"])):
                    all_texte = all_coupage_line_y[categorie]["liste_texte"]
                    draw_text(all_texte[i],font_paragraphe,blanc,y = 40 + ((size_text[z]+5)*i),contener = surface_ecriture_categorie,
                                importer = True,size = size_text[z], x = 5)
            
                
        if aucun_affichage:
            text = "Pourquoi choisir une catégorie ?"
            size = verification_size(pygame.Rect(0,0,surface_ecriture_categorie.get_width(),0),TNN,30,text,True)
            draw_text(text,ombre = True,size = size, x = surface_ecriture_categorie.get_width()/2 - font(TNN,size,True).size(text)[0]/2, y = 10, color = (255,100,100), contener = surface_ecriture_categorie, font = TNN, importer = True)
            for i in range(len(all_text_base)):
                draw_text(all_text_base[i],font_paragraphe,blanc,y = 40 + ((size_base+5)*i),contener = surface_ecriture_categorie,
                            importer = True,size = size_base, x = 5)
        surface_categorie.fill((255,255,255,100))
        surface_categorie.blit(surface_glissante,(0,pos_y_surf_glissante))
        screen.blit(surface_categorie,(w_origine/2 - taille_totale/2,h_origine/2 - height/2))
        screen.blit(surface_ecriture_categorie,(w_origine/2  - taille_totale/2 +surface_categorie.get_width() + 20 ,h_origine/2 - height/2))
        pygame.display.update()
        if go_back:
            break
    return Categorie_choisi
    
def add_to_texte(text,cursor,ajout):
    return text[:len(text) + cursor] + ajout + text[len(text) + cursor:]

def contact():
    
    def look_valid(dict_input):
        for key,value in dict_input.items():
            if len(value["input"]) > 1:
                if " ".join(value["input"]).strip() in ("", " "):
                    return False
            else:
                if (value["input"][0] == value["Default"] or value["input"][0].strip() in (""," ")) and key != "Input_emails":
                    return False
        return True 
                
    global fond_nav
    global continuer
    back = False
    barre_input = pygame.Surface((2,20))
    barre_input.fill((0,0,0))
    background_input = (255,255,255)
    font_paragraphe = apple_titre

    rect_input_nom = pygame.Rect(50,115,w_origine * 20/100,50)
    surface_nom = pygame.Surface((rect_input_nom.w,rect_input_nom.h),pygame.SRCALPHA)
    surface_gliss_nom = pygame.Surface((2000,rect_input_nom.h),pygame.SRCALPHA)
    
    rect_input_objet = pygame.Rect(rect_input_nom.x + rect_input_nom.w + 10,rect_input_nom.y,rect_input_nom.w,rect_input_nom.h)
    surface_input_objet = surface_nom.copy()
    surface_gliss_objet = surface_gliss_nom.copy()
    
    rect_input_emails = pygame.Rect(rect_input_objet.x + rect_input_objet.w + 20 ,rect_input_nom.y,w_origine - rect_input_objet.w - rect_input_objet.x - 20 - rect_input_nom.x,rect_input_nom.h)
    surface_emails = pygame.Surface((rect_input_emails.w,rect_input_emails.h),pygame.SRCALPHA)
    surface_gliss_emails = pygame.Surface((2000,rect_input_nom.h),pygame.SRCALPHA)
    
    rect_input_contenu = pygame.Rect(rect_input_nom.x,rect_input_nom.h + rect_input_nom.y + 40,w_origine - rect_input_nom.x*2, h_origine - (rect_input_nom.h + rect_input_nom.y) - 50)
    surface_contenu = pygame.Surface((rect_input_contenu.w,rect_input_contenu.h),pygame.SRCALPHA)
    surface_gliss_contenu = pygame.Surface((rect_input_contenu.w,5000),pygame.SRCALPHA)
    
    
    rect_valider = pygame.Rect(0,10,w_origine*8/100,80)
    rect_valider.x = w_origine - rect_valider.w - 20
    dict_input = {
        
        "Input_nom" : {"Cursor" :  0 ,"Default" : "Nom", "max" : 100,"input" : ["Nom",],"active" : False,"surf_exacte" :surface_nom, "surf" : surface_gliss_nom, "rect" :rect_input_nom,"pos_x" : 0,"pos_y" : 0,"ligne_ecrit" : 0},
        "Input_emails" : {"Cursor" : 0,"Default" : "Emails (Non obligatoire)", "max" : 100,"input" : ["Emails (Non obligatoire)",],"surf_exacte" : surface_emails,"surf" : surface_gliss_emails,"active" : False,"rect" :rect_input_emails,"pos_x" : 0,"pos_y" : 0,"ligne_ecrit" : 0},
        "Input_contenu" : {"Cursor" : 0,"Default" : "Contenu", "max" : 3000,"input" : ["Contenu",],"active" : False,"surf_exacte" : surface_contenu,"surf" : surface_gliss_contenu,"rect" :rect_input_contenu,"pos_x" : 0,"pos_y" : 0,"ligne_ecrit" : 0},
        "Input_objet" : {"Cursor" : 0,"Default" : "Sujet", "max" : 100,"input" : ["Sujet",],"active" : False,"surf_exacte" : surface_input_objet,"surf" : surface_gliss_objet,"rect" :rect_input_objet,"pos_x" : 0,"pos_y" : 0,"ligne_ecrit" : 0},
    }
    all_rect = [rect_input_nom,rect_input_emails,rect_input_contenu]
    k_down = False
    text_envoyer = "Envoyez"
    taille_envoyez = font(font_paragraphe,30,True).size(text_envoyer)
    go_back = False
    while continuer:
        screen.fill(palette_couleur.Gris_clair)
        fond_nav.fill(palette_couleur.Noir)
        screen.blit(fond_nav,(0,0))
        title("Envoyez nous un email :)")
        mouse = pygame.mouse.get_pos()
        screen.blit(image_retour,(5,5))
        try:
            for event in pygame.event.get():
                if rect_valider.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if look_valid(dict_input):
                        pass
                    else:
                        dialog.message("Veuillez bien complétez les cases avant d'envoyez",dernier_ecran,"Contact")
                if rect_goback.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    go_back = True
                for value in dict_input.values():
                    if value["rect"].collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        value["active"] = not value["active"]
                        if value["active"]:
                            if len(value["input"]) == 1 and value["input"][0] == value["Default"]:
                                value["input"] = ["",]
                            for other_value in dict_input.values():
                                if other_value != value:
                                    other_value["active"] = False
                                    if len(value["input"]) == 1 and other_value["input"][0] == "":
                                        other_value["input"][0] = other_value["Default"]
                        else:
                            if len(value["input"]) == 1 and value["input"] == "":
                                value["input"][0] = value["Default"]
                    if value["active"]:
                        input = value["input"][value["ligne_ecrit"]]
                        cursor = value["Cursor"]
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_UP:
                                value["ligne_ecrit"] -= 1
                                if value["ligne_ecrit"]< 0:
                                    value["ligne_ecrit"] = 1
                            elif event.key == pygame.K_DOWN:
                                value["ligne_ecrit"] += 1
                                if value["ligne_ecrit"] >= len(value["input"]):
                                    value["ligne_ecrit"] = len(value["input"]) -1
                                    
                            elif event.key == pygame.K_LEFT:
                                value["Cursor"] -= 1
                                if abs(value["Cursor"]) > len(value["input"][value["ligne_ecrit"]]):
                                    if value["ligne_ecrit"] - 1 >= 0 :
                                        value["ligne_ecrit"] -= 1
                                        value["Cursor"] = 0
                                    else:
                                        value["Cursor"] = -len(value["input"][value["ligne_ecrit"]])
                            elif event.key == pygame.K_RIGHT:
                                value["Cursor"] += 1
                                if value["Cursor"] > 0:
                                    if value["ligne_ecrit"] + 1 < len(value["input"]):
                                        value["ligne_ecrit"] += 1
                                        value["Cursor"] = -len(value["input"][value["ligne_ecrit"]])
                                    else:
                                        value["Cursor"] = 0 
                            
                            if event.key == pygame.K_SPACE:
                                value["input"][value["ligne_ecrit"]] = add_to_texte(value["input"][value["ligne_ecrit"]],cursor," ")
                            elif event.key == pygame.K_BACKSPACE:
                                value["input"][value["ligne_ecrit"]] = value["input"][value["ligne_ecrit"]][:len(value["input"][value["ligne_ecrit"]]) + cursor][:-1] + value["input"][value["ligne_ecrit"]][len(value["input"][value["ligne_ecrit"]]) + cursor:]
                            elif event.key == pygame.K_RETURN:
                                value["input"].insert(value["ligne_ecrit"] + 1,"")
                                value["Cursor"] = 0
                                value["ligne_ecrit"] += 1
                            else:
                                if event.unicode.isprintable() and event.unicode != "":
                                    value["input"][value["ligne_ecrit"]] = add_to_texte(input,cursor,event.unicode)
        except:
            pass
        if rect_valider.collidepoint(mouse):
            pygame.draw.rect(screen,(0,0,0),rect_valider,0,20)
        pygame.draw.rect(screen,palette_couleur.Bleu,rect_valider,3,20)
        
        
        draw_text(text_envoyer,font_paragraphe,blanc,rect_valider.x +rect_valider.w/2 - taille_envoyez[0]/2,rect_valider.y +rect_valider.h/2 - taille_envoyez[1]/2,size = 30, importer=True)
        for value in dict_input.values():
            rect = value["rect"]
            pygame.draw.rect(screen,background_input,rect,0,20)
            pygame.draw.rect(screen,palette_couleur.Bleu_clair,rect,5,20)
            
            value["surf"].fill((0,0,0,0)) #effacer l'ancienne ecriture pour pas réécrire au dessus systématiquement
            ligne = 0
            for text in value["input"]:
                draw_text(text,font_paragraphe,(0,0,0),10,10 +(20*ligne),contener = value["surf"],importer = True)
                ligne+=1
            
            if value["active"]:
                input = value["input"][value["ligne_ecrit"]]
                len_texte = len(input)
                if value["Default"] != "Contenu":
                    longueur_texte = font(font_paragraphe,20,True).size(input[:len_texte + value["Cursor"]])[0]
                else:
                    longueur_texte = font(font_paragraphe,20,True).size(input[:len_texte + value["Cursor"]])[0]
                value["surf"].blit(barre_input,(10 + value["pos_x"] + longueur_texte,10 + 20 * (value["ligne_ecrit"]) + value["pos_y"]))
            value["surf_exacte"].fill((0,0,0,0)) #effacer l'ancienne ecriture pour pas réécrire au dessus systématiquement
            value["surf_exacte"].blit(value["surf"],(value["pos_x"],value["pos_y"]))
            screen.blit(value["surf_exacte"],(rect.x,rect.y))
            
        dernier_ecran = screen.copy()
        pygame.display.update(all_rect)
        if go_back:
            break
        
    """if send.collidepoint(mouse):
        is_valid = look_valid()
        if mouse_click[0] and is_valid:
            #center_screen("Chargement...", comic_sans_ms, get_dimension("Chargement...", csm, 20), 0, False)
            pygame.display.flip()
            msg = EmailMessage()
            msg["From"] = "sylvio0801@gmail.com"
            dict_active['active_adresse']['input'] = "" if dict_active['active_adresse']['input'] == "votre Email (non obligatoire)" else dict_active['active_adresse']['input']  
            msg.set_content(f" message de {dict_active['active_name']['input']} - {dict_active['active_adresse']['input']}\n {dict_active['active_desc']['input']}")
            msg["Subject"] = dict_active["active_object"]["input"]
            msg["To"] = "sylvio0801@gmail.com"
            context=ssl.create_default_context()
            with smtplib.SMTP('smtp.gmail.com', port=587) as smtp:
                smtp.starttls(context=context)
                #Clé smtp
                #smtp.login(msg["To"] ,env.get("MDP_EMAIL"))
                smtp.send_message(msg)
                finish = True
        if mouse_click[0] and not is_valid:
            #center_screen("Champs invalide", comic_sans_ms, get_dimension("Champs invalide", csm, 20), 0, False)
            pygame.display.flip()
            pygame.time.delay(1000)                        
    pygame.display.flip()"""
                
def page_info(id_ = 0,text = "",nom_projet = "",auteur = "",date : datetime.datetime = None, id_tuto : int = None,image_photo_profil : pygame.Surface= None, is_document = None,doc_tuto = None):
    """Fonction permettant d'image_userr un texte au sujet de Sylver_Service, cette fonction sert aussi a image_userr un tuto

    Args:
        id_ (int): Id permettant d'identifier dans quel but est utiliser la fonctio . Defaults to 0.
        text (str, optional): texte du tuto a image_userr dans la fonction. Defaults to "".
        nom_projet (str, optional): Le nom du tuto a image_userr. Defaults to "".
        auteur (str, optional): Le nom de l'auteur du tuto. Defaults to "".
        date (datetime.datetime, optional): La date de transmission du tuto. Defaults to None.
        id_tuto (int, optional): Id du tuto selectionner. Defaults to None.
    """
    global continuer
    global fond_nav
    go_back = False
    width = w_origine - 50
    height = h_origine - 200
    surface_ecriture = pygame.Surface((width, height), pygame.SRCALPHA)
    pos_surface_ecriture = (25,150)
    surface_glissant_ecriture = pygame.Surface((width,5000), pygame.SRCALPHA)
    rect_surface_ecriture = surface_ecriture.get_rect()
    rect_surface_ecriture.x = pos_surface_ecriture[0]
    rect_surface_ecriture.y = pos_surface_ecriture[1]
    text_title = "A quoi sert Sylver_Service ?"
    font_paragraphe = apple_titre
    rect_a_ne_pas_depasser = rect_screen.copy()
    rect_a_ne_pas_depasser.w -= 5 + image_retour.get_width()
    affiche_corbeille = False
    if connect:
        if user.pseudo == auteur:
            affiche_corbeille = True
    if id_ > 1:
        date = date.strftime("%d/%m/%Y")
        date_save = date
        date = f"posté le : {date}"
        date_actuelle = datetime.datetime.now()
        date_actuelle = date_actuelle.strftime("%d/%m/%Y")
        if date_actuelle == date_save:
            date = "posté aujourd'hui"   
        rect_a_ne_pas_depasser.w -= font(font_paragraphe,20,True).size(date)[0] + 100     
        text_title = f"{nom_projet.upper()} | par  {auteur}"
        
        text_info = text
    if id_ == 0:
        with open("./Ressource/fichier_info.txt", "r+",encoding="utf-8") as fichier:
            text_info = fichier.read().replace("\n", " ")
    size_title = verification_size(rect_a_ne_pas_depasser,chivo_titre,40,text_title,True)
    size_max = width
    i = 0
    font_40 = pygame.font.Font(font_paragraphe, 40)
    font_20 = pygame.font.Font(font_paragraphe, 20)
    taille_ecriture = 30
    text_info,line,heigth_text = make_line_n(text = text_info, font = font(font_paragraphe,taille_ecriture,True), size_max= size_max)
    depassement_texte = rect_surface_ecriture.bottom - (heigth_text + 20)
    #mini système pour permettre l'adaptation au écran trop petit
    #all_text = decoupe_text(coupage,line,text_info)
    width_surface_popup = 350 
    
    surface_popup_fond = pygame.Surface((width_surface_popup,220), pygame.SRCALPHA) 
    rect_popup = pygame.Rect(w_origine - width_surface_popup,40,width_surface_popup,surface_popup_fond.get_height())
    surface_popup = pygame.Surface((surface_popup_fond.get_width() - 40, surface_popup_fond.get_height() - 40),pygame.SRCALPHA)
    case_dans_popup = pygame.Surface((surface_popup.get_width() - 20,surface_popup.get_height()/2 - 20), pygame.SRCALPHA)
    triple_bar_option = pygame.image.load(os.path.join("Image","3_barre_proto.png"))
    triple_bar_option = pygame.transform.smoothscale(triple_bar_option,(45,45))
    rect_triple_bar = pygame.Rect(w_origine - surface_popup_fond.get_width()/2 - triple_bar_option.get_width()/2
                                ,45,triple_bar_option.get_width(),triple_bar_option.get_height())
    icone_signalement = pygame.image.load(os.path.join("Image","warning_icone.png"))
    icone_signalement = pygame.transform.smoothscale(icone_signalement,(50, 50))
    rect_icone_signalement = icone_signalement.get_rect() #rect relatif a surface_popup_fond
    rect_icone_signalement.x = 5
    rect_icone_signalement.y = case_dans_popup.get_height()/2 - rect_icone_signalement.h/2

    #creation du rect_de_collision pour l'icone signalement
    icone_tuto_utilisateur = pygame.image.load(os.path.join("Image","loupe_icone.png"))
    icone_tuto_utilisateur = pygame.transform.smoothscale(icone_tuto_utilisateur,taille_icone)
    rect_icone_tuto_utilisateur = icone_tuto_utilisateur.get_rect() #rect relatif a surface_popup_fond
    rect_icone_tuto_utilisateur.x = 5
    rect_icone_tuto_utilisateur.y = case_dans_popup.get_height()/2 - rect_icone_tuto_utilisateur.h/2

    
    texte_pour_signalement = "Signaler ce tuto"
    taille_signal,taille_voir_tuto = 30,30
    font_signal = font(font_paragraphe,taille_signal,True)
    font_voir_tuto = font(font_paragraphe,taille_voir_tuto,True)
    texte_pour_voir_tout_les_tuto = "Voir les tutos de cette utilisateur"
    rect_a_pas_depasser = pygame.Rect(0,0,surface_popup_fond.get_width() - 50 - 25,0 )
    max_size = case_dans_popup.get_width() - rect_icone_signalement.x - rect_icone_signalement.w - 5 - 10
    #coupage pour le texte du signalement
    coupage_signal,line_signal,y_signal = make_line(texte_pour_signalement,font_signal,max_size)
    while y_signal > case_dans_popup.get_height():
        taille_signal -= 2
        coupage_signal,line_signal,y_signal = make_line(texte_pour_signalement,font(font_paragraphe,taille_signal,True),max_size)
    all_texte_signal = decoupe_text(coupage_signal,line_signal,texte_pour_signalement)
    #coupage pour le texte de voir tuto
    coupage_voir_tuto,line_voir_tuto,y_voir_tuto = make_line(texte_pour_voir_tout_les_tuto,font_voir_tuto,max_size)
    while y_voir_tuto > case_dans_popup.get_height():
        taille_voir_tuto -= 2
        coupage_voir_tuto,line_voir_tuto,y_voir_tuto = make_line(texte_pour_voir_tout_les_tuto,font(font_paragraphe,taille_voir_tuto,True),max_size)
    all_text_voir_tuto = decoupe_text(coupage_voir_tuto,line_voir_tuto,texte_pour_voir_tout_les_tuto)

    position_case_signal_rel = (10,10)
    rect_case_signal_rel = pygame.Rect(*position_case_signal_rel, *case_dans_popup.get_size()) #relatif a case_dans_popup
    rect_case_signal = rect_case_signal_rel.copy()
    rect_case_signal.x += rect_popup.x + 20
    rect_case_signal.y += rect_popup.y + 20
    
    position_case_voir_tuto_rel = (10,surface_popup.get_height() - case_dans_popup.get_height()-10)
    rect_case_voir_tuto = pygame.Rect(rect_popup.x + 20 + position_case_voir_tuto_rel[0],
                                    rect_popup.y + 20 + position_case_voir_tuto_rel[1],
                                    *case_dans_popup.get_size())

    position_popup = -h_origine/4
    position_de_fin = 40
    popup_option_activer = False
    retirez_option = False
    animation_ouverture.stop_anime()
    if id_>1:
        position_photo_pp = w_origine - image_photo_profil.get_width() - 10, fond_nav.get_height() - image_photo_profil.get_height() - 10
        rect_photo_pp = pygame.Rect(*position_photo_pp,*image_photo_profil.get_size())
    pos_y_ecriture = 0
    surf_contact = pygame.Surface((200,60),pygame.SRCALPHA)
    rect_contact = surf_contact.get_rect()
    rect_contact.right = w_origine
    rect_contact.top = 0
    rect_corbeille = pygame.Rect(10 + image_retour.get_width() + 5 ,fond_nav.get_height(),*taille_icone)
    rect_corbeille.bottom = fond_nav.get_height() - 5
    icone_corbeille = pygame.image.load(os.path.join("Image","Icone_corbeille.png"))
    icone_corbeille = pygame.transform.smoothscale(icone_corbeille,taille_icone)
    icone_editer = pygame.image.load(os.path.join("Image","Icone_modification.png"))
    icone_editer = pygame.transform.smoothscale(icone_editer,taille_icone)
    rect_editer = rect_corbeille.copy()
    rect_editer.x += rect_corbeille.w + 5
    while continuer:
        Clock.tick(120)
        mouse = pygame.mouse.get_pos()
        screen.fill(fond_ecran)
        surface_ecriture.fill((255,255,255,0))     
        surface_glissant_ecriture.fill((255,255,255,0))  
        pygame.draw.rect(screen,palette_couleur.Gris_clair,(10,120,width + 30, height + 60),0,20)
        pygame.draw.rect(surface_ecriture,blanc,(0,0,width,height),0,20)
        
        for event in pygame.event.get():            
            if event.type == pygame.QUIT:
                continuer = False
                break
            if affiche_corbeille:
                if rect_corbeille.collidepoint(mouse):
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        processus_delete_tuto(id_tuto,last_screen)  
                if rect_editer.collidepoint(mouse):
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if not is_document:
                            ecrire_tuto(user,text,nom_projet,id_tuto)
                        else:
                            screen.blit(last_screen,(0,0))
                            nom_tuto = input_popup()
                            if nom_tuto != False:
                                path = User.get_file(1)[0]
                                if path != " ":
                                    if user.categorie != None:
                                        rep = dialog.ask_yes_no_cancel(f"Souhaiter vous mettre a ce tuto la même catégorie que votre compte ? ({user.categorie}) ")
                                    else:
                                        rep = False
                                    if rep is False:
                                        categorie = interface_deroullante_categorie(last_screen)
                                    elif rep is True:
                                        categorie = user.categorie
                                    else:
                                        categorie = None
                                    if categorie != None:
                                        if dialog.ask_yes_no("Doit-on considerer votre tuto comme une demande de tuto ?",last_screen):
                                            is_annonce = 1
                                        else:
                                            is_annonce = 0
                                        try:
                                            animation_mise_en_ligne.start_anime(last_screen)
                                            user.modifier_tuto(path,"",nom_tuto,categorie,is_annonce,id_tuto)
                                            animation_mise_en_ligne.stop_anime()
                                        except:
                                            dialog.message("Une erreur est survenue ! ", last_screen,title = "Erreur")
                                        else:
                                            dialog.message("Votre tuto a bien été modifié !",last_screen)
                                    else:
                                        dialog.message("La modification n'a pas été effectué",last_screen)
            if rect_goback.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                go_back = True
            
            if rect_surface_ecriture.collidepoint(mouse) and depassement_texte < 0:
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 4 ) or (event.type == pygame.KEYDOWN and event.key == pygame.K_UP):
                    pos_y_ecriture += 30
                elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 5 ) or (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN):
                    pos_y_ecriture -= 30
                if abs(pos_y_ecriture) > abs(depassement_texte) + 20:
                    pos_y_ecriture = depassement_texte - 20
                if pos_y_ecriture > 0:
                    pos_y_ecriture = 0
                    
            if id_ > 1:               
                if rect_case_signal.collidepoint(mouse) and position_popup == position_de_fin and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and popup_option_activer:
                    if connect:
                        try:
                            can_signal = user.can_signal(id_tuto)
                            if can_signal:
                                text_signalement, titre = ecrire_tuto(None)
                                signalement_final = titre + " | " + text_signalement
                                user.signalement(id_tuto, auteur, signalement_final)
                                animation_mise_en_ligne.stop_anime()
                            else:
                                dialog.message("Vous avez déjà signalé ce tuto ! ",last_screen)
                        except noConnection:
                            dialog.message("Une erreur de connexion a eu lieu !",last_screen)
                        except Exception as e:
                            
                            pass
                        else:
                            if can_signal:
                                dialog.message("Votre signalement a bien été envoyée !",last_screen)
                    else:
                        dialog.message("Pour signalez un tuto vous devez être connecté !",last_screen)
                if not rect_popup.collidepoint(mouse):
                    if popup_option_activer and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        retirez_option = True
                        popup_option_activer = False
                if rect_triple_bar.collidepoint(mouse) and popup_option_activer == False and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    popup_option_activer =True
                
                if popup_option_activer  and rect_case_voir_tuto.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if auteur != "":
                        menu(1,auteur.split(",")[0])
                    else:
                        dialog.message("L'auteur n'existe pas !",last_screen)
                        
                
                if rect_photo_pp.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if connect and auteur.split(",")[0] == user.pseudo:
                        affiche_photo_profil(last_screen)
                    else:
                        affiche_photo_profil(last_screen,True,auteur.split(",")[0])
            else:
                if rect_contact.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    rep = dialog.ask_yes_no_cancel("Voulez vous envoyez un message depuis l'application ?", last_screen,title="Contact")
                    if rep is True:
                        pass
                    elif rep is False:
                        webbrowser.open(f"mailto:SylverService@outlook.fr") 
                        pygame.display.iconify()
            
        
    
        draw_text(text_info, color = (0,0,0),x = 10,y = 20,
                    size = taille_ecriture, contener = surface_glissant_ecriture, font = font_paragraphe, importer = True)
        #pygame.draw.rect(surface_ecriture, (255,0,0),(0,height/2,width,2))
        fond_nav.fill(palette_couleur.Noir)         
        screen.blit(fond_nav,(0,0))  
        screen.blit(image_retour,rect_goback)
        title(text_title, size = size_title)
        if id_ > 1:
            pygame.draw.rect(surface_popup_fond,fond_ecran,surface_popup_fond.get_rect(),0,20)
            pygame.draw.rect(surface_popup_fond,(0,0,0),surface_popup_fond.get_rect(),1,20)
            pygame.draw.rect(surface_popup,blanc,surface_popup.get_rect(),0,20)
            
            taille_case = surface_popup_fond.get_height() - rect_icone_signalement.y - 10
            #image_userr le texte de signalement dans les options
            #case_dans_popup.fill(palette_couleur.Bleu)
            pygame.draw.rect(case_dans_popup,palette_couleur.Bleu,case_dans_popup.get_rect(),0,20)
            e = 0
            for i in all_texte_signal:
                draw_text(i,font_paragraphe,blanc,
                        x  = rect_icone_signalement.x + rect_icone_signalement.w + 5, y = case_dans_popup.get_height()/2 - y_signal/2 + font(font_paragraphe,taille_signal,True).size(i)[1] * e,
                        size = taille_signal, importer=True,contener=case_dans_popup)
                e+=1
            case_dans_popup.blit(icone_signalement,rect_icone_signalement)
            surface_popup.blit(case_dans_popup,position_case_signal_rel)
            #case_dans_popup.fill(palette_couleur.Bleu)
            pygame.draw.rect(case_dans_popup,palette_couleur.Gris_clair,case_dans_popup.get_rect(),0,20)
            for i in range(len(all_text_voir_tuto)):
                draw_text(all_text_voir_tuto[i],font_paragraphe,blanc,
                        x  = rect_icone_tuto_utilisateur.x + rect_icone_signalement.w + 5,
                        y = case_dans_popup.get_height()/2 - y_voir_tuto/2 + font(font_paragraphe,taille_voir_tuto,True).size(all_text_voir_tuto[i])[1] * i,
                        size = taille_voir_tuto, importer=True,contener=case_dans_popup) 
            case_dans_popup.blit(icone_tuto_utilisateur,rect_icone_tuto_utilisateur)
            surface_popup.blit(case_dans_popup,position_case_voir_tuto_rel)
            
            
            surface_popup_fond.blit(surface_popup,(20,20))
            draw_text(date, x = w_origine - font_20.size(str(date))[0] - 10,y = 10, font = font_paragraphe, color = (255,255,255),importer = True)
            
        if go_back:
            break
        surface_ecriture.blit(surface_glissant_ecriture,(0,pos_y_ecriture))
        screen.blit(surface_ecriture, (25,150))
        if id_ >1:
            #image_userr pp_user
            screen.blit(triple_bar_option,rect_triple_bar)
            screen.blit(image_photo_profil,position_photo_pp)
            if popup_option_activer:
                position_popup += 80
                if position_popup >= position_de_fin:
                    position_popup = position_de_fin            
                screen.blit(surface_popup_fond,(rect_popup.x,position_popup))
            elif retirez_option:
                position_popup -= 80
                if position_popup <= -surface_popup_fond.get_height():
                    position_popup = -surface_popup_fond.get_height()            
                screen.blit(surface_popup_fond,(rect_popup.x,position_popup))
        else:
            surf_contact.fill((0,0,0,0))
            pygame.draw.rect(surf_contact,palette_couleur.Bleu_clair,surf_contact.get_rect(),1,20)
            draw_text(contener = surf_contact,text = "CONTACT", font = font_paragraphe,size = 40,color = blanc,
                    x = surf_contact.get_width()/2 - font(font_paragraphe,40,True).size("CONTACT")[0]/2,
                    y = surf_contact.get_height()/2 - font(font_paragraphe,40,True).size("CONTACT")[1]/2,importer=True)
            screen.blit(surf_contact,rect_contact)
        screen.blit(surface_status_co,pos_surface_status_co)
        if affiche_corbeille:
            screen.blit(icone_corbeille,rect_corbeille)
            screen.blit(icone_editer,rect_editer)
        last_screen = screen.copy()
        pygame.display.flip()
    
def processus_delete_tuto(id_,l):
    try:
        recup_reponse_user = user.delete_tuto(id_)
    except:
        dialog.message("Votre tuto n'a pas pû être supprimé ! ",l,title="Erreur")
    else:
        if recup_reponse_user:
            dialog.message("Votre tuto a bien été supprimé :)",l) 
        else:
            pass 
                
def menu(id_ : int = 0,auteur_rechercher : str = None):
    """Fonction permettant de rechercher des tutos | elle sert également a image_userr tout les tutos d'un utilisateur

    Args:
        id_ (int, optional): _description_. Variable permettant de changer l'utilisation de la fonction to 0.
        auteur_rechercher (str, optional): Auteur recherché si la fonction sert a image_userr les tutos d'un utilisateur. Defaults to None.
    """
    #ecrire_tuto(None)
    global display
    global processing
    #savoir quand la recherche est en cours
    processing = False             
    display = False
    global zone_page
    longueur_recherche = w_origine -400
    surface_rechercher = pygame.Surface((longueur_recherche, 70), pygame.SRCALPHA)
    rect_surf_rechercher = pygame.Rect(100,fond_nav.get_height() + 50,surface_rechercher.get_width(),surface_rechercher.get_height())
    zone_page = 0
    long_case = w_origine/2 - 20
    depart_tuto = rect_surf_rechercher.bottom + 60
    separation_tuto = 10
    max_par_page = 12
    taille_reference = h_origine - depart_tuto  - 100
    haut_case = 60
    max_par_page = int(taille_reference/(haut_case+separation_tuto)) * 2 #pour ne pas toucher la flèche
    if max_par_page % 2 == 1:
        max_par_page -= 1
    liste_indicey = [depart_tuto+(haut_case+separation_tuto)*i  for i in range(int(max_par_page/2))] *2 #on fait *2 car il est prévu 2 colonne
    liste_indicex = [w_origine/2 - long_case -5] * int(max_par_page/2) + [w_origine/2 + 5] * int(max_par_page/2) #on fait *max_par_page/2 car il y a max_par_page/2  element par colonne
    surface_fleche = pygame.Surface(taille_icone)
    global page
    page = []
    #font = pygame.font.SysFont(chivo_titre, 30)
    y_all = h_origine - 100
    global can_add
    can_add = False
    global flop_de_recherche
    flop_de_recherche = False
    
    def display_result(num):
        """Fonction permettant d'image_userr le résultat d'une recherche précise

        Args:
            num (int): nombres de résultats obtenu
        """
        global access,zone_page,all_case_data,dict_rect_fleche,add_fleche,can_add,have_supprime,flop_de_recherche,categorie_rechercher
        #pygame.event.clear()        
        text = f"{num} résultat.s pour cette recherche !" if not flop_de_recherche else "Une erreur est survenue ! la recherche n'a pas aboutie"
        text = "Faites une recherche :)" if have_supprime else text
        if dict_recherche["nom_categorie"] != None and num == 0 and (liste_rech[indice_type] == "Catégorie" or dict_recherche["nom_categorie"] == user.categorie):
            text = f'La categorie {categorie_rechercher} est vide :('
        elif dict_recherche["nom_categorie"] != None and num != 0 and (liste_rech[indice_type] == "Catégorie" or dict_recherche["nom_categorie"] == user.categorie):
            text = f'{num} résultat.s dans la catégorie {categorie_rechercher}'
        if id_ == 2:
            text = f"Il y a {num} annonce.s disponible.s" if not flop_de_recherche else "Une erreur est survenue ! la recherche n'a pas aboutie"
        draw_text(text,color = (255,255,255),
                x = w_origine/2 - font(chivo_titre,30,False).size(text)[0]/2,y = rect_surf_rechercher.y + rect_surf_rechercher.h + 10,
                font = chivo_titre,size = 30
                ,ombre = True)        
        if access:
            try:                
                global page
                page = []
                count = 0
                sous_list = []
                for i in range(len(detail)):
                    sous_list.append(detail[i])
                    count+=1
                    if count >= max_par_page:
                        page.append(sous_list)
                        sous_list = []
                        count = 0
                if len(sous_list) > 0:
                    page.append(sous_list)
                elif len(page) == 0:
                    page.append([])
                decount_page = f"{zone_page+1}/{len(page)}"
                longueur_decompte = font(font_paragraphe,int(taille_icone[0]),True).size(decount_page)[0]
                x1 = w_origine/2 + longueur_decompte/2 + 10
                x2 = w_origine/2  -longueur_decompte/2 - surface_fleche.get_width() - 10
                use_list = page[zone_page]
                rect_1 = pygame.Rect(x1,y_all,surface_fleche.get_width(),surface_fleche.get_height())
                rect_2 = pygame.Rect(x2,y_all,surface_fleche.get_width(),surface_fleche.get_height())
                dict_rect_fleche = [rect_1,rect_2]
                flèche_droite = pygame.image.load(os.path.join("Image", "flèches_droites.png"))
                flèche_droite = pygame.transform.smoothscale(flèche_droite,(surface_fleche.get_width(),surface_fleche.get_height()))
                flèche_gauche = pygame.image.load(os.path.join("Image", "flèches_gauches.png"))
                flèche_gauche = pygame.transform.smoothscale(flèche_gauche,(surface_fleche.get_width(),surface_fleche.get_height()))
                add_fleche = [1,-1]
                screen.blit(flèche_droite,(x1,y_all))
                screen.blit(flèche_gauche,(x2,y_all))
                draw_text(decount_page,color = blanc,
                        x = w_origine/2 - longueur_decompte/2,
                        y = y_all,
                        font = font_paragraphe, importer = True,size = int(taille_icone[0]))
                for index,tuto in enumerate(use_list):
                    nom_projet = tuto.nom
                    auteur = User.get_only_pseudo(tuto.auteur)
                    id_tuto = tuto.id_
                    doc  = tuto.doc
                    date = tuto.date
                    file = tuto.extension
                    date = date.strftime("%d/%m/%Y")
                    date_actuelle = datetime.datetime.now()
                    date_actuelle = date_actuelle.strftime("%d/%m/%Y")
                    if date_actuelle == date:
                        text_date = "posté aujourd'hui"
                    else:
                        text_date = f"posté le {date}"
                    text = tuto.contenu
                    
                    if len(use_list) <=max_par_page/2:
                        #dans ce cas les tuto se positionne au milieu de la page
                        rect_case = pygame.Rect(w_origine/2 - long_case/2, liste_indicey[index],
                                                long_case,
                                                haut_case)
                    else:
                        rect_case = pygame.Rect(liste_indicex[index],
                                            liste_indicey[index],
                                            long_case,
                                            haut_case)
                    surface = pygame.Surface((rect_case.w,rect_case.h),pygame.SRCALPHA)
                    surface.fill((0,0,0,0))
                    pygame.draw.rect(surface,palette_couleur.Bleu,(0,0,surface.get_width(),surface.get_height()),0,20)
                    color_auteur = palette_couleur.Noir_clair if Gerer_requete.est_bytes(doc) else blanc
                    
                    ecrit_auteur = auteur if len(auteur) <= 15 else auteur[:15]
                    rect_no_depasse = pygame.Rect(0,0,long_case-10-font(font_paragraphe,30,True).size(text_date)[0] - 20 - 20,0)
                    size_ = verification_size(rect_no_depasse,font_paragraphe,30,f"{nom_projet} par {ecrit_auteur}",True)
                    draw_text(color = color_auteur,contener = surface,
                            text = f"{nom_projet} - par {ecrit_auteur}", x = 10,
                            y = 0, font = font_paragraphe,
                            size = size_, importer = True)
                    draw_text(color = blanc,contener = surface,
                            text = text_date, x = rect_case.w - font_30.size(text_date)[0] - 20,
                            y = 5, importer = True,
                            size = 30, font = font_paragraphe)
                    if len(use_list) > max_par_page/2:
                        screen.blit(surface,(liste_indicex[index],liste_indicey[index]))
                    else:
                        screen.blit(surface,(w_origine/2 - long_case/2, liste_indicey[index]))                
                    pygame.draw.rect(screen,(255,255,255),rect_case,3,20)
                    case_data = {"zone" : zone_page,"nom_projet" : nom_projet, "contenu" : text, "auteur" : auteur, "date" : date,"rect" : rect_case,"doc" : doc,"id" : id_tuto,"extension" : file}
                    if can_add:
                        pygame.display.flip()
                        all_case_data.append(case_data)
                can_add = False
            except Exception as e:
                access = False
                flop_de_recherche = True
                dialog.message("Une erreur est survenue ! ", last_screen,title="Erreur")
                
    def start_tuto(data):
        global photo_deja_charger
        """Fonction permettant de lancer le tuto

        Args:
            data (dict): donnée au sujet du tuto
        """
        text = data["contenu"]
        auteur = data["auteur"]
        date = data["date"]
        id_tuto = data["id"]
        date = datetime.datetime.strptime(date,"%d/%m/%Y")
        nom_projet = data["nom_projet"]
        doc = data["doc"]
        file = data["extension"]
        is_document = False
        if connect:
            if user.pseudo == auteur.split(",")[0]:
                #si c'est un tuto de l'utilisateur connectez, on va simplement prendre sa pp qu'on avait déjà charger
                if Gerer_requete.est_bytes(doc):
                    dir = Gerer_requete.open_dir(title = "Lieu du téléchargement")
                    is_document = True
                    if dir != "":
                        Gerer_requete.demarrer_fichier(dir = dir,doc = doc, ext = file,auteur = auteur, nom_tuto=nom_projet)
                    else:
                        animation_ouverture.stop_anime()
                        return
                    text = "Le fichier a été ouvert profitez en :)\nMaintenant vous pouvez donc signalez un tuto visuel et voir tout les autres tutos de l'utilisateur, comme si c'était un tuto texte :) c'est cool non ?"
                page_info(2,text,nom_projet,auteur,date,id_tuto,pygame.transform.smoothscale(image_pp_user,taille_icone),is_document,doc)
                return  
        
        if not auteur.split(",")[0] in photo_deja_charger:
            #recuperation de la pp de l'user qui a fait le tuto
            try:
                bin_pp,rect_pp = Gerer_requete.look_for_user_pp(auteur.split(",")[0])        
                if rect_pp != None:   
                    rect_pp = [int(i) for i in rect_pp.split(",")]
                    rect_pp = pygame.Rect(rect_pp)
                photo_deja_charger[auteur.split(",")[0]] = (bin_pp,rect_pp)
            except:
                return
        else:
            bin_pp, rect_pp = photo_deja_charger[auteur.split(",")[0]]
            
        img_ = pygame.image.load(io.BytesIO(bin_pp)).convert_alpha()
        old_width, old_height = img_.get_size()
        # Définir la nouvelle largeur (ou hauteur)
        new_width = 500
        # Calculer la nouvelle hauteur (ou largeur) pour conserver le rapport d'aspect (produit en croix)
        new_height = int(old_height * new_width / old_width)
        # Redimensionner l'image
        img_ = pygame.transform.smoothscale(img_, (new_width,new_height))
        if rect_pp == None:
            rect_pp = pygame.Rect(0,0,*img_.get_size())
        image_pp = resizeImage.rendre_transparent(img_,rect_pp,0)
        image_pp = pygame.transform.smoothscale(image_pp,taille_icone)
        if Gerer_requete.est_bytes(doc):
            is_document = True
            dir = Gerer_requete.open_dir(title = "Lieu du téléchargement")
            if dir != "":
                Gerer_requete.demarrer_fichier(dir = dir,doc = doc, ext = file,auteur = auteur, nom_tuto=nom_projet)
            else:
                animation_ouverture.stop_anime()
                return
            text = "Le fichier a été ouvert profitez en :)\nMaintenant vous pouvez donc signalez un tuto visuel et voir tout les autres tutos de l'utilisateur, comme si c'était un tuto texte :) c'est cool non ?"
        page_info(2,text,nom_projet,auteur,date,id_tuto,image_pp,is_document,doc)
                
    def research(data, id_ = 0):
        """Fonction effectuant la recherche

        Args:
            data (dict): donnée au sujet du tuto selectionner
        """
        global all_case_data,enter_pressed
        all_case_data = []
        global processing
        processing = True
        global have_supprime
        have_supprime = False   
        global detail,can_add,access,display,num_resultat,flop_de_recherche,enter_pressed,categorie_rechercher
        can_add = True
        access = False
        global zone_page
        zone_page = 0
        try:      
            flop_de_recherche = False   
            if id_ == 0:
                print("recherche :",data["nom_categorie"])
                detail,categorie_rechercher = Gerer_requete.rechercher_data(nom_auteur = data["nom_auteur"], nom_tuto = data["nom_projet"], nom_categorie = data["nom_categorie"])
            else:
                detail = Gerer_requete.rechercher_annonce()
            processing = False
            num_resultat = len(detail)
            access = True
            display = True
            enter_pressed = False
        except noConnection as err:
            print(err)
            enter_pressed = False
            processing = False
            Gerer_requete.error_occured()
            
        except noCategorie as e:
            processing = False
            enter_pressed= False
            
        except Exception as e:
            print(e)
            enter_pressed = False
            flop_de_recherche = True
            processing = False
            access = False
            display = True
            Gerer_requete.error_occured()
        
    
    global continuer
    global finish
    global have_supprime
    have_supprime = False
    finish = False
    go_back = False
    font_paragraphe = apple_titre
    font_40 = pygame.font.Font(font_paragraphe, 40)
    font_30 = pygame.font.Font(font_paragraphe,30)
    font_20 = pygame.font.Font(font_paragraphe,20)
    

    #represente le btn qui efface la recherche
    rect_btn = pygame.Rect(0,0,50,40)
    rect_rechearch = pygame.Rect(100,fond_nav.get_height() + 50,longueur_recherche,70)
    rect_btn.x = rect_rechearch.x + rect_rechearch.w - 100
    rect_btn.y = rect_rechearch.y + rect_rechearch.h/2 - rect_btn.h/2
    input_research = input_apple
    barre_input = pygame.Surface((3,30))
    barre_input.fill((0,0,0))
    phrase_base ="Appuyer pour Rechercher"
    input_host = phrase_base
    active = False
    take_time = False
    max_letter = 50
    global access
    access = False
    global num_resultat
    num_resultat = None
    global all_case_data
    all_case_data = []
    text_on = ""
    global dict_rect_fleche
    dict_rect_fleche = {}
    recherche_type = "nom_auteur"
    liste_rech = ["Auteur","Nom", "Catégorie","nom_auteur","nom_projet","nom_categorie"]
    
    rect_type_recherche = pygame.Rect(100 + longueur_recherche + 100, fond_nav.get_height() + 55, 100,60)
    surface_type_recherche = pygame.Surface((100,60), pygame.SRCALPHA)
    nom_categorie = liste_rech[:3]
    size_nom_categorie = [] #toute les taille d'écriture pour les noms de catégorie
    for nom in nom_categorie:
        size_nom = verification_size(pygame.Rect(0,0,surface_type_recherche.get_width() - 10,0),font_paragraphe,
                                    30,nom,True)
        size_nom_categorie.append(size_nom)
    indice_type = 0
    text_rechercher = "Recherche par"
    rect_aide = pygame.Rect(w_origine - taille_icone[0]- 5, 5, *taille_icone)
    image_aide = pygame.image.load(os.path.join("Image","icone_interrogation.png"))
    image_aide = pygame.transform.smoothscale(image_aide,(rect_aide.w,rect_aide.h))
    #boucle principale
    image_effacer_recherche = pygame.image.load(os.path.join("Image","icone_annule_recherche.png"))
    image_effacer_recherche = pygame.transform.smoothscale(image_effacer_recherche,(rect_btn.w,rect_btn.h))
    rect_a_ne_pas_depasser = rect_screen.copy()
    rect_a_ne_pas_depasser.w -= (rect_aide.w + 5)
    rect_a_ne_pas_depasser.w -= (rect_goback.w+5)
    text_title = "Bienvenue Dans l'espace recherche !" if id_ == 0 else f"Voici les tutos de l'utilisateur {auteur_rechercher} !"
    text_title = "Voici les annonces les plus récentes de l'applications" if id_ == 2 else text_title
    size_du_titre = verification_size(rect_a_ne_pas_depasser,chivo_titre,size_for_title,text_title,True)
    global enter_pressed
    enter_pressed = False
    not_enter = False #sert juste a bloquer l'acces
    dict_recherche_base = {"nom_projet" : None,"nom_auteur" : None,"nom_categorie" : None}
    dict_recherche = {"nom_projet" : None,"nom_auteur" : None,"nom_categorie" : None}
    #boucle principale
    cursor_position = 0
    while continuer:
        Clock.tick(120)
        if id_ == 1 and not not_enter:
            dict_recherche = {"nom_auteur": auteur_rechercher,"nom_projet" : None,"nom_categorie" : None}
            th = threading.Thread(target = research, args=(dict_recherche,),daemon=True)
            if not th.is_alive():
                debut = time.time()
                th.start()
                not_enter = True
        if id_ == 2 and not not_enter:
            dict_recherche = {"nom_auteur": None,"nom_projet" : "*","nom_categorie" : None}
            th = threading.Thread(target = research, args=(dict_recherche,1),daemon=True)
            if not th.is_alive():
                debut = time.time()
                th.start()
                not_enter = True
        if id_ == 0 and connect and user.categorie != None and not not_enter:
            #faire la recherche par défaut de l'utilisateur
            dict_recherche = {"nom_auteur": None,"nom_projet" : None,"nom_categorie" : user.categorie}
            th = threading.Thread(target = research, args=(dict_recherche,),daemon=True)
            input_host = user.categorie
            if not th.is_alive():
                debut = time.time()
                th.start()
                not_enter = True        
        mouse = pygame.mouse.get_pos()
        screen.fill(fond_ecran)            
        surface_rechercher.fill((0,0,0,0))
        surface_type_recherche.fill((0,0,0,0))
        #boucle evenementielle
        if processing:
            actu = time.time()
            if actu - debut >= 2:
                ajout_text = "Pardon pour l'attente.."
            else:
                ajout_text = ""
            animation_chargement.animate(fond_ecran,ajout_decriture=ajout_text)
        for event in pygame.event.get():
            if active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        cursor_position -= 1
                        if abs(cursor_position) >= len(input_host):
                            cursor_position = -len(input_host)
                            
                    if event.key == pygame.K_RIGHT:
                        cursor_position += 1
                        if cursor_position >= 0 :
                            cursor_position = 0
                    if event.key == pygame.K_SPACE:
                        input_host = input_host[:len(input_host) + cursor_position] + " " + input_host[len(input_host) + cursor_position:]
                    elif event.key == pygame.K_BACKSPACE:
                        input_host =  input_host[:len(input_host) + cursor_position][:-1] +  input_host[len(input_host) + cursor_position:]
                    elif event.key == pygame.K_RETURN and not enter_pressed:
                        dict_recherche = dict_recherche_base.copy()
                        all_case_data = {}
                        display = False
                        enter_pressed = True
                        recherche_type = liste_rech[indice_type+3]
                        dict_recherche[recherche_type] = input_host
                    
                        thread_recherche = threading.Thread(target=research, args=(dict_recherche,), daemon=True)                       
                        if not thread_recherche.is_alive():
                            debut = time.time()
                            thread_recherche.start()
                                            
                    elif event.key == pygame.K_ESCAPE:
                        pass
                    elif event.key == pygame.K_TAB:
                        pass                       
                    else:                            
                        if (len(input_host) < max_letter) and (event.unicode.isprintable() and event.unicode != ""):
                            input_host = input_host[:len(input_host) + cursor_position] + event.unicode + input_host[len(input_host) + cursor_position:]
            for index,data_recup in enumerate(all_case_data):
                if data_recup["rect"].collidepoint(mouse) and data_recup["zone"] == zone_page:
                    text_on = data_recup["id"]
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
                        animation_ouverture.start_anime(last_screen)
                        start_tuto(data_recup)    
                        animation_ouverture.stop_anime()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button ==3:
                        if connect:
                            if user.pseudo == data_recup["auteur"]:
                                processus_delete_tuto(text_on,last_screen)       
            for index,values in enumerate(dict_rect_fleche):
                if values.collidepoint(mouse):
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if zone_page + add_fleche[index] >= 0 and zone_page + add_fleche[index] < len(page):
                            zone_page += add_fleche[index]
                            can_add = True
                            all_case_data = []
            if rect_type_recherche.collidepoint(mouse) and id_ == 0:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if indice_type < len(dict_recherche) - 1:
                        indice_type += 1
                    else:
                        indice_type = 0
            if rect_aide.collidepoint(mouse):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if id_ != 2:
                        title_confirm_open = "RECHERCHE"
                        texte_confirm_open ="du Menu"
                    else:
                        title_confirm_open = "ANNONCE"
                        texte_confirm_open = "de la page annonce"
                    reponse = dialog.ask_yes_no(f"Souhaitez vous ouvrir le document d'aide {texte_confirm_open} ?",last_screen)
                    if reponse:
                        animation_ouverture.start_anime(last_screen)
                        try:
                            if id_ != 2 :
                                Gerer_requete.demarrer_fichier(doc = os.path.join("Ressource","SYLVER.docx"),with_path=True,ext = None)
                            else:
                                Gerer_requete.demarrer_fichier(doc = os.path.join("Ressource","Information_page_annonce.docx"),with_path=True,ext = None)     
                        except OSError as e:
                            dialog.message("L'ouverture de ce document à échouer !",last_screen,title="Erreur")
                        except Exception as e:
                            dialog.message("Une erreur est survenue ! ", last_screen,title="Erreur")
                        finally:
                            animation_ouverture.stop_anime()

            if event.type == pygame.QUIT:
                continuer = False
                break
            if rect_goback.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                go_back = True
            if rect_rechearch.collidepoint(mouse) and not rect_btn.collidepoint(mouse) and id_ == 0:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    active = not active
                    if len(input_host) == 0 and not active:
                        input_host = phrase_base
                    if active and input_host == phrase_base:
                        input_host = ""            
            if rect_btn.collidepoint(mouse):
                if id_ == 0 and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and bool(input_host):
                    access = False
                    all_case_data = {}
                    display = True
                    have_supprime = True
                    input_host = ""
                    dict_recherche = dict_recherche_base

        pygame.draw.rect(surface_rechercher,(255,255,255),(0,0,rect_surf_rechercher[2],rect_surf_rechercher[3]),0,20)

        couleur = (255,0,0) if not rect_btn.collidepoint(mouse) else (255,255,255)
        blit_input = input_research.render(input_host,True,(0,0,0))
        center_y = rect_rechearch.h/2 - input_research.size(input_host)[1]/2
        #il est mieux d'utiliser draw_text car ça va plus vite, mais j'ai fait comme ça
        #en tout cas c'est similaire a draw_text
        surface_rechercher.blit(blit_input,(10,center_y))
        
        if active:
            surface_rechercher.blit(barre_input, (10 + input_research.size(input_host[:len(input_host) + cursor_position])[0],2 + input_research.size(input_host[:len(input_host) + cursor_position])[1]/2))

        else:
            time_ = 0
            take_time = False
        
        if id_ == 0:
            screen.blit(surface_rechercher,rect_surf_rechercher)    
            pygame.draw.rect(screen,palette_couleur.Bleu,rect_surf_rechercher,5,20)
            #pygame.draw.rect(screen,couleur,rect_btn)
            screen.blit(image_effacer_recherche,rect_btn)
        fond_nav.fill(palette_couleur.Noir)
        screen.blit(fond_nav,(0,0))
        title(text_title, size = size_du_titre)       
        pygame.draw.rect(surface_type_recherche,palette_couleur.Bleu,(0,0,rect_type_recherche[2],rect_type_recherche[3]),0,20)
        pygame.draw.rect(surface_type_recherche,(255,255,255),(0,0,rect_type_recherche.w,rect_type_recherche.h),2,20)
        taille_actuelle = size_nom_categorie[indice_type]
        draw_text(contener = surface_type_recherche,
                text = liste_rech[indice_type],
                x = rect_type_recherche.w/2 - font(font_paragraphe,taille_actuelle,True).size(liste_rech[indice_type])[0]/2,
                y = rect_type_recherche.h/2 - font(font_paragraphe,taille_actuelle,True).size(liste_rech[indice_type])[1]/2,size = taille_actuelle,
                font = font_paragraphe,
                importer = True)
        if id_ == 0:
            draw_text(text = text_rechercher,
                    x = rect_type_recherche.x
                    + rect_type_recherche.w/2 - font_30.size(text_rechercher)[0]/2,
                    y = rect_type_recherche.y - 40,
                    color = blanc, importer = True, font = font_paragraphe,size = 30,
                    )
        if id_ == 0:
            screen.blit(surface_type_recherche,rect_type_recherche)
        screen.blit(image_aide,rect_aide)
        if display:
            display_result(num_resultat)
        screen.blit(image_retour,rect_goback)
        if id_ == 0:
            draw_text(text_on,color = (255,255,255),
                    x =0,
                    y = 0, font = chivo_titre,
                    size = 30)
        if go_back:
            break
        screen.blit(surface_status_co,pos_surface_status_co)
        last_screen = screen.copy()
        pygame.display.update(rect_surf_rechercher)
        pygame.display.flip()

    
def charger_playlist(dossier):
    """Charge la liste des fichiers audio du dossier spécifié."""
    fichiers_audio = []
    for fichier in os.listdir(dossier):
        if fichier.lower().endswith((".mp3", ".wav")):
            chemin_complet = os.path.join(dossier, fichier)
            fichiers_audio.append(chemin_complet)
    return fichiers_audio

PLAYLIST = charger_playlist("FCP3")
stop = False

        
def jouer_musique(playlist = PLAYLIST):
    """Joue les musiques de la playlist dans un ordre aléatoire."""
    global stop
    
    pygame.mixer.init()
    random.shuffle(playlist)# Mélange la playlist
    stop = False
    pause = False
    paused = 0
    for musique in playlist:
        pygame.mixer.music.load(musique)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():# Attente jusqu'à ce que la musique soit terminée
            if keyboard.is_pressed("ctrl+space"):
                pygame.mixer.music.pause()
                paused += 1
                pause = True
            if keyboard.is_pressed("ctrl") and keyboard.is_pressed("-"):
                pygame.mixer.music.stop()
                stop = True
            if keyboard.is_pressed("ctrl") and keyboard.is_pressed("+"): 
                pygame.mixer.music.rewind()
            time.sleep(0.1)
        
        if pause:
            while True: 
                if keyboard.is_pressed("ctrl+space"):
                    if paused % 2 == 1:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
                    paused += 1
                if keyboard.is_pressed("ctrl") and keyboard.is_pressed("-"):
                    pygame.mixer.music.stop()
                if keyboard.is_pressed("ctrl") and keyboard.is_pressed("+"): 
                    pygame.mixer.music.rewind()
                time.sleep(0.1)
            
        if stop :
            break
    

def key_press(event):
    global stop
    if keyboard.is_pressed("m+u+s+i+c"):
        rep = Gerer_requete.message("SECRET","TU AS DECOUVERTS LE SECRET DE L'APP, MAIS POUR L'INSTANT IL SE FAIT PETIT !")
        """thread_music = threading.Thread(target = jouer_musique,daemon=True) 

        if not thread_music.is_alive():
            if rep:
                thread_music.start()
            else:
                Gerer_requete.message("DOMMAGE")"""
    elif keyboard.is_pressed("ctrl+c"):
        sys.exit()
        quit()
    
        
keyboard.on_press(key_press)
    
    
def relative_at(rect : pygame.Rect,relative : pygame.Rect) -> pygame.Rect:
    """Fonction permettant d'avoir le rect relatif d'un element a un autre

    Args:
        rect (pygame.Rect): Rect de l'element ciblé
        relative (pygame.Rect): Rect du referentiel

    Returns:
        pygame.Rect: Rect relatif de rect a relative
    """
    return pygame.Rect(rect.x - relative.x,rect.y - relative.y,rect.w,rect.h)
            
            
surf_image2 = None 
continue_charging = None     

def compte():
    """Fonction affichant la partie compte de l'application"""
    global surf_image2,creer_compte,zone,dict_categorie,recup_categorie
    global connect,pp_base
    global continue_charging
    global fond_nav
    
    def look_valid(zone) -> bool:
        """Fonction qui Verifie si les input remplit le son correctement

        Args:
            zone (int): Precise la zone dans laquel se trouve l'utilisateur

        Returns:
            bool: Valider des input ou non
        """
        for key,value in dict_input[zone].items():
            if key != "input_mdp":
                if len(value["input"]) <= 0 or value["input"] == value["default"]:
                    return False
            else:
                if len(value["input_visible"]) <= 0 or value["input_visible"] == value["default"]:
                    return False
        return True
    
    def look_mdp(zone):
        """Verifie si le mot de passe est suffisament grand

        Args:
            zone (int): Precise la zone dans laquel se trouve l'utilisateur

        Returns:
            bool:  Precision  de si le mdp est suffisament grand
        """
        return len(dict_input[zone]["input_mdp"]["input_visible"]) >= dict_input[zone]["input_mdp"]["min"]
        
    def write_connection_tools(pseudo,mdp):
        """Fonction ecrivant les données de connection dans un fichier pour "sauvegarder" l'utilisateur

        Args:
            pseudo (str): Pseudo de l'utilisateur
            mdp (str): mot de passe de l'utilisateur
        """
        with open(os.path.join("Ressource","compte_connecter.txt"),"w") as fichier:
            fichier.write(f"{pseudo}\n{mdp}")
    
    def erase_connection_tools():
        with open(os.path.join("Ressource","compte_connecter.txt"),"w" ):
            pass
    def in_input_mdp_zone(dict_input):
        return (zone == 1 and dict_input[1]["input_mdp"]["active"] ==  True) or (zone == 0 and dict_input[0]["input_mdp"]["active"])
    
    def look_for_connection_tools():
        """Fonction qui verifie si des données d'utilisateur sont déjà enregistrez

        Returns:
            bool: Precision de si il y a un utilisateur connecter ou non
        """
        with open("Ressource/compte_connecter.txt", "r") as fichier:
            return len(fichier.read().splitlines()) != 0
        
    def desactiver_les_autres_input(key,value):
        pass
        
                        
    text_edit = "Clickez pour editer"
    text_creer_compte = "Bienvenue parmis nous ! Creez votre compte :)"
    text_con_compte = "Bon retour parmis nous ! Connectez vous :)"
    rect_pas_depasser = rect_screen.copy()
    rect_pas_depasser.w -= (20+ 50)
    size_titre = verification_size(rect_pas_depasser,chivo_titre,60,text_creer_compte,True)
    global continuer,size_grand
    barre_type = pygame.Surface((2,20))
    go_back = False
    creer_compte = True if not connect else False
    size_photo_pp_petit = (h_origine*(1-80/100),)*2
    font_paragraphe = apple_titre
    font_40 = pygame.font.Font(font_paragraphe, 40)
    font_30 = pygame.font.Font(font_paragraphe,30)
    font_20 = pygame.font.Font(font_paragraphe,20)
    rect_editer_photo = pygame.Rect(0,0,0,0)
    rect_editer_photo.w = font_20.size(text_edit)[0]
    rect_editer_photo.h = font_20.size(text_edit)[1]
    
    chemin_pp = os.path.join("image_user","photo_profil_user.png")
    if not connect:
        with open(chemin_pp,"wb") as fichier:
            fichier.write(pp_base)
    global image_pp
    #image_pp est la photo_de_profil basique de l'app
    image_pp = pygame.image.load(io.BytesIO(pp_base))
    if not connect:
        image_pp = pygame.transform.smoothscale(image_pp,size_photo_pp_petit)
    else:
        image_pp = pygame.transform.smoothscale(image_pp,size_grand)
    #ces ensembles de surface permette de faire une photo de profil en rond
    surf2 = pygame.Surface(size_photo_pp_petit, pygame.SRCALPHA)
    surf3 = pygame.Surface(size_photo_pp_petit, pygame.SRCALPHA)
    surf2g = pygame.Surface(size_grand,pygame.SRCALPHA)
    surf3g = pygame.Surface(size_grand,pygame.SRCALPHA)
    rect_host = pygame.Rect(0,0,w_origine/3,h_origine * (1-30/100))
    rect_ctn_host = pygame.Rect(0,0,rect_host.w + 300,rect_host.h + 40)
    
    rect_host.y = (h_origine + fond_nav.get_height())/2 - rect_host.h/2 #+fond_nav.get_height() pour le centrer dans la partie entre le nav et le bas de l'ecran
    rect_host.x = w_origine/2 - rect_host.w/2
    rect_ctn_host.x = rect_host.x - 20
    rect_ctn_host.y = rect_host.y - 20
    Surface_edit_photo = pygame.Surface((rect_editer_photo.w,rect_editer_photo.h),pygame.SRCALPHA)
    y_photo = rect_host.y + 10
    y_photo2 = 50
    x_photo2 = w_origine/2 - size_grand[0]/2
    rect_editer_photo.x = rect_host.x +rect_host.w/2 - rect_editer_photo.w/2
    rect_editer_photo.y = y_photo + size_photo_pp_petit[0] + 5
    Surface_host = pygame.Surface((rect_host.w,rect_host.h),pygame.SRCALPHA)
    #rect des inputs
    
    btn_submit = pygame.Rect(0,0,100,50)
    btn_submit.x = rect_host.x + rect_host.w/2 - btn_submit.w/2
    btn_submit.y = rect_host.y + rect_host.h - btn_submit.h - 30
    hauteur_input = 30

    taille_ref = btn_submit.y - rect_editer_photo.y - 30
    taille_ref -= 30

    ecart_entre_input = (taille_ref-4*hauteur_input)/3
    ec = ecart_entre_input
    
    
    ec += hauteur_input #l'ecart est calculé depuis le haut de l'input et non le bas, donc on fait +30
    rect_input_nom = pygame.Rect(rect_host.x + 10, rect_editer_photo.y + 30,rect_host.w/2 +50,hauteur_input)
    rect_test = pygame.Rect(rect_input_nom.x,rect_input_nom.y,rect_host.w,taille_ref)
    rect_input_age = pygame.Rect(rect_input_nom.x + rect_input_nom.w + 50 - 20,
                                    rect_input_nom.y,
                                    rect_host.w - rect_input_nom.w - 60,
                                    rect_input_nom.h)
    rect_input_prenom = pygame.Rect(rect_input_nom.x,rect_input_nom.y + ec, rect_input_nom.w,rect_input_nom.h)
    rect_input_pseudo = pygame.Rect(rect_input_nom.x, rect_input_prenom.y + ec,rect_input_nom.w, rect_input_nom.h)
    rect_input_mdp = pygame.Rect(rect_host.x + rect_host.w - 205, rect_input_pseudo.y +ec, 200,rect_input_nom.h)
    rect_input_pseudo2 = pygame.Rect(0, rect_input_nom.y,rect_input_nom.w, rect_input_nom.h)
    rect_input_mdp2 = pygame.Rect(0, rect_input_prenom.y, 200,rect_input_nom.h)
    #dictionnaire qui gère toute les inputs
    dict_input = [
                {
                "input_nom" : {"can_space" : True,"max" : 20, "input" : 'Nom', "default" : "Nom", "active" : False,"coupage" : 0,"depasse" : False,"rect_w" : rect_input_nom.w},
                "input_prenom" : {"can_space" : True,"max" : 20, "input" : 'Prenom', "default" : "Prenom", "active" : False,"coupage" : 0,"depasse" : False,"rect_w" : rect_input_nom.w},
                "input_pseudo" : {"can_space" : False,"max" : 20, "input" : 'Pseudo', "default" : "Pseudo", "active" : False,"coupage" : 0,"depasse" : False,"rect_w" : rect_input_nom.w},
                "input_age" : {"can_space" :  False,"max" : 3, "input" : 'Age', "default" : "Age", "active" : False,"coupage" : 0,"depasse" : False,"rect_w" : rect_input_age.w},
                "input_mdp" : {"can_space" : True,"max" : 15, "input_cache" : 'Mot de passe',"input_visible" : "", "default" : "Mot de passe","min" : 8, "active" : False,"coupage" : 0,"depasse" : False,"rect_w" : rect_input_mdp.w}
                },
                {
                "input_pseudo" : {"can_space" : False,"max" : 20, "input" : 'Pseudo', "default" : "Pseudo", "active" : False,"coupage" : 0,"depasse" : False,"rect_w" : rect_input_pseudo2.w},
                "input_mdp" : {"can_space" :  True,"max" : 15, "input_cache" : 'Mot de passe',"input_visible" : "", "default" : "Mot de passe","min" : 8, "active" : False,"coupage" : 0,"depasse" : False,"rect_w" : rect_input_mdp2.w}
                }
                ]
    
    schema_input = [
                    ["input_nom","input_age","input_prenom","input_pseudo","input_mdp"],
                    ["input_pseudo","input_mdp"]
                    ]
    if look_for_connection_tools():
        with open("./Ressource/compte_connecter.txt","r") as fichier:
            li = fichier.read().splitlines()
            con_pseudo = li[0]
            con_mdp = li[1]
        dict_input[1]["input_pseudo"]["input"] = con_pseudo
        dict_input[1]["input_mdp"]["input_visible"] = con_mdp
        dict_input[1]["input_mdp"]["input_cache"] = "*"*len(con_mdp)
        
    #tout les rects dispo dans les inputs
    all_rect = [
            [rect_input_nom,rect_input_prenom,rect_input_pseudo,rect_input_age,rect_input_mdp],
            [rect_input_pseudo2,rect_input_mdp2]
        ]
    color_edit = (0,0,200)
    
    invalid_champ = False
    check_save_con_data =  False
    take = False
    text_invalid = "Certain champs sont mal remplie"
    pseudo_ndispo = False
    text_ndispo = "Pseudo déjà existant"
    visible = False
    #erreur un peu de nom, rect_visible reprensente la taille des images pour cacher/voir le mdp
    rect_visible = pygame.Rect(0,0,39,rect_input_mdp.h-5)
    rect_visible.x = rect_input_mdp.x + rect_input_mdp.w - rect_visible.w - 10
    rect_visible.y = rect_input_mdp.y + rect_input_mdp.h/2 - rect_visible.h/2
    icone_mdp = pygame.image.load(os.path.join("Image", "image_mdp_visu.png")).convert_alpha()    
    icone_mdp = pygame.transform.smoothscale(icone_mdp,(rect_visible.w,rect_visible.h))
    invalid_mdp = False
    text_nmdp = "Minimum 8 caractères"
    text_log = "Vous avez déjà un compte ? connectez vous !"
    text_con = "Vous n'avez pas encore de compte ? creez en un !"
    coupage, line, size_y = make_line(text=text_log,font = font_40, size_max = 300)
    coupage2, line2, size_y2 = make_line(text=text_con,font = font_40, size_max = rect_ctn_host.w - 20)
    #reprensente les rects pour changer de mode de connection, erreur de nom
    rect_valider = pygame.Rect(0,0,120,50)
    rect_valider.x = rect_ctn_host.x + 10 + rect_ctn_host.w/2 - rect_valider.w/2
    rect_valider.y = rect_ctn_host.y + rect_ctn_host.h/2 - rect_valider.h/2 + size_y/2 + 30
    text_switch_log = "CONNECTION"
    text_switch_con = "CREER"
    zone = 0
    pas_correspondance = False
    n_pseudo = False
    #rect representant les dimensions de l'icone pour le restez connectez
    rect_save_user_data = pygame.Rect(0,0,30,30)
    text_n_correspond = 'Mot de passe incorrect'
    text_n_pseudo = "Pseudo inexistants"
    
    marge_cote_droit_contenaire_fond = (rect_ctn_host.x + rect_ctn_host.w) - (rect_host.x + rect_host.w)
    disposition = [
        {
            "rect_valider_x" : rect_host.w +20 + marge_cote_droit_contenaire_fond/2 - rect_valider.w/2,
            "rect_valider_y" : rect_ctn_host.y + rect_ctn_host.h/2 - rect_valider.h/2 + size_y/2 + 30,
            "btn_submit_x" : rect_host.w/2 - btn_submit.w/2,
            "btn_submit_y" :  rect_host.y + rect_host.h - btn_submit.h - 20,
            "rect_host_x" : w_origine/2 - rect_host.w/2,
            "rect_ctn_host_x" : rect_host.x - 20,
            "rect_editer_photo_x" : rect_host.w/2 - rect_editer_photo.w/2,
            "rect_editer_photo_y" : y_photo + size_photo_pp_petit[0] +5,
            "top_right" : 20,
            "top_left" : 0,
            "bottom_right" : 20,
            "bottom_left" : 0,
            "outil_line" : (coupage,line,size_y),
            "text_log" : text_log,
            "ajout_con" : 10,
            "rect_visible_x" : rect_input_mdp.w - rect_visible.w - 10,
            "rect_visible_y" : rect_input_mdp.h/2 - rect_visible.h/2,
            "text_bienvenu" : text_creer_compte,
            "question_compte" : "Vous avez déjà un compte ?",
            "reponse_compte" : "Connectez vous !",
            "x_question_rep_compte" : rect_host.x + rect_host.w + marge_cote_droit_contenaire_fond/2,
            "y_question_compte" : rect_host.y + 120,
            "text_switch_log_con" :text_switch_log
            },
        {
            "rect_valider_x" : marge_cote_droit_contenaire_fond/2 - rect_valider.w/2,
            "rect_valider_y" : rect_ctn_host.y + rect_ctn_host.h/2 - rect_valider.h/2 + size_y/2 + 59,
            "btn_submit_x"  : rect_host.w/2 - btn_submit.w/2,
            "btn_submit_y" : rect_host.y + rect_host.h - btn_submit.h - 20,
            "rect_ctn_host_x" : rect_host.x - marge_cote_droit_contenaire_fond,
            "rect_host_x" : w_origine/2 - rect_host.w/2,
            "rect_editer_photo_x" : rect_host.w/2 - rect_editer_photo.w/2,
            "rect_editer_photo_y" : y_photo + size_photo_pp_petit[0] + 5,
            "top_right" : 0,
            "top_left" : 20,
            "bottom_right" : 0,
            "bottom_left" : 20,
            "outil_line" : (coupage2,line2,size_y2),
            "text_log" : text_con,
            "ajout_con" : -10,
            "rect_visible_x" : rect_input_mdp.w - rect_visible.w - 10,
            "rect_visible_y" : rect_input_mdp.h/2 - rect_visible.h/2,
            "text_bienvenu" : text_con_compte,
            "question_compte" : "Vous n'avez pas encore de compte?",
            "reponse_compte" : "Creez en un !",
            "x_question_rep_compte" : rect_host.x - marge_cote_droit_contenaire_fond/2,
            "y_question_compte" : rect_host.y + 120,
            "text_switch_log_con" : text_switch_con
        }
        ]
    #btn en attendant la fin
    btn_disconnect = pygame.Rect(0,0,200,80)
    btn_disconnect.x = w_origine/2 - btn_disconnect.w/2
    
    btn_postimg = pygame.Surface((210,100),pygame.SRCALPHA)
    rect_postimg = pygame.Rect(w_origine/2 - 20 - btn_postimg.get_width(),
                    y_photo2 + size_grand[1] + 150,
                    btn_postimg.get_width(),
                    btn_postimg.get_height())
    rect_maketuto = pygame.Rect(w_origine/2 + 20,
                    y_photo2 + size_grand[1] + 150,
                    btn_postimg.get_width(),
                    btn_postimg.get_height())
    element_page_user = False
    x_effet1,x_effet2 = 0,0
    y_effet1,y_effet2 = 0,0
    intensiter_effet = 0
    collide_image = False
    color_bordure_image = (0,0,0)
    bordure = 1
    pp_choisi = False
    rect_ellipse = None
    global user
    liste_image_restez_co = [pygame.transform.scale(pygame.image.load(os.path.join("Image","icone_restez_co_inactif.png")),(rect_save_user_data.w,rect_save_user_data.h)),
                            pygame.transform.scale(pygame.image.load(os.path.join("Image","icone_restez_co_actif.png")),(rect_save_user_data.w,rect_save_user_data.h))]
    icone_restez_co = liste_image_restez_co[0]
    changement_image = 0
    zone = 0 if creer_compte else 1 #permet une logique par rapport a creer_compte
    cursor_position = 0 
    message_photo_profil = ""
    temoin_processus_fini_pp = [False,]
    press_tab = False
    rect_icone_reglage = pygame.Rect(-1500,2522,1,1)
    icone_aide = pygame.image.load(os.path.join("Image","icone_interrogation.png"))
    rect_aide = pygame.Rect(w_origine - taille_icone[0]- 5, 5, *taille_icone)
    icone_aide = pygame.transform.smoothscale(icone_aide,(rect_aide.w,rect_aide.h))
    click_return = False
    while continuer:
        Clock.tick(120)
        mouse = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        screen.fill(fond_ecran)
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                continuer = False          
            if rect_valider.collidepoint(mouse):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    creer_compte = not creer_compte
                    zone = 0 if creer_compte else 1
            elif rect_goback.collidepoint(mouse) and (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                go_back = True
            if rect_save_user_data.collidepoint(mouse):
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    changement_image += 1
                    check_save_con_data = not check_save_con_data
                    icone_restez_co = liste_image_restez_co[changement_image % 2]
                
            if (rect_editer_photo.collidepoint(mouse) or collide_image) and (zone == 0 or connect):
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    try:
                        path_ext = User.get_file(1)
                        path = path_ext[0]
                        img = resizeImage(path)                        
                        try:
                            global surf_image
                            screen.blit(last_screen,(0,0))
                            draw_text("Clickez pour valider\nAppuyer sur 'q' ou 'Echap' pour Annuler",x = w_origine/2 - font(font_paragraphe,35,True).size("Clickez pour valider")[0]/2,
                                    y = fond_nav.get_height() + 5, importer = True, size = 35,center_multi_line=True, font = font_paragraphe,ombre = True,color = blanc)
                            pygame.display.update()
                            surf_image,rect_ellipse,image_photo_pp = img.try_to_resize(screen)
                            if not connect:
                                surf_image = pygame.transform.smoothscale(surf_image,size_photo_pp_petit)
                            else:
                                surf_image2 = pygame.transform.smoothscale(surf_image,size_grand)
                            try:                                
                                with open(path,"rb") as fichier:
                                    nv_pp = fichier.read()
                                with open(chemin_pp,"wb") as fichier:
                                    fichier.write(nv_pp)
                                if connect:
                                    message_photo_profil = "Votre photo de profil est cours de traitement, si vous quittez/vous déconnectez maintenant elle ne sera pas sauvegardée"
                                    """th_pp = threading.Thread(target = user.change_element, args=(False,False,False,True,False,False,nv_pp,False,temoin_processus_fini_pp))
                                    th_pp.start()
                                    th_rect_pp = threading.Thread(target = user.change_element, args=(False,False,False,False,False,True,rect_ellipse,True,temoin_processus_fini_pp))
                                    th_rect_pp.start()"""
                                    thread_changement = threading.Thread(target=user.change_element, args=(False,False,False,True,False,True,
                                        [nv_pp,rect_ellipse],True,temoin_processus_fini_pp))
                                    thread_changement.start()
                                pp_choisi = True
                            except OSError:
                                dialog.message("L'ouverture de ce document à échouer !",last_screen,title="Erreur")
                                                
                            except Exception:
                                dialog.message("Une erreur est survenue ! ", last_screen,title="Erreur")
                                
                        except AnnuleCropPhoto as err:
                            pass    
                        except Exception as e:
                            pass     
                            dialog.message("Une erreur est survenue ! ", last_screen,title="Erreur")
                                        
                    except noFileException:
                        pass
            ###################################################### Système après connection #################################################
            if connect:
                if rect_aide.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    reponse = dialog.ask_yes_no("Souhaitez vous ouvrir le document aide de la page compte ? ", last_screen)
                    if reponse:
                        animation_ouverture.start_anime(last_screen)
                        try:
                            Gerer_requete.demarrer_fichier(doc = os.path.join("Ressource","Aide_interface_compte.docx"),with_path=True,ext = None)
                        except OSError as e:
                            dialog.message("L'ouverture de ce document à échouer !",last_screen,title="Erreur")
                        except Exception as e:
                            dialog.message("Une erreur est survenue ! ", last_screen,title="Erreur")
                        finally:
                            animation_ouverture.stop_anime()

                if btn_disconnect.collidepoint(mouse):
                    if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                        #remettre la photo de profil de base dans chemin_pp
                        with open(chemin_pp,"wb") as fichier:
                            fichier.write(pp_base)
                        connect = False
                        del user
                        erase_connection_tools()
                        pp_choisi = False
                        #image_pp = pygame.image.load(io.BytesIO(pp_base))
                        image_pp = pygame.transform.smoothscale(image_pp,size_photo_pp_petit)
                        element_page_user = False
                    
                                        
                elif rect_postimg.collidepoint(mouse):
                    if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                        try:          
                            screen.blit(last_screen,(0,0))
                            pygame.display.update()                  
                            nom_tuto = input_popup()
                            if nom_tuto != False:
                                path = User.get_file(1)[0]
                                if path != " ":
                                    if user.categorie != None:
                                        rep = dialog.ask_yes_no_cancel(f"Souhaitez vous mettre a ce tuto la même catégorie que votre compte ? ({user.categorie})",last_screen)
                                    else:
                                        rep = False
                                    if rep is False:
                                        categorie = interface_deroullante_categorie(last_screen)
                                    elif rep is True:
                                        categorie = user.categorie
                                    else:
                                        categorie = None
                                    if categorie != None:
                                        if dialog.ask_yes_no("Doit on considérez votre tuto comme une demande de tutos ?",last_screen):
                                            is_annonce = 1
                                        else:
                                            is_annonce = 0
                                        animation_mise_en_ligne.start_anime(last_screen)
                                        user.save_tuto(path,"",nom_tuto,categorie,is_annonce)
                                        animation_mise_en_ligne.stop_anime()
                            else:
                                break
                        except noConnection:
                            dialog.message("Une erreur de connexion a eu lieu !",last_screen,title="Erreur") 
                        except Exception as e:
                            dialog.message("Une erreur est survenue ! ", last_screen,title="Erreur")
                        else:
                            if rep != None:
                                dialog.message("Votre tuto a bien été mis en ligne ! ",last_screen)
                        finally:
                            animation_mise_en_ligne.stop_anime()

                elif rect_maketuto.collidepoint(mouse):
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        ecrire_tuto(user)
                        
                if element_page_user: 
                    if rect_icone_reglage.collidepoint(mouse):
                        
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            try:
                                if recup_categorie == None :
                                    recup_categorie = Gerer_requete.take_categorie()
                                else:
                                    categorie = interface_deroullante_categorie(last_screen)
                                
                                    if categorie != None:
                                        animation_update.start_anime(last_screen)
                                        try:
                                            ancien_cate = user.categorie
                                            user.change_categorie_compte(categorie)
                                            dict_categorie[categorie]["membre"] += 1
                                            dict_categorie[ancien_cate]["membre"] -= 1
                                        except noConnection:
                                            animation_update.stop_anime()
                                            dialog.message("Une erreur de connexion a eu lieu !",last_screen,title="Erreur")
                                        except Exception as e:
                                            animation_update.stop_anime()
                                            dialog.message("Une erreur est survenue ! ", last_screen,title="Erreur")
                                        else:
                                            animation_update.stop_anime()
                                            dialog.message("La catégorie de votre compte a bien été changeée",last_screen)

                            except Exception as e:
                                dialog.message("Les catégories n'ont pas pu être récupéré",last_screen,title="Erreur")
                            
            elif creer_compte or not creer_compte:
                if rect_visible.collidepoint(mouse):
                    if mouse_click:
                        visible = not visible
                        icone_mdp = pygame.image.load("Image/image_mdp_visu.png").convert_alpha() if not visible else pygame.image.load("Image/image_mdp_cacher.png").convert_alpha()
                        icone_mdp = pygame.transform.smoothscale(icone_mdp,(rect_visible.w,rect_visible.h))
                elif rect_editer_photo.collidepoint(mouse):
                    color_edit = palette_couleur.Bleu
                    
                else:
                    color_edit = (0,0,200)
                condi_1 = btn_submit.collidepoint(mouse) and (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)   
                condi_2 = in_input_mdp_zone(dict_input) and (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and not click_return)
                if condi_1 or condi_2:
                    click_return = True                        
                    animation_connection.start_anime(last_screen)                    
                    if look_valid(zone):
                        if look_mdp(zone):
                            try:
                                disponibilite_pseudo = User.verifier_pseudo(dict_input[zone]["input_pseudo"]["input"])
                                if disponibilite_pseudo and zone == 0:
                                    #Le pseudo est disponible, il peut crée un compte
                                    nom = dict_input[0]["input_nom"]["input"].strip()
                                    prenom = dict_input[0]["input_prenom"]["input"].strip()
                                    age = int(dict_input[0]["input_age"]["input"])
                                    pseudo = dict_input[0]["input_pseudo"]["input"].strip()
                                    mdp = dict_input[0]["input_mdp"]["input_visible"].strip()
                                    with open(chemin_pp,"rb") as fichier:
                                        photo_profil = fichier.read()                                            
                                    user = User(nom,prenom,age,pseudo,mdp,photo_profil,rect_pp = rect_ellipse)
                                    try:                               
                                        user.save_user() 
                                    except noConnection:
                                        dialog.message("Une erreur de connexion a eu lieu !",last_screen,title="Erreur")
                                    else:
                                        connect = True
                                        #creer_compte = False
                                        with open(chemin_pp,"wb") as fichier:                                                
                                            if user.photo_profil != pp_base:
                                                fichier.write(user.photo_profil)
                                            else:
                                                fichier.write(pp_base)                                            
                                        if check_save_con_data:
                                            write_connection_tools(pseudo,mdp)
                                        else:
                                            erase_connection_tools()
                                        if user.photo_profil == pp_base:
                                            image_pp = pygame.image.load(chemin_pp)
                                            image_pp = pygame.transform.smoothscale(image_pp,size_grand)
                                        else:
                                            #processus de reconstruction de la pdp car sinon si on aggrandi juste la surface surf_image elle est flou
                                            rect_pp = user.rect_pp
                                            if isinstance(rect_pp,pygame.Rect):
                                                rect_pp = Gerer_requete.separe_rect(user.rect_pp)
                                            rect_pp = rect_pp.split(",")
                                            rect_pp = [int(i) for i in rect_pp]
                                            rect_pp = pygame.Rect(rect_pp)
                                            img_ = pygame.image.load(chemin_pp).convert_alpha()
                                            old_width, old_height = img_.get_size()
                                            # Définir la nouvelle largeur (ou hauteur)
                                            new_width = 500#le rect a été calculer par rapport a une image qui était en width = 500, alors l'image envoyé doit l'être aussi
                                            # Calculer la nouvelle hauteur (ou largeur) pour conserver le rapport d'aspect (produit en croix)
                                            new_height = int(old_height * new_width / old_width)
                                            # Redimensionner l'image
                                            img_ = pygame.transform.smoothscale(img_, (new_width,new_height))
                                            surf_image2 = resizeImage.rendre_transparent(img_,rect_pp,0)
                                            surf_image2 = pygame.transform.smoothscale(surf_image2, size_grand)                                                
                                
                                elif not disponibilite_pseudo and zone == 0:
                                    #Le pseudo n'est pas disponible, il ne  peut créé un compte
                                    pseudo_ndispo = True
                                elif not disponibilite_pseudo and zone == 1:
                                    #Le pseudo n'est pas disponible, donc un compte existe, donc il peut essayer de s'y connecter
                                    pseudo = dict_input[zone]["input_pseudo"]["input"]
                                    mdp = dict_input[zone]["input_mdp"]["input_visible"]                                     
                                    try:
                                        user = User.log_user(pseudo,mdp)
                                    except userNonCharger:
                                        pas_correspondance = True
                                    except noConnection:
                                        dialog.message("Une erreur de connexion a eu lieu !",last_screen,title="Erreur")
                                    else:
                                        
                                        connect = True
                                        creer_compte = False
                                        with open(chemin_pp,"wb") as fichier:
                                            if user.photo_profil != pp_base:
                                                fichier.write(user.photo_profil)
                                            else:
                                                fichier.write(pp_base)
                                        if check_save_con_data:
                                            write_connection_tools(pseudo,mdp)
                                        else:
                                            erase_connection_tools()
                                        if user.photo_profil == pp_base:
                                            image_pp = pygame.image.load(chemin_pp)
                                            image_pp = pygame.transform.smoothscale(image_pp,size_grand)
                                        else:
                                            #processus de reconstruction de la pdp car sinon si on aggrandi juste la surface surf_image elle est flou
                                            rect_pp = user.rect_pp
                                            if isinstance(rect_pp,pygame.Rect):
                                                rect_pp = Gerer_requete.separe_rect(user.rect_pp)
                                            rect_pp = rect_pp.split(",")
                                            rect_pp = [int(i) for i in rect_pp]
                                            rect_pp = pygame.Rect(rect_pp)
                                            img_ = pygame.image.load(chemin_pp).convert_alpha()
                                            old_width, old_height = img_.get_size()
                                            # Définir la nouvelle largeur (ou hauteur)
                                            new_width = 500 #le rect a été calculer par rapport a une image qui était en width = 500, alors l'image envoyé doit l'être aussi
                                            # Calculer la nouvelle hauteur (ou largeur) pour conserver le rapport d'aspect (produit en croix)
                                            new_height = int(old_height * new_width / old_width)
                                            # Redimensionner l'image
                                            img_ = pygame.transform.smoothscale(img_, (new_width,new_height))
                                            surf_image2 = resizeImage.rendre_transparent(img_,rect_pp,0)
                                            surf_image2 = pygame.transform.smoothscale(surf_image2, size_grand)                                                
    
                                elif disponibilite_pseudo and zone == 1:
                                    #Le pseudo est disponible, donc aucun compte n'existe, donc il ne peut s'y connnecter
                                    n_pseudo = True
                                
                            except noConnection:
                                dialog.message("Une erreur de connexion a eu lieu !",last_screen,title="Erreur")
                            except Exception as e:
                                dialog.message("Une erreur est survenue ! ", last_screen,title="Erreur")
                            finally:
                                animation_connection.stop_anime()
                        else:
                            invalid_mdp = True
                    else:
                        invalid_champ = True   
                    animation_connection.stop_anime() 
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:
                        click_return = False
                ################################################################ Système de l'input #################################################################     
                if not connect:       
                    i = 0         
                    for key,value in dict_input[zone].items():
                        if all_rect[zone][i].collidepoint(mouse):
                            if mouse_click and not rect_visible.collidepoint(mouse):
                                cursor_position = 0
                                if key != "input_mdp":
                                    value["active"] = not value["active"]
                                    value["input"] = "" if value["input"] == value["default"] else value["input"]
                                    if not value["active"]:
                                        value["input"] = value["default"] if value["input"] == "" else value["input"]
                                    else:
                                        for key2,value in dict_input[zone].items():
                                            if key2 != key:
                                                value["active"] = False
                                                if key2 != "input_mdp":
                                                    value["input"] = value["default"] if value["input"] == "" else value["input"]
                                                else:
                                                    value["input_visible"] = value["default"] if value["input_visible"] == "" else value["input_visible"]
                                                    value["input_cache"] = value["default"] if value["input_cache"] == "" else value["input_cache"]
                                else:
                                    value["active"] = not value["active"]
                                    value["input_visible"] = "" if value["input_visible"] == value["default"] else value["input_visible"]
                                    value["input_cache"] = "" if value["input_cache"] == value["default"] else value["input_cache"]
                                    if not value["active"]:
                                        value["input_cache"] = value["default"] if value["input_cache"] == "" else value["input_cache"]
                                        value["input_visible"] = value["default"] if value["input_visible"] == "" else value["input_visible"]

                                    else:
                                        for key2,value in dict_input[zone].items():
                                            if key2 != key:
                                                value["active"] = False
                                                value["input"] = value["default"] if value["input"] == "" else value["input"]
                                                    
                        if value["active"]:
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_TAB and not press_tab:
                                    press_tab = True
                                    position = schema_input[zone].index(key) #récuper la position dans la liste a laquel est situé l'input utilisé
                                    if position == len(schema_input[zone]) - 1:
                                        next_input = 0 #Dans ce cas, l'input est situé en derniere position donc on doit revenir au début
                                    else:
                                        next_input = position + 1 #On prend l'input suivant 
                                    key_ = schema_input[zone][next_input]
                                    dict_input[zone][key_]["active"] = True #On active l'input suivant
                                    if key_ != "input_mdp":
                                        #On le vide si besoin
                                        dict_input[zone][key_]["input"] = "" if dict_input[zone][key_]["input"] == dict_input[zone][key_]["default"] else dict_input[zone][key_]["input"]
                                    else:
                                        #on le vide si besoin, methode special pour input_mdp
                                        dict_input[zone][key_]["input_visible"] = "" if dict_input[zone][key_]["input_visible"] == dict_input[zone][key_]["default"] else dict_input[zone][key_]["input_visible"]
                                        dict_input[zone][key_]["input_cache"] = "" if dict_input[zone][key_]["input_cache"] == dict_input[zone][key_]["default"] else dict_input[zone][key_]["input_cache"]
                                    
                                    #Processus pour désactiver les autres input
                                    if key_ == "input_mdp":
                                        for key2,value_ in dict_input[zone].items():
                                            if key2 != key_:
                                                value_["active"] = False
                                                value_["input"] = value_["default"] if value_["input"] == "" else value_["input"]
                                    else:
                                        for key2,value_ in dict_input[zone].items():
                                            if key2 != key_:
                                                value_["active"] = False
                                                if key2 != "input_mdp":
                                                    value_["input"] = value_["default"] if value_["input"] == "" else value_["input"]
                                                else:
                                                    value_["input_visible"] = value_["default"] if value_["input_visible"] == "" else value_["input_visible"]
                                                    value_["input_cache"] = value_["default"] if value_["input_cache"] == "" else value_["input_cache"]
                                
                                
                                if event.key == pygame.K_LEFT:
                                    cursor_position -= 1
                                    if key != "input_mdp":
                                        if len(value["input"][value["coupage"]:]) - cursor_position <= 0:
                                            cursor_position = len(value["input"])
                                    else:
                                        if len(value["input_visible"][value["coupage"]]) - cursor_position <= 0:
                                            cursor_position = 0
                                elif event.key == pygame.K_RIGHT:
                                    cursor_position += 1
                                    if cursor_position >= 0:
                                        cursor_position = 0
                                if event.key == pygame.K_BACKSPACE:
                                    if key != "input_mdp":
                                        separation_1 = value["input"][:len(value["input"]) + cursor_position][:-1]
                                        separation_2 = value["input"][len(value["input"]) + cursor_position:]
                                        value["input"] = separation_1 + separation_2
                                    else:
                                        separation_1_1 = value["input_visible"][:len(value["input_visible"]) + cursor_position][:-1]
                                        separation_2_1 = value["input_visible"][len(value["input_visible"]) + cursor_position:]
                                        value["input_visible"] = separation_1_1 + separation_2_1 
                                        separation_1_2 = value["input_cache"][:len(value["input_cache"]) + cursor_position][:-1]
                                        separation_2_2 = value["input_cache"][len(value["input_cache"]) + cursor_position:]
                                        value["input_cache"] = separation_1_2 + separation_2_2
                                    if value["depasse"] and value["coupage"] > 0:
                                        value["coupage"] -= 1
                                elif event.key == pygame.K_SPACE and value["can_space"]:
                                    if key != "input_mdp":
                                        separation_1 = value["input"][:len(value["input"]) + cursor_position]
                                        separation_2 = value["input"][len(value["input"]) + cursor_position:]
                                        value["input"] = separation_1 + " " + separation_2
                                    else:  
                                        separation_1_1 = value["input_visible"][:len(value["input_visible"]) + cursor_position] + " "
                                        separation_2_1 = value["input_visible"][len(value["input_visible"]) + cursor_position:]
                                        value["input_visible"] = separation_1_1 + separation_2_1 
                                        separation_1_2 = value["input_cache"][:len(value["input_cache"]) + cursor_position] + " "
                                        separation_2_2 = value["input_cache"][len(value["input_cache"]) + cursor_position:]
                                        value["input_cache"] = separation_1_2 + separation_2_2
                                    if value["depasse"]:
                                        value["coupage"] += 1
                                elif event.key == pygame.K_RETURN:
                                    pass
                                                                    
                                else:
                                    if key != "input_mdp":
                                        if len(value["input"]) < value["max"]:
                                            if key == "input_age":
                                                if event.unicode.isdigit():
                                                    value["input"] += event.unicode
                                                else:
                                                    pass
                                            else:
                                                if event.unicode.isprintable() and event.unicode != "":
                                                    separation_1 = value["input"][:len(value["input"]) + cursor_position]
                                                    separation_2 = value["input"][len(value["input"]) + cursor_position:]
                                                    value["input"] = separation_1 + event.unicode + separation_2
                                                    if value["depasse"]:
                                                        value["coupage"] += 1                                        
                                    else:
                                        if len(value["input_visible"]) < value["max"]:
                                            if key == "input_age":
                                                if event.unicode.isdigit():
                                                    value["input_visible"] += event.unicode
                                                    value["input_cache"] += "*"
                                                else:
                                                    pass
                                            else:
                                                if event.unicode.isprintable() and event.unicode != "":
                                                    separation_1 = value["input_visible"][:len(value["input_visible"]) + cursor_position]
                                                    separation_2 = value["input_visible"][len(value["input_visible"]) + cursor_position:]
                                                    value["input_visible"] = separation_1 + event.unicode + separation_2
                                                    value["input_cache"] += "*"
                                                    if value["depasse"]:
                                                        value["coupage"] += 1
                            elif event.type == pygame.KEYUP and event.key == pygame.K_TAB:
                                press_tab = False #Eviter la detection indésirable de l'appuie 2 fois sur la touche tab
                        i += 1
                    
        #interface user quand il n'est pas connecter
        if (creer_compte or not creer_compte) and not connect:
            fond_nav.fill(palette_couleur.Noir)
            screen.blit(fond_nav, (0,0))
            
            rect_host.x = disposition[zone]["rect_host_x"]
            rect_ctn_host.x = disposition[zone]["rect_ctn_host_x"] #rpresente le 2e fond de connection et aussi creer compte
            rect_valider.x = disposition[zone]["rect_valider_x"] + rect_ctn_host.x
            rect_valider.y = disposition[zone]["rect_valider_y"]
            btn_submit.x = disposition[zone]["btn_submit_x"] + rect_host.x
            btn_submit.y = disposition[zone]["btn_submit_y"]
            rect_editer_photo.x = disposition[zone]["rect_editer_photo_x"] + rect_host.x
            rect_editer_photo.y = disposition[zone]["rect_editer_photo_y"]
            all_rect[1][0].x = disposition[1]["rect_host_x"] + 10
            all_rect[1][1].x = disposition[1]["rect_host_x"] + rect_host.w - 220
            rect_visible.y = disposition[zone]["rect_visible_y"] + all_rect[zone][-1].y
            rect_visible.x = disposition[zone]["rect_visible_x"] + all_rect[zone][-1].x
            text_switch_log_con = disposition[zone]["text_switch_log_con"]
            x_text_switch_question = disposition[zone]["x_question_rep_compte"]
            y_text_switch_question_compte = disposition[zone]["y_question_compte"]
            question_compte = disposition[zone]["question_compte"] #represente la premiere partie de la question sur le compte
            reponse_compte = disposition[zone]["reponse_compte"] #represente la 2e partie
            rect_input_mdp = all_rect[zone][-1]
            rect_save_user_data.x = rect_input_mdp.x + 10
            rect_save_user_data.y = rect_input_mdp.y + rect_input_mdp.h + 5            
            text_bienvenu = disposition[zone]["text_bienvenu"]
            #gestion des champs invalides
            if invalid_champ:
                if not take:
                    time_start = pygame.time.get_ticks()
                    take = True
                time = pygame.time.get_ticks() - time_start
                draw_text(f"*{text_invalid}*", font = font_paragraphe,
                    size = 20, x = w_origine/2 - font_20.size(text_invalid)[0]/2,
                    y = rect_host.y - 50,importer = True,color = (200,0,0))
                if time/1000 >= 2:
                    invalid_champ = False
                    take = False
            elif pas_correspondance:    
                if not take:
                    time_start = pygame.time.get_ticks()
                    take = True
                time = pygame.time.get_ticks() - time_start
                draw_text(f"*{text_n_correspond}*", font = font_paragraphe,
                    size = 20, x = w_origine/2 - font_20.size(text_n_correspond)[0]/2,
                    y = rect_host.y - 50,importer = True,color = (200,0,0))
                if time/1000 >= 2:
                    pas_correspondance = False
                    take = False 
            elif n_pseudo:
                if not take:
                    time_start = pygame.time.get_ticks()
                    take = True
                time = pygame.time.get_ticks() - time_start
                draw_text(f"*{text_n_pseudo}*", font = font_paragraphe,
                    size = 20, x = w_origine/2 - font_20.size(text_n_pseudo)[0]/2,
                    y = rect_host.y - 50,importer = True,color = (200,0,0))
                if time/1000 >= 2:
                    n_pseudo = False
                    take = False
            
        
            title(text_bienvenu,size = size_titre)
            Surface_host.fill((255,255,255,0))
            couleur_save_user_data = (255,0,0) if not check_save_con_data else (0,255,0)
            pygame.draw.rect(Surface_host,palette_couleur.Gris_clair,(0,0,rect_host.w,rect_host.h),0,20)
            pygame.draw.rect(Surface_host,(0,0,0),(0,0,rect_host.w,rect_host.h),2,20)
            
            Surface_host.blit(icone_restez_co,((rect_save_user_data.x - rect_host.x,rect_save_user_data.y - rect_host.y)))
            draw_text(contener = Surface_host, text = "Restez connecter",x = rect_save_user_data.x - rect_host.x + rect_save_user_data.w + 10,
                    y = rect_save_user_data.y - rect_host.y +5, font = "Arial")
            pygame.draw.rect(screen,palette_couleur.Noir,(rect_ctn_host),0,20) #rpresente le 2e fond de connection et aussi creer compte
            pygame.draw.rect(screen,(0,0,0),(rect_ctn_host),2,20)
            screen.blit(Surface_host,(rect_host.x,rect_host.y))  #represente la surface principal grise         
            if pseudo_ndispo:
                if not take:
                    time_start = pygame.time.get_ticks()
                    take = True
                time = pygame.time.get_ticks() - time_start
                draw_text(f"*{text_ndispo}*", font = font_paragraphe,
                    size = 20, x = rect_input_pseudo.x,
                    y = rect_input_pseudo.y -20,importer = True,color = (200,0,0))
                if time/1000 >= 2:
                    pseudo_ndispo = False
                    take = False
            elif invalid_mdp:               
                if not take:
                    time_start = pygame.time.get_ticks()
                    take = True
                time = pygame.time.get_ticks() - time_start
                draw_text(f"*{text_nmdp}*", font = font_paragraphe,
                    size = 20, x = rect_input_mdp.x,
                    y = rect_input_mdp.y - 25,importer = True,color = (200,0,0))
                if time/1000 >= 2:
                    invalid_mdp = False
                    take = False 
            color_submit = bleu_s if not btn_submit.collidepoint(mouse) else (255,255,255)
            
            pygame.draw.rect(screen,palette_couleur.Bleu,btn_submit,0,10)
            pygame.draw.rect(screen,(0,0,0),btn_submit,1,10)            
            draw_text("VALIDER", x = btn_submit.x + btn_submit.w/2 - font_20.size("VALIDER")[0]/2,
                    y = btn_submit.y + btn_submit.h/2 - font_20.size("VALIDER")[1]/2,
                    font = font_paragraphe, importer = True, color = blanc)
            
            #mettre ma ptn de pp merde
            if not pp_choisi or not creer_compte or zone == 1:
                pygame.draw.ellipse(surf2, (255, 255, 255), (0,0,*size_photo_pp_petit))
                surf3.blit(surf2, (0, 0))
                surf3.blit(image_pp, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)     
                screen.blit(surf3, (rect_host.x + rect_host.w/2 - size_photo_pp_petit[0]/2, y_photo))
            elif pp_choisi and creer_compte:
                screen.blit(surf_image,(rect_host.x + rect_host.w/2 - size_photo_pp_petit[0]/2, y_photo))
            mask = pygame.mask.from_surface(surf2)
            ellipse = pygame.draw.ellipse(screen,color_bordure_image,(rect_host.x + rect_host.w/2 - size_photo_pp_petit[0]/2, y_photo,*size_photo_pp_petit),int(bordure))
            if ellipse.collidepoint(mouse):
                #on créé la position relative avec la souris par rapport a l'ellipse
                mask_x = mouse[0] - ellipse.x
                mask_y = mouse[1] - ellipse.y
                if mask.get_at((mask_x, mask_y)):
                    collide_image = True
                    color_bordure_image = palette_couleur.Bleu
                else:
                    collide_image = False
                    color_bordure_image = (0,0,200)
            else:                
                color_bordure_image = (0,0,200)
                collide_image = False
            Surface_edit_photo.fill((0,0,0,0))
            if zone == 0:
                draw_text(contener = Surface_edit_photo, text = text_edit,
                        x = rect_editer_photo.w/2 - font_20.size(text_edit)[0]/2, y = 0,
                        font = font_paragraphe, importer = True,
                        size = 20, color = color_edit)           
            for rect in all_rect[zone]:
                pygame.draw.rect(screen,blanc, rect,0,20)
                pygame.draw.rect(screen,palette_couleur.Bleu, rect,2,20)
            
            
            #pygame.draw.rect(screen,(0,0,0),rect_visible)
            screen.blit(icone_mdp, rect_visible)
            #a remettre a une autre position
            
            pygame.draw.rect(screen,palette_couleur.Bleu,rect_valider,0,40)
            pygame.draw.rect(screen,(0,0,0),rect_valider,1,40)
            #dessine le texte dans case pour changer de compte
            draw_text(x = rect_valider.x + rect_valider.w/2 - font_20.size(text_switch_log_con)[0]/2,
                    y = rect_valider.y + rect_valider.h/2 - font_20.size(text_switch_log_con)[1]/2,
                    text = text_switch_log_con, font = font_paragraphe, importer = True,color = blanc)
            #dessine la question du compte
            y_text_switch_question_compte += 20
            draw_text(x = x_text_switch_question - font(font_paragraphe,20,True).size(question_compte)[0]/2, y = y_text_switch_question_compte, text = question_compte, size = 20,
                    font = font_paragraphe,
                    importer =True, color = blanc)
            for i in range(2):
                draw_text(x = x_text_switch_question - font(font_paragraphe,40,True).size(reponse_compte)[0]/2,
                        y = y_text_switch_question_compte + 40, text = reponse_compte, font = font_paragraphe,importer =True, color = blanc,
                        size = 40)            
            i = 0
            #image_user les inputs
            for key,value in dict_input[zone].items():
                if key != "input_mdp":
                    input_ = value["input"]
                else:
                    input_ = value["input_cache"] if not visible else value["input_visible"]
                
                if font_20.size(input_)[0] +5 >= value["rect_w"]:
                    value["depasse"] = True
                else:
                    value["depasse"] = False 
                x = all_rect[zone][i].x + 10
                y = all_rect[zone][i].y + 5        
                draw_text(input_[value["coupage"]:], size = 20,
                        x = x,
                        y = y, font = font_paragraphe, importer = True,color = (0,0,0))                    
                if value["active"]:
                    barre_type.fill((0,0,0))
                    rect_bt = (x + font_20.size(input_[value["coupage"]:][:len(input_) + cursor_position])[0] ,y)
                    screen.blit(barre_type,rect_bt)
                i += 1      
            
            screen.blit(Surface_edit_photo,(rect_editer_photo.x,rect_editer_photo.y))
        else:
            if not element_page_user:
                size_for_case = verification_size(pygame.Rect(0,0,w_origine/7,0),arial,100,"TUTO EN TEXTE !",False)
                font_for_case = font(arial,size_for_case,False)
                btn_postimg = pygame.Surface((font_for_case.size("TUTO EN TEXTE !")[0] + 20,font_for_case.size("TUTO EN TEXTE !")[1] * 2 +30),pygame.SRCALPHA)
                btn_maketuto = btn_postimg.copy()
                btn_disconnect.w = btn_postimg.get_width()
                btn_disconnect.h = btn_postimg.get_height()
                btn_disconnect.x = w_origine/2 - btn_disconnect.w/2
                size_deconnexion = verification_size(pygame.Rect(0,0,btn_disconnect.w - 40,0),font_paragraphe,100,"Déconnexion",True)
                surface_message_info = pygame.Surface((h_origine/3,h_origine/3), pygame.SRCALPHA)
                categorie = user.categorie if user.categorie != None else "Aucune"
                if dict_categorie == {}:
                    try:
                        dict_categorie = Gerer_requete.update_categorie_member()
                    except:
                        dialog.message("Une erreur est survenue ! ", last_screen,title="Erreur")
                        return
                
                try:
                    membre_categorie = " " if user.categorie == None else f' Membre de cette catégorie : {dict_categorie[user.categorie]["membre"]}' 
                except:
                    membre_categorie = ""
                message = f"Actuellement votre catégorie est : {categorie}. Avoir une catégorie de compte permettra a l'application de vous mettre par défaut des tutos dans l'espace menu."\
                    + membre_categorie              
                size = 30
                coupage,line,y = make_line(message,font(TNN,size,True),surface_message_info.get_width() -5)
                while y > surface_message_info.get_height():
                    size -= 2
                    coupage,line,y = make_line(message,font(TNN,size,True),surface_message_info.get_width() -5)
                surface_message_info = pygame.Surface((surface_message_info.get_width(),y + 5),pygame.SRCALPHA)
                surface_message_info.fill((0,0,0,0))
                pygame.draw.rect(surface_message_info,palette_couleur.Noir,(0,0,*surface_message_info.get_size()),0,20)
                all_text = decoupe_text(coupage,line,message)
                for i in range(len(all_text)):
                    draw_text(all_text[i], font = TNN, size = size ,color = blanc, center_multi_line= True,contener = surface_message_info,importer = True, y = 5 + (size*i))
                icone_reglage = pygame.image.load(os.path.join("Image","icone_reglage.png"))
                icone_reglage = pygame.transform.scale(icone_reglage,(taille_icone))
                text_postimg = "POSTEZ UN\n TUTO VISUEL !"
                text_maketuto = "CREEZ UN\n TUTO EN TEXTE !"
                coupage, line, size_y = make_line(text=text_postimg,font = font_for_case, size_max = btn_postimg.get_width())
                coupage2, line2, size_y2 = make_line(text=text_maketuto,font = font_for_case, size_max = btn_postimg.get_width())
                taille_texte_approximate = 160
                hauteur_font_surf_co = (10 + size_grand[1] + taille_texte_approximate + btn_postimg.get_height() +60 + btn_disconnect.h + 10)
                y_fond_surf_user_co = h_origine/2 - hauteur_font_surf_co/2
                y_photo2 = y_fond_surf_user_co + 10
                rect_postimg = pygame.Rect(w_origine/2 - 20 - btn_postimg.get_width(),
                        y_photo2 + size_grand[1] + 160,
                        btn_postimg.get_width(),
                        btn_postimg.get_height())
                rect_maketuto = pygame.Rect(w_origine/2 + 20,
                        y_photo2 + size_grand[1] + 160,
                        btn_postimg.get_width(),
                        btn_postimg.get_height())
                surface_fond_user_co = pygame.Surface((btn_postimg.get_width() + 40 + btn_postimg.get_width() + 200,hauteur_font_surf_co), pygame.SRCALPHA)
                taille_en_plus = 30
                surface_fond_user_co_back = pygame.Surface((surface_fond_user_co.get_width() + taille_en_plus,
                                                            surface_fond_user_co.get_height() + taille_en_plus), pygame.SRCALPHA)
                
                pos_icone_reglage = (w_origine/2 - surface_fond_user_co.get_width()/2 + surface_fond_user_co.get_width() - taille_icone[0] - 5,h_origine/2 - surface_fond_user_co.get_height()/2 + 5)
                rect_icone_reglage = pygame.Rect(*pos_icone_reglage,*icone_reglage.get_size())
                rect_postimg.y = y_photo2 + size_grand[1] + 160
                rect_maketuto.y = rect_postimg.y
                btn_disconnect.y = rect_maketuto.bottom +60
                element_page_user = True
                x_fond_2 = w_origine/2 - surface_fond_user_co_back.get_width()/2
                x_fond_1 = w_origine/2 - surface_fond_user_co.get_width()/2
                y_fond_2 = h_origine/2 - surface_fond_user_co_back.get_height()/2
                y_fond_1 = h_origine/2 - surface_fond_user_co.get_height()/2
            surface_fond_user_co.fill((0,0,0,0))
            surface_fond_user_co_back.fill((0,0,0,0))
            pygame.draw.rect(surface_fond_user_co_back, palette_couleur.Noir, (0,0,surface_fond_user_co_back.get_width(),
                                                                                surface_fond_user_co_back.get_height()),0,20)
            pygame.draw.rect(surface_fond_user_co, palette_couleur.Gris_clair, (0,0,surface_fond_user_co.get_width(),surface_fond_user_co.get_height()),0,20)
            
            screen.blit(surface_fond_user_co_back,
                        (x_fond_2, y_fond_2))
            screen.blit(surface_fond_user_co,
                        (x_fond_1, y_fond_1))
            #Informer l'utilisateur qu'il ne doit pas quitter
            if message_photo_profil:
                draw_text(message_photo_profil,font = font_paragraphe,importer = True,center_multi_line=True,color = (255,255,255))
                if temoin_processus_fini_pp[0] == True:
                    message_photo_profil = ""
                    temoin_processus_fini_pp[0] = False
            color_btn1 =  (255,255,255) if not rect_postimg.collidepoint(mouse) else palette_couleur.Noir
            color_btn2 =  (255,255,255) if not rect_maketuto.collidepoint(mouse) else  palette_couleur.Noir
            pygame.draw.rect(btn_postimg,palette_couleur.Bleu,(0,0,btn_postimg.get_width(),btn_postimg.get_height()),0,20)
            pygame.draw.rect(btn_maketuto,palette_couleur.Bleu,(0,0,btn_maketuto.get_width(),btn_maketuto.get_height()),0,20)
            surface_ombre = pygame.Surface((btn_postimg.get_width() + 10, btn_postimg.get_height() + 10), pygame.SRCALPHA)
            surface_ombre.fill((0,0,0,0))
            draw_text(contener = btn_postimg,font = font_paragraphe, size = size_for_case, importer = True, center_multi_line_y=True, center_multi_line=True,
                    text = text_postimg, color = (255,255,255))
            draw_text(contener = btn_maketuto,font = font_paragraphe, size = size_for_case, importer = True, center_multi_line_y=True, center_multi_line=True,
                    text = text_maketuto, color = (255,255,255))
            pygame.draw.rect(btn_postimg,color_btn1,(0,0,btn_postimg.get_width(),btn_postimg.get_height()),1,20)
            pygame.draw.rect(btn_maketuto,color_btn2,(0,0,btn_maketuto.get_width(),btn_maketuto.get_height()),1,20)
            #animation pour le survol de post_img ou make_tuto. J'hesite a la supp
            """if rect_postimg.collidepoint(mouse):                
                x_effet1 += 1 if x_effet1 < 4 else 0
                y_effet1 += 1 if y_effet1 < 4 else 0
                intensiter_effet += 255/4 if intensiter_effet < 255 else 0
                pygame.draw.rect(surface_ombre,(0,0,200,intensiter_effet),(x_effet1,y_effet1,btn_postimg.get_width(),btn_postimg.get_height()),0,20)
                screen.blit(surface_ombre,(
                    w_origine/2 - 20 - btn_postimg.get_width(), y_photo2 + size_grand[1] + 150
                ))
            else:
                x_effet1 -= 2 if x_effet1  > 0 else 0
                y_effet1 -= 2 if y_effet1 > 0 else 0
                intensiter_effet -= 255/5 if intensiter_effet < 0 else 0
                pygame.draw.rect(surface_ombre,(0,0,200,intensiter_effet),(x_effet1,y_effet1,btn_postimg.get_width(),btn_postimg.get_height()),0,20)
                if x_effet1 > 0:
                    screen.blit(surface_ombre,(
                        w_origine/2 - 20 - btn_postimg.get_width(), y_photo2 + size_grand[1] + 150
                    ))  
            if rect_maketuto.collidepoint(mouse):                
                x_effet2 += 1 if x_effet2 < 4 else 0
                y_effet2 += 1 if y_effet2 < 4 else 0
                intensiter_effet += 255/4 if intensiter_effet < 255 else 0
                pygame.draw.rect(surface_ombre2,(0,0,200,intensiter_effet),(x_effet2,y_effet2,btn_postimg.get_width(),btn_postimg.get_height()),0,20)
                screen.blit(surface_ombre2,(
                w_origine/2 + 20, y_photo2 + size_grand[1] + 150
                ))                
            else:
                x_effet2 -= 2 if x_effet2  > 0 else 0
                y_effet2 -= 2 if y_effet2 > 0 else 0
                intensiter_effet -= 255/5 if intensiter_effet < 0 else 0
                pygame.draw.rect(surface_ombre2,(0,0,200,intensiter_effet),(x_effet2,y_effet2,btn_postimg.get_width(),btn_postimg.get_height()),0,20)
                if x_effet2 > 0:
                    screen.blit(surface_ombre2,(
                        w_origine/2 + 20, y_photo2 + size_grand[1] + 150
                    ))    """        
            screen.blit(btn_postimg,rect_postimg)
            screen.blit(btn_maketuto,rect_maketuto)
            #image_pp = pygame.transform.smoothscale(image_pp,size_grand)
            rect_editer_photo.x = x_photo2 + size_grand[0]/2 - font_20.size(text_edit)[0]/2
            rect_editer_photo.y = y_photo2 + size_grand[1] + 5
            pygame.draw.rect(screen,palette_couleur.Bleu,btn_disconnect,0,20)
            couleur_contour_disconnect = (255,255,255) if not btn_disconnect.collidepoint(mouse) else (0,0,0)
            pygame.draw.rect(screen,couleur_contour_disconnect,btn_disconnect,1,20)
            draw_text("Déconnexion", x = btn_disconnect.x + btn_disconnect.w/2 - font(font_paragraphe,size_deconnexion,True).size("Déconnexion")[0]/2, y = btn_disconnect.y + btn_disconnect.h/2 - font(font_paragraphe,size_deconnexion,True).size("Déconnexion")[1]/2,
                    font = font_paragraphe, importer = True, color = blanc, size = size_deconnexion)
            if user.rect_pp == None:
                pygame.draw.ellipse(surf2g, (255, 255, 255), (0,0,*size_grand))            
                surf3g.blit(surf2g, (0, 0))
                surf3g.blit(image_pp, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
                screen.blit(surf3g, (x_photo2, y_photo2))                
            else:
                #blit pp
                screen.blit(surf_image2,(x_photo2,y_photo2))
            #masque fait pour detecter la collision très précisément
            #mask = pygame.mask.from_surface(surf_image2)
            #pygame.draw.ellipse(screen,color_bordure_image,(x_photo2,y_photo2,size_grand[0],size_grand[1]),1)
            
            fake_screen  =  screen.copy()
            #pour eviter l'erreur que les mask_x et mask_y deborde du mask car l'ellipse dessiner est aggrandi intentionnellement a cause du
            #dessin d'un rond merdique de pygame
            ellipse = pygame.draw.circle(fake_screen,(0,0,0,0),(x_photo2 + size_grand[0]/2 ,y_photo2+size_grand[0]/2),size_grand[0]/2,1)
            x1,y1 = x_photo2 + size_grand[0]/2,y_photo2+size_grand[0]/2
            radius = size_grand[0]/2
            
            if ellipse.collidepoint(mouse):
                mask_x = mouse[0] - ellipse.left
                mask_y = mouse[1] - ellipse.top   
                x2,y2 = mouse[0],mouse[1]
                X = x2 - x1
                Y = y2 - y1
                
                distance_to_mouse = math.sqrt(X**2+Y**2)
                if distance_to_mouse <= radius:
                    collide_image = True
                    color_bordure_image = palette_couleur.Bleu
                else:
                    collide_image =False
                    color_bordure_image = (0,0,0)
            else:
                color_bordure_image = (0,0,0)
                collide_image = False                                 
            text_nom_prenom =  user.nom + " " + user.prenom
            text_pseudo = user.pseudo
            tuto_poster = user.tuto_transmis
            annonce_poster = user.annonce_transmis
            color_edit = (255,255,255) if not rect_editer_photo.collidepoint(mouse) else palette_couleur.Bleu
            draw_text(text_edit,
                    color = color_edit, 
                    x = x_photo2 + size_grand[0]/2 - font_20.size(text_edit)[0]/2
                    ,y = y_photo2 + size_grand[1] + 5, size = 20,
                    importer = True, font = font_paragraphe)
            draw_text(text_nom_prenom,
                    color = (255,255,255), 
                    x = x_photo2 + size_grand[0]/2 - font_30.size(text_nom_prenom)[0]/2
                    ,y = y_photo2 + size_grand[1] + 5 + font_20.size(text_edit)[1], size = 30,
                    importer = True, font = font_paragraphe)
            draw_text("~ " + text_pseudo + " ~",
                    color = palette_couleur.Bleu_clair, 
                    x = x_photo2 + size_grand[0]/2 - font(font_paragraphe,40,True).size("~ " + text_pseudo + " ~")[0]/2
                    ,y = y_photo2 + size_grand[1] + 5 + font_20.size(text_edit)[1] + font_30.size(text_nom_prenom)[1], size = 40,
                    importer = True, font = font_paragraphe)
            draw_text(f"Vous avez postez {tuto_poster} tutoriel.s | {annonce_poster} demande.s de tutos",
                    color = (255,255,255), 
                    x = x_photo2 + size_grand[0]/2 - font_30.size(f"Vous avez postez {tuto_poster} tutoriel.s | {annonce_poster} demande.s de tutos")[0]/2
                    ,y = y_photo2 + size_grand[1] + 5 + font_20.size(text_edit)[1] + font_30.size(text_nom_prenom)[1] + font(font_paragraphe,40,True).size("~ " + text_pseudo + " ~")[1],
                    size = 30,
                    importer = True, font = font_paragraphe)    
            screen.blit(icone_reglage,pos_icone_reglage)
            if rect_icone_reglage.collidepoint(mouse):
                if user.categorie != None and  user.categorie not in  message:
                    categorie = user.categorie if user.categorie != None else "Aucune"
                    try:
                        membre_categorie = " " if user.categorie == None else f' Membre de cette catégorie : {dict_categorie[user.categorie]["membre"]}' 
                    except:
                        membre_categorie = " "
                    message = f"Actuellement votre catégorie est : {categorie}. Avoir une catégorie de compte permettra a l'application de vous mettre par défaut des tutos dans l'espace menu."\
                    + membre_categorie
                    size = 30
                    coupage,line,y = make_line(message,font(TNN,size,True),surface_message_info.get_width() -5)
                    while y > surface_message_info.get_height():
                        size -= 2
                        coupage,line,y = make_line(message,font(TNN,size,True),surface_message_info.get_width() -5)
                    pygame.draw.rect(surface_message_info,palette_couleur.Noir,(0,0,*surface_message_info.get_size()),0,20)
                    all_text = decoupe_text(coupage,line,message)
                    for i in range(len(all_text)):
                        draw_text(all_text[i], font = TNN, size = size ,color = blanc, center_multi_line= True,contener = surface_message_info,importer = True, y = 5 + (size*i))
                screen.blit(surface_message_info,(x_fond_2 + surface_fond_user_co_back.get_width() + 20,y_fond_2))
            screen.blit(icone_aide,rect_aide)
        screen.blit(image_retour,rect_goback)
        screen.blit(surface_status_co,pos_surface_status_co)
        pygame.display.flip()
        last_screen = screen.copy()
        if go_back:
            break

        
        
def request():
    menu(2)

def input_popup():
    """Fonction permettant d'image_userr une input en popup

    Returns:
        bool | str: retourne False si l'input n'a pas été validez, le texte de l'input sinon
    """
    pygame.display.flip()
    global continuer
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
    while continuer:
        Clock.tick(120)
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
        if cancel or finished:
            break
    if finished:
        return text_input.strip()
    
    return False

fond_ecran =  palette_couleur.Gris
bleu_s =(106,178,202)

continuer = True
#variable qui va permettre de savoir si l'utilisateur est connecté
connect = False
##proeccessus de verification si l'uti
chemin_image_logo_app = os.path.join("Image","Icone_accueil.png")
image_logo_app = pygame.image.load(chemin_image_logo_app)
width_logo,height_logo = image_logo_app.get_width(),image_logo_app.get_height()
r = (w_origine/2)/width_logo
image_logo_app = pygame.transform.smoothscale(image_logo_app,(width_logo * r,height_logo*r))
screen.blit(image_logo_app,(w_origine/2 - (width_logo*r)/2,h_origine/2 - (height_logo*r)/2))
pygame.display.update()
with open(os.path.join("img_base","photo_profil_user.png"),"rb") as fichier:
        pp_base = fichier.read()
size_grand = (h_origine * (1-72/100),)*2 #diminution de 75% de la taille originel
#processus de verification de si l'utilisateur est connecter, si oui, connexion au compte

with open(os.path.join("Ressource", "compte_connecter.txt"), "r+") as fichier:
    contenu = fichier.read().splitlines()
    last_screen = screen.copy()
    fondd_ecran = (0,0,0)
    if contenu:
        animation_demarrage_application.start_anime(last_screen,20)
        animation_demarrage_application.texte = "Récupération des catégories"
        try:
            recup_categorie = Gerer_requete.take_categorie() #recuperer le nom de toutes les catégories
        
            dict_categorie = Gerer_requete.update_categorie_member()     
        except noConnection:
            recup_categorie = None
            dialog.message("Une erreur de connexion a eu lieu !",last_screen,title="Erreur")
        except Exception as e :
            recup_categorie = None
            dialog.message("Une erreur est survenue ! ", last_screen,title="Erreur")
        else:
            pseudo = contenu[0]
            mdp = contenu[1]
            try:
                animation_demarrage_application.texte = "Connexion a votre compte"
                user = User.log_user(pseudo,mdp)
            except userNonCharger:
                animation_demarrage_application.stop_anime()
                dialog.message("Connection inachevé, il semblerait que le mot de passe ne corresponde pas !\n(Avez vous jouez dans les fichiers de l'appli ?)",last_screen,title="Erreur")
                animation_demarrage_application.start_anime(last_screen,20)
            except noConnection:
                animation_demarrage_application.stop_anime()
                dialog.message("Une erreur de connexion a eu lieu !",last_screen,title="Erreur")
                animation_demarrage_application.start_anime(last_screen,20)
            except UserNotExist:
                animation_demarrage_application.stop_anime()
                dialog.message("Ce compte n'existe pas, il se peut que vous ayez été bannis",last_screen,title="Erreur")
                animation_demarrage_application.start_anime(last_screen,20)
            else:
                animation_demarrage_application.texte = "Récupération de votre photo de profil"
                chemin_pp = os.path.join("image_user","photo_profil_user.png") 
                connect = True
                creer_compte = False
                with open(chemin_pp,"wb") as fichier:
                    if user.photo_profil != pp_base:
                        fichier.write(user.photo_profil)
                    else:
                        fichier.write(pp_base)
                #pygame.time.delay(2000)
                if user.photo_profil == pp_base:
                    image_pp = pygame.image.load(chemin_pp)
                    image_pp = pygame.transform.smoothscale(image_pp,size_grand)
                else:
                    #processus de reconstruction de la pdp car sinon si on aggrandi juste la surface surf_image elle est flou
                    animation_demarrage_application.texte = "Reconstruction de votre photo de profil"
                    img_ = pygame.image.load(chemin_pp).convert_alpha()
                    old_width, old_height = img_.get_size()
                    # Définir la nouvelle largeur (ou hauteur)
                    new_width = 500
                    # Calculer la nouvelle hauteur (ou largeur) pour conserver le rapport d'aspect (produit en croix)
                    new_height = int(old_height * new_width / old_width)
                    # Redimensionner l'image
                    img_ = pygame.transform.smoothscale(img_, (new_width,new_height))
                    rect_pp = user.rect_pp
                    if isinstance(rect_pp,pygame.Rect):
                        rect_pp = Gerer_requete.separe_rect(user.rect_pp)
                    if rect_pp != None:
                        rect_pp = rect_pp.split(",")
                        rect_pp = [int(i) for i in rect_pp]
                        rect_pp = pygame.Rect(rect_pp)
                    else:
                        rect_pp = pygame.Rect(0,0,*img_.get_size())
                    surf_image2 = resizeImage.rendre_transparent(img_,rect_pp,0)
                    surf_image2 = pygame.transform.smoothscale(surf_image2, size_grand)
                creer_compte = False
                zone = 1
    else:
        animation_demarrage_application.start_anime(last_screen) 
        try:
            recup_categorie = Gerer_requete.take_categorie()
            dict_categorie = Gerer_requete.update_categorie_member()     
        except:
            recup_categorie = None
            animation_demarrage_application.stop_anime() 
            dialog.message("Une erreur de connexion a eu lieu !",last_screen)
            animation_demarrage_application.start_anime(last_screen)
    try:
        animation_demarrage_application.texte = "Vérification des mises à jours"
        Gerer_requete.verifier_version_app()
        Gerer_requete.verifier_version_doc_aide()
        Gerer_requete.verifier_version_doc_info()
        Gerer_requete.verifier_version_doc_aide_compte()
        Gerer_requete.verifier_version_doc_info_annonce()
    except Exception as e:
        animation_demarrage_application.stop_anime()  
        dialog.message(f"La vérification des mises à jours a echoué\nerreur : '{e}'",last_screen,title="Erreur")
        
animation_demarrage_application.stop_anime()
comic_sans_ms = pygame.font.SysFont("Comic Sans Ms", 20)
input_apple = pygame.font.Font(apple_titre,40)

blanc = (255,255,255)
noir = (0,0,0)
proposition = ["MENU","COMPTE","ANNONCE"]

etat = ["alpha","alpha","alpha"]
size_box_grand_w = w_origine/5.5
size_box_grand_h = h_origine/8
size_box_w = size_box_grand_w * (1-30/100)
size_box_h = size_box_grand_h * (1-20/100)
millieu_w = (w_origine/2) - size_box_w/2
millieu_h = (h_origine/2) - size_box_h/2
pos = [[w_origine/2 - size_box_grand_w/2, h_origine/2 - size_box_grand_h/2 - size_box_h - 30],
    [w_origine/2 - size_box_w/2, h_origine/2 - size_box_h/2],
    [w_origine/2 - size_box_w/2, h_origine/2 - size_box_h/2 + size_box_h +20]]
for liste in pos:
    liste[1] += 100
rect_dispo = []
is_on = [False]*3
color_text = [(255,255,255)]*3
text_choose = ""
droite = [True] * 3
reference = w_origine
accueil_complement = "Bienvenue sur"
accueil = "SYLVER.SERVICE"
font_accueil = pygame.font.SysFont("Comic Sans Ms", 40)
fond_nav = pygame.Surface((w_origine,100))
info = pygame.Rect(w_origine - taille_icone[0] - 5, 15, *taille_icone)
icone_aide = pygame.image.load("Image/icone_interrogation.png")
icone_aide = pygame.transform.smoothscale(icone_aide,(info.w,info.h))
font_chivo = font(chivo_titre,72,True)
font_chivo_14 = font(chivo_titre,14,True)
size_for_title = 72
rect_pas_depasser = pygame.Rect(0,0,size_box_w * (1-40/100),0)
size_text_case = verification_size(rect_pas_depasser,TNN,50,"Annonce",True)
rect_pas_depasser = pygame.Rect(0,0,size_box_grand_w * (1-40/100),0)
size_text_case_grand = verification_size(rect_pas_depasser,TNN,50,"Annonce",True)
all_size = [size_text_case_grand,size_text_case,size_text_case]
text_user_pas_co = "Salut :) Connecte toi se sera mieux ! "

def title(text, size = size_for_title, color = blanc,importer = True, y = 5):
    """Fonction permettant de mettre un titre

    Args:
        text (str): Texte en titre
        size (str, optional): taille du texte. Defaults to size_for_title.
        color (list, optional): couleur du texte. Defaults to blanc.
        importer (bool, optional): Indique si la police est importer ou non. Defaults to True.
    """
    font_ = font(chivo_titre,size,True)
    draw_text(text, size = size,color = palette_couleur.Bleu, x = (w_origine/2 - font_.size(text)[0]/2), y = y,importer = importer, font = chivo_titre)


clock = pygame.time.Clock()

def gestion_event():
    """
        Gère l'évènement pour quitter l'app
    """
    global continuer,connection_principale,in_event
    while continuer:
        try:
            if keyboard.is_pressed("Escape"):
                continuer = not User.confirm_close()      
        except:
            continue
        
        time.sleep(0.1)
    print("bye")
    
rect_choose = pygame.Surface((size_box_w,size_box_h), pygame.SRCALPHA)
rect_grand_choose = pygame.Surface((size_box_grand_w,size_box_grand_h), pygame.SRCALPHA)
rect_dispo = [pygame.Rect(pos[0][0],pos[0][1],size_box_grand_w,size_box_grand_h),
            pygame.Rect(pos[1][0],pos[1][1],size_box_w,size_box_h),
            pygame.Rect(pos[2][0],pos[2][1],size_box_w,size_box_h)
            ]
clock = pygame.time.Clock()
status_connection_started = False
surface_status_co = pygame.Surface((50,50), pygame.SRCALPHA)
surface_status_co.fill((0,0,0,0))
pos_surface_status_co = (w_origine-10,h_origine-10)
size_for_accueil = verification_size(pygame.Rect(0,0,w_origine * (1-60/100),0),chivo_titre,125,accueil,True)
#Boucle principale de l'accueil

dict_categorie = {}
def update_categorie():
    """Fonction permettant de mettre a jour le nombre de participant dans les catégories, ainsi que récuperer leur nom"""
    global dict_categorie
    global recup_categorie
    while continuer:
        try:
            dict_categorie = Gerer_requete.update_categorie_member()
            recup_categorie = Gerer_requete.take_categorie() #recuperer le nom de toutes les catégories
            Gerer_requete.update_categorie_data()
            time.sleep(20)
        except:
            pass

def affiche_photo_profil(last_screen,Photo_pp_tiers = False,pseudo = None):
    """Fonction permettant d'image_userr la photo de profil de l'utilisateur ou d'un utilisateur
    
    Args:
        last_screen (pygame.Surface): Dernier écran a image_userr
        Photo_pp_tiers (bool): Si False, c'est que c'est la photo de profil de l'utilisateur qu'il faut image_userr, sinon c'est celle d'un
        utilisateur tiers
    """
    screen.blit(last_screen,(0,0))
    go_back = False
    global continuer
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
    draw_text(text,apple_titre,blanc,w_origine/2 - font(apple_titre,20,True).size(text)[0]/2,h_origine - font(apple_titre,20,True).size(text)[1] - 10,
            size = size,importer = True,ombre = True)
    while continuer:
        Clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                go_back = True
        surface_photo.fill((0,0,0,0))
        pygame.draw.rect(surface_photo,palette_couleur.Noir,(0,0,*surface_photo.get_size()),0,60)
        surface_photo.blit(photo_pp,position_photo_pp)
        screen.blit(surface_photo,position_surface_photo_pp)
        if go_back:
            break
        pygame.display.flip()
        
threading.Thread(target=update_categorie,daemon = True).start()
threading.Thread(target=gestion_event,daemon=True).start()

size_pp_user = (80,80)
x_pp,y_pp = 20,fond_nav.get_height()/2 - size_pp_user[1]/2
rect_photo_profil_user = pygame.Rect(x_pp,y_pp,*size_pp_user)
while continuer:
    #contact()
    Clock.tick(120)
    fps = Clock.get_fps()
    screen.fill(fond_ecran)
    if connect:
        text_user_co = f"Salut {user.pseudo} ravis de te voir :)"
        draw_text(text_user_co, x = w_origine/2 - font(chivo_titre,36,True).size(text_user_co)[0]/2,
                y = fond_nav.get_height() + 10, font = chivo_titre, color = blanc,
                size = 36, importer = True)
    else:
        draw_text(text_user_pas_co, x = w_origine/2 - font(chivo_titre,36,True).size(text_user_pas_co)[0]/2,
                y = fond_nav.get_height() + 10, font = chivo_titre, color = blanc,
                size = 36, importer = True)
    mouse = pygame.mouse.get_pos()    
    fond_nav.fill(palette_couleur.Noir)
    screen.blit(fond_nav,(0,0))
    #pp user
    if connect:
        
        if user.photo_profil == pp_base:            
            surf1 = pygame.Surface(size_pp_user,pygame.SRCALPHA)
            surf2 = pygame.Surface(size_pp_user,pygame.SRCALPHA)
            pygame.draw.ellipse(surf1, (255, 255, 255), (0,0,*size_pp_user))
            surf2.blit(surf1,(0,0))
            photo_profil_user = pygame.transform.smoothscale(image_pp,size_pp_user)
            surf2.blit(photo_profil_user, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            screen.blit(surf2,(x_pp,y_pp))
        else:
            image_pp_user = pygame.transform.smoothscale(surf_image2,size_pp_user)
            screen.blit(image_pp_user,(x_pp,y_pp))
        draw_text(user.pseudo, x = x_pp + size_pp_user[0] + 5, y = y_pp + size_pp_user[0]/2 - font(TNN,25,True).size(user.pseudo)[1]/2,
                color = (255,255,255),font = TNN, importer=True,size = 25)
    draw_text(accueil_complement, size = 14, color=blanc, x = w_origine/2 - font(chivo_titre,14,True).size(accueil_complement)[0]/2,
            y = 5, importer= True, font=chivo_titre)
    title(accueil, size = size_for_accueil, y = fond_nav.get_height()/2 - font(chivo_titre, size_for_accueil,True).size(accueil)[1]/2)
    try:
        for event in pygame.event.get():        
            if event.type == pygame.KEYDOWN:
                pass
            if rect_photo_profil_user.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and connect:
                affiche_photo_profil(last_screen)
            elif event.type == pygame.QUIT:
                continuer = False
            elif info.collidepoint(mouse):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    page_info()
            if len(rect_dispo) > 0:
                for index, rect in enumerate(rect_dispo):
                    if rect.collidepoint(mouse):
                        text_choose = proposition[index]
                        if etat[index] == "alpha":
                            is_on[index] = True                        
                        decal = 200
                        pos_souris_relat_souris = (mouse[0] - rect.x, mouse[1] - rect.y)
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            if text_choose == "MENU":
                                menu()
                            elif text_choose == "ANNONCE":
                                request()
                            else:
                                compte()
                    else:
                        is_on[index] = False
                        color_text[index] = blanc    
    except:
        pass
    date = datetime.datetime.today().strftime('%Hh%M')
    draw_text(date, size = 20, color = blanc, x = w_origine - 70, y = fond_nav.get_height() +10)
    screen.blit(icone_aide,info)
    
    draw_text(f"fps : {int(fps)}",x=10,y=fond_nav.get_height() + 10,color=(255,255,255))
    draw_text(f'VERSION : {os.environ.get("VERSION")}',x = 10, y = h_origine - 20,
            color = blanc,size =14, font = chivo_titre, importer = True)
    if not status_connection_started:
        status_connection(surface_status_co)
        status_connection_started = True
    screen.blit(surface_status_co,pos_surface_status_co)
    for index,elt in enumerate(proposition):
        if index != 0:
            rect = rect_choose
        else:
            rect = rect_grand_choose
        rect.fill((0,0,0,0))
        w,l = rect.get_size()
        color_bord = palette_couleur.Bleu if is_on[index] == False else palette_couleur.Noir
        pygame.draw.rect(rect,palette_couleur.Noir_clair,(0,0,w,l),0,20)
        pygame.draw.rect(rect,color_bord,(0,0,w,l),1,20)
        draw_text(proposition[index],contener = rect,color = color_text[index], x = rect.get_width()/2 - font(TNN,all_size[index],True).size(proposition[index])[0]/2,
                y = rect.get_height()/2 - font(TNN,all_size[index],True).size(proposition[index])[1]/2,size = all_size[index], font = TNN, importer = True)
        screen.blit(rect,pos[index])
    last_screen = screen.copy()
    
    pygame.display.flip()
pygame.quit()
sys.exit()
