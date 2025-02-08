import hashlib
import tkinter
import tkinter.filedialog,tkinter.messagebox,pygame
import pymysql as sql
import datetime
from font_import import *
from customException import *

from connection_fonction import connect_to_database
from Class.Gerer_requete import Gerer_requete
from Class.Doc import Doc
from Class.status_connection import connection_principale,look_for_connection
import Sylver_filedialog
class User:
    """Class Representant le compte de l'utilisateur

        Args:
            nom (str): Nom de l'utilisateur
            prenom (str): Prenom de l'utilisateur
            age (int): Age de l'utilisateur
            pseudo (str): Pseudo de l'utilisateur
            mdp (str): Mot de passe du compte de l'utilisateur
            photo_profil (bytes, optional): Photo de profil de l'utilisateur. Defaults to None.
            tuto_transmis (int, optional): Nombre de tuto que l'utilisateur a transmis. Defaults to 0.
            rect_pp (pygame.Rect, optional): Rect de la photo de profil de l'utilisateur. Defaults to None.
    """
    def __init__(self,nom,prenom,age,pseudo,mdp,photo_profil = None,tuto_transmis = 0,rect_pp = None,categorie = None,annonce_transmis = 0):
                
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.photo_profil = photo_profil
        self.tuto_transmis = tuto_transmis
        self.pseudo = pseudo
        self.mdp = mdp
        self.rect_pp = rect_pp
        self.auteur = f"{self.pseudo}, {self.nom} {self.prenom}"
        self.categorie = categorie
        self.annonce_transmis = annonce_transmis
    
    @staticmethod
    def confirm_close(screen : pygame.Surface,last_screen : pygame.Surface) -> bool:
        """Fonction confirmant une fermeture

        Returns:
            bool: Renvoie la réponse de l'utilisateur
        """
        dialog = Sylver_filedialog.BoiteDialogPygame(400,200,screen,1,True,echap_destroy_windows=True,base_title="Attention")
        ans = dialog.ask_yes_no("Voulez-vous fermer Sylver.service?",last_screen)
        ans = ans if False == None else ans

        return ans
    
    @staticmethod
    def confirm_open(open = "RECHERCHE",aide = "La recherche",screen : pygame.Surface = None,BoiteDialogPygame = None):
        """Fonction permettant de confirmer une ouverture

        Args:
            open (str, optional): Nom du logiciel ouvert. Defaults to "Word".

        Returns:
            boolean: Renvoie la reponse de l'utilisateur (True or False)
        """
        dialog = BoiteDialogPygame(400,200,screen,1,True,echap_destroy_windows=True)
        ans = dialog.ask_yes_no(f"Ouvrir le document d'aide pour {aide} ?",screen.copy())
        ans = ans if False == None else ans
        return ans
    
    @staticmethod
    def get_only_pseudo(text : str) -> str:
        """Fonction permettant de prendre que le pseudo de l'auteur

        Args:
            text (str): nom complet auteur (pseudo,prenom nom)

        Returns:
            str: Uniquement le pseudo de l'utilisateur, separe au virgule et renvoie l'element 0
        """
        return text.split(",")[0]
    
    
    def can_signal(self,id_tuto_signaler):
        """Fonction verifiant si l'utilisateur peut signaler un tuto

        Args:
            id_tuto_signaler (int): id du tuto signalé

        Raises:
            noConnection: Renvoie noConnection quand la connexion a la base a echoué

        Returns:
            bool: True si il peut signaler,sinon False
        """
        no_connection = False 
        can_signal = True
        try:
            if look_for_connection():
                with connection_principale.cursor() as cursor:
                    request = f"SELECT COUNT(*) FROM signalements WHERE id_tuto_signaler = '{id_tuto_signaler}' AND pseudo_accuseur = '{self.pseudo}'"
                    cursor.execute(request)
                    data = cursor.fetchone()
                    if data[0] != 0:
                        can_signal = False
            else:
                no_connection = True
        except sql.Error as err:
            
            no_connection = True
        except Exception as e:
            
            no_connection = True
        finally:
            if no_connection:
                raise noConnection("connection failed")
            else:
                return can_signal
                    
    def signalement(self, id_tuto_signaler : int, pseudo_accuser : str,text_signalement : str):
        """Fonction gérant les soumissions de signalement par les utilisateurs

        Args:
            id_tuto_signaler (int): Numéro d'identification du tuto signalé
            pseudo_accuser (str): Pseudo du propriétaire du tuto signalé
            id_signaleur (str): Nom de l'utilisateur qui signal le tuto
            text_signalement (str): Texte de justification rédigé par l'utilisateur lorsqu'il signal le tuto

        Raises:
            noConnection: Renvoie noConnection quand aucune connection n'a pu être initalisé
        """     
        no_connection = False 
        try:
            connection_principale = connect_to_database()
            connection_principale.begin()
            with connection_principale.cursor() as cursor:
                
                
                current_date = datetime.datetime.now()
                current_date = current_date.strftime("%Y-%m-%d")
                request = """ INSERT INTO `signalements` (`id_tuto_signaler`, `signalement`, `pseudo_accuseur`, `date`, `pseudo_accuse`)
                            VALUES (%s,%s,%s,%s,%s);"""
                
                infos = (id_tuto_signaler, text_signalement, self.pseudo, current_date,  pseudo_accuser)
                cursor.execute(request,infos)
                request = f'UPDATE tuto SET signalement = signalement + 1 WHERE id = {id_tuto_signaler}'
                cursor.execute(request)
                
                   
                
        except sql.MySQLError as err:
            print("errr : ",err.args[1])
            if(err.args[1] == "CannotSignal"):
                raise cannotSignal("cannot signal")
            no_connection = True
        except Exception as e:
            
            no_connection = True
        finally:
            if no_connection:
                raise noConnection("connection failed")
            else:
                connection_principale.commit()
                connection_principale.close()
                    
    def save_user(self):
        """Fonction permettant de sauvegarder un compte d'utilisateur

        Raises:
            noConnection: Renvoie noConnection quand aucune connection n'a pu être initialisation
        """
        no_connection = False        
        try:
            connection_principale = connect_to_database()
            connection_principale.begin()       
            with connection_principale.cursor() as cursor:
                request = """ INSERT INTO `utilisateur` (`nom`, `prenom`, `tuto_transmis`,`photo_profil`, `age`,`pseudo`,`mot_de_passe`,`rect_photo_profil`)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"""
                if isinstance(self.rect_pp,pygame.Rect):
                    rect_pp = Gerer_requete.separe_rect(self.rect_pp)
                else:
                    rect_pp = None
                sha_256 = hashlib.sha256()
                sha_256.update(bytes(self.mdp,"utf-8"))
                mdp_hash = sha_256.hexdigest()
                infos = (self.nom,self.prenom,self.tuto_transmis,self.photo_profil,self.age,self.pseudo,mdp_hash,rect_pp)
                cursor.execute(request,infos)            
          
        except sql.Error as err:
            no_connection = True
        except:
            no_connection = True
        finally:
            if no_connection:
                raise noConnection("connection failed")   
            else:
                connection_principale.commit()
                connection_principale.close()
        
    def change_categorie_compte(self,Nouvelle_value = None):
        """Fonction permettant de changer la catégorie d'un compte

        Args:
            Nouvelle_value (str, optional): Nouvelle catégorie choisi. Defaults to None.

        Raises:
            noConnection: renvoie noConnection quand la connexion n'a pas être initialisé
        """
        no_connection = False
        try:
            connection_principale = connect_to_database()
            with connection_principale.cursor() as cursor:
                request = f"UPDATE utilisateur SET categorie = '{Nouvelle_value}' WHERE pseudo = %s "
                cursor.execute(request,(self.pseudo))
                if self.categorie != None:
                    request = f"UPDATE categorie SET membre = membre - 1 WHERE nom = '{self.categorie}'"
                    cursor.execute(request)
                request = f"UPDATE categorie SET membre = membre + 1 WHERE nom = '{Nouvelle_value}'"
                cursor.execute(request)
        except sql.Error as err:
            
            connection_principale.rollback()
            no_connection = True
        except Exception as err:
            
            connection_principale.rollback()
            no_connection = True
        finally:
            if not no_connection:
                self.categorie = Nouvelle_value
                connection_principale.commit()
                connection_principale.close()
                
            else:
                raise noConnection("no connection")
            
    def save_tuto(self,doc : str = None, Text :str = "",nom_tuto : str = "",categorie = None,is_annonce = 0,experiment = False) -> None:
        """Fonction permettant de sauvegarder un tuto a mettre en ligne

        Args:
            doc (str, optional): Path du fichier a mettre en ligne. Defaults to None.
            Text (str, optional): Text du tuto a mettre en ligne. Defaults to "".
            nom_tuto (str): Nom du tuto. Defaults to "".
            categorie (str): Catégorie dans laquelle se trouve le tuto
            is_annonce(bool): si is_annonce est True, le tuto est une annonce

        Raises:
            noConnection: Renvoie noConnection quand la conenction n'a pu être établie
        """
        no_connection = False     
        current_date = datetime.datetime.now()
        current_date = current_date.strftime("%Y-%m-%d")
        date = current_date
        nom = nom_tuto
        
        auteur = f"{self.pseudo}, {self.nom} {self.prenom}"
        file = Doc(doc).get_extension()
        try:
            connection_principale = connect_to_database()
            connection_principale.begin()
            with connection_principale.cursor() as cursor:                    
                if doc != None:
                    with open(doc,"rb") as fichier:
                        doc = fichier.read()
                request =  "INSERT INTO `tuto` (`nom`,`date`,`doc`,`text_ctn`,`auteur`,`file`,`categorie`,`is_annonce`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                infos = (nom,date,doc,Text,auteur,file,categorie,is_annonce)
                cursor.execute(request,infos)
                request = f"UPDATE utilisateur SET tuto_transmis = tuto_transmis + 1 WHERE pseudo = '{self.pseudo}'"
                cursor.execute(request)
                request = f"UPDATE categorie SET tuto_count = tuto_count + 1 WHERE nom = '{categorie}'"
                cursor.execute(request)
                request = f"UPDATE utilisateur SET annonce_count = annonce_count + 1 WHERE pseudo = '{self.pseudo}'"
                cursor.execute(request)
                
           
        except sql.Error as err:
            no_connection = True
        except Exception as err:
            no_connection = True
        finally:
            if no_connection:
                raise noConnection("connection failed")
            else:
                if is_annonce == 0:
                    self.tuto_transmis += 1
                else:
                    self.annonce_transmis += 1
                connection_principale.commit()
                connection_principale.close()
                     
    def change_element(self,nom = False, pseudo = False, prenom = False, photo_pp = False, tuto_transmi = False,rect_pp = False,Nouvelle_value = 0, notif = False,temoin = None)-> None:
        """Fonction permettant de mettre a jour les éléments du compte de l'utilisation

        Args:
            nom (bool, optional): Représente si c'est le nom a changer. Defaults to False.
            pseudo (bool, optional): Représente si c'est le pseudo a changer. Defaults to False.
            prenom (bool, optional): Représente si c'est le prenom a changer. Defaults to False.
            photo_pp (bool, optional): Représente si c'est la photo profil a changer. Defaults to False.
            tuto_transmi (bool, optional): Représente si c'est le nombre de tuto transmis a changer. Defaults to False.
            rect_pp (bool, optional): Représente si c'est le rect de la photo de profil a changer. Defaults to False.
            Nouvelle_value (int, optional): Nouvelle valeur a mettre. Defaults to 0.

        Raises:
            noConnection: Renvoie noConnection quand aucune connection n'a pu être initialisé
        """
        element=[]
        no_connection = False
        if nom:
            element += ["nom"]
            self.nom = Nouvelle_value
        if pseudo:
            element += ["pseudo"]
            self.pseudo = Nouvelle_value
        if prenom:
            element += ["prenom"]
            self.prenom = Nouvelle_value
        if photo_pp:
            element += ["photo_profil"]
            self.photo_profil = Nouvelle_value
        if tuto_transmi:
            element += ["tuto_transmis"]
            self.tuto_transmis = Nouvelle_value
        if rect_pp:
            element += ["rect_photo_profil"]
            i = 0
            while not isinstance(Nouvelle_value[i], pygame.Rect):
                i +=1
            self.rect_pp = Gerer_requete.separe_rect(Nouvelle_value[i])
            Nouvelle_value[i] = self.rect_pp
        try:
            connection_principale = connect_to_database()
            connection_principale.begin()
            with connection_principale.cursor() as cursor:
                for i in range(len(element)):
                    request = f"UPDATE `utilisateur` SET `{element[i]}` = %s WHERE `pseudo` = %s;"
                    infos = (Nouvelle_value[i],self.pseudo)
                    cursor.execute(request,infos)
     
        except sql.Error as err:
            
            connection_principale.rollback()
            no_connection = True
        except Exception as err:
            
            connection_principale.rollback()
            no_connection = True
        finally:
            if not no_connection:
                connection_principale.commit()
                connection_principale.close()

                if notif:
                    Gerer_requete.processus_fini(temoin=temoin)    
                else:
                    pass
            else:
                
                temoin[0] = True
                Gerer_requete.connection_failed()
            
    @staticmethod
    def verifier_mdp(input_user,mdp):
        sha_256 = hashlib.sha256()
        sha_256.update(bytes(input_user,"utf-8"))
        if sha_256.hexdigest() == mdp:
            return True
        elif input_user == mdp:
            print("mauvais endroit")
            return True
        return False
    
    @staticmethod    
    def log_user(pseudo,mdp):
        """Fonction permettant de charger le compte de l'utilisateur

        Args:
            pseudo (str): pseudo du compte voulu
            mdp (str): mot de passe du compte voulu

        Raises:
            userNonCharger: Renvoie userNonCharger quand le mot de passe n'est pas bon
            noConnection: Renvoie noConnection quand aucune connection n'a pu être initialisé

        Returns:
            User: Renvoie la classe User du compte
        """
        no_connection = False
        user_do_not_exist = False
        try:
            if look_for_connection():
                with connection_principale.cursor() as cursor:
                    cursor = connection_principale.cursor()
                    request =f"SELECT * FROM `utilisateur` WHERE pseudo = '{pseudo}';"
                    cursor.execute(request)
                    data = cursor.fetchone()
                    if data == None:
                        user_do_not_exist = True
                    else:
                        request = f"SELECT COUNT(*) FROM tuto WHERE auteur = '{data[6]}, {data[1]} {data[2]}'"
                        cursor.execute(request)
                        tuto_transmis = cursor.fetchone()[0]
                        request = f"SELECT COUNT(*) FROM tuto WHERE auteur = '{data[6]}, {data[1]} {data[2]}' AND is_annonce = 1"
                        cursor.execute(request)
                        annonce_transmis = cursor.fetchone()[0]
            else:
                no_connection = True
                raise noConnection("connection failed")
        except sql.Error as err:
            
            no_connection = True
        except Exception as e:
            
            no_connection = True            
        finally:
            if not no_connection:
                if user_do_not_exist == False:
                    if not User.verifier_mdp(mdp,data[7]):
                        raise userNonCharger("mauvais mdp")
                    else:
                        return User(data[1],data[2],data[5],data[6],data[7],data[4],tuto_transmis,data[8],data[10],annonce_transmis)
                else:
                    raise UserNotExist("Auncun utilisateur trouvée")
            else:
                raise noConnection("connection failed")
            
    @staticmethod
    def verifier_pseudo(pseudo)->bool:
        """Fonction permettant de verifier que le pseudo saisi est disponible

        Args:
            pseudo (str): pseudo a verifier

        Raises:
            noConnection: Renvoie noConnection quand aucune connection n'a pu être initialisé

        Returns:
            bool: Renvoie True si le tuto est disponible, False sinon
        """        
        disponible = True
        no_connection = False
        try:
            if look_for_connection():
                with connection_principale.cursor() as cursor:
                    request = f"SELECT `pseudo` FROM `utilisateur` WHERE `pseudo` LIKE '{pseudo}%';"
                    cursor.execute(request)
                    all_pseudo = cursor.fetchall()
                    if (pseudo,) in all_pseudo:
                        disponible = False
            else:
                no_connection = True
                raise noConnection("connection failed")
            
        except sql.Error as err:
            
            no_connection = True

        except Exception as e:
            
            no_connection = True
        finally:
            if not no_connection:
                return disponible
            else:
                raise noConnection("connection failed")
      
    
    def modifier_tuto(self,doc : str = None, Text :str = "",nom_tuto : str = "",categorie = None,is_annonce = 0,id_tuto = 0):
        """Fonction qui nous sert a modifier un tuto, elle supprime l'ancien pour en mettre un autre

        Args:

            doc (str, optional): Path du fichier a mettre en ligne. Defaults to None.
            Text (str, optional): Text du tuto a mettre en ligne. Defaults to "".
            nom_tuto (str): Nom du tuto. Defaults to "".
            categorie (str): Catégorie dans laquelle se trouve le tuto
            is_annonce(bool): si is_annonce est True, le tuto est une annonce
            id_tuto(int): id du tuto a supprimé
        """
        self.delete_tuto(id_tuto,demander_user=False)
        self.save_tuto(doc,Text,nom_tuto,categorie,is_annonce)
        
    def delete_tuto(self,id_tuto,demander_user = True):
        """Fonction permettant de supprimer un tuto de la base de donnée

        Args:
            id_tuto (int): id du tuto a supprimé de la bdd
            demander_user (bool, optional): Si True, demande la confirmation de la suppression. Defaults to True.
        """
        if demander_user:
            rep_user = Gerer_requete.askyesno_basic("Suppression","Voulez vous vraiment supprimer définitivement ce tuto ?")
        else:
            rep_user = True
        no_connection = False
        if rep_user:
            try:
                connection_principale = connect_to_database()
                connection_principale.begin()
                with connection_principale.cursor() as cursor:
                    request = "DELETE FROM tuto WHERE id = %s"
                    cursor.execute(request,id_tuto)
            except sql.Error as err:
                
                connection_principale.rollback()
                no_connection = True
            except Exception as err:
                
                connection_principale.rollback()
                no_connection = True
            finally:
                if not no_connection:
                    connection_principale.commit()
                    connection_principale.close()
                    return rep_user
                else:
                    raise noConnection("Connexion non initialisé")
        else:
            return
    
    @staticmethod
    def get_file(idd = 0):
        """Fonction permettant de choisir le un fichier pour différent type d'utilisation

        Args:
            idd (int, optional): Id reprensentant le type d'utilisation, 0 : utilisation pour pdp, 1 : utilisation pour tuto. Defaults to 0.

        Raises:
            noFileException: Retournes noFileException quand le processus de choix est annulé

        Returns:
            path(str): Path du fichier choisi
            extention(str) : extention du fichier choisi
        """
        if idd == 1:
            #si c'est pour poster un tuto
            ext_dispo = [("*","*.png"),("*","*.jpg"),("*","*.pdf"),("*","*.docx"),("*","*.odt"),("*","*.xlsx"),("*","*.py")]
        else:
            #si c'est pour choisir une pp
            ext_dispo = [("*","*.png"),("*","*.jpg")]
        
        path = tkinter.filedialog.askopenfilename(filetypes = ext_dispo)
        if path != "":
            doc = Doc(path)
            extension = doc.get_extension()
            return path,extension
        else:
            raise noFileException("joue meme pas avec mes nerfs toi")        