from http.client import TOO_MANY_REQUESTS
import pygame
import tkinter.filedialog
import tkinter as tk
import mysql.connector as sql
import dotenv,os,datetime,sys,threading




env = dotenv.dotenv_values()


class Doc:
    
    def __init__(self,chemin):
        self.chemin = chemin
    
    def get_extension(self):
        if self.chemin == None:
            return None
        path = self.chemin
        cursor = -1
        while path[:cursor][-1] != ".":
            cursor -= 1
        ext = path[cursor-1:]
        return ext

class noFileException(Exception):
    def __init__(self, what : str) -> None:
        self.what = what
        super().__init__(self.what)
        
class userNonCharger(Exception):
    def __init__(self, what) -> None:
        self.what = what
        super().__init__(self.what)
    
class noConnection(Exception):
    def __init__(self, what) -> None:
        self.what = what
        super().__init__(self.what)

def draw_text(text, font = "Comic Sans Ms", color = (0,0,0), x = 0, y = 0,contener = None,size = 20,importer = False, center_multi_line_y = False, ombre = False,center_multi_line = False):
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

    def __init__(self,screen : pygame.Surface,text_chargement : str = "Chargement",id_ : int = 1):
        """Class permettant de generer une animation de chargement

        Args:
            screen (pygame.Surface): Surface sur laquelle l'animation est dessiner
            text_chargement (str, optional): Texte du chargement Defaults to "Chargement".
            id_ (int, optional): id representant si l'animation est situé dans un endroit bloquant ou non. Defaults to 1.
        """
        self.screen = screen
        self.texte = text_chargement
        self.running = True
        self.font = pygame.font.SysFont("Comic Sans Ms",20)
        self.id_ = id_
        self.nb_point = 0
        
    def start_anime(self,last_screen,fond_ecran):
        self.running = 1
        self.id_ = 0
        th = threading.Thread(target=self.animate, args=(fond_ecran,last_screen),daemon=True)
        th.start()
        
    def animate(self,fond_ecran,last_screen = None,ajout_decriture = None):
        screen = self.screen
        if self.id_ == 1:
            self.nb_point += 0.05
            point = "."*((int(self.nb_point) %4))                                                
            rect_a_update = pygame.Rect(screen.get_rect()[2]/2 - self.font.size(self.texte)[0]/2,screen.get_rect()[3] - 40,200,
                                        50)
            screen.fill(fond_ecran,rect_a_update)            
            draw_text(self.texte + point +"\n"+ajout_decriture,center_multi_line=True, y = screen.get_rect()[3] - 100,contener=screen)
        else:
            pygame.display.update()
            screen.blit(last_screen,(0,0))
            while self.running:
                self.nb_point += 1
                point = "."*((int(self.nb_point) %4))                                                
                rect_a_update = pygame.Rect(screen.get_rect()[2]/2 - self.font.size(self.texte)[0]/2,screen.get_rect()[3] - 40,200,
                                            50)
                screen.fill(fond_ecran,rect_a_update)            
                draw_text(self.texte + point,center_multi_line= True, y = screen.get_rect()[3] - 100,contener=screen)
                pygame.display.update(rect_a_update)
                pygame.time.delay(250)
            
    def stop_anime(self):
        self.running = False
        self.id_ = 1
        
class User:
    
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
        ans = tk.messagebox.askyesno(title = "Exit", message = "Tu veux vraiment nous quitter :(")
        return ans
    
    @staticmethod
    def confirm_open(open = "Word"):
        ans = tk.messagebox.askyesno(title = "Exit", message = f"Es-tu pour l'ouverture de {open} ?")
        return ans
    
    @staticmethod
    def get_only_pseudo(text : str) -> str:
        return text.split(",")[0]
    
    def get_tuto(self) -> int:
        
        data = None
        try:
            connection = sql.connect(
                host = env.get('HOST'),
                user = env.get('USER'),
                password  = env.get('SQL_MOT_DE_PASSE'),
                db=env.get('DB_NAME'),
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
                    
                return data 
            except:
                raise noConnection("connection failed")
                
    def save_user(self):
        try:
            connection = sql.connect(
                host = env.get('HOST'),
                user = env.get('USER'),
                password  = env.get('SQL_MOT_DE_PASSE'),
                db=env.get('DB_NAME'),
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
        pseudo_user = self.pseudo
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
            print("boum")
        print("h")
        try:
            connection = sql.connect(
                host = env.get('HOST'),
                user = env.get('USER'),
                password  = env.get('SQL_MOT_DE_PASSE'),
                db=env.get('DB_NAME'),
                auth_plugin='mysql_native_password')
            cursor = connection.cursor()
            request = f"UPDATE utilisateur SET `{element}` = %s WHERE pseudo = %s;"
            infos = (Nouvelle_value,self.pseudo)
            cursor.execute(request,infos)
            connection.commit()
        except sql.Error as err:
            print("ERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
            print(err)
        finally:
            try:
                if connection.is_connected():
                    print("mp",self.rect_pp)
                    connection.close()
                else:
                    print("not connected")
            except:
                raise noConnection("connection failed")
        
    @staticmethod    
    def log_user(pseudo,mdp):
        try:
            connection = sql.connect(
                host = env.get('HOST'),
                user = env.get('USER'),
                password  = env.get('SQL_MOT_DE_PASSE'),
                db=env.get('DB_NAME'),
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
                    if mdp == data[7]:
                        return User(data[1],data[2],data[5],data[6],data[7],data[4],data[3],data[8])
                    raise userNonCharger
            except:
                raise noConnection("connection failed")
                  
    @staticmethod
    def verifier_pseudo(pseudo)->bool:
        disponible = True
        print("in")
        try:
            connection = sql.connect(
                host = env.get('HOST'),
                user = env.get('USER'),
                password  = env.get('SQL_MOT_DE_PASSE'),
                db=env.get('DB_NAME'),
                auth_plugin='mysql_native_password')
            cursor = connection.cursor()
            request = """ SELECT pseudo FROM utilisateur
                        """
            cursor.execute(request)
            all_pseudo = cursor.fetchall()
            print(all_pseudo)
            print(pseudo)
            print("pseudo :",all_pseudo)
            for pseudo_ in all_pseudo:
                if pseudo_[0] == pseudo:
                    disponible = False
        except sql.Error as err:
            print(err)
        except Exception as e:
            print(e)
        finally:
            try:
                if connection.is_connected():
                    connection.close()
                return disponible
            except:
                return noConnection("connection failed")
    
    @staticmethod
    def get_file(idd = 0):
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
        return f"{rect[0]},{rect[1]},{rect[2]},{rect[3]}"
    
    def save_tuto(self,doc = None, Text = "",nom_tuto= "",experiment = False) -> None:
        current_date = datetime.datetime.now()
        current_date = current_date.strftime("%Y-%m-%d")
        date = current_date
        nom = nom_tuto
        print(self)
        self.user.tuto_transmis += 1
        auteur = f"{self.pseudo}, {self.nom} {self.prenom}"
        file = Doc(doc).get_extension()
        try:
            connection = sql.connect(
                host = env.get('HOST'),
                user = env.get('USER'),
                password  = env.get('SQL_MOT_DE_PASSE'),
                db=env.get('DB_NAME'),
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
            except:
                raise noConnection("connection failed")
                
    @staticmethod  
    def rechercher_data(nom_tuto = None,nom_auteur = None)->list:
        try:
            data_recup = [None]
            
            connection = sql.connect(
                host = env.get('HOST'),
                user = env.get('USER'),
                password  = env.get('SQL_MOT_DE_PASSE'),
                db=env.get('DB_NAME'),
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
            print("wow")
        
        finally:
            try:
                if connection.is_connected():
                    connection.close()
                return data_recup
            except:
                raise noConnection("connection failed")
    
    @staticmethod
    def demarrer_fichier(doc,ext,with_path = False)->None:
        if not with_path:
            print(ext)
            print("demarrer_fichier")
            path = os.path.join('img_center',f"document{ext}")
            if os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass
            try:
                with open(path,"wb") as File:
                    File.write(doc)
            except OSError as e:
                print("erreur : ",e)
                Gerer_requete.fail_open()
                return None
        else:
            path = doc
        try:
            os.startfile(path,'open')
            print("ouvert")
        except Exception as e:
            print(e)
            Gerer_requete.fail_open()
        
    @staticmethod
    def fail_open():
        tk.messagebox.showerror("Erreur", "WOW ! L'ouverture a flop :( \n On vous conseille de verifier si le fichier n'est pas déjà ouvert !")
        pygame.event.clear()
        
    @staticmethod
    def error_occured():
        tkinter.messagebox.showerror("Erreur","WOW ! Une erreur a eu lieu")
        pygame.event.clear()
        
    def connection_failed():
        tkinter.messagebox.showerror("Erreur","WOW ! La connection n'a pas pu être initialisé :(")
        pygame.event.clear()
        
    @staticmethod
    def est_bytes(doc):
        return isinstance(doc,bytes) and doc != b"0"
    
    
        
    
    
    
                
if __name__ == "__main__":
    pass