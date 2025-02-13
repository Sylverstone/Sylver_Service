
import hashlib
import tkinter
import tkinter.filedialog,tkinter.messagebox
import pymysql as sql
import os
import webbrowser
from typing import List

from connection_fonction import connect_to_database
from Class.customException import *
from get_co import connection_principale

from Class.Tuto import Tuto
from Class.Doc import Doc
from Class.status_connection import look_for_connection



def categorie_plus_proche(noms_categories,categorie):
    """Fonction permettant de reperer la catégorie qui ressemble le plus a l'entrée de l'utilisateur par rapport a une liste de forme [(nom,)]

    Args:
        noms_categories (list): liste des catégories existantes
        categorie (str): catégorie entrez par l'utilisateur

    Returns:
        str: La catégorie la plus proche est retourner
    """
    if categorie in noms_categories: 
        return categorie
    
    nom_categorie_use = [c[0] for c in noms_categories if c[0][0].lower() == categorie[0].lower()]
    if len(nom_categorie_use) == 0: 
        return None
    
    if len(nom_categorie_use) == 1:
        return nom_categorie_use[0]
    
    score_with_categorie = {n : 0 for n in nom_categorie_use} #d'abord on calcule le score entre les catégories existante, leur nombre de lettre en commun
    for nom in nom_categorie_use:
        i = 0
        for lettre in nom:
            if i < len(categorie) and lettre.lower() == categorie[i].lower():
                score_with_categorie[nom] += 1
            i+= 1
            
    maxi = 0
    for value in score_with_categorie.values():
        if value > maxi:
            maxi = value
    all_max = [elt for elt in score_with_categorie.keys() if score_with_categorie[elt] == maxi] # On ne garde que les catégories qui on le plus au score avec l'entrée de l'utilisateur
    if len(all_max) == 1:
        return all_max[0]
    difference_de_lettre = {c : len(c) - len(categorie) for c in all_max} #Maintenant on vérifie la différence de taille
    mini = 100
    for value in difference_de_lettre.values():
        if value < mini:
            mini = value
    all_mini = [elt for elt in difference_de_lettre.keys() if difference_de_lettre[elt] == mini] #on garde la categorie avec la plus petite difference de taille
    return all_mini[0]

def changer_valeur_env(valeur,new_valeur):
    """Fonction permettant de changer une version du .env

    Args:
        valeur (str): début de la ligne a changer
        new_valeur (str): nouvelle valeur a y écrire
    """
    chemin_du_env = '.env'
    # Lirele contenu actuel du fichier .env
    with open(chemin_du_env, 'r') as fichier_env:
        lignes = fichier_env.readlines()

    # Modifiez la valeur souhaitée
    for i in range(len(lignes)):
        if lignes[i].startswith(f'{valeur}='):
            lignes[i] = f'{valeur}="{new_valeur}"\n'
            break

    # Écrivez le nouveau contenu dans le fichier .env
    with open(chemin_du_env, 'w') as fichier_env:
        fichier_env.writelines(lignes)   

class Gerer_requete():   
    """Fonction qui gère les actions de l'application hormis les actions incluant l'utilisateur et ses données    """
    
    @staticmethod
    def separe_rect(rect):
        """Fonction permettant de mettre les rects en chaine de caractère pour la base de données

        Args:
            rect (pygame.Rect): Rect a mettre en string

        Returns:
            str: Rect transformer en str separer par des ,
        """
        return f"{rect[0]},{rect[1]},{rect[2]},{rect[3]}"
    
    @staticmethod
    def take_categorie():
        """Fonction récupérant tout sur les catégories

        Raises:
            noConnection: renvoie noConnection quand la connexion n'a pu être initialisé

        Returns:
            list: donnée de toutes les catégories
        """
        no_connection = False     
        data = [[],[]]
        try:
            if look_for_connection():
                with connection_principale.cursor() as cursor:    
                    request = f"SELECT * FROM categorie"
                    cursor.execute(request)
                    data = cursor.fetchall()
            else:
                no_connection = True
        except sql.Error as err:
            no_connection = True
        except Exception as err:
            no_connection = True
        finally:
            if no_connection:
                raise noConnection("connection failed")
            else:
                return data
    
    @staticmethod  
    def rechercher_annonce()->List[Tuto]:
        """Fonction permettant de rechercher des tuto dans la base de données grâce a différente
           données relatives

        Args:
            nom_tuto (str, optional): Nom du tuto rechercher. Defaults to None.
            nom_auteur (str, optional): Nom de l'auteur des tutos rechercher. Defaults to None.

        Raises:
            noConnection: Renvoie noConnection quand la connection n'a pu être établie

        Returns:
            list: Liste comportant tout les tuto retourner
        """
        no_connection = False
        tutos = None
        try:
            
            data_recup = [None]
            if look_for_connection():
                with connection_principale.cursor() as cursor:
                    request = "SELECT * FROM tuto WHERE is_annonce = 1 ORDER BY date DESC"
                    cursor.execute(request)
                    data_recup = cursor.fetchall()
                    tutos = []
                    for tuto in data_recup:
                        tutos.append(Tuto(*tuto))
            else:
                no_connection = True
        except sql.Error as err:
            no_connection = True
            
        except noConnection as err:
            
            no_connection = True
        except Exception as err:
            no_connection = True
            
        finally:
            if not no_connection:
                return tutos
            raise noConnection("l")
             

    @staticmethod  
    def rechercher_data(nom_tuto : str = None,nom_auteur : str = None,nom_categorie = None)->List:
        """Fonction permettant de rechercher des tuto dans la base de données grâce a différente
           données relatives

        Args:
            nom_tuto (str, optional): Nom du tuto rechercher. Defaults to None.
            nom_auteur (str, optional): Nom de l'auteur des tutos rechercher. Defaults to None.

        Raises:
            noConnection: Renvoie noConnection quand la connection n'a pu être établie

        Returns:
            list: Liste comportant tout les tuto retourner
        """
        no_connection = False
        no_categorie = False
        categorie_la_plus_proche = None
        try:
            
            data_recup = [None]
                
            if look_for_connection():
                with connection_principale.cursor() as cursor:
                    request = None
                    if nom_tuto != None:
                        if nom_tuto != "*":
                            request = f" SELECT * FROM tuto WHERE nom LIKE '%{nom_tuto}%' AND is_annonce = 0 ORDER BY date DESC;"
                        else:
                            request = f" SELECT * FROM tuto  WHERE is_annonce = 0 ORDER BY date DESC;"
                    elif nom_auteur != None:
                        request = f"SELECT * FROM tuto WHERE auteur LIKE '{nom_auteur}%' AND is_annonce = 0 ORDER BY date DESC;"
                    elif nom_categorie != None:
                        noms_categories = Gerer_requete.take_categorie("nom")
                        print(noms_categories)
                        categorie_la_plus_proche = categorie_plus_proche(noms_categories,nom_categorie)
                        if categorie_la_plus_proche != None:
                            request = f"SELECT * from tuto WHERE categorie = '{categorie_la_plus_proche}' AND is_annonce = 0 ORDER BY date DESC;"
                    print(request)
                    if request != None:
                        cursor.execute(request)
                        data_recup = cursor.fetchall()
                        tutos = []
                        for tuto in data_recup:
                            tutos.append(Tuto(*tuto))
                    else:
                        raise noCategorie("La catégorie n'existe pas !")
            else:
                no_connection = True
                
        except sql.Error as err:
            print("err 1 : ",err)
            no_connection = True
            
        except noConnection as err:
            print("err 2 : ",err)
            no_connection = True
            
        except noCategorie as err:
            print("err 3 : ",err)
            no_categorie = True
        
        except Exception as err:
            print("err 4 : ",err)
            no_connection = True
            
        finally:
            if not no_connection and not no_categorie:
                return tutos,categorie_la_plus_proche
            if no_connection:
                raise noConnection("l")
            raise noCategorie("La catégorie n'existe pas !")

    @staticmethod
    def demarrer_fichier(doc : bytes | str,ext,with_path = False,nom_tuto = "",auteur = "",dir = None)->None:
        """Fonction permettant de démarrer un fichier

        Args:
            doc (bytes|str): Reprensete soit les bytes du document soit le chemin d'accès 
            ext (str): Reprensente l'extension du document
            with_path (bool, optional): Indique si doc est un str ou non. Defaults to False.
            nom_tuto (str, optional): Nom du projet ouvert. Defaults to "".
            auteur (str, optional): Nom de l'auteur du projet. Defaults to "".
        """
        print("starting file")
        if not with_path:
            #créé le fichier si il n'existe pas
            if dir:
                path = os.path.join(dir,f"{nom_tuto} par {auteur}{ext}")
                document = Doc(path,Gerer_requete,doc,nom_tuto,auteur,ext)
                document.start()
        else:
            path = doc
            document = Doc(path)
            document.start_now()
        
        
    @staticmethod
    def message(text):
        """Fonction permettant d'afficher un warning a l'écran

        Args:
            text(str): Warning a afficher
        """
        root = tkinter.Tk()
        root.withdraw()
        tkinter.messagebox.showwarning("Info",text)
        root.destroy()
        
   
        
    @staticmethod
    def fail_open(nom_fichier = ""):
        """Fonction permettant d'afficher une erreur d'ouverture

        Args:
            nom_fichier (str, optional): Nom du fichier dont l'ouverture a echouer. Defaults to "".
        """
        root = tkinter.Tk()
        root.withdraw()
        tkinter.messagebox.showerror("Erreur",f"WOW ! L'ouverture a flop :( \n Il se peut que le fichier ({nom_fichier}) \nsoit déjà ouvert !")
        root.destroy()
      
    @staticmethod
    def processus_fini(message = "Votre photo de profil a été sauvegardée",temoin = [False,]):
        
        """Fonction permettant d'afficher un message sur un processus fini"""  
        temoin[0] = True
        root = tkinter.Tk()
        root.withdraw()
        tkinter.messagebox.showinfo("Fini",message)
        root.destroy()

    @staticmethod
    def error_occured():
        """Fonction permettant d'afficher un message d'erreur"""
        root = tkinter.Tk()
        root.withdraw()
        tkinter.messagebox.showerror("Erreur","WOW ! Une erreur a eu lieu")
        root.destroy()
        
    @staticmethod
    def look_for_user_pp(pseudo):
        no_connection = False
        try:
            data_recup = [None]
            
            with connection_principale.cursor() as cursor:
                request = f"SELECT photo_profil,rect_photo_profil FROM utilisateur WHERE pseudo = '{pseudo}'"
                cursor.execute(request)
                data_recup = cursor.fetchone()
          
        except sql.Error as err:
            
            no_connection = False
            
        except noConnection as e:
            
            no_connection = True
            
        except Exception as e:
            
            no_connection = True
            
        finally:
            if not no_connection:
                return data_recup
            raise noConnection("l")
        
    @staticmethod
    def connection_failed():
        """Fonction permettant d'afficher une erreur de connection"""
        root = tkinter.Tk()
        root.withdraw()
        tkinter.messagebox.showerror("Erreur","WOW ! La connection n'a pas pu être initialisé :(")
        root.destroy()
        
    @staticmethod
    def est_bytes(doc):
        """Fonction determinant si l'element est un fichier ou non

        Args:
            doc (bytes | any): element verifier

        Returns:
            boolean: Return True si l'element est un fichier, sinon non
        """
        return isinstance(doc,bytes) and doc != b"0"
    
    @staticmethod
    def open_dir(title = "Titre"):
        """Fonction permmettant a l'utilisateur de choisir un dossier

        Args:
            title (str, optional): titre de la fenetre. Defaults to "Titre".

        Returns:
            str: chemin du dossier choisi
        """
        root = tkinter.Tk()
        root.withdraw()
        path = tkinter.filedialog.askdirectory(title = title)
        root.destroy()
        return path
    
    @staticmethod
    def connecte_toi():
        """Fonction permettant de prévenir l'utilisateur qu'il doit se conecter pour signaler un tuto"""
        tkinter.messagebox.showerror("Erreur","Vous ne pouvez pas signaler sans être connecté !")
        
    @staticmethod
    def look_for_membre_categorie(categorie):
        """Fonction permmettant de récupérer les membres d'une catégorie

        Args:
            categorie (str): nom de la catégorie rechercher

        Returns:
            int : renvoie le nombre de membre dans la catégoriek
        """
        no_connetion = False
        try:
            if look_for_connection():
                with connection_principale.cursor() as cursor:
                    request = "SELECT membre FROM categorie WHERE nom = %s"
                    cursor.execute(request,(categorie))
                    data = cursor.fetchone()                    
            else:
                no_connetion = True
        except sql.Error as e:
            
            no_connetion = True
        except Exception as e :
            
            no_connetion = True
        finally:
            if not no_connetion:
                return data[0]
            else:
                return None
            
    @staticmethod
    def categorie_tuto_default_ou_non():
        """Fonction permettant de savoir si l'utilisateur veut qu'un tuto soit de la même catégorie que son tuto ou non

        Returns:
            bool: réponse selectionnée par l'utilisateur
        """
        root = tkinter.Tk()
        root.withdraw()
        ans = tkinter.messagebox.askyesnocancel("Categorie","Souhaiter vous mettre a ce tuto la même catégorie que votre compte ? ")
        root.destroy()
        return ans
    
    @staticmethod
    def update_categorie_data():
        #supprimer cette fonction quand je pourrais faire des events
        """Fonnction permettant de remettre a jour les informations des categories concernant les tutos/membres"""
        no_connection = False     
        try:
            connection_principale = connect_to_database()
            connection_principale.begin()
            with connection_principale.cursor() as cursor:    
                request = """UPDATE categorie AS c
                                SET c.tuto_count = (
                                SELECT COUNT(*)
                                FROM tuto AS t
                                WHERE t.categorie = c.nom
                                )"""
                cursor.execute(request)
                request = """UPDATE categorie AS c
                                SET c.membre = (
                                SELECT COUNT(*)
                                FROM utilisateur AS t
                                WHERE t.categorie = c.nom
                                )"""
                cursor.execute(request)
           
        except sql.Error as err:
            
            no_connection = True
        except Exception as err:
            
            no_connection = True
        finally:
            if no_connection:
                raise noConnection("connection failed")
            else:
                connection_principale.commit()
                connection_principale.close()
                
    @staticmethod
    def modifier_stat_tuto(id_tuto : int):
        pass
    
    @staticmethod 
    def update_categorie_member():
        """Fonction permettant de mettre a jour les membres d'une catégorie

        Raises:
            noConnection: renvoie noConnection quand la connexion n'a pu être initialisé

        Returns:
            dict: renvoie un dictionnaire avec des infos sur les catégories, une clé 'membre' et une clé 'nombre_de_tuto'
        """
        no_connection = False     
        try:
            if look_for_connection():
                with connection_principale.cursor() as cursor:                    
                    request = f"SELECT nom,membre,tuto_count FROM categorie"
                    cursor.execute(request)
                    data_recup = cursor.fetchall()
                    #dico_categorie = data[0] : {"membre" : data[1], "nombre_de_tuto" : data[2]}
            else:
               raise noConnection("connection failed")
        except sql.Error as err:
            print(err)
            no_connection = True
        except Exception as err:
            no_connection = True
        finally:
            if no_connection:
                raise noConnection("connection failed")
            else:
                return None
            
    @staticmethod
    def askyesno_basic(title = None,message = ""):
        """Fonction permettant d'afficher une messagebox oui ou non

        Args:
            title (str, optional): titre de la messagebox. Defaults to None.
            message (str, optional): message de la messagebox. Defaults to "".

        Returns:
            bool: retourne la réponse selectionner par l'utilisateur
        """
        root = tkinter.Tk()
        root.withdraw()
        rep = tkinter.messagebox.askyesno(title,message)
        root.destroy()
        return rep
    
    @staticmethod
    def ask_ok_cancel(titre = "ATTENTION",message = "Default text"):
        root = tkinter.Tk()
        root.withdraw()
        rep = tkinter.messagebox.askokcancel(title=titre,message=message)
        root.destroy()
        return rep
    
    @staticmethod
    def verifier_version_app():
        """Fonction permettant de vérifier la version de l'app, et donc de proposer une mise a jour si besoin"""
        no_connection = False
        try:
            if look_for_connection():
                with connection_principale.cursor() as cursor:
                    request = """SELECT Version,date_de_publication FROM VERSIONNAGE WHERE nom = 'SylverService' ORDER BY id DESC LIMIT 1"""
                    cursor.execute(request)
                    data_recup = cursor.fetchone()
            else:
                no_connection = True
        except sql.Error:
            no_connection = True
        except Exception as e:
            
            no_connection = True
        else:
            if not no_connection and data_recup[0] != os.environ.get("VERSION") and not no_connection:
                
                ans = Gerer_requete.askyesno_basic("NOUVELLE VERSION",f"Une Nouvelle version de l'application est disponible !\n({os.environ['VERSION']} -> {data_recup[0]})\n Souhaitez vous l'installer ?")
                if not ans:
                    Gerer_requete.message("OK")
                else:
                    if "unins000.exe" in os.listdir():
                        Gerer_requete.message("Pensez a valider la désinstallation de l'application")
                        os.startfile("unins000.exe")
                    webbrowser.open(f"https://github.com/Sylverstone/Sylver_Service/releases/tag/{data_recup[0]}")
            elif no_connection:
                raise noConnection("connexion failed")
            else:
                pass
    
    @staticmethod
    def ask_if_annonce():
        root = tkinter.Tk()
        root.withdraw()
        ans = tkinter.messagebox.askyesno("ATTENTION","Doit t'on considérez votre post comme une demande de tuto ?")
        root.destroy()
        return ans
    
    @staticmethod
    def verifier_version_doc_aide():
        """Fonction permet de vérifier la version du document aide de l'interface Menu et donc de changer le doc si besoin"""
        no_connection = False
        try:
            if look_for_connection():
                with connection_principale.cursor() as cursor:
                    request = """SELECT Version,date_de_publication,doc FROM VERSIONNAGE WHERE nom = 'Fichier_aide_sylver_service' ORDER BY id DESC LIMIT 1"""
                    cursor.execute(request)
                    data_recup = cursor.fetchone()
            else:
                no_connection = True
        except sql.Error:
            no_connection = True
        except Exception as e:
            
            no_connection = True
        else:
            if not no_connection and data_recup[0] != os.environ.get("VERSION_DOC_AIDE") and not no_connection:
                
                os.remove("Ressource/SYLVER.docx")
                with open("Ressource/SYLVER.docx","wb") as f:
                    f.write(data_recup[2])  #MET A JOUR LE FICHIER WORD  
                changer_valeur_env("VERSION_DOC_AIDE",data_recup[0])
            elif no_connection:
                raise noConnection("connexion failed")
            else:
                pass
        
    @staticmethod
    def verifier_version_doc_info():
        """Fonction permet de vérifier la version du document info sur SylverService et donc de changer le doc si besoin"""
        no_connection = False
        try:
            if look_for_connection():
                with connection_principale.cursor() as cursor:
                    request = """SELECT Version,date_de_publication,doc FROM VERSIONNAGE WHERE nom = 'Fichier_info_sylver_service' ORDER BY id DESC LIMIT 1"""
                    cursor.execute(request)
                    data_recup = cursor.fetchone()
            else:
                no_connection = True
        except sql.Error:
            no_connection = True
        except Exception as e:
            
            no_connection = True
        else:
            if not no_connection and data_recup[0] != os.environ.get("VERSION_DOC_INFO") and not no_connection:
                
                os.remove("Ressource/fichier_info.txt")
                with open("Ressource/fichier_info.txt","wb") as f:
                    f.write(data_recup[2]) #remet le nouveau fichier
                changer_valeur_env("VERSION_DOC_INFO",data_recup[0])
            elif no_connection:
                raise noConnection("connexion failed")
            else:
                pass
                
    @staticmethod
    def verifier_version_doc_info_annonce():
        """Fonction permet de vérifier la version du document info sur SylverService et donc de changer le doc si besoin"""
        no_connection = False
        try:
            if look_for_connection():
                with connection_principale.cursor() as cursor:
                    request = """SELECT Version,date_de_publication,doc FROM VERSIONNAGE WHERE nom = 'Fichier_info_annonce' ORDER BY id DESC LIMIT 1"""
                    cursor.execute(request)
                    data_recup = cursor.fetchone()
            else:
                no_connection = True
        except sql.Error:
            no_connection = True
        except Exception as e:
            
            no_connection = True
        else:
            if not no_connection and data_recup[0] != os.environ.get("VERSION_DOC_INFO_ANNONCE") and not no_connection:
                
                Gerer_requete.message("pas a jour detect")
                os.remove("Ressource/Information_page_annonce.docx")
                with open("Ressource/Information_page_annonce.docx","wb") as f:
                    f.write(data_recup[2]) #remet le nouveau fichier
                changer_valeur_env("VERSION_DOC_INFO_ANNONCE",data_recup[0])
            elif no_connection:
                raise noConnection("connexion failed")
            else:
                pass
        
                
    @staticmethod           
    def verifier_version_doc_aide_compte():
        """Fonction permet de vérifier la version du document aide de l'interface compte et donc de changer le doc si besoin"""
        no_connection = False
        try:
            if look_for_connection():
                with connection_principale.cursor() as cursor:
                    request = """SELECT Version,date_de_publication,doc FROM VERSIONNAGE WHERE nom = 'Fichier_aide_compte' ORDER BY id DESC LIMIT 1"""
                    cursor.execute(request)
                    data_recup = cursor.fetchone()
            else:
                no_connection = False
        except sql.Error:
            no_connection = True
        except Exception as e:
            
            no_connection = True
        else:
            if  not no_connection and data_recup[0] != os.environ.get("VERSION_DOC_AIDE_COMPTE") :
                
                os.remove("Ressource/Aide_interface_compte.docx")
                with open("Ressource/Aide_interface_compte.docx","wb") as f:
                    f.write(data_recup[2]) #remet le nouveau fichier
                changer_valeur_env("VERSION_DOC_AIDE_COMPTE",data_recup[0])
            elif no_connection:
                raise noConnection("connexion failed")
            else:
                pass
        
    @staticmethod
    def hash_all_password():
        # a ne surtout pas executer avant que les trophées nsi soit fini, rend les autres versions obsolète
        # pas faire de commit dessus, que des print et test
        try:
            connection_principale = connect_to_database()
            connection_principale.begin()
            with connection_principale.cursor() as cursor:    
                request = "SELECT id,mot_de_passe FROM utilisateur"
                cursor.execute(request)
                data = cursor.fetchall()
                for elt in data:
                    print(elt)
                    mdp = elt[1]
                    sha256 =  hashlib.sha256()
                    sha256.update(bytes(mdp,"utf-8"))
                    print("New password : ",sha256.hexdigest())
                    break
                    
        except:
            pass