
import tkinter as tk
import tkinter.filedialog
from typing import Self
import mysql.connector as sql
import os,datetime

import pygame   


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
    def get_only_pseudo(text) -> str:
        return text.split(",")[0]
    
    def get_tuto(self) -> int:
        
        data = None
        try:
            connection = sql.connect(
                host = "localhost",
                user = "root",
                password  = "Daryll08Sylvio08",
                db="sylver_service",
                auth_plugin='mysql_native_password')
            cursor = connection.cursor()
            request = f"SELECT COUNT(*) FROM tuto WHERE auteur = '{self.auteur}';"
            cursor.execute(request)
            data = cursor.fetchone()[0]
        except sql.Error as err:
            print(err)
            print("errsql")
        finally:
            if connection.is_connected():
                connection.close()
                
            return data 
                
    def save_user(self) -> None:
        try:
            connection = sql.connect(
                host = "localhost",
                user = "root",
                password  = "Daryll08Sylvio08",
                db="sylver_service",
                auth_plugin='mysql_native_password')
            cursor = connection.cursor()
            request = """ INSERT INTO utilisateur (`nom`, `prenom`, `tuto_transmis`,`photo_profil`, `age`,`pseudo`,`mot_de_passe`,`rect_photo_profil`)
                          VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
                        """
            infos = (self.nom,self.prenom,self.tuto_transmis,self.photo_profil,self.age,self.pseudo,self.mdp,self.rect_pp)
            cursor.execute(request,infos)            
            connection.commit()
        except sql.Error as err:
            print(err)
        finally:
            if connection.is_connected():
                connection.close()   
                
    
                
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
                    host = "localhost",
                    user = "root",
                    password  = "Daryll08Sylvio08",
                    db="sylver_service",
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
            if connection.is_connected():
                print("mp",self.rect_pp)
                connection.close()
            else:
                print("not connected")
    
    @staticmethod    
    def log_user(pseudo,mdp)-> Self | userNonCharger:
        try:
            connection = sql.connect(
                host = "localhost",
                user = "root",
                password  = "Daryll08Sylvio08",
                db="sylver_service",
                auth_plugin='mysql_native_password')
            cursor = connection.cursor()
            request =f"SELECT * FROM utilisateur WHERE pseudo = '{pseudo}'"
            cursor.execute(request)
            data = cursor.fetchone()
            connection.commit()
        except sql.Error as err:
            print(err)
        finally:
            if connection.is_connected():
                connection.close()
                if mdp == data[7]:
                    return User(data[1],data[2],data[5],data[6],data[7],data[4],data[3],data[8])
                raise userNonCharger
                  
    @staticmethod
    def verifier_pseudo(pseudo)->bool:
        disponible = True
        try:
            connection = sql.connect(
                host = "localhost",
                user = "root",
                password  = "Daryll08Sylvio08",
                db="sylver_service",
                auth_plugin='mysql_native_password')
            cursor = connection.cursor()
            request = """ SELECT pseudo FROM utilisateur;
                        """
            cursor.execute(request)
            all_pseudo = cursor.fetchall()
            print(all_pseudo)
            if (pseudo,) in all_pseudo:
                disponible = False
            connection.commit()
        except sql.Error as err:
            print(err)
        finally:
            if connection.is_connected():
                connection.close()
            return disponible
    
    @staticmethod
    def get_file(idd = 0)->tuple | noFileException :
        if idd == 1:
            #si c'est pour poster un tuto
            ext_dispo = [("*","*.png"),("*","*.jpg"),("*","*.pdf"),("*","*.docx")]
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
    
    @staticmethod
    def get_r_id():
        m = None
        try:
            connection = sql.connect(
                    host = "localhost",
                    user = "root",
                    password  = "Daryll08Sylvio08",
                    db="sylver_service",
                    auth_plugin='mysql_native_password'
                    )
            cursor = connection.cursor()
            request = "SELECT COUNT(*) FROM utilisateur"
            cursor.execute(request)
            m = cursor.fetchone()[0]
            m += 1
        except sql.Error as err:
            print(err)
        finally:
            if connection.is_connected():
                connection.close()
        return m    
        
#methode pour fichier word, pdt. juste les lires les transfo en bytes et les stocker. reflechir a une maniere de supprimer les tutos depuis sql
class Gerer_requete(User):   
    
    def __init__(self,user : User):
        self.user = user
        super().__init__(prenom=user.prenom,nom = user.nom,age = user.age,pseudo = user.pseudo,
                         mdp = user.mdp,photo_profil=user.photo_profil, tuto_transmis= user.tuto_transmis)       
    
    def save_tuto(self,doc = None, Text = "",nom_tuto= "") -> None:
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
                host = "localhost",
                user = "root",
                password  = "Daryll08Sylvio08",
                db="sylver_service",
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
            connection.commit()
        except sql.Error as err:
            print(err)
        finally:
            if connection.is_connected():
                connection.close()
                
    @staticmethod  
    def rechercher_data(nom_tuto = None,nom_auteur = None)->list:
        try:
            data_recup = [None]
            
            connection = sql.connect(
                host = "localhost",
                user = "root",
                password  = "Daryll08Sylvio08",
                db="sylver_service",
                auth_plugin='mysql_native_password')
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
            if connection.is_connected():
                connection.close()
            return data_recup
    
    @staticmethod
    def fail_open():
        tk.messagebox.showerror("Erreur", "WOW ! L'ouverture a flop :(")
        
    @staticmethod
    def demarrer_fichier(doc,ext,with_path = False)->None:
        if not with_path:
            path = os.path.join('img_center',f"document.{ext}")
            if os.path.exists(path):
                os.remove(path)
            try:
                with open(path,"wb") as File:
                    File.write(doc)
            except OSError:
                # Utilisé pour cacher la fenêtre Tkinter
                Gerer_requete.fail_open()
                return
        else:
            path = doc
        os.startfile(path,'open')
        
    @staticmethod
    def error_occured():
        tkinter.messagebox.showerror("Erreur","WOW ! Une erreur a eu lieu")
        
    @staticmethod
    def est_bytes(doc):
        return isinstance(doc,bytes) and doc != b"0"
    
    
        
    
    
    
                
if __name__ == "__main__":
    connection = sql.connect(
                host = "localhost",
                user = "root",
                password  = "Daryll08Sylvio08",
                db="sylver_service",
                auth_plugin='mysql_native_password')
    cursor = connection.cursor()
    request = "SELECT pseudo,nom,prenom FROM utilisateur;"
    cursor.execute(request)
    recup = cursor.fetchall()
    auteur = []
    for i in recup:
        auteur.append(f"{i[0]}, {i[1]} {i[2]}")
    print(auteur)
    count = []
    for index,i in enumerate(auteur):
        request = f"SELECT COUNT(*) FROM tuto WHERE auteur = '{i}'"
        cursor.execute(request)
        r = cursor.fetchone()
        print(r[0])
        print(auteur[index].split(',')[0])
        request = f"UPDATE utilisateur SET tuto_transmis = tuto_transmis + {r[0]} WHERE pseudo = '{auteur[index].split(',')[0]}'"
        cursor.execute(request)
        count.append(r)
    print(count)