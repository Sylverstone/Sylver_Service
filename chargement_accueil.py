import os,pygame
from Class.Animation import Animation
from Class.Gerer_requete import Gerer_requete
from Class.customException import *
from Class.User import User
from Resize_image import resizeImage
from base_variables import *
from fonction_ui import setup_categorie_data

def load_app():
    
    animation_demarrage_application = Animation(screen,color = (255,255,255), text_chargement="Sylver.service",W = w_origine)
    chemin_image_logo_app = os.path.join("Image","Icone_accueil.png")
    image_logo_app = pygame.image.load(chemin_image_logo_app)
    width_logo,height_logo = image_logo_app.get_width(),image_logo_app.get_height()
    r = (w_origine/2)/width_logo
    image_logo_app = pygame.transform.smoothscale(image_logo_app,(width_logo * r,height_logo*r))
    screen.blit(image_logo_app,(w_origine/2 - (width_logo*r)/2,h_origine/2 - (height_logo*r)/2))
    pygame.display.update()

    size_grand = (h_origine * (1-72/100),)*2 #diminution de 75% de la taille originel
    with open(os.path.join("img_base","photo_profil_user.png"),"rb") as fichier:
        pp_base = fichier.read()
    #processus de verification de si l'utilisateur est connecter, si oui, connexion au compte
    connect = False
    user = None
    creer_compte = True
    recup_categorie = []
    dict_categorie = {}
    zone = 0 #zone est soit 0 soit 1
    surf_image2 = None
    with open(os.path.join("Ressource", "compte_connecter.txt"), "r+") as fichier:
        
        contenu = fichier.read().splitlines()
        last_screen = screen.copy()
        if contenu:
            animation_demarrage_application.start_anime(last_screen,20)
            animation_demarrage_application.texte = "Récupération des catégories"
            try:
                recup_categorie = Gerer_requete.take_categorie() #recuperer le nom de toutes les catégories
                dict_categorie = Gerer_requete.update_categorie_member()     
            except noConnection:
                animation_demarrage_application.stop_anime()
                dialog.message("Une erreur de connexion a eu lieu !",last_screen,title="Erreur")
                animation_demarrage_application.start_anime(last_screen,20)
            except Exception as e :
                animation_demarrage_application.stop_anime()
                dialog.message("Une erreur est survenue ! ", last_screen,title="Erreur")
                animation_demarrage_application.start_anime(last_screen,20)
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
                    zone = 1
        else:
            animation_demarrage_application.start_anime(last_screen) 
            try:
                recup_categorie,dict_categorie = setup_categorie_data()
            except Exception as e:
                print("errrrrrrror")
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
    return { "dict_categorie" : dict_categorie , "recup_categorie" : recup_categorie , "connect" : connect, "zone" : zone, 
            'creer_compte' : creer_compte,"pp_base" : pp_base,"size_grand" : size_grand,"user" : user,"surf_image2" : surf_image2}