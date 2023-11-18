import time
from tkinter import font
import pygame,os,datetime,sys,threading,keyboard
from Sylver_class_import import Gerer_requete,User,noFileException, userNonCharger
from Z_Prototype_resize_image import AnnuleCropPhoto, resizeImage

"""
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.mixer.init()
pygame.display.init()
pygame.font.init()
pygame.key.set_repeat(200,50)

# Obtenir la résolution de l'écran
info = pygame.display.Info()
width, height = info.current_w, info.current_h

# Créer la fenêtre Pygame en plein écran et à la résolution native de l'écran
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
print(screen.get_rect())
"""
os.environ ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.mixer.init()
pygame.display.init()
pygame.font.init()
pygame.key.set_repeat(200,50)
resolution = pygame.display.Info()
width = resolution.current_w
height = resolution.current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN | pygame.SCALED | pygame.HWSURFACE | pygame.DOUBLEBUF)

def draw_text(text, font = "Comic Sans Ms", color = (0,0,0), x = 0, y = 0,contener = screen,size = 20,importer = False, ombre = False):
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
       

def make_line(text : str,font : pygame.font.SysFont,size_max : int):
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

def draw_line(line,coupage,text,size,contener,font,fontz,importer = True,x=0,y=0):
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


def decoupe_text(coupage,line,text_info) :
    all_text = []
    for i in range(line):
        start = coupage[i]
        try:
            limite = coupage[i+1]
        except:
            limite = len(text_info)
        all_text.append(text_info[start:limite].strip())
    return all_text

def type_tuto():
    for event in pygame.event.get():
        pass
    global fond_nav
    global continuer
    barre_input = pygame.Surface((2,15))
    barre_input.fill(noir)
    font_paragraphe = apple_titre
    font20 = pygame.font.Font(font_paragraphe, 20)
    font40 = pygame.font.Font(font_paragraphe, 40)
    surf_valider = pygame.Surface((200,50), pygame.SRCALPHA)
    surf_titre = pygame.Surface((20,100))
    surf_valider.fill((0,0,0,0))
    s_width = surf_valider.get_width()
    s_height = surf_valider.get_height()
    rect_valider = pygame.Rect(0,0,s_width,s_height)
    pygame.draw.rect(surf_valider,(0,0,0),rect_valider,1)
    draw_text(text = "valider", contener = surf_valider,x= s_width/2 - font40.size("valider")[0]/2, font = font_paragraphe, importer=True, size = 40)    
    surf_ecrit = pygame.Surface((w_origine - 20, h_origine - 250 ))
    active = True
    line = 0
    zone_ecrit = 0    
    all_input = [""]
    time = 0
    menos = False
    take_time = False
    while continuer:
        screen.fill((100,100,100))
        fond_nav.fill((0,0,0))
        mouse = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        for event in pygame.event.get():
            if active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        #changer de zone d'ecriture vers le haut
                        zone_ecrit -= 1 if len(all_input) > 1 else 0
                    elif event.key == pygame.K_DOWN:
                        #ajouter une zone d'ecriture
                        zone_ecrit += 1
                        all_input.append("")
                    if event.key == pygame.K_SPACE:
                        all_input[zone_ecrit] += " "
                    elif event.key == pygame.K_BACKSPACE:
                        if all_input[zone_ecrit] != "":
                            all_input[zone_ecrit] = all_input[zone_ecrit][:-1]
                        else:
                            if len(all_input) > 1:
                                #supprimer la ligne
                                del(all_input[zone_ecrit])
                                zone_ecrit -= 1 
                                menos = True
                                print("menos")        
                            else:
                                print("wut")   
                                
                    elif event.key == pygame.K_RETURN:
                        all_input.append("")
                        #ajouter une zone d'ecriture
                        zone_ecrit+=1
                    elif event.key == pygame.K_ESCAPE:
                        pass
                    else:
                        all_input[zone_ecrit] += event.unicode
                    if len(all_input[zone_ecrit]) > 0 and not menos:
                        if font20.size(all_input[zone_ecrit])[0] >= surf_ecrit.get_width() - 40:
                            all_input.append("")
                            zone_ecrit +=1
                            print("add")
                            #ajouter une zone d'ecriture
                    menos = False
                    
            if rect_surf_ecrit.collidepoint(mouse):
                if mouse_click:
                    active = not active
        
        
        text = "Vous pouvez écrire" if active else "Vous ne pouvez pas ecrire"
        draw_text(text, x = w_origine/2 - font40.size(text)[0]/2, y = 100, importer=True,font = font_paragraphe, size = 40)
        surf_ecrit.fill((255,255,255))
        rect_surf_ecrit = pygame.draw.rect(surf_ecrit,(0,0,0),(0,0,surf_ecrit.get_width(),surf_ecrit.get_height()),1)
        for enum,i in enumerate(all_input):
            #ecrire tout les lignes dans all_input
            draw_text(i,importer=True,contener=surf_ecrit, x = 10, y = 20*enum, font=font_paragraphe)
        if active:
            if not take_time:
                time_start = pygame.time.get_ticks()
                take_time = True
            time = int(pygame.time.get_ticks() - time_start)/1000
            surf_ecrit.blit(barre_input, (10 + font20.size(all_input[zone_ecrit])[0], 20 * (zone_ecrit+1) - font20.size(all_input[zone_ecrit])[1]/2)) #le y le met a la position du texte adapter en fonction de zone_ecrit
        
            if int(time) % 2 == 0:
                surf_ecrit.fill(blanc, (10 + font20.size(all_input[zone_ecrit])[0],20 * (zone_ecrit+1) - font20.size(all_input[zone_ecrit])[1]/2, 2,15))
        else:
            time = 0
            take_time = False
        screen.blit(surf_valider,(w_origine - s_width - 30, h_origine - s_height - 20))
        screen.blit(surf_ecrit,(10,175))
        screen.blit(fond_nav,(0,0))
        title("Ecrivez ici votre tutoriel")
        pygame.display.flip()
        
def page_info(id_ = 0,text = None,nom_projet = None,auteur = None,date = None, id_tuto = None):
    global continuer
    global fond_nav
    rect_goback = pygame.Rect(5,5,20,20)
    go_back = False
    width = w_origine - 20
    height = h_origine - 200
    surface_ecriture = pygame.Surface((width, height))
    text_title = "A quoi sert Sylver_Service ?"
    if id_ > 1:
        date = date.strftime("%d/%m/%Y")
        date_save = date
        date = f"posté le : {date}"
        date_actuelle = datetime.datetime.now()
        date_actuelle = date_actuelle.strftime("%d/%m/%Y")
        if date_actuelle == date_save:
            date = "posté aujourd'hui"
        else:
            text_title = f"{nom_projet.upper()} par {auteur}"
        text_info = text
    if id_ == 0:
        with open("fichier_info.txt", "r+") as fichier:
            text_info = fichier.read().replace("\n"," ")
        text_info = text_info.replace("Ã©","é")
        text_info = text_info.replace("Ã¨","è")
        text_info = text_info.replace("Ãª","ê")
    size_max = width
    i = 0
    font_paragraphe = apple_titre
    font_40 = pygame.font.Font(font_paragraphe, 40)
    font_20 = pygame.font.Font(font_paragraphe, 20)
    """
    while i < len(text_info):
        size = font_40.size(text_info[start:i])[0]
        if size + 5 > size_max:
            w = -1
            while text_info[start:i][w] != " ":
                w -= 1
            i += w
            start = i
            coupage.append(start)
            line+=1
        i+=1
    """
    coupage,line,heigth_text = make_line(text = text_info, font = font_40, size_max= size_max)
    all_text = decoupe_text(coupage,line,text_info)
    """"
    for i in range(line):
        start = coupage[i]
        try:
            limite = coupage[i+1]
        except:
            limite = len(text_info)
        all_text.append(text_info[start:limite].strip())
    """
    moitier_text = []
    for i in range(len(all_text)):
        moitier_text.append(font_40.size(all_text[i])[0]/2)
    while continuer:
        mouse = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        screen.fill((100,100,100))
        surface_ecriture.fill((255,255,255))
        pygame.draw.rect(surface_ecriture,(0,0,0),(0,0,width,height),2)
        for event in pygame.event.get():            
            if event.type == pygame.QUIT:
                continuer = False
                break
            if rect_goback.collidepoint(mouse) and mouse_click:
                go_back = True
        for i in range(line):
            draw_text(all_text[i], color = (0,0,0), x = width/2 - moitier_text[i], y = height/2 - heigth_text/2, size = 40, contener = surface_ecriture, font = font_paragraphe, importer = True)
        pygame.draw.rect(screen,(0,0,0),rect_goback)
        fond_nav.fill((0,0,0))
        screen.blit(fond_nav,(0,0))
        title(text_title,color = (255,255,255), size = 40)
        if id_ > 1:
            draw_text(date, x = w_origine - font_20.size(str(date))[0]/2 - 10,y = 10, font = font_paragraphe, color = (255,255,255),importer = True)
        if go_back:
            break
        screen.blit(surface_ecriture, (10,150))
        pygame.display.flip()
        
        
cv = threading.Condition()

def menu():
    type_tuto()
    global display       
    global processing
    #savoir quand la recherche est en cours
    processing = False             
    display = False
    global zone
    zone = 0
    long_case = w_origine/2 - 10
    haut_case = 60
    liste_indicey = [300+haut_case*i for i in range(6)] *2
    liste_indicex = [w_origine/2 - long_case] * 6 + [w_origine/2] * 6
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
        global access,zone,all_case_data,dict_rect_fleche,add_fleche,can_add,have_supprime
        #pygame.event.clear()        
        text = f"{num} résultat.s pour cette recherche !" if not flop_de_recherche else "OH :() une erreur est survenue"
        text = "Faites une recherche :)" if have_supprime else text
        draw_text(text,color = (255,255,255),
                  x = w_origine/2 - font.size(text)[0]/2,y = 230,
                  font = chivo_titre,size = 30
                  ,ombre = True)
        
        if access:
            max_par_page = 12
            global page
            page = []
            count = 0
            sous_list = []
            for i in range(len(detail)):
                sous_list.append(detail[i])
                count += 1
                if count >= max_par_page:
                    page.append(sous_list)
                    sous_list = []
                    count = 0
            if len(page) == 0:
                page.append(sous_list)
            decount_page = f"{zone+1}/{len(page)}"
            longueur_decompte = font_40.size(decount_page)[0]
            x1 = w_origine/2 + longueur_decompte + 10
            x2 = w_origine/2 - longueur_decompte - 20            
            use_list = page[zone]
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
                surface = pygame.Surface((rect_case.w,rect_case.h))
                surface.fill((0,0,0))
                color_auteur = blanc if Gerer_requete.est_bytes(doc) else (255,0,0)
                draw_text(color = color_auteur,contener = surface,
                          text = f"{nom_projet} par {auteur}", x = 10,
                          y = 0, font = font_paragraphe,
                          size = 30, importer = True)
                draw_text(color = blanc,contener = surface,
                          text = text_date, x = rect_case.w - font_30.size(text_date)[0] - 20,
                          y = 5, importer = True,
                          size = 30, font = font_paragraphe)
                if len(use_list) > 3:
                    screen.blit(surface,(liste_indicex[index],liste_indicey[index]))
                else:
                    screen.blit(surface,(w_origine/2 - long_case/2, liste_indicey[index]))
                
                pygame.draw.rect(screen,(255,255,255),rect_case,2)
                case_data = {"nom_projet" : nom_projet, "contenu" : text, "auteur" : auteur, "date" : date,"rect" : rect_case,"doc" : doc,"id" : id_,"extension" : file}
                if can_add:
                    pygame.display.flip()
                    all_case_data.append(case_data)
            can_add = False         
    
    def start_tuto(data):
        text = data["contenu"]
        auteur = data["auteur"]
        date = data["date"]
        id_ = data["id"]
        date = datetime.datetime.strptime(date,"%d/%m/%Y")
        nom_projet = data["nom_projet"]
        doc = data["doc"]
        file = data["extension"]
        print(doc[:2])
        print(bool(doc))
        print(text)
        if not Gerer_requete.est_bytes(doc):
            page_info(2,text,nom_projet,auteur,date,id_)
        else:
            Gerer_requete.demarrer_fichier(doc = doc, ext = file)
            
    def research(data):
        """        global detail,can_add
        can_add = True
        detail = Gerer_requete.rechercher_data(nom_auteur = data["nom_auteur"], nom_tuto = data["nom_projet"])
        num_resultat = len(detail)
        return num_resultat
        """
        global processing
        processing = True
        global have_supprime
        have_supprime = False   
        global detail,can_add,access,display,num_resultat,flop_de_recherche
        can_add = True
        access = False
        detail = Gerer_requete.rechercher_data(nom_auteur = data["nom_auteur"], nom_tuto = data["nom_projet"])
        processing = False
        num_resultat = len(detail)
        if detail != [None]:
            access = True
        else:
            flop_de_recherche = True
        display = True
        
  
            
    global continuer
    global finish
    global have_supprime
    have_supprime = False
    finish = False
    rect_goback = pygame.Rect(5,5,20,20)
    go_back = False
    font_paragraphe = apple_titre
    font_40 = pygame.font.Font(font_paragraphe, 40)
    font_30 = pygame.font.Font(font_paragraphe,30)
    font_20 = pygame.font.Font(font_paragraphe,20)
    longueur_recherche = w_origine - 400
    surface_rechercher = pygame.Surface((longueur_recherche, 70))
    rect_btn = pygame.Rect(0,0,50,20)
    rect_rechearch = pygame.Rect(100,150,longueur_recherche,70)
    rect_btn.x = 100 + (longueur_recherche) - 100
    rect_btn.y = 150 + 70/2 - 20/2
    input_research = input_apple
    barre_input = pygame.Surface((2,25))
    barre_input.fill(blanc)
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
    surface_type_recherche = pygame.Surface((100,60))
    indice_type = 0
    text_rechercher = "-- Recherche par --"
    rect_aide = pygame.Rect(0,0,100,50)
    surface_aide = pygame.Surface((100,50))
    rect_aide.x = w_origine - rect_aide.w - 50
    rect_aide.y = 25
    while continuer:
        clock.tick(120)
        dict_recherche = {"nom_projet" : None,"nom_auteur" : None}
        mouse = pygame.mouse.get_pos()
        screen.fill(fond_ecran)
        if processing:
            draw_text("Processing...", x = w_origine/2 - font_40.size("Processing...")[0]/2, y = h_origine/2,size=40)
        surface_rechercher.fill((0,0,0))
        pygame.draw.rect(surface_rechercher,(255,255,255),(0,0,w_origine - 400,70),2)
        mouse_click = pygame.mouse.get_pressed()[0]
        for event in pygame.event.get():
            if active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        input_host += " "
                    elif event.key == pygame.K_BACKSPACE:
                        input_host = input_host[:-1]
                    elif event.key == pygame.K_RETURN:
                        recherche_type = liste_rech[indice_type+2]
                        dict_recherche[recherche_type] = input_host
                        th = threading.Thread(target = research,args=(dict_recherche,),daemon= True)
                        if not th.is_alive():
                            th.start()                        
                        """
                        num_resultat = research(dict_recherche)
                        access = True
                        display = True
                        """
                    elif event.key == pygame.K_ESCAPE:
                        pass
                    elif event.key == pygame.K_TAB:
                        pass                       
                    else:
                            
                        if len(input_host) < max_letter:
                            input_host += event.unicode
            for index,data_recup in enumerate(all_case_data):
                if all_case_data[index]["rect"].collidepoint(mouse):
                    text_on = data_recup["id"]
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
                        start_tuto(data_recup)
                        
            for index,values in enumerate(dict_rect_fleche):
                if values.collidepoint(mouse):
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if zone + add_fleche[index] > 0 and zone + add_fleche[index] < len(page):
                            zone += add_fleche[index]
            if rect_type_recherche.collidepoint(mouse):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if indice_type < len(dict_recherche) - 1:
                        indice_type += 1
                    else:
                        indice_type = 0
            if rect_aide.collidepoint(mouse):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    Gerer_requete.demarrer_fichier(doc = "SYLVER.docx",with_path=True,ext = None)
            
            if event.type == pygame.QUIT:
                continuer = False
                break
            if rect_goback.collidepoint(mouse) and mouse_click:
                go_back = True
            if rect_rechearch.collidepoint(mouse) and not rect_btn.collidepoint(mouse):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    active = not active
                    if len(input_host) == 0 and not active:
                        input_host = phrase_base
                    if active and input_host == phrase_base:
                        input_host = ""            
            if rect_btn.collidepoint(mouse):
                if mouse_click and bool(input_host):
                    access = False
                    display = True
                    have_supprime = True
        couleur = (255,0,0) if not rect_btn.collidepoint(mouse) else (255,255,255)
        blit_input = input_research.render(input_host,True,(255,255,255))
        center_y = rect_rechearch.h/2 - input_research.size(input_host)[1]/2
        surface_rechercher.blit(blit_input,(5,center_y))
        #crée un rect semblable a la surface et a la bonne pos
        rect_surf_rechercher = pygame.Rect(100,150,surface_rechercher.get_width(),surface_rechercher.get_height())
        if active:
            if not take_time:
                time_start = pygame.time.get_ticks()
                take_time = True
            time = int(pygame.time.get_ticks() - time_start)/1000
            surface_rechercher.blit(barre_input, (5 + input_research.size(input_host)[0],2 + input_research.size(input_host)[1]/2))
            if int(time) % 2 == 0:
                surface_rechercher.fill((0,0,0), (5 + input_research.size(input_host)[0],2 + input_research.size(input_host)[1]/2,2,25))
        else:
            time = 0
            take_time = False
         
        screen.blit(surface_rechercher,(100,150))    
           
        pygame.draw.rect(screen,couleur,rect_btn)
        fond_nav.fill((0,0,0))
        screen.blit(fond_nav,(0,0))
        title("Bienvenue Dans l'espace recherche!")       
        pygame.draw.rect(screen,bleu_s,rect_type_recherche)
        surface_type_recherche.fill(bleu_s)
        pygame.draw.rect(surface_type_recherche,(255,255,255),(0,0,rect_type_recherche.w,rect_type_recherche.h),2)
        draw_text(contener = surface_type_recherche,
                  text = liste_rech[indice_type],
                  x = rect_type_recherche.w/2 - font_30.size(liste_rech[indice_type])[0]/2,
                  y = rect_type_recherche.h/2 - font_30.size(liste_rech[indice_type])[1]/2,size = 30,
                  font = font_paragraphe,
                  importer = True)
        draw_text(text = text_rechercher,
                  x = rect_type_recherche.x
                  + rect_type_recherche.w/2 - font_30.size(text_rechercher)[0]/2,
                  y = rect_type_recherche.y - 50,
                  color = bleu_s, importer = True, font = font_paragraphe,size = 30,
                  ombre = True)
        screen.blit(surface_type_recherche,rect_type_recherche)
        surface_aide.fill(fond_ecran)
        pygame.draw.rect(surface_aide,blanc,(0,0,rect_aide.w,rect_aide.h),1)
        draw_text("AIDE", contener = surface_aide,
                  x = rect_aide.w/2 - font_30.size("AIDE")[0]/2,
                  font = font_paragraphe, y = rect_aide.h/2 - font_30.size("AIDE")[1]/2,
                  importer = True, size = 30)
        screen.blit(surface_aide,(rect_aide.x,rect_aide.y))
        if display:
            display_result(num_resultat)
        pygame.draw.rect(screen,(0,0,0),rect_goback)
        draw_text(text_on,color = (255,255,255),
                  x =0,
                  y = 0, font = chivo_titre,
                  size = 30)
        if go_back:
            break
        pygame.display.update(rect_surf_rechercher)
        pygame.display.flip()
        
        
def relative_at(rect : pygame.Rect,relative : pygame.Rect) -> pygame.Rect:
    return pygame.Rect(rect.x - relative.x,rect.y - relative.y,rect.w,rect.h)
         
def compte():
    global connect
    def take_file():
        pass

    def look_valid(zone):
        for key,value in dict_input[zone].items():
            if key != "input_mdp":
                if len(value["input"]) <= 0 or value["input"] == value["default"]:
                    return False
            else:
                if len(value["input_visible"]) <= 0 or value["input_visible"] == value["default"]:
                    return False
        return True
    
    def look_mdp(zone):
        return len(dict_input[zone]["input_mdp"]["input_visible"]) >= dict_input[zone]["input_mdp"]["min"]
        
    def write_connection_tools(pseudo,mdp):
        with open("compte_connecter.txt","w") as fichier:
            fichier.write(f"{pseudo}\n{mdp}")
    
    def look_for_connection_tools():
        with open("./compte_connecter.txt", "r") as fichier:
            return len(fichier.read().splitlines()) != 0
        
    text_edit = "Clickez pour editer"
    text_creer_compte = "Bienvenue parmis nous ! Creez votre compte :)"
    text_con_compte = "Bon retour parmis nous ! Connectez vous :)"
    global continuer
    rect_goback = pygame.Rect(5,5,20,20)
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
    with open(os.path.join("img_base","photo_profil_user.png"),"rb") as fichier:
        pp_base = fichier.read()
        
    with open(chemin_pp,"wb") as fichier:
        fichier.write(pp_base)
    image_pp = pygame.image.load(chemin_pp)
    image_pp = pygame.transform.scale(image_pp,size)
    surf2 = pygame.Surface(size, pygame.SRCALPHA)
    surf3 = pygame.Surface(size, pygame.SRCALPHA)
    surf2g = pygame.Surface(size_grand,pygame.SRCALPHA)
    surf3g = pygame.Surface(size_grand,pygame.SRCALPHA)
    rect_host = pygame.Rect(0,0,w_origine/3,h_origine - 400)
    rect_ctn_host = pygame.Rect(0,0,rect_host.w/2,rect_host.h)
    rect_host.y = h_origine/2 - rect_host.h/2
    rect_host.x = w_origine/2 - (rect_host.w + rect_ctn_host.w -20)/2
    rect_ctn_host.x = w_origine/2 - (rect_host.w + rect_ctn_host.w -20)/2 + rect_host.w - 20
    rect_ctn_host.y = rect_host.y
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
    dict_input = [
                {
                "input_nom" : {"can_space" : True,"max" : 50, "input" : 'Nom', "default" : "Nom", "active" : False,"coupage" : 0,"depasse" : False,"rect_w" : rect_input_nom.w},
                "input_prenom" : {"can_space" : True,"max" : 50, "input" : 'Prenom', "default" : "Prenom", "active" : False,"coupage" : 0,"depasse" : False,"rect_w" : rect_input_nom.w},
                "input_pseudo" : {"can_space" : False,"max" : 50, "input" : 'Pseudo', "default" : "Pseudo", "active" : False,"coupage" : 0,"depasse" : False,"rect_w" : rect_input_nom.w},
                "input_age" : {"can_space" :  False,"max" : 3, "input" : 'Age', "default" : "Age", "active" : False,"coupage" : 0,"depasse" : False,"rect_w" : rect_input_age.w},
                "input_mdp" : {"can_space" : True,"max" : 20, "input_cache" : 'Mot de passe',"input_visible" : "", "default" : "Mot de passe","min" : 8, "active" : False,"coupage" : 0,"depasse" : False,"rect_w" : rect_input_mdp.w}
                },
                {
                "input_pseudo" : {"can_space" : False,"max" : 50, "input" : 'Pseudo', "default" : "Pseudo", "active" : False,"coupage" : 0,"depasse" : False,"rect_w" : rect_input_pseudo2.w},
                "input_mdp" : {"can_space" :  True,"max" : 20, "input_cache" : 'Mot de passe',"input_visible" : "", "default" : "Mot de passe","min" : 8, "active" : False,"coupage" : 0,"depasse" : False,"rect_w" : rect_input_mdp2.w}
                }
                ]
    
    if look_for_connection_tools():
        with open("./compte_connecter.txt","r") as fichier:
            li = fichier.read().splitlines()
            con_pseudo = li[0]
            con_mdp = li[1]
        dict_input[1]["input_pseudo"]["input"] = con_pseudo
        dict_input[1]["input_mdp"]["input_visible"] = con_mdp
        dict_input[1]["input_mdp"]["input_cache"] = "*"*len(con_mdp)
        
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
    rect_visible = pygame.Rect(0,0,40,20)
    rect_visible.x = rect_input_mdp.x + rect_input_mdp.w - rect_visible.w - 10
    rect_visible.y = rect_input_mdp.y + rect_input_mdp.h/2 - rect_visible.h/2
    invalid_mdp = False
    text_nmdp = "Minimum 8 caractères"
    text_log = "Vous avez déjà un compte ? connectez vous !"
    text_con = "Vous n'avez pas encore de compte ? creez en un !"
    coupage, line, size_y = make_line(text=text_log,font = font_40, size_max = rect_ctn_host.w - 20)
    coupage2, line2, size_y2 = make_line(text=text_con,font = font_40, size_max = rect_ctn_host.w - 20)
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
    disposition = [
        {
            "rect_valider_x" : 10 + rect_ctn_host.w/2 - rect_valider.w/2,
            "rect_valider_y" : rect_ctn_host.y + rect_ctn_host.h/2 - rect_valider.h/2 + size_y/2 + 30,
            "btn_submit_x" : rect_host.w/2 - btn_submit.w/2,
            "btn_submit_y" : rect_host.y + rect_host.h - btn_submit.h - 30,
            "rect_host_x" : w_origine/2 - (rect_host.w + rect_ctn_host.w -20)/2,
            "rect_ctn_host_x" : w_origine/2 - (rect_host.w + rect_ctn_host.w -20)/2 + rect_host.w - 20,
            "rect_editer_photo_x" : rect_host.w/2 - rect_editer_photo.w/2,
            "rect_editer_photo_y" : y_photo + 130,
            "top_right" : 20,
            "top_left" : 0,
            "bottom_right" : 20,
            "bottom_left" : 0,
            "switch" : text_switch_log,
            "outil_line" : (coupage,line,size_y),
            "text_log" : text_log,
            "ajout_con" : 10,
            "rect_visible_x" : rect_input_mdp.w - rect_visible.w - 10,
            "rect_visible_y" : rect_input_mdp.h/2 - rect_visible.h/2,
            "coupage" : coupage,
            "line": line,
            "size_y" : size_y,
            "text_bienvenu" : text_creer_compte
            },
        {
            "rect_valider_x" :  -10 + rect_ctn_host.w/2 - rect_valider.w/2,
            "rect_valider_y" : rect_ctn_host.y + rect_ctn_host.h/2 - rect_valider.h/2 + size_y/2 + 59,
            "btn_submit_x"  : rect_host.w/2 - btn_submit.w/2,
            "btn_submit_y" : rect_host.y + rect_host.h - btn_submit.h - 20,
            "rect_ctn_host_x" : w_origine/2 - (rect_host.w + rect_ctn_host.w+20)/2 +20,
            "rect_host_x" : w_origine/2 - (rect_host.w + rect_ctn_host.w +20)/2 + rect_ctn_host.w,
            "rect_editer_photo_x" : rect_host.w/2 - rect_editer_photo.w/2,
            "rect_editer_photo_y" : y_photo + 130,
            "top_right" : 0,
            "top_left" : 20,
            "bottom_right" : 0,
            "bottom_left" : 20,
            "switch" : text_switch_con,
            "outil_line" : (coupage2,line2,size_y2),
            "text_log" : text_con,
            "ajout_con" : -10,
            "rect_visible_x" : rect_input_mdp.w - rect_visible.w - 10,
            "rect_visible_y" : rect_input_mdp.h/2 - rect_visible.h/2,
            "coupage" : coupage2,
            "line": line2,
            "size_y" : size_y2,
            "text_bienvenu" : text_con_compte
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
    global user
    color_bordure_image = (0,0,0)
    bordure = 1
    pp_choisi = False
    rect_ellipse = None
    while continuer:
        zone = 0 if creer_compte else 1
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
                if mouse_click:
                    check_save_con_data = not check_save_con_data
            if (rect_editer_photo.collidepoint(mouse) or collide_image) and (zone == 0 or connect):
                if mouse_click:
                    try:
                        path_ext = User.get_file(1)
                        path = path_ext[0]
                        img = resizeImage(path)                        
                        try:
                            surf_image,rect_ellipse,image_photo_pp = img.try_to_resize(screen)
                            
                            if not connect:
                                surf_image = pygame.transform.smoothscale(surf_image,size)
                            else:
                                surf_image = pygame.transform.smoothscale(surf_image,size_grand)
                            
                            try:                                
                                with open(path,"rb") as fichier:
                                    nv_pp = fichier.read()
                                with open(chemin_pp,"wb") as fichier:
                                    fichier.write(nv_pp)
                                if connect:
                                    print("1")
                                    user.change_element(photo_pp= True,Nouvelle_value=nv_pp)
                                    print("2")
                                    user.change_element(rect_pp = True,Nouvelle_value=rect_ellipse)
                                pp_choisi = True
                            except OSError:
                                Gerer_requete.fail_open()    
                                                                
                            except Exception:
                                Gerer_requete.error_occured()
                                
                        except AnnuleCropPhoto as err:
                            print(err.what)         
                                           
                    except noFileException:
                        print("wow")
                    """
                    path_ext = User.get_file(1)
                    path = path_ext[0]
                    if path != 0:
                        try:
                            with open(path,"rb") as fichier:
                                nv_pp = fichier.read()
                            with open(chemin_pp,"wb") as fichier:
                                fichier.write(nv_pp)
                        except:
                            pass
                        finally:
                            if connect:
                                transform_s = size_grand
                                user.photo_profil = nv_pp
                            else:
                                transform_s = size
                            image_pp = pygame.image.load(chemin_pp)
                            image_pp = pygame.transform.scale(image_pp,transform_s)
                    """
            if connect:
                if btn_disconnect.collidepoint(mouse):
                    if mouse_click:
                        connect = False
                        del user
                        image_pp = pygame.transform.smoothscale(image_pp,size)
                        surf_image = pygame.transform.smoothscale(surf_image,size)                        
                elif rect_postimg.collidepoint(mouse):
                    if mouse_click:
                        try:
                            #d'abord faire une input pour pouvoir entrer le nom du tuto a poster
                            path = User.get_file(1)[0]
                            Gerer_requete(user).save_tuto(path,"","Je teste de poste")
                        except noFileException:
                            print("tu joues avec les nerfs de mon appli")                    
                            
                elif rect_maketuto.collidepoint(mouse):
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        pass
            elif creer_compte or not creer_compte:
                if rect_visible.collidepoint(mouse):
                    if mouse_click:
                        visible = not visible
                   
                elif rect_editer_photo.collidepoint(mouse):
                    color_edit = (0,200,0)
                    if mouse_click:
                        color_edit = (200,0,0)
                else:
                    color_edit = (0,0,200)
                if btn_submit.collidepoint(mouse):
                    if mouse_click:
                        if look_valid(zone):
                            if User.verifier_pseudo(dict_input[zone]["input_pseudo"]["input"]):
                                if zone == 0:
                                    if look_mdp(0):
                                        try:
                                            nom = dict_input[0]["input_nom"]["input"]
                                            prenom = dict_input[0]["input_prenom"]["input"]
                                            age = int(dict_input[0]["input_age"]["input"])
                                            pseudo = dict_input[0]["input_pseudo"]["input"]
                                            mdp = dict_input[0]["input_mdp"]["input_visible"]
                                            with open(chemin_pp,"rb") as fichier:
                                                photo_profil = fichier.read()
                                            user = User(nom,prenom,age,pseudo,mdp,photo_profil,rect_ellipse)
                                            user.save_user()
                                            connect = True
                                            creer_compte = False
                                            with open(chemin_pp,"wb") as fichier:
                                                try:
                                                    fichier.write(user.photo_profil)
                                                except:
                                                    fichier.write(pp_base)
                                            if check_save_con_data:
                                                write_connection_tools(pseudo,mdp)
                                            image_pp = pygame.image.load(chemin_pp)
                                            image_pp = pygame.transform.scale(image_pp,size_grand)
                                        except:
                                            pass
                                    else:
                                        invalid_mdp = True
                                else:
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
                                            with open(chemin_pp,"wb") as fichier:
                                                try:
                                                    fichier.write(user.photo_profil)
                                                except:
                                                    fichier.write(pp_base)
                                            if check_save_con_data:
                                                write_connection_tools(pseudo,mdp)
                                            if user.photo_profil == None:
                                                image_pp = pygame.image.load(chemin_pp)
                                                image_pp = pygame.transform.smoothscale(image_pp,size_grand)
                                            else:
                                                print(user.rect_pp)
                                                rect_pp = user.rect_pp
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
                                                img_trans = resizeImage.rendre_transparent(img_,rect_pp)
                                                surf2g = pygame.Surface(size_grand, pygame.SRCALPHA)
                                                surf_image2 = pygame.Surface(size_grand, pygame.SRCALPHA)
                                                pygame.draw.ellipse(surf2g, (255, 255, 255), (0,0,*size_grand))
                                                surf_image2.blit(surf2g, (0, 0))
                                                surf_image2.fill((0,0,0,0))
                                                surf_image2.blit(img_trans, (0, 0),rect_pp)
                                                
                                        except userNonCharger:
                                            pas_correspondance = True
                                        """
                                        user = User.log_user(pseudo,mdp)
                                        if user == False:
                                            pas_correspondance = True
                                        else:
                                            connect = True
                                            with open(chemin_pp,"wb") as fichier:
                                                try:
                                                    fichier.write(user.photo_profil)
                                                except:
                                                    fichier.write(pp_base)
                                            image_pp = pygame.image.load(chemin_pp)
                                            image_pp = pygame.transform.scale(image_pp,size_grand)
                                        """
                                    else:
                                        invalid_mdp = True
                        else:
                            invalid_champ = True
                        
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
                                                if event.unicode != " ":
                                                    value["input"] += event.unicode
                                                    if value["depasse"]:
                                                        value["coupage"] += 1                                        
                                    else:
                                        if len(value["input_visible"]) < value["max"]:
                                            if event.unicode != "":
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
            rect_input_mdp = all_rect[zone][-1]
            rect_save_user_data.x = rect_input_mdp.x
            rect_save_user_data.y = rect_input_mdp.y + rect_input_mdp.h + 5
            text_log = disposition[zone]["text_log"]
            coupage = disposition[zone]["coupage"]
            line = disposition[zone]["line"]
            size_y = disposition[zone]["size_y"]
            text_switch_log_con = disposition[zone]["switch"]
            text_bienvenu = disposition[zone]["text_bienvenu"]
            #gestion des champs invalides
            if invalid_champ:
                if not take:
                    time_start = pygame.time.get_ticks()
                    take = True
                time = pygame.time.get_ticks() - time_start
                draw_text(f"*{text_invalid}*", font = font_paragraphe,
                      size = 20, x = w_origine/2 - font_20.size(text_invalid)[0]/2,
                      y = rect_host.y - 30,importer = True,color = (200,0,0))
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
                      y = rect_host.y - 30,importer = True,color = (200,0,0))
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
                      y = rect_host.y - 30,importer = True,color = (200,0,0))
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
           
            draw_text(text_bienvenu, font = font_paragraphe,
                    size = 60, x = w_origine/2 - font_60.size(text_bienvenu)[0]/2,
                    y = 20,importer = True)
            Surface_host.fill((255,255,255,0))
            couleur_save_user_data = (255,0,0) if not check_save_con_data else (0,255,0)
            pygame.draw.rect(Surface_host,blanc,(0,0,rect_host.w,rect_host.h),0,20)
            pygame.draw.rect(Surface_host,(0,0,0),(0,0,rect_host.w,rect_host.h),2,20)
            pygame.draw.rect(Surface_host,couleur_save_user_data,(rect_save_user_data.x - rect_host.x,rect_save_user_data.y - rect_host.y,
                            rect_save_user_data.w,rect_save_user_data.h))
            draw_text(contener = Surface_host, text = "Restez connecter",x = rect_save_user_data.x - rect_host.x + rect_save_user_data.w + 10,
                      y = rect_save_user_data.y - rect_host.y - 2, font = "Arial")
            pygame.draw.rect(screen,(220,220,220),(rect_ctn_host))
            pygame.draw.rect(screen,(0,0,0),(rect_ctn_host),2,
                             border_top_right_radius = disposition[zone]["top_right"],
                             border_bottom_right_radius = disposition[zone]["bottom_right"],
                             border_top_left_radius = disposition[zone]["top_left"],
                             border_bottom_left_radius = disposition[zone]["bottom_left"])
            screen.blit(Surface_host,(rect_host.x,rect_host.y))            
            color_submit = bleu_s if not btn_submit.collidepoint(mouse) else (255,255,255)
            pygame.draw.rect(screen,color_submit,btn_submit,0,10)
            pygame.draw.rect(screen,(0,0,0),btn_submit,1,10)            
            draw_text("VALIDER", x = btn_submit.x + btn_submit.w/2 - font_20.size("VALIDER")[0]/2,
                      y = btn_submit.y + btn_submit.h/2 - font_20.size("VALIDER")[1]/2,
                      font = font_paragraphe, importer = True)
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
                    color_bordure_image = (5,180,0)
                else:
                    collide_image = False
                    color_bordure_image = (0,0,0)
            else:                
                color_bordure_image = (0,0,0)
                collide_image = False
            Surface_edit_photo.fill((0,0,0,0))
            if zone == 0:
                draw_text(contener = Surface_edit_photo, text = text_edit,
                        x = rect_editer_photo.w/2 - font_20.size(text_edit)[0]/2, y = 0,
                        font = font_paragraphe, importer = True,
                        size = 20, color = color_edit)           
            for rect in all_rect[zone]:
                pygame.draw.rect(screen,(fond_ecran), rect)
                pygame.draw.rect(screen,(0,0,0), rect,1)
            for i in range(line):
                start = coupage[i]
                if i != line -1:
                    limite = coupage[i+1]
                else:
                    limite = len(text_log)
                draw_text(f"{text_log[start:limite]}", x = rect_ctn_host.x + disposition[zone]["ajout_con"] + rect_ctn_host.w/2 - font_40.size(f"{text_log[start:limite]}")[0]/2,
                          y = rect_ctn_host.y + rect_ctn_host.h/2 - size_y/2 + (font_40.size(f"{text_log[start:limite]}")[1]) * i,
                          font = font_paragraphe, importer = True, size = 40,color = (0,0,200))
            pygame.draw.rect(screen,(0,0,0),rect_visible)
            pygame.draw.rect(screen,bleu_s,rect_valider,0,40)
            pygame.draw.rect(screen,(00,0,0),rect_valider,1,40)
            draw_text(x = rect_valider.x + rect_valider.w/2 - font_20.size(text_switch_log_con)[0]/2,
                      y = rect_valider.y + rect_valider.h/2 - font_20.size(text_switch_log_con)[1]/2,
                      text = text_switch_log_con, font = font_paragraphe, importer = True)
            i = 0
            for key,value in dict_input[zone].items():
                if key != "input_mdp":
                    input_ = value["input"]
                else:
                    input_ = value["input_cache"] if not visible else value["input_visible"]
                
                if font_20.size(input_)[0] +5 >= value["rect_w"]:
                    value["depasse"] = True
                else:
                    value["depasse"] = False 
                x = all_rect[zone][i].x + 5       
                y = all_rect[zone][i].y +5             
                draw_text(input_[value["coupage"]:], size = 20,
                        x = x,
                        y = y, font = font_paragraphe, importer = True)
                    
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
                screen.blit(surf_image2,(x_photo2,y_photo2))
            mask = pygame.mask.from_surface(surf2g)
            ellipse = pygame.draw.ellipse(screen,color_bordure_image,(x_photo2,y_photo2,*size_grand),1)
            if ellipse.collidepoint(mouse):
                mask_x = mouse[0] - ellipse.left
                mask_y = mouse[1] - ellipse.top
                if mask.get_at((mask_x, mask_y)):
                    collide_image = True
                    color_bordure_image = (5,180,0)
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
        pygame.draw.rect(screen,(0,0,0),rect_goback)
        
        pygame.display.flip()
        if go_back:
            break
        
        
def request():
    global continuer
    rect_goback = pygame.Rect(5,5,20,20)
    go_back = False
    while continuer:
        mouse = pygame.mouse.get_pos()
        screen.fill((100,100,100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
                break
            if rect_goback.collidepoint(mouse) and (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                go_back = True        
        pygame.draw.rect(screen,(0,0,0),rect_goback)
        draw_text("futur request",color = (255,255,255), x = 500,y = 500)
        if go_back:
            break
        pygame.display.flip()

        
fond_ecran = (210, 223, 228)
bleu_s = (106,178,202)
taille_origine = pygame.display.Info()
print(taille_origine)
w_origine = taille_origine.current_w
h_origine = taille_origine.current_h
continuer = True
connect = False
comic_sans_ms = pygame.font.SysFont("Comic Sans Ms", 20)
csm = "Comic Sans Ms"
arial = "Arial"
chivo_titre = r"dossier_police\chivo\Chivo-Black.otf"
dream_orphans = r"dossier_police\dream_orphans\Dream Orphans.otf"
apple_titre = r"dossier_police\apple_garamond\AppleGaramond-Light.ttf"
input_apple = pygame.font.Font(apple_titre,40)
beackman = r"dossier_police\Beckman.otf"
TNN = r"dossier_police\TNN.ttf"
blanc = (255,255,255)
noir = (0,0,0)
proposition = ["MENU","ANNONCE","COMPTE"]
etat = ["alpha","beta","alpha"]
size_box_w = 200
size_box_h = 50
millieu_w = (w_origine/2) - size_box_w/2
millieu_h = (h_origine/2) - size_box_h/2
pos = [[millieu_w,millieu_h - 4 * size_box_h],[millieu_w,millieu_h],[millieu_w,millieu_h + 4* size_box_h]]
rect_dispo = []
color = [(0,0,0)]*3
color_text = [(255,255,255)]*3
text_choose = ""
droite = [True] * 3
reference = w_origine
accueil = "BIENVENUE DANS SYLVER_SERVICE"
font_accueil = pygame.font.SysFont("Comic Sans Ms", 40)
fond_nav = pygame.Surface((w_origine,100))
info = pygame.Rect(w_origine - 40, 5, 20,20)
font_chivo = pygame.font.Font(chivo_titre,40)

def title(text, size = 40, color = blanc, font = font_chivo,importer = True):
    draw_text(text, size = size,color = color, x = (w_origine/2 - font.size(text)[0]/2), y = 5,importer = importer, font = chivo_titre)


clock = pygame.time.Clock()

def gestion_event():
    global continuer
    while continuer:
        try:
            if keyboard.is_pressed("Escape"):
                print(threading.current_thread())
                continuer = not User.confirm_close()
        except:
            print("f")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
        time.sleep(0.1)
    print("bye")


t1 = threading.Thread(target=gestion_event,daemon=True)
t1.start()
dict_fontion = {0 : lambda : menu(), 1: lambda : request(), 2 : lambda : compte()}
rect_choose = pygame.Surface((size_box_w,size_box_h))
w,l = rect_choose.get_size()
clock = pygame.time.Clock()
while continuer:
    mouse = pygame.mouse.get_pos()
    screen.fill((0,25,25))
    fond_nav.fill((0,0,0))
    screen.blit(fond_nav,(0,0))
    draw_text(accueil, size = 40,color = blanc, x = w_origine/2 - font_chivo.size(accueil)[0]/2, y = 5, font = chivo_titre,importer = True)
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
                        color[index] = blanc
                        color_text[index] = noir
                    decal = 200
                    pos_souris_relat_souris = (mouse[0] - rect.x, mouse[1] - rect.y)
                    if etat[index] == "beta":
                        if pos_souris_relat_souris[0] > size_box_w/2:
                            if pos[index][0] - decal > 0:
                                pos[index][0] -= decal
                            else:
                                pos[index][0] += decal
                        else:
                            if pos[index][0] + decal < w_origine - 200:
                                pos[index][0] += decal
                            else:
                                pos[index][0] -= decal
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if text_choose == "MENU":
                            menu()
                        elif text_choose == "ANNONCE":
                            request()
                        else:
                            compte()
                else:
                    color[index] = (0,0,0)
                    color_text[index] = blanc
    
    date = datetime.datetime.today().strftime('%Hh%M')
    draw_text(date, size = 20, color = blanc, x = w_origine - 70, y = 110)
    pygame.draw.rect(screen,(255,255,255),info)
    clock.tick(144)
    fps = clock.get_fps()
    draw_text(f"fps : {int(fps)}",x=10,y=200,color=(255,255,255))

    rect_dispo = []
    for index,elt in enumerate(proposition):
        rect_choose.fill(color[index])
        color_bord = (255,0,255) if color[index] == noir else (0,255,255)
        pygame.draw.rect(rect_choose,color_bord,(0,0,w,l),1)
        draw_text(proposition[index],contener = rect_choose,color = color_text[index], x = 5)
        screen.blit(rect_choose,pos[index])
        rect_dispo.append(pygame.Rect(pos[index][0],pos[index][1],w,l))
    draw_text(text_choose,color = blanc, x = 5)
    pygame.display.flip()
pygame.quit()
sys.exit()