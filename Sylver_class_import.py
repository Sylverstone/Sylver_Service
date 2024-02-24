import time
from mysqlx import InterfaceError
import pygame
import tkinter.filedialog,tkinter.messagebox
import mysql.connector as sql
import os,datetime,threading,dotenv

path = ".env"
dotenv.load_dotenv(path)

chemin = os.path.join("Ressource","compte_connecter.txt")
if not os.path.exists(chemin):
    #Creation du fichier vide
    with open(chemin, "w") as fichier:
        pass
class Color:
    """
        Class repertoriant toute les couleurs possible dans l'applications
    """
    def __init__(self):
        self.fond_principal = (64,64,64)
        self.fond_bar_de_navigation = (33,33,33)
        self.couleur_titre = (106,109,255)
        self.fond_case = (40,40,40)
        self.couleur_contour_case = (106,109,255)
        self.contour_contenaire_tuto = (142,142,142)
        self.fond_contenaire_login = (142,142,142)
        self.contour_input_login = (116,109,255)
        self.fond_case_login = (106,109,255)
        self.couleur_texte_editer_pp = (116,108,255)
        self.arriere_fond_login = (30,30,30)
        self.couleur_fond_case_tuto = (116,109,255)
        self.fond_un_login = (142,142,142)
        self.fond_deux_login = (30,30,30)
        self.fond_contenaire_page_tuto = (142,142,142)
    
class Doc:
    """Class representant un fichier

        Args:
            chemin (str): chemin du fichier
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
   
            
class noFileException(Exception):
    """Class reprensentant aucun fichier choisi

        Args:
            what (str): Message d'erreur
    """   
    def __init__(self, what : str) -> None:
        self.what = what
        super().__init__(self.what)
   
        
class userNonCharger(Exception):
    """Classe representant un utilisateur non chargé

        Args:
            what (str): Message d'erreur
    """
    def __init__(self, what) -> None:        
        self.what = what
        super().__init__(self.what)
    

class noConnection(Exception):
    """Class representant une erreur de connection

        Args:
            what (str): Message d'erreur
    """
    def __init__(self, what) -> None:
        
        self.what = what
        super().__init__(self.what)

def draw_text(text, font = "Comic Sans Ms", color = (0,0,0), x = 0, y = 0,contener : pygame.Surface = None,size = 20,importer = False, center_multi_line_y = False, ombre = False,center_multi_line = False):
    """
        dessiner un texte a une position donné
        :param 1: text qu'on veut dessiner
        :param 2: font qu'utilise le texte
        :param 3: couleur du texte
        :param 4: coordonne x ou le dessiner
        :param 5: coordonne y ou le dessiner
        :CU: arg 1 est un str, arg 2 est de type font.FONT ou font.SysFont, arg 3 est un rbg, arg 4 et 5 sont des int
    """
    w_origine = contener.get_rect()[2]
    text = str(text) #transformer le texte en str 
    all_text = text.split("\n")
    if not importer:
        font_ = pygame.font.SysFont(font, size)
    else:
        font_ = pygame.font.Font(font,size)
    #boucle pour afficher tout les textes de all_text
    for enum,text in enumerate(all_text):
        if center_multi_line:
            x = w_origine/2 - font_.size(text)[0]/2
        if ombre:
            text_ = font_.render(str(text), True, (0,0,0))            
            contener.blit(text_, (x+2,y+(size+2)*enum))
        text_ = font_.render(str(text), True, color)
        contener.blit(text_, (x,y+(size + 2)*enum))     
        

class Animation:
    """Class permettant de generer une animation de chargement

        Args:
            screen (pygame.Surface): Surface sur laquelle l'animation est dessiner
            text_chargement (str, optional): Texte du chargement Defaults to "Chargement".
            id_ (int, optional): id representant si l'animation est situé dans un endroit bloquant ou non. Defaults to 1.
    """
    def __init__(self,screen : pygame.Surface,text_chargement : str = "Chargement",id_ : int = 1, color = (0,0,0)):
        self.screen = screen
        self.texte = text_chargement
        self.running = True
        self.font = pygame.font.SysFont("Comic Sans Ms",20)
        self.id_ = id_
        self.nb_point = 0
        self.color = color
        
    def start_anime(self,last_screen,fond_ecran,delay = 0):
        """Fonction démarrant une animation dans une situation bloquante
            (situation bloquant : le chargement se fait en parallèle du code)
        Args:
            last_screen (pygame.Surface): Dernier écran a afficher
            fond_ecran (list): Fond de l'ecran
            delay(int,optional) : delay représente le temp qu'il faut attendre avant de forcer l'arret de l'animation
        """
        self.running = 1
        self.id_ = 0
        th = threading.Thread(target=self.animate, args=(fond_ecran,last_screen, "",delay),daemon=True)
        th.start()
        
    def animate(self,fond_ecran : list,last_screen : pygame.Surface= None,ajout_decriture :str = None, delay = 0):
        """Fonction permettant d'animer l'animation

        Args:
            fond_ecran (list): couleur du fond de l'ecran
            last_screen (pygame.Surface, optional): Dernier ecran a afficher. Defaults to None.
            ajout_decriture (str, optional): Ajout de texte . Defaults to None.
            delay(int,optional) : delay représente le temp qu'il faut attendre avant de forcer l'arret de l'animation
        """
        screen = self.screen
        if self.id_ == 1:
            self.nb_point += 0.05
            point = "."*((int(self.nb_point) %4))    
            rect_a_update = pygame.Rect(screen.get_rect()[2]/2 - self.font.size(self.texte)[0]/2,screen.get_rect()[3] - 80,200,
                                        50)                                            
            screen.fill(fond_ecran,rect_a_update)            
            draw_text(self.texte + point +"\n"+ajout_decriture,center_multi_line=True, y = screen.get_rect()[3] - 80,contener=screen,color = self.color)
        else:
            print("chargement started")
            pygame.display.update()
            screen.blit(last_screen,(0,0))
            debut = time.time()
            while self.running:
                self.nb_point += 1
                point = "."*((int(self.nb_point) %4))                                                
                rect_a_update = pygame.Rect(screen.get_rect()[2]/2 - self.font.size(self.texte)[0]/2 - 200,screen.get_rect()[3] - 60,600,300)
                screen.fill(fond_ecran,rect_a_update) 
                actu = time.time() - debut
                if delay == 0:
                    if actu >= 2:
                        ajout_texte = "Cela prend plus de temps que prévu :("
                    else:
                        ajout_texte = ""
                else:
                    ajout_texte = ""
                    if actu >= delay:
                        self.stop_anime()
                draw_text(self.texte + point + "\n" + ajout_texte,center_multi_line= True, y = screen.get_rect()[3] - 60,contener=screen,color=self.color)
                pygame.display.update(rect_a_update)
                pygame.time.delay(250)
            print("chargement ended")
            
    def stop_anime(self):
        """Fonction permettant d'arreter une animation qui a été démarrer dans une situation bloquante"""
        self.running = False
        self.id_ = 1
        
        
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
    def __init__(self,nom,prenom,age,pseudo,mdp,photo_profil = None,tuto_transmis = 0,rect_pp = None):
                
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.photo_profil = photo_profil
        self.tuto_transmis = tuto_transmis
        self.pseudo = pseudo
        self.mdp = mdp
        self.rect_pp = rect_pp
        self.auteur = f"{self.pseudo}, {self.nom} {self.prenom}"
    
    @staticmethod
    def confirm_close() -> bool:
        """Fonction confirmant une fermeture

        Returns:
            bool: Renvoie la réponse de l'utilisateur
        """
        ans = tkinter.messagebox.askyesno(title = "Exit", message = "Tu veux vraiment nous quitter :(")
        return ans
    
    @staticmethod
    def confirm_open(open = "Word"):
        """Fonction permettant de confirmer une ouverture

        Args:
            open (str, optional): Nom du logiciel ouvert. Defaults to "Word".

        Returns:
            boolean: Renvoie la reponse de l'utilisateur (True or False)
        """
        ans = tkinter.messagebox.askyesno(title = "Word", message = f"Es-tu pour l'ouverture de {open} ?")
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
    
    def get_tuto(self) -> list:
        """Fonction selectionnant tout les tuto de l'utilisateur

        Raises:
            noConnection: Renvoie noConnection quand aucune connection n'a pu être initalisé

        Returns:
            list: Tout les tuto de l'utilisateur
        """
        data = None
        try:
            connection = sql.connect(
                host = os.environ.get('HOST'),
                user = os.environ.get('USER'),
                password  = os.environ.get('SQL_MOT_DE_PASSE'),
                db=os.environ.get('DB_NAME'),
                auth_plugin='mysql_native_password')
            cursor = connection.cursor()
            request = f"SELECT COUNT(*) FROM tuto WHERE auteur = '{self.auteur}';"
            cursor.execute(request)
            data = cursor.fetchone()[0]
        except sql.Error as err:
            print(err)
        finally:
            try:
                if connection.is_connected():
                    connection.close()
                else:
                    raise noConnection("connection faild") 
            except:
                raise noConnection("connection failed")
            else:
                return data
         
    def signalement(self, id_tuto_signaler : int, pseudo_accuser : str,text_signalement : str):
        print("test")
        """Fonction gérant les soumissions de signalement par les utilisateurs

        Args:
            id_tuto_signaler (int): Numéro d'identification du tuto signalé
            pseudo_accuser (str): Pseudo du propriétaire du tuto signalé
            id_signaleur (str): Nom de l'utilisateur qui signal le tuto
            text_signalement (str): Texte de justification rédigé par l'utilisateur lorsqu'il signal le tuto

        Raises:
            noConnection: Renvoie noConnection quand aucune connection n'a pu être initalisé
        """        
        try:
            connection = sql.connect(
                    host = os.environ.get('HOST'),
                    user = os.environ.get('USER'),
                    password  = os.environ.get('SQL_MOT_DE_PASSE'),
                    db=os.environ.get('DB_NAME'),
                    auth_plugin='mysql_native_password')
            cursor = connection.cursor()
            current_date = datetime.datetime.now()
            current_date = current_date.strftime("%Y-%m-%d")
            request = """ INSERT INTO signalements (`id_tuto_signaler`, `signalement`, `pseudo_accuseur`, `date`, `pseudo_accuse`)
                          VALUES (%s,%s,%s,%s,%s);
                        """
            infos = (id_tuto_signaler, text_signalement, self.pseudo, current_date,  pseudo_accuser)
            cursor.execute(request,infos)            
            connection.commit()
        except sql.Error as err:
            print(err)
        finally:
            try:
                if connection.is_connected():
                    connection.close()
                    
            except Exception as e:
                print(e)
                raise noConnection("connection failed")
        
            
        
    def save_user(self):
        """Fonction permettant de sauvegarder un compte d'utilisateur

        Raises:
            noConnection: Renvoie noConnection quand aucune connection n'a pu être initialisation
        """        
        try:
            connection = sql.connect(
                host = os.environ.get('HOST'),
                user = os.environ.get('USER'),
                password  = os.environ.get('SQL_MOT_DE_PASSE'),
                db=os.environ.get('DB_NAME'),
                auth_plugin='mysql_native_password')
            cursor = connection.cursor()
            request = """ INSERT INTO utilisateur (`nom`, `prenom`, `tuto_transmis`,`photo_profil`, `age`,`pseudo`,`mot_de_passe`,`rect_photo_profil`)
                          VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
                        """
            if isinstance(self.rect_pp,pygame.Rect):
                rect_pp = Gerer_requete.separe_rect(self.rect_pp)
            else:
                rect_pp = None
            infos = (self.nom,self.prenom,self.tuto_transmis,self.photo_profil,self.age,self.pseudo,self.mdp,rect_pp)
            cursor.execute(request,infos)            
            connection.commit()
        except sql.Error as err:
            print(err,"wesh")
        finally:
            try:
                if connection.is_connected():
                    connection.close()
            except:
                raise noConnection("connection failed")   
                      
    def change_element(self,nom = False, pseudo = False, prenom = False, photo_pp = False, tuto_transmi = False,rect_pp = False,Nouvelle_value = 0)-> None:
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
        print("h")
        if nom:
            element = "nom"
            self.nom = Nouvelle_value
        elif pseudo:
            element = "pseudo"
            self.pseudo = Nouvelle_value
        elif prenom:
            element = "prenom"
            self.prenom = Nouvelle_value
        elif photo_pp:
            element = "photo_profil"
            self.photo_profil = Nouvelle_value
        elif tuto_transmi:
            element = "tuto_transmis"
            self.tuto_transmis = Nouvelle_value
        elif rect_pp:
            element = "rect_photo_profil"
            self.rect_pp = Gerer_requete.separe_rect(Nouvelle_value)
            Nouvelle_value = self.rect_pp
        try:
            connection = sql.connect(
                host = os.environ.get('HOST'),
                user = os.environ.get('USER'),
                password  = os.environ.get('SQL_MOT_DE_PASSE'),
                db=os.environ.get('DB_NAME'),
                auth_plugin='mysql_native_password')
            cursor = connection.cursor()
            request = f"UPDATE utilisateur SET `{element}` = %s WHERE pseudo = %s;"
            infos = (Nouvelle_value,self.pseudo)
            cursor.execute(request,infos)
            connection.commit()
        except sql.Error as err:
            print(err)
        finally:
            try:
                if connection.is_connected():
                    print("mp",self.rect_pp)
                    connection.close()
                else:
                    raise noConnection("connection failed")
            except:
                raise noConnection("connection failed")
        
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
        try:
            connection = sql.connect(
                host = os.environ.get('HOST'),
                user = os.environ.get('USER'),
                password  = os.environ.get('SQL_MOT_DE_PASSE'),
                db=os.environ.get('DB_NAME'),
                auth_plugin='mysql_native_password')
            cursor = connection.cursor()
            request =f"SELECT * FROM utilisateur WHERE pseudo = '{pseudo}'"
            cursor.execute(request)
            data = cursor.fetchone()
            connection.commit()
        except sql.Error as err:
            print(err)
        finally:
            try:
                if connection.is_connected():
                    connection.close()
                    if mdp != data[7]:
                        raise userNonCharger("mauvais mdp") 
                else:
                    raise noConnection("connection failed")
            except userNonCharger:
                raise userNonCharger("mauvais mdp")
            except:
                raise noConnection("connection failed")
            else:
                return User(data[1],data[2],data[5],data[6],data[7],data[4],data[3],data[8])
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
        try:
            connection = sql.connect(
                host = os.environ.get('HOST'),
                user = os.environ.get('USER'),
                password  = os.environ.get('SQL_MOT_DE_PASSE'),
                db=os.environ.get('DB_NAME'),
                auth_plugin='mysql_native_password')
            cursor = connection.cursor()
            request = f"SELECT pseudo FROM utilisateur WHERE pseudo LIKE '{pseudo}%'"
            cursor.execute(request)
            all_pseudo = cursor.fetchall()
            print("pseudo :",all_pseudo)
            if (pseudo,) in all_pseudo:
                disponible = False
        except sql.Error as err:
            print(err)
        except Exception as e:
            print(e)
        finally:
            try:
                if connection.is_connected():
                    connection.close()
                else:
                    raise noConnection("connection failed")
            except:
                print("no con")
                raise noConnection("connection failed")
            else:
                #aucune erreur n'a eu lieu
                return disponible
            
                
            
    
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
            ext_dispo = [("*","*.png"),("*","*.jpg"),("*","*.pdf"),("*","*.docx"),("*","*.odt")]
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
class Gerer_requete(User):   
    
    def __init__(self,user : User):
        self.user = user
        super().__init__(prenom=user.prenom,nom = user.nom,age = user.age,pseudo = user.pseudo,
                         mdp = user.mdp,photo_profil=user.photo_profil, tuto_transmis= user.tuto_transmis)       
    
    @staticmethod
    def separe_rect(rect):
        """Fonction permettant de mettre les rects en chaine de caractère pour la base de données

        Args:
            rect (pygame.Rect): Rect a mettre en string

        Returns:
            str: Rect transformer en str separer par des ,
        """
        return f"{rect[0]},{rect[1]},{rect[2]},{rect[3]}"
    
    def save_tuto(self,doc : str = None, Text :str = "",nom_tuto : str = "",experiment = False) -> None:
        """Fonction permettant de sauvegarder un tuto a mettre en ligne

        Args:
            doc (str, optional): Path du fichier a mettre en ligne. Defaults to None.
            Text (str, optional): Text du tuto a mettre en ligne. Defaults to "".
            nom_tuto (str, optional): Nom du tuto. Defaults to "".

        Raises:
            noConnection: Renvoie noConnection quand la conenction n'a pu être établie
        """        
        current_date = datetime.datetime.now()
        current_date = current_date.strftime("%Y-%m-%d")
        date = current_date
        nom = nom_tuto
        self.user.tuto_transmis += 1
        auteur = f"{self.pseudo}, {self.nom} {self.prenom}"
        file = Doc(doc).get_extension()
        try:
            connection = sql.connect(
                host = os.environ.get('HOST'),
                user = os.environ.get('USER'),
                password  = os.environ.get('SQL_MOT_DE_PASSE'),
                db=os.environ.get('DB_NAME'),
                auth_plugin='mysql_native_password')
            cursor = connection.cursor()
            if doc != None:
                with open(doc,"rb") as fichier:
                    doc = fichier.read()
            request = """ INSERT INTO tuto (`nom`,`date`,`doc`,`text_ctn`,`auteur`,`file`)
                          VALUES (%s,%s,%s,%s,%s,%s);
                        """
            infos = (nom,date,doc,Text,auteur,file)
            cursor.execute(request,infos)
            request = f"UPDATE utilisateur SET tuto_transmis = tuto_transmis + 1 WHERE pseudo = '{self.pseudo}'"
            cursor.execute(request)
            if not experiment:
                connection.commit()
        except sql.Error as err:
            print(err)
        finally:
            try:
                if connection.is_connected():
                    connection.close()
                else:
                    raise noConnection("connection failed")
            except:
                raise noConnection("connection failed")
                
    @staticmethod  
    def rechercher_data(nom_tuto : str = None,nom_auteur : str = None)->list:
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
        try:
            data_recup = [None]            
            connection = sql.connect(
                host = os.environ.get('HOST'),
                user = os.environ.get('USER'),
                password  = os.environ.get('SQL_MOT_DE_PASSE'),
                db=os.environ.get('DB_NAME'),
                auth_plugin='mysql_native_password')
            print(connection)
            cursor = connection.cursor()
            if nom_tuto != None:
                 request = f" SELECT * FROM tuto WHERE nom LIKE '%{nom_tuto}%'"
            elif nom_auteur != None:
                request = f"SELECT * FROM tuto WHERE auteur LIKE '{nom_auteur}%' ORDER BY date DESC"
            cursor.execute(request)
            data_recup = cursor.fetchall()  
            connection.commit()
        except sql.Error as err:
            print(err)
            print("erreur")
        
        finally:
            try:
                if connection.is_connected():
                    connection.close()
                else:
                    raise noConnection("connection failed")
            except:
                raise noConnection("connection failed")
            else:
                return data_recup

    @staticmethod
    def demarrer_fichier(doc : bytes | str,ext,with_path = False,nom_tuto = "",auteur = "")->None:
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
            dir = tkinter.filedialog.askdirectory(title = "Lieu du Telechargement")
            if dir:
                path = os.path.join(dir,f"{nom_tuto} par {auteur}{ext}")
                document = Doc(path,doc,nom_tuto,auteur,ext)
                document.start()
            else:
                return 
        else:
            path = doc
            document = Doc(path)
            document.start_now()
        
        
    @staticmethod
    def fail_open(nom_fichier = ""):
        """Fonction permettant d'afficher une erreur d'ouverture

        Args:
            nom_fichier (str, optional): Nom du fichier dont l'ouverture a echouer. Defaults to "".
        """
        tkinter.messagebox.showerror("Erreur",f"WOW ! L'ouverture a flop :( \n Il se peut que le fichier ({nom_fichier}) \nsoit déjà ouvert !")
        
    @staticmethod
    def error_occured():
        """Fonction permettant d'afficher un message d'erreur"""
        tkinter.messagebox.showerror("Erreur","WOW ! Une erreur a eu lieu")
    
    @staticmethod
    def connection_failed():
        """Fonction permettant d'afficher une erreur de connection"""
        tkinter.messagebox.showerror("Erreur","WOW ! La connection n'a pas pu être initialisé :(")
        
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
    def connecte_toi():
        """Fonction permettant de prévenir l'utilisateur qu'il doit se conecter pour signaler un tuto"""
        tkinter.messagebox.showerror("Erreur","Vous ne pouvez pas signaler sans être connecté !")
          
if __name__ == "__main__":
    pass