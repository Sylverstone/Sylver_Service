from typing import List,Dict,Tuple
from Class.Gerer_requete import Gerer_requete
from Class.customException import *
from fonction_ui import draw_text, font,verification_size,handleEscape,title,processus_delete_tuto
from font_import import *
from Class.Tuto import Tuto
from Class.User import User
import datetime,pygame
from Class.Color import Color
import io
from Resize_image import resizeImage

from base_variables import *


def menu(id_ : int = 0,auteur_rechercher : str = None,
         user : User = None, page_info = None, connect : bool = False, image_pp_user : pygame.Surface = None,
         input_apple = None, last_screen_accueil : pygame.Surface = None) -> bool:
    
    """Fonction permettant de rechercher des tutos | elle sert également a image_userr tout les tutos d'un utilisateur

    Args:
        id_ (int, optional): _description_. Variable permettant de changer l'utilisation de la fonction to 0.
        auteur_rechercher (str, optional): Auteur recherché si la fonction sert a image_userr les tutos d'un utilisateur. Defaults to None.
    """
    palette_couleur = Color()
    blanc = (255,)*3
    display = False #indicateur si il faut afficher les tutos ou non
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
    page = [] #regroupe les pages donnée des pages de tuto
    #font = pygame.font.SysFont(chivo_titre, 30)
    y_all = h_origine - 100
    can_add = False #sécurité pour controler l'ajout de donné dans la liste
    flop_de_recherche = False #indicateur de si la recherche n'a pas aboutit
    add_fleche = [1,-1]
    
    def display_result(zone_page,all_case_data : List[Dict],can_add : bool,flop_de_recherche : bool,
                       liste_rect_fleche : List[pygame.Rect],
                       access : bool)-> Tuple[List[Dict],bool,bool]:
        
        """Fonction permettant d'image_userr le résultat d'une recherche précise

        Args:
            num (int): nombres de résultats obtenu
        """
        num = len(infos_tuto)
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
                ,ombre = True,contener=screen)        
        page =  []
        if access:
            try:                
                
                count = 0
                sous_list = []
                for i in range(len(infos_tuto)):
                    sous_list.append(infos_tuto[i])
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
                use_list : List[Tuto] = page[zone_page]
                rect_1 = pygame.Rect(x1,y_all,surface_fleche.get_width(),surface_fleche.get_height())
                rect_2 = pygame.Rect(x2,y_all,surface_fleche.get_width(),surface_fleche.get_height())
                liste_rect_fleche.append(rect_1)
                liste_rect_fleche.append(rect_2)
                flèche_droite = pygame.image.load(os.path.join("Image", "flèches_droites.png"))
                flèche_droite = pygame.transform.smoothscale(flèche_droite,(surface_fleche.get_width(),surface_fleche.get_height()))
                flèche_gauche = pygame.image.load(os.path.join("Image", "flèches_gauches.png"))
                flèche_gauche = pygame.transform.smoothscale(flèche_gauche,(surface_fleche.get_width(),surface_fleche.get_height()))
                screen.blit(flèche_droite,(x1,y_all))
                screen.blit(flèche_gauche,(x2,y_all))
                draw_text(decount_page,color = blanc,
                        x = w_origine/2 - longueur_decompte/2,
                        y = y_all,
                        font = font_paragraphe, importer = True,size = int(taille_icone[0]),contener=screen)
                for index,tuto  in enumerate(use_list):
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
                print("error 7 :",e)
                access = False
                flop_de_recherche = True
                dialog.message("Une erreur est survenue ! ", last_screen,title="Erreur")
        return can_add,all_case_data,flop_de_recherche,access,page
                
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
                        animation_ouverture.stop_anime()
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
                animation_ouverture.stop_anime()
                Gerer_requete.demarrer_fichier(dir = dir,doc = doc, ext = file,auteur = auteur, nom_tuto=nom_projet)
            else:
                animation_ouverture.stop_anime()
                return
            text = "Le fichier a été ouvert profitez en :)\nMaintenant vous pouvez donc signalez un tuto visuel et voir tout les autres tutos de l'utilisateur, comme si c'était un tuto texte :) c'est cool non ?"
        page_info(2,text,nom_projet,auteur,date,id_tuto,image_pp,is_document,doc)
                
    def research(data, id_ = 0,flop_de_recherche = False,access = False):
        """Fonction effectuant la recherche

        Args:
            data (dict): donnée au sujet du tuto selectionner
        """


        #global zone_page
        infos_tuto = []
        categorie_rechercher = None
        try:      
            flop_de_recherche = False   
            if id_ == 0:
                infos_tuto,categorie_rechercher = Gerer_requete.rechercher_data(nom_auteur = data["nom_auteur"], nom_tuto = data["nom_projet"], nom_categorie = data["nom_categorie"])
                
            else:
                infos_tuto = Gerer_requete.rechercher_annonce()
                
            infos_tuto : List[Tuto] 
            access = True
            
        except noConnection as e:
            print("error : ",e)
            Gerer_requete.connection_failed()
            
        except noCategorie as e:
            print("error : ",e)
            pass       
             
        except Exception as e:
            print("error : ",e)
            flop_de_recherche = True
            access = False
            Gerer_requete.error_occured()
            
        print("research done")
        return flop_de_recherche,access,infos_tuto,categorie_rechercher
        
    def setup_default_research(flop_de_recherche,dict_recherche):
        flop_de_recherche,access,infos_tuto,categorie_rechercher = research(dict_recherche,flop_de_recherche)
        have_supprime = False
        display = True
        can_add = True
        
        return flop_de_recherche,have_supprime,access,display,can_add,infos_tuto,categorie_rechercher
    
    have_supprime = False
    go_back = False
    font_paragraphe = apple_titre
    font_30 = pygame.font.Font(font_paragraphe,30)
    

    #represente le btn qui efface la recherche
    rect_btn_effacer = pygame.Rect(0,0,50,40)
    rect_rechearch = pygame.Rect(100,fond_nav.get_height() + 50,longueur_recherche,70)
    rect_btn_effacer.x = rect_rechearch.x + rect_rechearch.w - 100
    rect_btn_effacer.y = rect_rechearch.y + rect_rechearch.h/2 - rect_btn_effacer.h/2
    input_research = input_apple
    barre_input = pygame.Surface((3,30))
    barre_input.fill((0,0,0))
    phrase_base ="Appuyer pour Rechercher"
    input_host = phrase_base
    active = False
    max_letter = 50
    access = False
    all_case_data = [] # liste contenant les informations des tutos ! (les tutos sont "mit" dans des cases)
    text_on = ""
    liste_rect_fleche = []
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
    image_effacer_recherche = pygame.image.load(os.path.join("Image","icone_annule_recherche.png"))
    image_effacer_recherche = pygame.transform.smoothscale(image_effacer_recherche,(rect_btn_effacer.w,rect_btn_effacer.h))
    rect_a_ne_pas_depasser = rect_screen.copy()
    rect_a_ne_pas_depasser.w -= (rect_aide.w + 5)
    rect_a_ne_pas_depasser.w -= (rect_goback.w+5)
    text_title = "Bienvenue Dans l'espace recherche !" if id_ == 0 else f"Voici les tutos de l'utilisateur {auteur_rechercher} !"
    text_title = "Voici les annonces les plus récentes de l'applications" if id_ == 2 else text_title
    size_du_titre = verification_size(rect_a_ne_pas_depasser,chivo_titre,size_for_title,text_title,True)
    dict_recherche_base = {"nom_projet" : None,"nom_auteur" : None,"nom_categorie" : None}
    dict_recherche = dict_recherche_base.copy()
    cursor_position = 0
    last_screen = screen.copy()
    infos_tuto = [] 
    animation_chargement.start_anime(last_screen_accueil)
    if id_ == 1:
            dict_recherche["nom_auteur"] = auteur_rechercher
            flop_de_recherche,have_supprime,access,display \
                ,can_add,infos_tuto,categorie_rechercher = setup_default_research(flop_de_recherche,dict_recherche)
          
    if id_ == 2 :
            dict_recherche["nom_projet"] = "*"
            flop_de_recherche,have_supprime,access,display,\
                can_add,infos_tuto,categorie_rechercher = setup_default_research(flop_de_recherche,dict_recherche)
            
    if id_ == 0 and connect and user.categorie != None:
            #faire la recherche par défaut de l'utilisateur
            dict_recherche["nom_categorie"] = user.categorie
            flop_de_recherche,have_supprime,access,display,\
                can_add,infos_tuto,categorie_rechercher = setup_default_research(flop_de_recherche,dict_recherche)
            input_host = user.categorie
            
    animation_chargement.stop_anime()
    continuer = True
    #regroupe les infos de la requete sql
    do_research = False
    while continuer and not go_back:
        pygame.time.Clock().tick(120)
        mouse = pygame.mouse.get_pos()
        screen.fill(fond_ecran)            
        surface_rechercher.fill((0,0,0,0))
        surface_type_recherche.fill((0,0,0,0))
        #boucle evenementielle
        
        for event in pygame.event.get():
            if handleEscape(event,screen,last_screen):
                continuer = False
                break
            if active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        cursor_position -= 1
                        if abs(cursor_position) >= len(input_host):
                            cursor_position = -len(input_host)
                            
                    elif event.key == pygame.K_RIGHT:
                        cursor_position += 1
                        if cursor_position >= 0 :
                            cursor_position = 0
                    elif event.key == pygame.K_SPACE:
                        input_host = input_host[:len(input_host) + cursor_position] + " " + input_host[len(input_host) + cursor_position:]
                    elif event.key == pygame.K_BACKSPACE:
                        input_host =  input_host[:len(input_host) + cursor_position][:-1] +  input_host[len(input_host) + cursor_position:]
                    elif event.key == pygame.K_RETURN:
                        do_research = True
            
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
                                processus_delete_tuto(text_on,last_screen,user,dialog)       
                                
            for index,values in enumerate(liste_rect_fleche):
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
                        texte_confirm_open ="du Menu"
                    else:
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
                
            if rect_rechearch.collidepoint(mouse) and not rect_btn_effacer.collidepoint(mouse) and id_ == 0:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    active = not active
                    if len(input_host) == 0 and not active:
                        input_host = phrase_base
                    if active and input_host == phrase_base:
                        input_host = ""      
                              
            if rect_btn_effacer.collidepoint(mouse):
                if id_ == 0 and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and bool(input_host):
                    print("click on sup")
                    access = False
                    all_case_data = []
                    display = True
                    have_supprime = True
                    input_host = ""
                    dict_recherche = dict_recherche_base.copy()

        if do_research:
            animation_chargement.start_anime(last_screen)
            dict_recherche = dict_recherche_base.copy()
            display = True
            recherche_type = liste_rech[indice_type+3]
            dict_recherche[recherche_type] = input_host
            flop_de_recherche,access,infos_tuto,categorie_rechercher = research(dict_recherche,flop_de_recherche,access)  
            pygame.event.clear()
            can_add = True
            all_case_data = []
            zone_page = 0    
            do_research = False
            animation_chargement.stop_anime()
            
        pygame.draw.rect(surface_rechercher,(255,255,255),(0,0,rect_surf_rechercher[2],rect_surf_rechercher[3]),0,20)
        blit_input = input_research.render(input_host,True,(0,0,0))
        center_y = rect_rechearch.h/2 - input_research.size(input_host)[1]/2
        #il est mieux d'utiliser draw_text car ça va plus vite, mais j'ai fait comme ça
        #en tout cas c'est similaire a draw_text
        surface_rechercher.blit(blit_input,(10,center_y))
        
        if active:
            surface_rechercher.blit(barre_input, (10 + input_research.size(input_host[:len(input_host) + cursor_position])[0],2 + input_research.size(input_host[:len(input_host) + cursor_position])[1]/2))
        
        if id_ == 0:
            screen.blit(surface_rechercher,rect_surf_rechercher)    
            pygame.draw.rect(screen,palette_couleur.Bleu,rect_surf_rechercher,5,20)
            screen.blit(image_effacer_recherche,rect_btn_effacer)
            
        fond_nav.fill(palette_couleur.Noir)
        screen.blit(fond_nav,(0,0))
        title(text_title, size = size_du_titre,screen=screen)       
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
                    color = blanc, importer = True, font = font_paragraphe,size = 30,contener=screen
                    )
            
        if id_ == 0:
            screen.blit(surface_type_recherche,rect_type_recherche)
            
        screen.blit(image_aide,rect_aide)
        if display:
            can_add,all_case_data,flop_de_recherche,access,page = display_result(zone_page,all_case_data,can_add,flop_de_recherche,
                                                                       liste_rect_fleche,access)
        screen.blit(image_retour,rect_goback)
        if id_ == 0:
            draw_text(text_on,color = (255,255,255),
                    x =0,
                    y = 0, font = chivo_titre,
                    size = 30,contener=screen)

        screen.blit(surface_status_co,pos_surface_status_co)
        last_screen = screen.copy()
        pygame.display.flip()
        
    return continuer