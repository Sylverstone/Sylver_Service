
import tkinter.filedialog,tkinter.messagebox,pygame
import pymysql as sql
import os,datetime,threading,dotenv
from font_import import *
from Exception import *
import webbrowser



path = ".env"
dotenv.load_dotenv(path)
lock = threading.Lock()
chemin = os.path.join("Ressource","compte_connecter.txt")
if not os.path.exists(chemin):
    #Creation du fichier vide
    with open(chemin, "w") as fichier:
        pass
try:
    #Initialisation de la connexion principale
    connection_principale = sql.connect(
                    host = os.environ.get('HOST'),
                    user = os.environ.get('USER'),
                    password  = os.environ.get('SQL_MOT_DE_PASSE'),
                    database=os.environ.get('DB_NAME'),
                    autocommit=True,collation="utf8mb4_unicode_ci"
                    )
    connection_principale.ping(False)
except Exception as e:
    print("erreur", e)
    connection_principale = None
    
def connect_to_database():
    """Fonction essayant d'établir une connecion avec la base

    Returns:
        retourne une connexion sql ou None si la connexion a échoué
    """
    try:
        conn = sql.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('SQL_MOT_DE_PASSE'),
            database=os.environ.get('DB_NAME'),
            autocommit=True,collation="utf8mb4_unicode_ci"
            )
        conn.ping(False)
        return conn
    except Exception as e:
        return None

class status_connection:
    """Class permettant de gerer le status de la connection

        Args:
            screen (pygame.Surface): surface sur laquelle sera dessiné le rond indiquant la connection
    """
    def __init__(self,screen):
        
        self.screen = screen
        self.running = True
        threading.Thread(target = self.affiche_status_connexion, daemon=True).start()
          
    def affiche_status_connexion(self):
        """Fonction permettant de vérifier le status de la connetion, une bonne connexion est transcrite par le dessin d'un rond vert sur une 
        surface, une connexion impossible est transcrite par un rond rouge. des tentatives de reconnexion seront faites si celle-ci échoue
        """
        global connection_principale
        while self.running:            
            r = 3
            if connection_principale is None:
                pygame.draw.rect(self.screen,(255,0,0),(0,0,5,5), 0,50)
                connection_principale = connect_to_database()
                if connection_principale != None:
                    pygame.draw.rect(self.screen,(0,255,0),(0,0,5,5), 0,50)
                else:
                    pygame.draw.rect(self.screen,(255,0,0),(0,0,5,5), 0,50)                    
            else:    
                conn = connect_to_database()
                if conn != None:
                    connection_principale = conn
                    pygame.draw.rect(self.screen,(0,255,0),(0,0,5,5), 0,50)
                else:
                    print("rouge")
                    connection_principale = None
                    pygame.draw.rect(self.screen,(255,0,0),(0,0,5,5), 0,50)
                        
def look_for_connection():
    """Fonction verifiant si la connexion est apte a être utilisé, si Non : return False, si Oui : return True

    Returns:
        bool: Return True quand la connexion est disponible, sinon False
    """
    global connection_principale
    with lock:
        if connection_principale is None:
            new_connection = connect_to_database()
            if new_connection:
                connection_principale = new_connection
                return True
            else:
                connection_principale = None
                return False
        else:
            try:
                print("verification connexion")
                connection_principale.ping(reconnect=True)
                return True
            except sql.Error as e:
                print("connection failed : ",e)
                connection_principale = None
                return False
            
            
            

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
        print(lignes)
        if lignes[i].startswith(f'{valeur}='):
            lignes[i] = f'{valeur}="{new_valeur}"\n'
            break

    # Écrivez le nouveau contenu dans le fichier .env
    with open(chemin_du_env, 'w') as fichier_env:
        fichier_env.writelines(lignes)      
    print("fini") 
class Doc:    
    """Class représentant un fichier

        Args:
            chemin (str): Chemin d'accès au fichier
            bytes_doc (bytes, optional): bytes présents dans le fichier. Defaults to None.
            nom_tuto (str, optional): nom du fichier. Defaults to None.
            auteur (str, optional): nom de l'auteur du fichier. Defaults to None.
            ext (str, optional): extension du fichier. Defaults to None.
        
        Il y a 2 types de documents:
            * Les documents déjà crée, dont il reste juste à accéder, composé seulement d'un chemin d'accès
            * Ainsi que les documents a crée de toutes pièces, composé de bytes, du chemin d'accès, nom_tuto et de l'auteur
    """
    def __init__(self,chemin,bytes_doc = None,nom_tuto = None,auteur = None,ext = None):
        
        self.nom_tuto = nom_tuto
        self.auteur = auteur
        self.ext = ext
        self.bytes = bytes_doc #represente le document en bit
        self.chemin = chemin
    
    def get_extension(self):
        """Fonction isolant l'extension du fichier

        Returns:
            str: extension du fichier
        """
        if self.chemin == None:
            return None
        path = self.chemin
        cursor = -1
        while path[:cursor][-1] != ".":
            cursor -= 1
        ext = path[cursor-1:]
        return ext
    
    def start(self):
        """Fonction permettant de faire le processus afin de lancer un document"""
        if os.path.exists(self.chemin):
            #verifier si le fichier existe déja, et donc le sup
            try:
                os.remove(self.chemin)
            except:
                pass
        try:
            with open(self.chemin,"wb") as File:
                File.write(self.bytes)
        except OSError as e:
            print("erreur : ",e)
            Gerer_requete.fail_open(f"{self.nom_tuto} par {self.auteur}{self.ext}")
            return
        else:
            #no erreur
            self.start_now()            
    
    def start_now(self):
        """Fonction permettant de lancer un document"""
        try:
            os.startfile(self.chemin,"open")
        except Exception as e:
            print("erreur : ",e)
            Gerer_requete.fail_open()
        else:
            #no erreur
            print("document started")      
                 
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
    def confirm_close() -> bool:
        """Fonction confirmant une fermeture

        Returns:
            bool: Renvoie la réponse de l'utilisateur
        """
        root = tkinter.Tk()
        root.wm_withdraw()
        ans = tkinter.messagebox.askyesno(title = "Exit", parent = root,message = "Tu veux vraiment nous quitter :(",default = "no")
        root.destroy()
        return ans
    
    @staticmethod
    def confirm_open(open = "RECHERCHE",aide = "La recherche"):
        """Fonction permettant de confirmer une ouverture

        Args:
            open (str, optional): Nom du logiciel ouvert. Defaults to "Word".

        Returns:
            boolean: Renvoie la reponse de l'utilisateur (True or False)
        """
        ans = tkinter.messagebox.askyesno(title = open, message = f"Ouvrir le document d'aide pour {aide} ?")
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
            print(err)
            no_connection = True
        except Exception as e:
            print(e)
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
                
                print("finished")   
                
        except sql.Error as err:
            print(err)
            
            no_connection = True
        except Exception as e:
            print(e)
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
                infos = (self.nom,self.prenom,self.tuto_transmis,self.photo_profil,self.age,self.pseudo,self.mdp,rect_pp)
                cursor.execute(request,infos)            
          
        except sql.Error as err:
            print(err,"wesh")
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
            print(err)
            connection_principale.rollback()
            no_connection = True
        except Exception as err:
            print(err)
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
            nom_tuto (str, optional): Nom du tuto. Defaults to "".

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
            print(connection_principale)
            connection_principale.begin()
            with connection_principale.cursor() as cursor:                    
                print(doc)
                if doc != None:
                    with open(doc,"rb") as fichier:
                        doc = fichier.read()
                print("requete 1")
                request =  "INSERT INTO `tuto` (`nom`,`date`,`doc`,`text_ctn`,`auteur`,`file`,`categorie`,`is_annonce`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                infos = (nom,date,doc,Text,auteur,file,categorie,is_annonce)
                cursor.execute(request,infos)
                print("requete 2")
                request = f"UPDATE utilisateur SET tuto_transmis = tuto_transmis + 1 WHERE pseudo = '{self.pseudo}'"
                cursor.execute(request)
                print("requete 3")
                request = f"UPDATE categorie SET tuto_count = tuto_count + 1 WHERE nom = '{categorie}'"
                cursor.execute(request)
                print("requete 4")
                request = f"UPDATE utilisateur SET annonce_count = annonce_count + 1 WHERE pseudo = '{self.pseudo}'"
                cursor.execute(request)
                
           
        except sql.Error as err:
            print("erreur :",err)
            no_connection = True
        except Exception as err:
            print("erreur :",err)
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
            print(element)
            print(len(element) == len(Nouvelle_value))
            connection_principale.begin()
            with connection_principale.cursor() as cursor:
                for i in range(len(element)):
                    print(element[i])
                    print(Nouvelle_value[i][:10])
                    request = f"UPDATE `utilisateur` SET `{element[i]}` = %s WHERE `pseudo` = %s;"
                    infos = (Nouvelle_value[i],self.pseudo)
                    cursor.execute(request,infos)
     
        except sql.Error as err:
            print(err)
            connection_principale.rollback()
            no_connection = True
        except Exception as err:
            print(err)
            connection_principale.rollback()
            no_connection = True
        finally:
            if not no_connection:
                connection_principale.commit()
                connection_principale.close()
                print(temoin)
                if notif:
                    Gerer_requete.processus_fini(temoin=temoin)    
                else:
                    pass
            else:
                
                temoin[0] = True
                Gerer_requete.connection_failed()
            
        
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
                    print(data[10])
                    if data == None:
                        user_do_not_exist = True                    
            else:
                no_connection = True
                raise noConnection("connection failed")
        except sql.Error as err:
            print(err)
            no_connection = True
        except Exception as e:
            print(e)
            no_connection = True
            
        finally:
            if not no_connection:
                if user_do_not_exist == False:
                    if mdp != data[7]:
                        raise userNonCharger("mauvais mdp")
                    else:
                        return User(data[1],data[2],data[5],data[6],data[7],data[4],data[3],data[8],data[10],data[11])
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
                    print("pseudo :",all_pseudo)
                    if (pseudo,) in all_pseudo:
                        disponible = False
            else:
                no_connection = True
                raise noConnection("connection failed")
            
        except sql.Error as err:
            print(err)
            no_connection = True

        except Exception as e:
            print(e)
            no_connection = True
        finally:
            if not no_connection:
                return disponible
            else:
                raise noConnection("connection failed")
           
            
                
            
    
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
            ext_dispo = [("*","*.png"),("*","*.jpg"),("*","*.pdf"),("*","*.docx"),("*","*.odt"),("*","*.xlsx")]
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
    

        
#methode pour fichier word, pdt. juste les lires les transfo en bytes et les stocker. reflechir a une maniere de supprimer les tutos depuis sql
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
    
        try:
            if look_for_connection():
                with connection_principale.cursor() as cursor:    
                    request = "SELECT * FROM categorie"
                    cursor.execute(request)
                    data = cursor.fetchall()
            else:
                no_connection = True                
        except sql.Error as err:
            print("erreur 1:",err)
            no_connection = True
        except Exception as err:
            print("erreur 2:",err)
            no_connection = True
        finally:
            if no_connection:
                raise noConnection("connection failed")
            else:
                return data
    
    @staticmethod  
    def rechercher_annonce()->list:
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
        try:
            
            data_recup = [None]
            if look_for_connection():
                with connection_principale.cursor() as cursor:
                    request = "SELECT * FROM tuto WHERE is_annonce = 1 ORDER BY date DESC"
                    cursor.execute(request)
                    data_recup = cursor.fetchall()
            else:
                no_connection = True
        except sql.Error as err:
            print(err)
            no_connection = False
            print("erreur")
        except noConnection as e:
            print(e)
            no_connection = True
        except Exception as e:
            print(e)
            no_connection = True
            print("raise")
        finally:
            if not no_connection:
                return data_recup
            raise noConnection("l")
             
    
            
            
                
    @staticmethod  
    def rechercher_data(nom_tuto : str = None,nom_auteur : str = None,nom_categorie = None)->list:
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
        try:
            
            data_recup = [None]
            if look_for_connection():
                with connection_principale.cursor() as cursor:
                    if nom_tuto != None:
                        if nom_tuto != "*":
                            request = f" SELECT * FROM tuto WHERE nom LIKE '%{nom_tuto}%' ORDER BY date DESC;"
                        else:
                            request = f" SELECT * FROM tuto ORDER BY date DESC;"
                    elif nom_auteur != None:
                        request = f"SELECT * FROM tuto WHERE auteur LIKE '{nom_auteur}%' ORDER BY date DESC;"
                    elif nom_categorie != None:
                        request = f"SELECT * from tuto WHERE categorie = '{nom_categorie}' ORDER BY date DESC;"
                    print("doing cursor")
                    cursor.execute(request)
                    print("recup cursor")
                    data_recup = cursor.fetchall()
            else:
                no_connection = True
        except sql.Error as err:
            print(err)
            no_connection = False
            print("erreur")
        except noConnection as e:
            print(e)
            no_connection = True
        except Exception as e:
            print(e)
            no_connection = True
            print("raise")
        finally:
            if not no_connection:
                return data_recup
            raise noConnection("l")

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
        if not with_path:
            #créé le fichier si il n'existe pas
            if dir:
                path = os.path.join(dir,f"{nom_tuto} par {auteur}{ext}")
                document = Doc(path,doc,nom_tuto,auteur,ext)
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
            print(err)
            no_connection = False
            print("erreur")
        except noConnection as e:
            print(e)
            no_connection = True
            
        except Exception as e:
            print(e)
            no_connection = True
            print("raise")
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
        path = tkinter.filedialog.askdirectory(title = title)
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
            print(e)
            no_connetion = True
        except Exception as e :
            print(e)
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
                    dico_categorie = {data[0] : {"membre" : data[1], "nombre_de_tuto" : data[2]} for data in data_recup}
            else:
                no_connection = True
        except sql.Error as err:
            print("erreur 1:",err)
            no_connection = True
        except Exception as err:
            print("erreur 2:",err)
            no_connection = True
        finally:
            if no_connection:
                raise noConnection("connection failed")
            else:
                return dico_categorie
            
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
                no_connection = False
        except sql.Error:
            no_connection = True
        except Exception as e:
            print(e)
            no_connection = True
        else:
            if data_recup[0] != os.environ.get("VERSION"):
                print("pas a jour")
                ans = Gerer_requete.askyesno_basic("NOUVELLE VERSION",f"Une Nouvelle version de l'application est disponible !\n({os.environ['VERSION']} -> {data_recup[0]})\n Souhaitez vous l'installer ?")
                if not ans:
                    Gerer_requete.message("OK")
                else:
                    try:
                        os.startfile("unins000.exe",'open')
                    except:
                        print("no unins000.exe")
                    webbrowser.open(f"https://github.com/Sylverstone/Sylver_Service/releases/tag/{data_recup[0]}")
            else:
                print("a jour")
    
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
                no_connection = False
        except sql.Error:
            no_connection = True
        except Exception as e:
            print(e)
            no_connection = True
        else:
            if data_recup[0] != os.environ.get("VERSION_DOC_AIDE"):
                print("pas a jour")
                os.remove("Ressource/SYLVER.docx")
                with open("Ressource/SYLVER.docx","wb") as f:
                    f.write(data_recup[2])  #MET A JOUR LE FICHIER WORD  
                changer_valeur_env("VERSION_DOC_AIDE",data_recup[0])
            else:
                print("a jour")
        
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
                no_connection = False
        except sql.Error:
            no_connection = True
        except Exception as e:
            print(e)
            no_connection = True
        else:
            if data_recup[0] != os.environ.get("VERSION_DOC_INFO"):
                print("pas a jour")
                os.remove("Ressource/fichier_info.txt")
                with open("Ressource/fichier_info.txt","wb") as f:
                    f.write(data_recup[2]) #remet le nouveau fichier
                changer_valeur_env("VERSION_DOC_INFO",data_recup[0])
            else:
                print("a jour")
        finally:
            if no_connection:
                Gerer_requete.error_occured()
                
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
            print(e)
            no_connection = True
        else:
            if data_recup[0] != os.environ.get("VERSION_DOC_AIDE_COMPTE"):
                print("pas a jour")
                os.remove("Ressource/Aide_interface_compte.docx")
                with open("Ressource/Aide_interface_compte.docx","wb") as f:
                    f.write(data_recup[2]) #remet le nouveau fichier
                changer_valeur_env("VERSION_DOC_AIDE_COMPTE",data_recup[0])
            else:
                print("a jour")
        finally:
            if no_connection:
                Gerer_requete.error_occured()



if __name__ == "__main__":
    Gerer_requete.verifier_version_app()