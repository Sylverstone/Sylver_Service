import pygame
from Sylver_filedialog import BoiteDialogPygame
from fonction_ui import *

def look_valid(dict_input):
    for key,value in dict_input.items():
        if len(value["input"]) > 1:
            if " ".join(value["input"]).strip() in ("", " "):
                return False
        else:
            if (value["input"][0] == value["Default"] or value["input"][0].strip() in (""," ")) and key != "Input_emails":
                return False
    return True 

def add_to_texte(text,cursor,ajout):
    return text[:len(text) + cursor] + ajout + text[len(text) + cursor:]
def contact(continuer : bool, fond_nav : pygame.Surface,w_origine : int, h_origine : int, screen : pygame.Surface,image_retour : pygame.Surface, dialog : BoiteDialogPygame,
            rect_goback : pygame.Rect,user : User):
    
    blanc = (255,) * 3
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
    text_envoyer = "Envoyez"
    taille_envoyez = font(font_paragraphe,30,True).size(text_envoyer)
    go_back = False
    dernier_ecran = screen.copy()
    while continuer and not go_back:
        screen.fill(palette_couleur.Gris_clair)
        fond_nav.fill(palette_couleur.Noir)
        screen.blit(fond_nav,(0,0))
        title("Envoyez nous un email :)",screen=screen)
        mouse = pygame.mouse.get_pos()
        screen.blit(image_retour,(5,5))
        try:
            for event in pygame.event.get():
                if rect_valider.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if look_valid(dict_input):
                        pass
                    else:
                        dialog.message("Veuillez bien complétez les cases avant d'envoyez",dernier_ecran,"Contact")
                    
                if handleEscape(event,screen,dernier_ecran):
                    continuer = False
                    break
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
        except Exception as e:
            print(e)
            pass
        if rect_valider.collidepoint(mouse):
            pygame.draw.rect(screen,(0,0,0),rect_valider,0,20)
        pygame.draw.rect(screen,palette_couleur.Bleu,rect_valider,3,20)
        
        
        draw_text(text_envoyer,font_paragraphe,blanc,rect_valider.x +rect_valider.w/2 - taille_envoyez[0]/2,rect_valider.y +rect_valider.h/2 - taille_envoyez[1]/2,size = 30, importer=True,contener=screen)
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
    return continuer