
import pygame,os,datetime,string,sys,threading,keyboard,time,pyperclip
from Sylver_class_import import Color,Gerer_requete,User,noFileException, userNonCharger, noConnection,Animation
from Resize_image import AnnuleCropPhoto, resizeImage


#reglage de l'ecran
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.mixer.init()
pygame.display.init()
pygame.font.init()
pygame.key.set_repeat(200,50)
resolution = pygame.display.Info()
width = resolution.current_w
height = resolution.current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN | pygame.SCALED | pygame.HWSURFACE | pygame.DOUBLEBUF)
#class animation qui servira a declencher des chargement de deux maniere, soit a des periodes bloquante ou nonj
animation_chargement = Animation(screen)
animation_mise_en_ligne = Animation(screen, text_chargement="Mise en ligne")
animation_connection = Animation(screen, text_chargement = "Connection")
animation_ouverture = Animation(screen, text_chargement = "Ouverture")
palette_couleur = Color()

def draw_text(text, font = "Comic Sans Ms", color = (0,0,0), x = 0, y = 0,contener = screen,size = 20,importer = False, center_multi_line_y = False, ombre = False,center_multi_line = False):
    """
        dessiner un texte a une position donné
        :param 1: text qu'on veut dessiner
        :param 2: font qu'utilise le texte
        :param 3: couleur du texte
        :param 4: coordonne x ou le dessiner
        :param 5: coordonne y ou le dessiner
        :CU: arg 1 est un str, arg 2 est de type font.FONT ou font.SysFont, arg 3 est un rbg, arg 4 et 5 sont des int
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
            x = contener.get_rect()[2]/2 - font_.size(text)[0]/2
        if center_multi_line_y:
            y = contener.get_rect()[3]/2 - font_.size(text)[1] * len(all_text)/2
        if ombre:
            text_ = font_.render(str(text), True, (0,0,0))            
            contener.blit(text_, (x+1,y+(size+2)*enum))
        text_ = font_.render(str(text), True, color)
        contener.blit(text_, (x,y+(size + 2)*enum))        
       

def make_line(text : str,font : pygame.font,size_max : int):
    """Fonction permettant de faire le coupage d'un texte par rapport a son contenaire,
    renvoie le nombre de ligne du texte et ses zones de coupages en plus de sa hauteur

    Args:
        text (str): text que l'on choisi
        font (pygame.font): la police attribué a ce text
        size_max (int): la taille maximum a ne pas depasser

    Returns:
        _type_: _description_
    """
    coupage = [0]
    line = 1
    start = 0
    i = 0
    while i < len(text):
        size = font.size(text[start:i])[0]
        if size + 5 > size_max:
            w = -1
            while text[start:i][w] != " ":
                w -= 1
            i += w
            start = i
            coupage.append(start)
            line+=1
        i+=1
    y = 0
    for i in range(line):
        y = font.size(text)[1] + font.size(text)[1] * i
    return coupage,line,y

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
    """Fonction permmettant d'afficher un texte contenant plusieurs ligne grace a son coupage de texte

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
        
def ecrire_tuto(user : User):  
    """Fonction permettant a l'utilisateur décrire son tuto

    Args:
        user (User): Class representant les données de l'utilisateur
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
    surf_valider.fill((0,0,0,0))
    s_width = surf_valider.get_width()
    s_height = surf_valider.get_height()
    rect_valider = surf_valider.get_rect(x=w_origine - s_width - 30,
                                         y = h_origine - s_height - 20)    
    surf_ecrit = pygame.Surface((w_origine - 40, h_origine - 300 ), pygame.SRCALPHA)
    rect_titre = pygame.Rect(20,120,200,50)
    rect_surf_ecrit = pygame.Rect(20,200,surf_ecrit.get_width(),surf_ecrit.get_height())

    #peut etre remplacer par dess classes jsp
    dict_input = {
        "input_titre" : { "max" : 25,"x" : 10,"y" : rect_titre.h/2 - font(font_paragraphe,30,True).size("m")[1]/2,"surf" : surf_titre,"input" : ["Titre",],
                         "zone_ecrit" : 0,"can_do_multiple_lines" : False, "base" : "Titre", "active" : False,"rect" : rect_titre, "time": 0, "take_time" : False,
                         "coupage" : 0,"all_size" : 0,"can_write" : True},
        
        "input_text" : {"coupage" : 0, "max" : 2000,"x" : 20,"y" : 30 ,"surf" : surf_ecrit, "input" : ["Contenu",], "zone_ecrit" : 0,
                        "can_do_multiple_lines" : True,"can_write" : True, "base" : "Contenu", "all_size" : 0,"active" : False,"rect" : rect_surf_ecrit,"time": 0, "take_time" : False}
    }
    menos = False #indique si le dernier effacement a supprimer uneligne
    rect_goback = pygame.Rect(5,5,50,50)
    image_retour = pygame.image.load("Image/Icone_retour.png")
    image_retour = pygame.transform.smoothscale(image_retour,(rect_goback.w,rect_goback.h))
    go_back = False
    #boucle principale
    while continuer:
        screen.fill((100,100,100))
        fond_nav.fill((0,0,0))  
        mouse = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        #boucle evenementielle
        for event in pygame.event.get():
            if rect_goback.collidepoint(mouse):
                if mouse_click:
                    go_back = True
            ### Validation de l'input => mettre le tuto en bdd ###
            if rect_valider.collidepoint(mouse):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    #.strip() utilisé pour supprimer les espaces au debut et a la fin
                    text_pour_tuto = ' '.join(dict_input["input_text"]["input"])
                    text_pour_tuto = text_pour_tuto.strip()
                    titre = ''.join(dict_input["input_titre"]["input"])
                    titre = titre.strip()
                    try:
                        animation_mise_en_ligne.start_anime(last_screen,(100,100,100))
                        Gerer_requete(user).save_tuto(None,text_pour_tuto,titre)
                        animation_mise_en_ligne.stop_anime()
                        go_back = True 
                    except noConnection:
                        Gerer_requete.connection_failed()
                        
                    except Exception as e:
                        Gerer_requete.error_occured()
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
                        if event.key == pygame.K_UP and elt["can_do_multiple_lines"]:
                            #changer de zone d'ecriture vers le haut
                            elt["zone_ecrit"] -= 1 if len(elt["input"]) > 1 else 0
                        
                        elif event.key == pygame.K_DOWN and elt["can_do_multiple_lines"] and elt["can_write"]:
                            elt["input"][elt["zone_ecrit"]] += "\n"
                            elt["input"].append("")
                            #ajouter une zone d'ecriture
                            elt["zone_ecrit"]+=1
                            elt["input"][elt["zone_ecrit"]] = elt["input"][elt["zone_ecrit"]].strip()                           
                                                                               
                        elif event.key == pygame.K_SPACE and elt["can_write"]:
                            if elt["all_size"] < elt["max"]:
                                elt["input"][elt["zone_ecrit"]] += " "
                                elt["all_size"] += 1
                                
                        elif event.key == pygame.K_BACKSPACE:
                            if elt["input"][elt["zone_ecrit"]] != "":
                                elt["input"][elt["zone_ecrit"]] = elt["input"][elt["zone_ecrit"]][:-1]
                                elt["all_size"] -= 1
                            else:
                                if elt["can_do_multiple_lines"]:
                                    if len(elt["input"]) > 1:
                                        #supprimer la ligne
                                        del(elt["input"][elt["zone_ecrit"]])
                                        elt["zone_ecrit"] -= 1 
                                        menos = True #indique que une ligne a été sup                                   
                        elif event.key == pygame.K_RETURN and elt["can_do_multiple_lines"] and elt["can_write"]:
                            elt["input"][elt["zone_ecrit"]] += "\n"
                            elt["input"].append("")
                            #ajouter une zone d'ecriture
                            elt["zone_ecrit"]+=1
                            elt["input"][elt["zone_ecrit"]] = elt["input"][elt["zone_ecrit"]].strip()
                        elif event.key == pygame.K_ESCAPE:
                            pass
                        else:
                            if elt["all_size"] < elt["max"] and elt["can_write"]:
                                if event.unicode.isprintable() and event.unicode != "":
                                    elt["input"][elt["zone_ecrit"]] += event.unicode
                                    elt["all_size"] += 1
                            
                        if len(elt["input"][elt["zone_ecrit"]]) > 0 and not menos and elt["can_do_multiple_lines"]:
                            if font(font_paragraphe,30,True).size(elt["input"][elt["zone_ecrit"]])[0] >= surf_ecrit.get_width() - 40:
                                if elt["y"] * len(elt["input"]) + 40 < surf_ecrit.get_height():
                                    elt["input"].append("")
                                    elt["zone_ecrit"] +=1
                                else:
                                    elt["can_write"] = False
                                
                        elif elt["can_do_multiple_lines"] == False:
                             if elt["all_size"] < elt["max"]:
                                if (font(font_paragraphe,30,True).size(elt["input"][elt["zone_ecrit"]][elt["coupage"]:])[0] >= elt["surf"].get_width() - 40) or elt["coupage"] > 0:
                                    elt["coupage"] += 1 if event.key != pygame.K_BACKSPACE else -1
                                    if elt["coupage"] <= 0:
                                        elt["coupage"] = 0
                        menos = False                  
        surf_valider.fill((0,0,0,0))
        surf_titre.fill((0,0,0,0))
        pygame.draw.rect(surf_titre,blanc,(0,0,*surf_titre.get_size()),0,20)
        pygame.draw.rect(screen,palette_couleur.fond_contenaire_page_tuto,(rect_titre[0] -10,
                                           rect_titre[1] -10
                                           ,surf_titre.get_width() + 20, surf_titre.get_height() +20),0,20)      
        surf_ecrit.fill((255,255,255,0))
        pygame.draw.rect(surf_ecrit,blanc,(0,0,surf_ecrit.get_width(),surf_ecrit.get_height()),0,20)
        pygame.draw.rect(screen,palette_couleur.fond_contenaire_page_tuto,(rect_surf_ecrit[0]-10,rect_surf_ecrit[1]-10,surf_ecrit.get_width() + 20,surf_ecrit.get_height() +20),0,20)
        color_valider = (0,255,0) if  rect_valider.collidepoint(mouse) else (0,0,0)
        pygame.draw.rect(surf_valider,color_valider,(0,0,*rect_valider[2:4]),1)
        draw_text(text = "Valider", contener = surf_valider,x= s_width/2 - font40.size("valider")[0]/2, font = font_paragraphe, importer=True, size = 40)       
        print(dict_input["input_text"]["all_size"])
        for keys,elt in dict_input.items():
            for enum,i in enumerate(elt["input"]):
                #ecrire tout les lignes dans all_input
                if keys == "input_titre":
                    add = 1
                else:
                    add = 0
                draw_text(i[elt["coupage"]:],importer=True,size = 30,contener=elt["surf"], x = elt["x"], y = elt["y"]*(enum+add), font=font_paragraphe)
            if elt["active"]:
                add = 1 if keys == "input_titre" else 0
                elt["surf"].blit(barre_input, (elt["x"] + font(font_paragraphe,30,True).size(elt["input"][elt["zone_ecrit"]][elt["coupage"]:])[0], 2 + elt["y"] * (elt["zone_ecrit"]+add))) #le y le met a la position du texte adapter en fonction de zone_ecrit
        screen.blit(surf_titre,(rect_titre[0],rect_titre[1]))
        screen.blit(surf_valider,(rect_valider[0],rect_valider[1]))
        screen.blit(surf_ecrit,(rect_surf_ecrit[0],rect_surf_ecrit[1]))
        screen.blit(fond_nav,(0,0))
        screen.blit(image_retour,rect_goback) 
        title(f"Ecrivez ici votre tutoriel {user.pseudo}")
        if go_back:
            break
        last_screen = screen.copy()
        pygame.display.flip()
        
def page_info(id_ = 0,text = "",nom_projet = "",auteur = "",date : datetime.datetime = None, id_tuto : int = None):
    """Fonction permettant d'afficher un texte au sujet de Sylver_Service, cette fonction sert aussi a afficher un tuto

    Args:
        id_ (int): Id permettant d'identifier dans quel but est utiliser la fonctio . Defaults to 0.
        text (str, optional): texte du tuto a afficher dans la fonction. Defaults to "".
        nom_projet (str, optional): Le nom du tuto a afficher. Defaults to "".
        auteur (str, optional): Le nom de l'auteur du tuto. Defaults to "".
        date (datetime.datetime, optional): La date de transmission du tuto. Defaults to None.
        id_tuto (int, optional): Id du tuto selectionner. Defaults to None.
    """
    global continuer
    global fond_nav
    rect_goback = pygame.Rect(5,5,50,50)
    image_retour = pygame.image.load("Image/Icone_retour.png")
    image_retour = pygame.transform.smoothscale(image_retour,(rect_goback.w,rect_goback.h))
    go_back = False
    width = w_origine - 50
    height = h_origine - 200
    surface_ecriture = pygame.Surface((width, height), pygame.SRCALPHA)
    text_title = "A quoi sert Sylver_Service ?"
    if id_ > 1:
        date = date.strftime("%d/%m/%Y")
        date_save = date
        date = f"posté le : {date}"
        date_actuelle = datetime.datetime.now()
        date_actuelle = date_actuelle.strftime("%d/%m/%Y")
        if date_actuelle == date_save:
            date = "posté aujourd'hui"
        
        text_title = f"{nom_projet.upper()} | par  {auteur}"
        
        text_info = text
    if id_ == 0:
        with open("./Ressource/fichier_info.txt", "r+") as fichier:
            text_info = fichier.read().replace("\n"," ")
        text_info = text_info.replace("Ã©","é")
        text_info = text_info.replace("Ã¨","è")
        text_info = text_info.replace("Ãª","ê")
    size_max = width
    i = 0
    font_paragraphe = apple_titre
    font_40 = pygame.font.Font(font_paragraphe, 40)
    font_20 = pygame.font.Font(font_paragraphe, 20)
    coupage,line,heigth_text = make_line(text = text_info, font = font(font_paragraphe,30,True), size_max= size_max)
    all_text = decoupe_text(coupage,line,text_info)
    text_signalement = "Signaler"
    surface_signalement = pygame.Surface(( font(font_paragraphe,30,True).size(text_signalement)[0] + 10, 40), pygame.SRCALPHA)
    rect_signalement  = surface_signalement.get_rect( x = w_origine - surface_signalement.get_width() - 10,
                                                      y = 50)
    moitier_text = []
    for i in range(len(all_text)):
        moitier_text.append(font_40.size(all_text[i])[0]/2)
    while continuer:
        mouse = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        screen.fill((100,100,100))
        surface_ecriture.fill((255,255,255,0))
        surface_signalement.fill((0,0,0,0))
        pygame.draw.rect(surface_signalement,palette_couleur.fond_case_login,(0,0,surface_signalement.get_width(),surface_signalement.get_height()),0,20)
        pygame.draw.rect(surface_signalement,(0,0,102),(0,0,surface_signalement.get_width(),surface_signalement.get_height()),1,20)
        pygame.draw.rect(screen,palette_couleur.fond_contenaire_page_tuto,(10,120,width + 30, height + 60),0,20)
        pygame.draw.rect(surface_ecriture,blanc,(0,0,width,height),0,20)
        for event in pygame.event.get():            
            if event.type == pygame.QUIT:
                continuer = False
                break
            if rect_goback.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                go_back = True
        if not "\n" in text_info:
            for i in range(line):
                draw_text(all_text[i], color = (0,0,0), x = 10, y =20 + 35*i, size = 30, contener = surface_ecriture, font = font_paragraphe, importer = True)
        else:
            draw_text(text_info, color = (0,0,0),x = 10,y = 35,
                       size = 30, contener = surface_ecriture, font = font_paragraphe, importer = True)

        #pygame.draw.rect(surface_ecriture, (255,0,0),(0,height/2,width,2))
        fond_nav.fill(palette_couleur.fond_bar_de_navigation)
                         
        screen.blit(fond_nav,(0,0))
        screen.blit(surface_signalement,(rect_signalement[0],rect_signalement[1]))
        screen.blit(image_retour,rect_goback)
        title(text_title, size = 40)
        if id_ > 1:
            draw_text(date, x = w_origine - font_20.size(str(date))[0] - 10,y = 10, font = font_paragraphe, color = (255,255,255),importer = True)
        if go_back:
            break
        screen.blit(surface_ecriture, (25,150))
        pygame.display.flip()
        
        

def menu():
    """Fonction affichant le menu recherche de l'application"""
    #ecrire_tuto(None)
    global display       
    global processing
    #savoir quand la recherche est en cours
    processing = False             
    display = False
    global zone_page
    zone_page = 0
    long_case = w_origine/2 - 20
    haut_case = 60
    
    liste_indicey = [300+(haut_case+10)*i  for i in range(6)] *2 #on fait *2 car il est prévu 2 colonne
    liste_indicex = [w_origine/2 - long_case -5] * 6 + [w_origine/2 + 5] * 6 #on fait *6 car c'est 6 par colonne
    surface_fleche = pygame.Surface((20,50))
    global page
    page = []
    font = pygame.font.SysFont(chivo_titre, 30)
    y_all = h_origine - 100
    global can_add
    can_add = False
    global flop_de_recherche
    flop_de_recherche = False
    
    def display_result(num):
        """Fonction permettant d'afficher le résultat d'une recherche précise

        Args:
            num (int): nombre de résultat obtenu
        """
    
        global access,zone_page,all_case_data,dict_rect_fleche,add_fleche,can_add,have_supprime
        #pygame.event.clear()        
        text = f"{num} résultat.s pour cette recherche !" if not flop_de_recherche else "OH :() une erreur est survenue"
        text = "Faites une recherche :)" if have_supprime else text
        screen.fill(fond_ecran,(w_origine/2 - font.size(text)[0]/2,230,300,100))
        draw_text(text,color = (255,255,255),
                  x = w_origine/2 - font.size(text)[0]/2,y = 230,
                  font = chivo_titre,size = 30
                  ,ombre = True)
        
        if access:
            try:
                max_par_page = 12
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
                longueur_decompte = font_40.size(decount_page)[0]
                x1 = w_origine/2 + longueur_decompte + 10
                x2 = w_origine/2 - longueur_decompte - 20            
                use_list = page[zone_page]
                rect_1 = pygame.Rect(x1,y_all,surface_fleche.get_width(),surface_fleche.get_height())
                rect_2 = pygame.Rect(x2,y_all,surface_fleche.get_width(),surface_fleche.get_height())
                dict_rect_fleche = [rect_1,rect_2]
                add_fleche = [1,-1]
                surface_fleche.fill((255,255,255))
                screen.blit(surface_fleche,(x1,y_all))
                screen.blit(surface_fleche,(x2,y_all))
                draw_text(decount_page,color = blanc,
                          x = w_origine/2 - longueur_decompte/2,
                          y = y_all,
                          font = font_paragraphe, importer = True,size = 40)
                for index,data in enumerate(use_list):
                    nom_projet = data[0]
                    auteur = User.get_only_pseudo(data[5])
                    id_ = data[4]
                    doc  = data[2]
                    date = data[1]
                    file = data[6]
                    date = date.strftime("%d/%m/%Y")
                    date_actuelle = datetime.datetime.now()
                    date_actuelle = date_actuelle.strftime("%d/%m/%Y")
                    if date_actuelle == date:
                        text_date = "posté aujourd'hui"
                    else:
                        text_date = f"posté le {date}"
                    text = data[3]
                    rect_case = pygame.Rect(liste_indicex[index],
                                            liste_indicey[index],
                                            long_case,
                                            haut_case)
                    if len(use_list) <=3:
                        rect_case = pygame.Rect(w_origine/2 - long_case/2, liste_indicey[index],
                                                long_case,
                                                haut_case)
                    surface = pygame.Surface((rect_case.w,rect_case.h),pygame.SRCALPHA)
                    surface.fill((0,0,0,0))
                    pygame.draw.rect(surface,palette_couleur.couleur_fond_case_tuto,(0,0,surface.get_width(),surface.get_height()),0,20)
                    color_auteur = (255,0,0) if Gerer_requete.est_bytes(doc) else blanc
                    if len(auteur) >= 20:
                        ecrit_auteur = auteur[:5] + ".."
                    else:
                        ecrit_auteur = auteur
                    draw_text(color = color_auteur,contener = surface,
                              text = f"{nom_projet} par {ecrit_auteur}", x = 10,
                              y = 0, font = font_paragraphe,
                              size = 30, importer = True)
                    draw_text(color = blanc,contener = surface,
                              text = text_date, x = rect_case.w - font_30.size(text_date)[0] - 20,
                              y = 5, importer = True,
                              size = 30, font = font_paragraphe)
                    if len(use_list) > 6:
                        screen.blit(surface,(liste_indicex[index],liste_indicey[index]))
                    else:
                        screen.blit(surface,(w_origine/2 - long_case/2, liste_indicey[index]))                
                    pygame.draw.rect(screen,(255,255,255),rect_case,3,20)
                    case_data = {"zone" : zone_page,"nom_projet" : nom_projet, "contenu" : text, "auteur" : auteur, "date" : date,"rect" : rect_case,"doc" : doc,"id" : id_,"extension" : file}
                    if can_add:
                        pygame.display.flip()
                        all_case_data.append(case_data)
                can_add = False
            except:
                Gerer_requete.error_occured()
    
    def start_tuto(data):
        """Fonction permettant de lancer le tuto

        Args:
            data (dict): donnée au sujet du tuto
        """
        text = data["contenu"]
        auteur = data["auteur"]
        date = data["date"]
        id_ = data["id"]
        date = datetime.datetime.strptime(date,"%d/%m/%Y")
        nom_projet = data["nom_projet"]
        doc = data["doc"]
        file = data["extension"]
        if not Gerer_requete.est_bytes(doc):
            page_info(2,text,nom_projet,auteur,date,id_)
        else:
            animation_ouverture.start_anime(last_screen,fond_ecran)
            Gerer_requete.demarrer_fichier(doc = doc, ext = file,auteur = auteur, nom_tuto=nom_projet)
            animation_ouverture.stop_anime()
        
            
    def research(data):
        """Fonction effectuant la recherche

        Args:
            data (dict): donnée au sujet du tuto selectionner
        """
        global all_case_data
        all_case_data = []
        global processing
        processing = True
        global have_supprime
        have_supprime = False   
        global detail,can_add,access,display,num_resultat,flop_de_recherche
        can_add = True
        access = False
        global zone_page
        zone_page = 0
        try:               
            detail = Gerer_requete.rechercher_data(nom_auteur = data["nom_auteur"], nom_tuto = data["nom_projet"])
            processing = False
            num_resultat = len(detail)
            access = True
            display = True
        except noConnection:
            processing = False
            Gerer_requete.connection_failed()
            
        except Exception as e:
            flop_de_recherche = True
            processing = False
            access = False
            display = True
        
       
    global continuer
    global finish
    global have_supprime
    have_supprime = False
    finish = False
    rect_goback = pygame.Rect(5,15,50,50)
    image_retour = pygame.image.load("Image/Icone_retour.png")
    image_retour = pygame.transform.smoothscale(image_retour,(rect_goback.w,rect_goback.h))
    go_back = False
    font_paragraphe = apple_titre
    font_40 = pygame.font.Font(font_paragraphe, 40)
    font_30 = pygame.font.Font(font_paragraphe,30)
    font_20 = pygame.font.Font(font_paragraphe,20)
    longueur_recherche = w_origine - 400
    surface_rechercher = pygame.Surface((longueur_recherche, 70), pygame.SRCALPHA)
    rect_btn = pygame.Rect(0,0,50,20)
    rect_rechearch = pygame.Rect(100,150,longueur_recherche,70)
    rect_btn.x = 100 + (longueur_recherche) - 100
    rect_btn.y = 150 + 70/2 - 20/2
    input_research = input_apple
    barre_input = pygame.Surface((2,25))
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
    liste_rech = ["Auteur","Nom","nom_auteur","nom_projet"]
    rect_type_recherche = pygame.Rect(100 + longueur_recherche + 100, 155, 100,60)
    surface_type_recherche = pygame.Surface((100,60), pygame.SRCALPHA)
    indice_type = 0
    text_rechercher = "Recherche par"
    rect_aide = pygame.Rect(w_origine - 70, 15, 50,50)
    image_aide = pygame.image.load("image/icone_interrogation.png")
    image_aide = pygame.transform.smoothscale(image_aide,(rect_aide.w,rect_aide.h))
    #boucle principale
    while continuer:
        clock.tick(120)
        dict_recherche = {"nom_projet" : None,"nom_auteur" : None}
        mouse = pygame.mouse.get_pos()
        screen.fill(fond_ecran)            
        surface_rechercher.fill((0,0,0,0))
        surface_type_recherche.fill((0,0,0,0))
        #boucle evenementielle
        if processing:
            actu = time.time()
            if actu - debut >= 2:
                ajout_text = "Cela prend plus de temps que prévu :("
            else:
                ajout_text = ""
            animation_chargement.animate(fond_ecran,ajout_decriture=ajout_text)
        for event in pygame.event.get():
            if active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        input_host += " "
                    elif event.key == pygame.K_BACKSPACE:
                        input_host = input_host[:-1]
                    elif event.key == pygame.K_RETURN:
                        pygame.event.clear()
                        recherche_type = liste_rech[indice_type+2]
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
                            input_host += event.unicode
            for index,data_recup in enumerate(all_case_data):
                if data_recup["rect"].collidepoint(mouse) and data_recup["zone"] == zone_page:
                    text_on = data_recup["id"]
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
                        start_tuto(data_recup)
                        
            for index,values in enumerate(dict_rect_fleche):
                if values.collidepoint(mouse):
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if zone_page + add_fleche[index] >= 0 and zone_page + add_fleche[index] < len(page):
                            zone_page += add_fleche[index]
                            can_add = True
                            all_case_data = []
            if rect_type_recherche.collidepoint(mouse):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if indice_type < len(dict_recherche) - 1:
                        indice_type += 1
                    else:
                        indice_type = 0
            if rect_aide.collidepoint(mouse):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    reponse = User.confirm_open()
                    if reponse:
                        animation_ouverture.start_anime(last_screen,fond_ecran)
                        Gerer_requete.demarrer_fichier(doc = os.path.join("Ressource","SYLVER.docx"),with_path=True,ext = None)
                        animation_ouverture.stop_anime()
            if event.type == pygame.QUIT:
                continuer = False
                break
            if rect_goback.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                go_back = True
            if rect_rechearch.collidepoint(mouse) and not rect_btn.collidepoint(mouse):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    active = not active
                    if len(input_host) == 0 and not active:
                        input_host = phrase_base
                    if active and input_host == phrase_base:
                        input_host = ""            
            if rect_btn.collidepoint(mouse):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and bool(input_host):
                    access = False
                    display = True
                    have_supprime = True
        rect_surf_rechercher = pygame.Rect(100,150,surface_rechercher.get_width(),surface_rechercher.get_height())
 
        pygame.draw.rect(surface_rechercher,(255,255,255),(0,0,rect_surf_rechercher[2],rect_surf_rechercher[3]),0,20)

        couleur = (255,0,0) if not rect_btn.collidepoint(mouse) else (255,255,255)
        blit_input = input_research.render(input_host,True,(0,0,0))
        center_y = rect_rechearch.h/2 - input_research.size(input_host)[1]/2
        #il est mieux d'utiliser draw_text car ça va plus vite, mais j'ai fait comme ça
        #en tout cas c'est similaire a draw_text
        surface_rechercher.blit(blit_input,(10,center_y))
        
        #crée un rect semblable a la surface et a la bonne pos
        contour_surface_rechercher = pygame.Rect(100,150,surface_rechercher.get_width(),surface_rechercher.get_height())
        if active:
            if not take_time:
                time_start = pygame.time.get_ticks()
                take_time = True
            time_ = int(pygame.time.get_ticks() - time_start)/1000
            surface_rechercher.blit(barre_input, (10 + input_research.size(input_host)[0],2 + input_research.size(input_host)[1]/2))
            #permet de faire clignoter la petite barre
            """if int(time_) % 2 == 0 and int(time_) != 0:
                surface_rechercher.fill((0,0,0), (5 + input_research.size(input_host)[0],2 + input_research.size(input_host)[1]/2,2,25))"""
        else:
            time_ = 0
            take_time = False
         
        screen.blit(surface_rechercher,(100,150))    
        pygame.draw.rect(screen,palette_couleur.couleur_contour_case,contour_surface_rechercher,5,20)
        pygame.draw.rect(screen,couleur,rect_btn)
        fond_nav.fill(palette_couleur.fond_bar_de_navigation)
        screen.blit(fond_nav,(0,0))
        title("Bienvenue Dans l'espace recherche!")       
        pygame.draw.rect(surface_type_recherche,palette_couleur.fond_case_login,(0,0,rect_type_recherche[2],rect_type_recherche[3]),0,20)
        pygame.draw.rect(surface_type_recherche,(255,255,255),(0,0,rect_type_recherche.w,rect_type_recherche.h),2,20)
        draw_text(contener = surface_type_recherche,
                  text = liste_rech[indice_type],
                  x = rect_type_recherche.w/2 - font_30.size(liste_rech[indice_type])[0]/2,
                  y = rect_type_recherche.h/2 - font_30.size(liste_rech[indice_type])[1]/2,size = 30,
                  font = font_paragraphe,
                  importer = True)
        draw_text(text = text_rechercher,
                  x = rect_type_recherche.x
                  + rect_type_recherche.w/2 - font_30.size(text_rechercher)[0]/2,
                  y = rect_type_recherche.y - 40,
                  color = blanc, importer = True, font = font_paragraphe,size = 30,
                  )
        screen.blit(surface_type_recherche,rect_type_recherche)
        screen.blit(image_aide,rect_aide)
        if display:
            display_result(num_resultat)
        screen.blit(image_retour,rect_goback)
        draw_text(text_on,color = (255,255,255),
                  x =0,
                  y = 0, font = chivo_titre,
                  size = 30)
        if go_back:
            break
        last_screen = screen.copy()
        pygame.display.update(rect_surf_rechercher)
        pygame.display.flip()
        
        
def relative_at(rect : pygame.Rect,relative : pygame.Rect) -> pygame.Rect:
    """Fonction permettant d'avoir le rect relatif d'un element a un autre

    Args:
        rect (pygame.Rect): Rect de l'element ciblé
        relative (pygame.Rect): Rect du referentiel

    Returns:
        pygame.Rect: Rect relatif de rect a relative
    """
    return pygame.Rect(rect.x - relative.x,rect.y - relative.y,rect.w,rect.h)

global make_chargement

def make_chargement(last_screen,text = "Chargement",delay = 200,animation = 2):
        """Fonction qui fait un chargement animer

        Args:
            text (str, optional): text a animer. Defaults to "Chargement...".
        """
        global continue_charging
        
        try:
            if animation == 1:
                screen.blit(last_screen,(0,0))
                pygame.display.flip()
                nb_point = 0
                while continue_charging:
                    nb_point += 1     
                    point = "."*((nb_point %4))                                                
                    rect_a_update = pygame.Rect(w_origine/2 - font(csm,20).size(text)[0]/2,h_origine - 40,200,
                                                50)
                    screen.fill(fond_ecran,rect_a_update)
                    
                    draw_text(text + point,x = w_origine/2 - font(csm,20).size(text)[0]/2, y = h_origine - 40)
                    pygame.display.update(rect_a_update)        
                    pygame.time.delay(delay)     
            elif animation == 2:
                text += "..." if not "..." in text else ""
                ensemble_text = [letter for letter in text]
                screen.blit(last_screen,(0,0))
                nb_caractere = len(ensemble_text)
                texte = ""
                caractere = 0
                while continue_charging:
                    
                    if caractere % nb_caractere == 0:
                        texte = ""
                    texte += ensemble_text[caractere % nb_caractere]
                    rect_a_update = pygame.Rect(w_origine/2 - font(csm,20).size(text)[0]/2,h_origine - 40,200,
                                                50)
                    screen.fill(fond_ecran,rect_a_update)
                    caractere += 1
                    draw_text(texte,x = w_origine/2 - font(csm,20).size(texte)[0]/2, y = h_origine - 40)
                    pygame.display.update(rect_a_update)        
                    pygame.time.delay(delay)             
        except Exception as e:
            print("erreur : ",e)
            
            
surf_image2 = None 
continue_charging = None     
def compte():
    """Fonction affichant la partie compte de l'application"""
    global surf_image2
    global connect
    global continue_charging
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
        with open("./Ressource/compte_connecter.txt","w") as fichier:
            fichier.write(f"{pseudo}\n{mdp}")
    
    def look_for_connection_tools():
        """Fonction qui verifie si des données d'utilisateur sont déjà enregistrez

        Returns:
            bool: Precision de si il y a un utilisateur connecter ou non
        """
        with open("./Ressource/compte_connecter.txt", "r") as fichier:
            return len(fichier.read().splitlines()) != 0
        
    text_edit = "Clickez pour editer"
    text_creer_compte = "Bienvenue parmis nous ! Creez votre compte :)"
    text_con_compte = "Bon retour parmis nous ! Connectez vous :)"
    global continuer
    rect_goback = pygame.Rect(5,5,50,50)
    barre_type = pygame.Surface((2,20))
    go_back = False
    creer_compte = True if not connect else False
    size = (125,125)
    size_grand = (200,200)
    font_paragraphe = apple_titre
    font_40 = pygame.font.Font(font_paragraphe, 40)
    font_60 = pygame.font.Font(font_paragraphe, 60)
    font_30 = pygame.font.Font(font_paragraphe,30)
    font_20 = pygame.font.Font(font_paragraphe,20)
    rect_editer_photo = pygame.Rect(0,0,0,0)
    rect_editer_photo.w = font_20.size(text_edit)[0]
    rect_editer_photo.h = font_20.size(text_edit)[1]
    chemin_pp = os.path.join("img_center","photo_profil_user.png")
    global pp_base
    #pp_base est le bit de la pw_origine/2 - rect_host.w/2hoto_de_profil basique de l'app
    with open(os.path.join("img_base","photo_profil_user.png"),"rb") as fichier:
        pp_base = fichier.read()
        
    with open(chemin_pp,"wb") as fichier:
        fichier.write(pp_base)
    global image_pp
    #image_pp est la photo_de_profil basique de l'app
    image_pp = pygame.image.load(chemin_pp)
    if not connect:
        image_pp = pygame.transform.smoothscale(image_pp,size)
    else:
        image_pp = pygame.transform.smoothscale(image_pp,size_grand)
    #ces ensembles de surface permette de faire une photo de profil en rond
    surf2 = pygame.Surface(size, pygame.SRCALPHA)
    surf3 = pygame.Surface(size, pygame.SRCALPHA)
    surf2g = pygame.Surface(size_grand,pygame.SRCALPHA)
    surf3g = pygame.Surface(size_grand,pygame.SRCALPHA)
    rect_host = pygame.Rect(0,0,w_origine/3,h_origine - 400)
    rect_ctn_host = pygame.Rect(0,0,rect_host.w + 300,rect_host.h + 40)
    rect_host.y = h_origine/2 - rect_host.h/2
    rect_host.x = w_origine/2 - rect_host.w/2
    rect_ctn_host.x = rect_host.x - 20
    rect_ctn_host.y = rect_host.y - 20
    Surface_edit_photo = pygame.Surface((rect_editer_photo.w,rect_editer_photo.h),pygame.SRCALPHA)
    y_photo = rect_host.y + 10
    y_photo2 = 50
    x_photo2 = w_origine/2 - size_grand[0]/2
    rect_editer_photo.x = rect_host.x +rect_host.w/2 - rect_editer_photo.w/2
    rect_editer_photo.y = y_photo + 130
    Surface_host = pygame.Surface((rect_host.w,rect_host.h),pygame.SRCALPHA)
    #rect des inputs
    
    rect_input_nom = pygame.Rect(rect_host.x + 10, rect_editer_photo.y + 30,rect_host.w/2 +50,30)
    rect_input_age = pygame.Rect(rect_input_nom.x + rect_input_nom.w + 50 - 20,
                                    rect_input_nom.y,
                                    rect_host.w - rect_input_nom.w - 60,
                                    rect_input_nom.h)
    rect_input_prenom = pygame.Rect(rect_input_nom.x,rect_input_nom.y + 70, rect_input_nom.w,rect_input_nom.h)
    rect_input_pseudo = pygame.Rect(rect_input_nom.x, rect_input_prenom.y + 70,rect_input_nom.w, rect_input_nom.h)
    rect_input_mdp = pygame.Rect(rect_host.x + rect_host.w - 205, rect_input_pseudo.y +70, 200,rect_input_nom.h)
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
    btn_submit = pygame.Rect(0,0,100,50)
    btn_submit.x = rect_host.x + rect_host.w/2 - btn_submit.w/2
    btn_submit.y = rect_host.y + rect_host.h - btn_submit.h - 30
    invalid_champ = False
    check_save_con_data =  False
    take = False
    text_invalid = "Certain champs sont mal remplie"
    pseudo_ndispo = False
    text_ndispo = "Pseudo déjà existant"
    visible = False
    rect_visible = pygame.Rect(0,0,39,rect_input_mdp.h-5)
    rect_visible.x = rect_input_mdp.x + rect_input_mdp.w - rect_visible.w - 10
    rect_visible.y = rect_input_mdp.y + rect_input_mdp.h/2 - rect_visible.h/2
    icone_mdp = pygame.image.load(os.path.join("image", "image_mdp_visu.png")).convert_alpha()    
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
    rect_save_user_data = pygame.Rect(0,0,20,20)
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
            "rect_editer_photo_y" : y_photo + 130,
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
            "rect_editer_photo_y" : y_photo + 130,
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
    btn_disconnect = pygame.Rect(200,200,20,20)
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
    
    image_retour = pygame.image.load("Image/Icone_retour.png")
    image_retour = pygame.transform.smoothscale(image_retour,(rect_goback.w,rect_goback.h))
    zone = 0 
    while continuer:
        mouse = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        screen.fill(fond_ecran)
        for event in pygame.event.get():            
            if rect_valider.collidepoint(mouse):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    creer_compte = not creer_compte
                    zone = 0 if creer_compte else 1
            elif rect_goback.collidepoint(mouse) and (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                go_back = True
            if rect_save_user_data.collidepoint(mouse):
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    check_save_con_data = not check_save_con_data
            if (rect_editer_photo.collidepoint(mouse) or collide_image) and (zone == 0 or connect):
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    try:
                        path_ext = User.get_file(1)
                        path = path_ext[0]
                        img = resizeImage(path)                        
                        try:
                            global surf_image
                            screen.blit(last_screen,(0,0))
                            draw_text("Clickez pour valider",x = w_origine/2 - font(font_paragraphe,18,True).size("Clickez pour valider")[0]/2,
                                      y = h_origine - 30, importer = True, size = 18, font = font_paragraphe)
                            pygame.display.update()
                            surf_image,rect_ellipse,image_photo_pp = img.try_to_resize(screen)
                            if not connect:
                                surf_image = pygame.transform.smoothscale(surf_image,size)
                            else:
                                surf_image2 = pygame.transform.smoothscale(surf_image2,size_grand)
                            try:                                
                                with open(path,"rb") as fichier:
                                    nv_pp = fichier.read()
                                with open(chemin_pp,"wb") as fichier:
                                    fichier.write(nv_pp)
                                if connect:
                                    user.change_element(photo_pp= True,Nouvelle_value=nv_pp)
                                    user.change_element(rect_pp = True,Nouvelle_value=rect_ellipse)
                                pp_choisi = True
                            except OSError:
                                Gerer_requete.fail_open()    
                                                                
                            except Exception:
                                Gerer_requete.error_occured()
                                
                        except AnnuleCropPhoto as err:
                            print(err.what)         
                                           
                    except noFileException:
                        pass
            ###################################################### Système après connection #################################################
            if connect:
                if btn_disconnect.collidepoint(mouse):
                    if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                        connect = False
                        del user
                        image_pp = pygame.transform.smoothscale(image_pp,size)
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
                                    animation_mise_en_ligne.start_anime(last_screen,fond_ecran)
                                    Gerer_requete(user).save_tuto(path,"",nom_tuto)
                                    animation_mise_en_ligne.stop_anime()
                            else:
                                break
                        except noConnection:
                            Gerer_requete.connection_failed()   
                        except:
                            Gerer_requete.error_occured()  
                            
                elif rect_maketuto.collidepoint(mouse):
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        ecrire_tuto(user)
                    
            elif creer_compte or not creer_compte:
                if rect_visible.collidepoint(mouse):
                    if mouse_click:
                        visible = not visible
                        icone_mdp = pygame.image.load("image/image_mdp_visu.png").convert_alpha() if not visible else pygame.image.load("image/image_mdp_cacher.png").convert_alpha()
                        icone_mdp = pygame.transform.smoothscale(icone_mdp,(rect_visible.w,rect_visible.h))
                elif rect_editer_photo.collidepoint(mouse):
                    color_edit = palette_couleur.contour_input_login
                    
                else:
                    color_edit = (0,0,200)
                if btn_submit.collidepoint(mouse):
                    
                    if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                        animation_connection.start_anime(last_screen,fond_ecran)
                        if look_valid(zone):
                            try:
                                if User.verifier_pseudo(dict_input[zone]["input_pseudo"]["input"]):
                                    if zone == 0:
                                        if look_mdp(0):
                                            
                                            try:
                                                nom = dict_input[0]["input_nom"]["input"].strip()
                                                prenom = dict_input[0]["input_prenom"]["input"].strip()
                                                age = int(dict_input[0]["input_age"]["input"])
                                                pseudo = dict_input[0]["input_pseudo"]["input"].strip()
                                                mdp = dict_input[0]["input_mdp"]["input_visible"].strip()
                                                with open(chemin_pp,"rb") as fichier:
                                                    photo_profil = fichier.read()                                            
                                                user = User(nom,prenom,age,pseudo,mdp,photo_profil,rect_pp = rect_ellipse)                                         
                                                user.save_user() 
                                                connect = True
                                                creer_compte = False
                                                with open(chemin_pp,"wb") as fichier:                                                
                                                    if user.photo_profil != pp_base:
                                                        fichier.write(user.photo_profil)
                                                    else:
                                                        fichier.write(pp_base)                                            
                                                if check_save_con_data:
                                                    write_connection_tools(pseudo,mdp)
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
                                                    new_width = 500
                                                    # Calculer la nouvelle hauteur (ou largeur) pour conserver le rapport d'aspect (produit en croix)
                                                    new_height = int(old_height * new_width / old_width)
                                                    # Redimensionner l'image
                                                    img_ = pygame.transform.smoothscale(img_, (new_width,new_height))
                                                    surf_image2 = resizeImage.rendre_transparent(img_,rect_pp,0)
                                                    surf_image2 = pygame.transform.smoothscale(surf_image2, size_grand)                                                
                                            except noConnection:
                                                Gerer_requete.connection_failed()                                                
                                            except Exception as e:
                                                Gerer_requete.error_occured()
                                        else:
                                            print("invalide")
                                            invalid_mdp = True
                                    else:
                                        print("no pseudo")
                                        n_pseudo = True
                                else:   
                                    if zone == 0:                         
                                        pseudo_ndispo = True
                                    
                                    else:
                                        if look_mdp(1):                                           
                                            pseudo = dict_input[zone]["input_pseudo"]["input"]
                                            mdp = dict_input[zone]["input_mdp"]["input_visible"]
                                            try:                                        
                                                user = User.log_user(pseudo,mdp)
                                                connect = True
                                                creer_compte = False
                                                with open(chemin_pp,"wb") as fichier:
                                                    if user.photo_profil != pp_base:
                                                        fichier.write(user.photo_profil)
                                                    else:
                                                        fichier.write(pp_base)
                                                if check_save_con_data:
                                                    write_connection_tools(pseudo,mdp)
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
                                                    new_width = 500
                                                    # Calculer la nouvelle hauteur (ou largeur) pour conserver le rapport d'aspect (produit en croix)
                                                    new_height = int(old_height * new_width / old_width)
                                                    # Redimensionner l'image
                                                    img_ = pygame.transform.smoothscale(img_, (new_width,new_height))
                                                    surf_image2 = resizeImage.rendre_transparent(img_,rect_pp,0)
                                                    surf_image2 = pygame.transform.smoothscale(surf_image2, size_grand)                                                
                                            except userNonCharger:
                                                pas_correspondance = True
                                            except noConnection:
                                                Gerer_requete.connection_failed()
                                            except Exception as e:
                                                Gerer_requete.error_occured()
                                        else:
                                            print("invalide")
                                            invalid_mdp = True
                            except noConnection:
                                animation_connection.stop_anime()
                                screen.blit(last_screen,(0,0))
                                pygame.display.update()
                                Gerer_requete.connection_failed()
                        else:
                            print("invalide")
                            invalid_champ = True
                        animation_connection.stop_anime()
                ################################################################ Système de l'input #################################################################     
                if not connect:       
                    i = 0         
                    for key,value in dict_input[zone].items():
                        if all_rect[zone][i].collidepoint(mouse):
                            if mouse_click and not rect_visible.collidepoint(mouse):
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
                                if event.key == pygame.K_BACKSPACE:
                                    if key != "input_mdp":
                                        value["input"] = value["input"][:-1]
                                    else:
                                        value["input_visible"] = value["input_visible"][:-1]
                                        value["input_cache"] = value["input_cache"][:-1]
                                    if value["depasse"] and value["coupage"] > 0:
                                        value["coupage"] -= 1
                                elif event.key == pygame.K_SPACE and value["can_space"]:
                                    if key != "input_mdp":
                                        value["input"] += " "
                                    else:  
                                        value["input_visible"] += " "
                                        value["input_cache"]  += "*"
                                    if value["depasse"]:
                                        value["coupage"] += 1
                                elif event.key == pygame.K_RETURN:
                                    pass                            
                                else:
                                    if key != "input_mdp":
                                        if len(value["input"]) < value["max"]:
                                            if key == "input_age":
                                                try:
                                                    m = int(event.unicode)
                                                    value["input"] += event.unicode
                                                except:
                                                    pass
                                            else:
                                                if event.unicode.isprintable() and event.unicode != "":
                                                    value["input"] += event.unicode
                                                    if value["depasse"]:
                                                        value["coupage"] += 1                                        
                                    else:
                                        if len(value["input_visible"]) < value["max"]:
                                            if event.unicode.isprintable() and event.unicode != "":
                                                value["input_visible"] += event.unicode
                                                value["input_cache"] += "*"
                                                if value["depasse"]:
                                                    value["coupage"] += 1
                        i += 1
        #interface user quand il n'est pas connecter
        if (creer_compte or not creer_compte) and not connect:
            rect_host.x = disposition[zone]["rect_host_x"]
            rect_ctn_host.x = disposition[zone]["rect_ctn_host_x"]
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
            if pas_correspondance:    
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
            if n_pseudo:
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
            if invalid_mdp:               
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
           
            title(text_bienvenu,size = 60)
            Surface_host.fill((255,255,255,0))
            couleur_save_user_data = (255,0,0) if not check_save_con_data else (0,255,0)
            pygame.draw.rect(Surface_host,palette_couleur.fond_un_login,(0,0,rect_host.w,rect_host.h),0,20)
            pygame.draw.rect(Surface_host,(0,0,0),(0,0,rect_host.w,rect_host.h),2,20)
            pygame.draw.rect(Surface_host,couleur_save_user_data,(rect_save_user_data.x - rect_host.x,rect_save_user_data.y - rect_host.y,
                            rect_save_user_data.w,rect_save_user_data.h))
            draw_text(contener = Surface_host, text = "Restez connecter",x = rect_save_user_data.x - rect_host.x + rect_save_user_data.w + 10,
                      y = rect_save_user_data.y - rect_host.y - 2, font = "Arial")
            pygame.draw.rect(screen,palette_couleur.fond_deux_login,(rect_ctn_host),0,20) #rpresente le 2e fond de connection et aussi creer compte
            pygame.draw.rect(screen,(0,0,0),(rect_ctn_host),2,20)
            screen.blit(Surface_host,(rect_host.x,rect_host.y))  #represente le contour forme du 2e fond          
            color_submit = bleu_s if not btn_submit.collidepoint(mouse) else (255,255,255)
            
            pygame.draw.rect(screen,palette_couleur.fond_case_login,btn_submit,0,10)
            pygame.draw.rect(screen,(0,0,0),btn_submit,1,10)            
            draw_text("VALIDER", x = btn_submit.x + btn_submit.w/2 - font_20.size("VALIDER")[0]/2,
                      y = btn_submit.y + btn_submit.h/2 - font_20.size("VALIDER")[1]/2,
                      font = font_paragraphe, importer = True, color = blanc)
            
            #mettre ma ptn de pp merde
            if not pp_choisi or not creer_compte:
                pygame.draw.ellipse(surf2, (255, 255, 255), (0,0,*size))
                surf3.blit(surf2, (0, 0))
                surf3.blit(image_pp, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)     
                screen.blit(surf3, (rect_host.x + rect_host.w/2 - size[0]/2, y_photo))
            elif pp_choisi and creer_compte:
                screen.blit(surf_image,(rect_host.x + rect_host.w/2 - size[0]/2, y_photo))
            mask = pygame.mask.from_surface(surf2)
            ellipse = pygame.draw.ellipse(screen,color_bordure_image,(rect_host.x + rect_host.w/2 - size[0]/2, y_photo,*size),int(bordure))
            if ellipse.collidepoint(mouse):
                #on créé la position relative avec la souris par rapport a l'ellipse
                mask_x = mouse[0] - ellipse.x
                mask_y = mouse[1] - ellipse.y
                if mask.get_at((mask_x, mask_y)):
                    collide_image = True
                    color_bordure_image = palette_couleur.contour_input_login
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
                pygame.draw.rect(screen,palette_couleur.couleur_contour_case, rect,2,20)
            
            
            #pygame.draw.rect(screen,(0,0,0),rect_visible)
            screen.blit(icone_mdp, rect_visible)
            #a remettre a une autre position
            
            pygame.draw.rect(screen,palette_couleur.fond_case_login,rect_valider,0,40)
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
            #affiche les inputs
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
                    rect_bt = (x + font_20.size(input_[value["coupage"]:])[0] ,y)
                    screen.blit(barre_type,rect_bt)
                i += 1       
            screen.blit(Surface_edit_photo,(rect_editer_photo.x,rect_editer_photo.y))
        else:
            if not element_page_user:
                font_25a = pygame.font.SysFont(arial, 25, bold=False, italic=True)
                btn_postimg = pygame.Surface((210,100),pygame.SRCALPHA)
                btn_maketuto = btn_postimg.copy()
                text_postimg = "POSTEZ UN TUTO VISUEL !"
                text_maketuto = "CREEZ UN TUTO EN TEXTE !"
                coupage, line, size_y = make_line(text=text_postimg,font = font_25a, size_max = btn_postimg.get_width())
                coupage2, line2, size_y2 = make_line(text=text_maketuto,font = font_25a, size_max = btn_postimg.get_width())
                rect_postimg = pygame.Rect(w_origine/2 - 20 - btn_postimg.get_width(),
                        y_photo2 + size_grand[1] + 150,
                        btn_postimg.get_width(),
                        btn_postimg.get_height())
                rect_maketuto = pygame.Rect(w_origine/2 + 20,
                        y_photo2 + size_grand[1] + 150,
                        btn_postimg.get_width(),
                        btn_postimg.get_height())
                element_page_user = True
            color_btn1 = (185,185,185) if not rect_postimg.collidepoint(mouse) else (255,255,255)
            color_btn2 = (185,185,185) if not rect_maketuto.collidepoint(mouse) else (255,255,255)
            pygame.draw.rect(btn_postimg,color_btn1,(0,0,btn_postimg.get_width(),btn_postimg.get_height()),0,20)
            pygame.draw.rect(btn_maketuto,color_btn2,(0,0,btn_maketuto.get_width(),btn_maketuto.get_height()),0,20)
            surface_ombre = pygame.Surface((btn_postimg.get_width() + 10, btn_postimg.get_height() + 10), pygame.SRCALPHA)
            surface_ombre.fill((0,0,0,0))
            surface_ombre2 = surface_ombre.copy()
            draw_line(text = text_postimg,
                      x = True,
                      y = rect_postimg.h/2 - size_y/2,
                      line = line, coupage = coupage,size = 25,
                      font = arial,fontz = font_25a,
                      contener = btn_postimg,importer = False)            
            draw_line(text = text_maketuto,
                      x = True,
                      y = rect_postimg.h/2 - size_y2/2,
                      line = line2, coupage = coupage2,size = 25,
                      font = arial,fontz = font_25a,
                      contener = btn_maketuto,importer = False)
            pygame.draw.rect(btn_postimg,(255,255,255),(0,0,btn_postimg.get_width(),btn_postimg.get_height()),1,20)
            pygame.draw.rect(btn_maketuto,(255,255,255),(0,0,btn_maketuto.get_width(),btn_maketuto.get_height()),1,20)
            #rep; continuez lanimation pour le 2e btn, continuer detoffer linterface user design
            if rect_postimg.collidepoint(mouse):                
                x_effet1 += 1 if x_effet1 < 4 else 0
                y_effet1 += 1 if y_effet1 < 4 else 0
                intensiter_effet += 255/4 if intensiter_effet < 255 else 0
                pygame.draw.rect(surface_ombre,(0,0,0,intensiter_effet),(x_effet1,y_effet1,btn_postimg.get_width(),btn_postimg.get_height()),0,20)
                screen.blit(surface_ombre,(
                    w_origine/2 - 20 - btn_postimg.get_width(), y_photo2 + size_grand[1] + 150
                ))
            else:
                x_effet1 -= 2 if x_effet1  > 0 else 0
                y_effet1 -= 2 if y_effet1 > 0 else 0
                intensiter_effet -= 255/5 if intensiter_effet < 0 else 0
                pygame.draw.rect(surface_ombre,(0,0,0,intensiter_effet),(x_effet1,y_effet1,btn_postimg.get_width(),btn_postimg.get_height()),0,20)
                if x_effet1 > 0:
                    screen.blit(surface_ombre,(
                        w_origine/2 - 20 - btn_postimg.get_width(), y_photo2 + size_grand[1] + 150
                    ))  
            if rect_maketuto.collidepoint(mouse):                
                x_effet2 += 1 if x_effet2 < 4 else 0
                y_effet2 += 1 if y_effet2 < 4 else 0
                intensiter_effet += 255/4 if intensiter_effet < 255 else 0
                pygame.draw.rect(surface_ombre2,(0,0,0,intensiter_effet),(x_effet2,y_effet2,btn_postimg.get_width(),btn_postimg.get_height()),0,20)
                screen.blit(surface_ombre2,(
                   w_origine/2 + 20, y_photo2 + size_grand[1] + 150
                ))                
            else:
                x_effet2 -= 2 if x_effet2  > 0 else 0
                y_effet2 -= 2 if y_effet2 > 0 else 0
                intensiter_effet -= 255/5 if intensiter_effet < 0 else 0
                pygame.draw.rect(surface_ombre2,(0,0,0,intensiter_effet),(x_effet2,y_effet2,btn_postimg.get_width(),btn_postimg.get_height()),0,20)
                if x_effet2 > 0:
                    screen.blit(surface_ombre2,(
                        w_origine/2 + 20, y_photo2 + size_grand[1] + 150
                    ))            
            screen.blit(btn_postimg,(
                w_origine/2 - 20 - btn_postimg.get_width(), y_photo2 + size_grand[1] + 150
            ))
            screen.blit(btn_maketuto,(
                w_origine/2 + 20, y_photo2 + size_grand[1] + 150
            ))
            #image_pp = pygame.transform.smoothscale(image_pp,size_grand)
            rect_editer_photo.x = x_photo2 + size_grand[0]/2 - font_20.size(text_edit)[0]/2
            rect_editer_photo.y = y_photo2 + size_grand[1] + 5
            pygame.draw.rect(screen,(0,0,0),btn_disconnect)
            if user.rect_pp == None:
                pygame.draw.ellipse(surf2g, (255, 255, 255), (0,0,*size_grand))            
                surf3g.blit(surf2g, (0, 0))
                surf3g.blit(image_pp, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
                screen.blit(surf3g, (x_photo2, y_photo2))
            else:
                #blit pp
                screen.blit(surf_image2,(x_photo2,y_photo2))
            #masque fait pour detecter la collision très précisément
            mask = pygame.mask.from_surface(surf2g)
            ellipse_dessiner = pygame.draw.circle(screen,color_bordure_image,(x_photo2 + size_grand[0]/2 ,y_photo2+size_grand[0]/2 +1),size_grand[0]/2 +1,1)
            fake_screen  =  pygame.Surface((screen.get_width(),screen.get_height()), pygame.SRCALPHA)
            #pour eviter l'erreur que les mask_x et mask_y deborde du mask car l'ellipse dessiner est aggrandi intentionnellement a cause du
            #dessin d'un rond merdique de pygame
            ellipse = pygame.draw.circle(fake_screen,(0,0,0,0),(x_photo2 + size_grand[0]/2 ,y_photo2+size_grand[0]/2),size_grand[0]/2,1)
            if ellipse.collidepoint(mouse):
                mask_x = mouse[0] - ellipse.left
                mask_y = mouse[1] - ellipse.top                
                if mask.get_at((mask_x, mask_y)):
                    collide_image = True
                    color_bordure_image = palette_couleur.contour_input_login
                else:
                    collide_image =False
                    color_bordure_image = (0,0,0)
            else:
                color_bordure_image = (0,0,0)
                collide_image = False                                 
            text_nom_prenom =  user.nom + " " + user.prenom
            text_pseudo = user.pseudo
            tuto_poster = user.tuto_transmis
            color_edit = (0,0,0) if not rect_editer_photo.collidepoint(mouse) else (200,0,0)
            draw_text(text_edit,
                      color = color_edit, 
                      x = x_photo2 + size_grand[0]/2 - font_20.size(text_edit)[0]/2
                      ,y = y_photo2 + size_grand[1] + 5, size = 20,
                      importer = True, font = font_paragraphe)
            draw_text(text_nom_prenom,
                      color = (0,0,0), 
                      x = x_photo2 + size_grand[0]/2 - font_30.size(text_nom_prenom)[0]/2
                      ,y = y_photo2 + size_grand[1] + 40, size = 30,
                      importer = True, font = font_paragraphe)
            draw_text(text_pseudo,
                      color = (0,0,0), 
                      x = x_photo2 + size_grand[0]/2 - font_30.size(text_pseudo)[0]/2
                      ,y = y_photo2 + size_grand[1] + 70, size = 30,
                      importer = True, font = font_paragraphe)
            draw_text(f"-Vous avez postez {tuto_poster} tutoriel.s-",
                      color = (0,0,0), 
                      x = x_photo2 + size_grand[0]/2 - font_30.size(f"-Vous avez postez {tuto_poster} tutoriel.s-")[0]/2
                      ,y = y_photo2 + size_grand[1] + 100, size = 30,
                      importer = True, font = font_paragraphe)            
        screen.blit(image_retour,rect_goback)
        
        pygame.display.flip()
        last_screen = screen.copy()
        if go_back:
            break
        
        
def request():
    global continuer
    rect_goback = pygame.Rect(5,5,50,50)
    image_retour = pygame.image.load("image/Icone_retour.png")
    image_retour = pygame.transform.smoothscale(image_retour,(rect_goback.w,rect_goback.h))
    go_back = False
    while continuer:
        mouse = pygame.mouse.get_pos()
        screen.fill(fond_ecran)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
            if rect_goback.collidepoint(mouse) and (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                go_back = True        
        
        text = "Alors déjà bien jouer !\nMais y'a rien ici sauf un gris bizarre\nCette partie de l'application devrait être faite bientot !\n Ou pas !\n \
            si elle est effectivement faite, ce sera une page qui regrouperait toute les annonces de tuto laissez par des utilisateurs ! :)"
        draw_text(text,color = (255,255,255), center_multi_line=True,x = 0,y = 0, center_multi_line_y= True,ombre = True)
        if go_back:
            break
        screen.blit(image_retour,rect_goback)
        pygame.display.flip()

def input_popup():
    pygame.display.flip()
    global continuer
    container = pygame.Surface((w_origine/3,h_origine/3), pygame.SRCALPHA)
    width = container.get_width()
    height = container.get_height()
    active_input = False
    text_input = ""
    max_input = 25
    rect_quit = pygame.Rect(5,30,30,30)
    image_retour = pygame.image.load("Image/Icone_retour.png")
    image_retour = pygame.transform.smoothscale(image_retour,(rect_quit.w,rect_quit.h))
    font_paragraphe = apple_titre
    rect_container = pygame.Rect(w_origine/2 - container.get_width()/2, h_origine/2 - container.get_height()/2,container.get_width(),container.get_height())
    rect_quit_absolute = pygame.Rect(rect_container.x + rect_quit.x, rect_container.y + rect_quit.y, 30,30)
    text_titre = "Ecrivez le nom de votre tuto"
    text_active = "Input désactivé"
    color_input = (255,0,0)
    cancel = False
    finished = False
    while continuer:
        container.fill((0,0,0,0))
        mouse = pygame.mouse.get_pos()
        rect_input_absolute = pygame.Rect(rect_container.x + width/2 - (max(width/2, font(apple_titre,30,True).size(text_input)[0]))/2,
                                          rect_container.y + height/2 - 50/2,
                                 max(width/2, font(apple_titre,30,True).size(text_input)[0]),
                                 50)
        for event in pygame.event.get():
            if rect_input_absolute.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                active_input = not active_input
                color_input = (0,0,0) if active_input else (255,0,0)
                text_active = "Input activé" if active_input else "Input désactivé"
            if rect_quit_absolute.collidepoint(mouse):
                if  event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    cancel = True
            if active_input:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        finished = True
                    elif event.key == pygame.K_SPACE and len(text_input) < max_input:
                        text_input += " "
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    else:
                        if len(text_input) < max_input:
                            if event.unicode.isprintable() and event.unicode != "":
                                text_input += event.unicode
                            
        rect_input = pygame.Rect(width/2 - (max(width/2, font(apple_titre,30,True).size(text_input)[0] + 15))/2,
                                 height/2 - 50/2,
                                 max(width/2, font(apple_titre,30,True).size(text_input)[0] +15),
                                 50)
        #fond
        pygame.draw.rect(container,bleu_s,(0,0,*rect_container[2:]),0,50)
        pygame.draw.rect(container,color_input,rect_input,1)
        draw_text(contener = container, text = text_titre,font = chivo_titre, size = 30, x = width/2 - font(chivo_titre,30,True).size(text_titre)[0]/2,
                  y = 10,importer = True)
        draw_text(contener = container, text = text_active, font = chivo_titre, size = 18, x = width/2 - font(chivo_titre,18,True).size(text_active)[0]/2,
                  y = height - 30, importer = True, color = blanc, ombre = True)
        draw_text(text_input, x = rect_input.x +10, y = rect_input.y + 5, font = font_paragraphe, size = 30,importer = True,contener = container)
        container.blit(image_retour,rect_quit)
        screen.blit(container,(rect_container.x,rect_container.y))
        pygame.display.update(rect_container)
        if cancel or finished:
            break
    if finished:
        return text_input.strip()
    return False
        

def font(font_name,size,importer = False):
    if not importer:
        return pygame.font.SysFont(font_name,size)
    return pygame.font.Font(font_name,size)

fond_ecran =  palette_couleur.fond_principal
bleu_s =(106,178,202)
taille_origine = pygame.display.Info()
w_origine = taille_origine.current_w
h_origine = taille_origine.current_h
continuer = True
connect = False
comic_sans_ms = pygame.font.SysFont("Comic Sans Ms", 20)
csm = "Comic Sans Ms"
arial = "Arial"
chivo_titre = r"font\chivo\Chivo-Black.otf"
dream_orphans = r"font\dream_orphans\Dream Orphans.otf"
apple_titre = r"font\apple_garamond\AppleGaramond-Light.ttf"
input_apple = pygame.font.Font(apple_titre,40)
beackman = r"font\Beckman.otf"
TNN = r"font\TNN.ttf"
blanc = (255,255,255)
noir = (0,0,0)
proposition = ["MENU","COMPTE","ANNONCE"]
etat = ["alpha","alpha","beta"]
size_box_grand_w = 270
size_box_grand_h = 100
size_box_w = 200
size_box_h = 80
millieu_w = (w_origine/2) - size_box_w/2
millieu_h = (h_origine/2) - size_box_h/2
pos = [[w_origine/2 - size_box_grand_w/2, h_origine/2 - size_box_grand_h/2 - size_box_h - 20],
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
accueil = "SYLVER_SERVICE"
font_accueil = pygame.font.SysFont("Comic Sans Ms", 40)
fond_nav = pygame.Surface((w_origine,100))
info = pygame.Rect(w_origine - 70, 15, 50,50)
icone_aide = pygame.image.load("Image/icone_interrogation.png")
icone_aide = pygame.transform.smoothscale(icone_aide,(info.w,info.h))
font_chivo = font(chivo_titre,72,True)
font_chivo_14 = font(chivo_titre,14,True)
size_for_title = 72

text_user_pas_co = "Salut :) Connecte toi ce sera mieux"

def title(text, size = size_for_title, color = blanc,importer = True):
    """Fonction permettant de mettre un titre

    Args:
        text (str): Texte en titre
        size (str, optional): taille du texte. Defaults to size_for_title.
        color (list, optional): couleur du texte. Defaults to blanc.
        importer (bool, optional): Indique si la police est importer ou non. Defaults to True.
    """
    font_ = font(chivo_titre,size,True)
    draw_text(text, size = size,color = palette_couleur.couleur_titre, x = (w_origine/2 - font_.size(text)[0]/2), y = 5,importer = importer, font = chivo_titre)


clock = pygame.time.Clock()

def gestion_event():
    """
        Gère l'évènement pour quitter l'app
    """
    global continuer
    while continuer:
        try:
            if keyboard.is_pressed("Escape"):
                print(threading.current_thread())
                continuer = not User.confirm_close()
        except:
            pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
        time.sleep(0.1)
    print("bye")


t1 = threading.Thread(target=gestion_event,daemon=True)
t1.start()
rect_choose = pygame.Surface((size_box_w,size_box_h), pygame.SRCALPHA)
rect_grand_choose = pygame.Surface((size_box_grand_w,size_box_grand_h), pygame.SRCALPHA)
rect_dispo = [pygame.Rect(pos[0][0],pos[0][1],size_box_grand_w,size_box_grand_h),
              pygame.Rect(pos[1][0],pos[1][1],size_box_w,size_box_h),
              pygame.Rect(pos[2][0],pos[2][1],size_box_w,size_box_h)
              ]
clock = pygame.time.Clock()
while continuer:
    screen.fill(fond_ecran)
    try:
        text_user_co = f"Salut {user.pseudo} ravis de te voir :)"
        draw_text(text_user_co, x = w_origine/2 - font(chivo_titre,36,True).size(text_user_co)[0]/2,
                  y = fond_nav.get_height() + 20, font = chivo_titre, color = blanc,
                  size = 36, importer = True)
    except Exception as e:
        draw_text(text_user_pas_co, x = w_origine/2 - font(chivo_titre,36,True).size(text_user_pas_co)[0]/2,
                  y = fond_nav.get_height() + 20, font = chivo_titre, color = blanc,
                  size = 36, importer = True)
    finally:
        #ici draw_text fr
        pass
    mouse = pygame.mouse.get_pos()    
    fond_nav.fill(palette_couleur.fond_bar_de_navigation)
    screen.blit(fond_nav,(0,0))
    #pp user
    if connect:
        size_pp_user = (75,75)
        x_pp,y_pp = 20,fond_nav.get_height() - size_pp_user[1] - 10
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
    draw_text(accueil_complement, size = 14, color=blanc, x = w_origine/2 - font_chivo_14.size(accueil_complement)[0]/2,
              y = 5, importer= True, font=chivo_titre)
    draw_text(accueil, size = 72,color = palette_couleur.couleur_titre, x = w_origine/2 - font_chivo.size(accueil)[0]/2, y = fond_nav.get_height() - font_chivo.size(accueil)[1], font = chivo_titre,importer = True)
    for event in pygame.event.get():        
        if event.type == pygame.KEYDOWN:
            pass
        if event.type == pygame.QUIT:
            continuer = False
        if info.collidepoint(mouse):
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
    date = datetime.datetime.today().strftime('%Hh%M')
    draw_text(date, size = 20, color = blanc, x = w_origine - 70, y = 110)
    screen.blit(icone_aide,info)
    clock.tick(144)
    fps = clock.get_fps()
    draw_text(f"fps : {int(fps)}",x=10,y=100,color=(255,255,255))
    
    for index,elt in enumerate(proposition):
        if index != 0:
            rect = rect_choose
        else:
            rect = rect_grand_choose
        rect.fill((0,0,0,0))
        w,l = rect.get_size()
        color_bord = palette_couleur.couleur_contour_case if is_on[index] == False else palette_couleur.fond_bar_de_navigation
        pygame.draw.rect(rect,palette_couleur.fond_case,(0,0,w,l),0,20)
        pygame.draw.rect(rect,color_bord,(0,0,w,l),1,20)
        draw_text(proposition[index],contener = rect,color = color_text[index], x = rect.get_width()/2 - font(csm,25).size(proposition[index])[0]/2,
                  y = rect.get_height()/2 - font(csm,25).size(proposition[index])[1]/2,size = 25)
        screen.blit(rect,pos[index])
    draw_text(text_choose,color = blanc, x = 5, y = h_origine - 25)
    pygame.display.flip()
pygame.quit()
sys.exit()