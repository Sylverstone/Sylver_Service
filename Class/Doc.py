import os

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
    def __init__(self,chemin,gerer_requete,bytes_doc = None,nom_tuto = None,auteur = None,ext = None):
        self.Gerer_requete = gerer_requete
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
        print(path)
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
            
            self.Gerer_requete.fail_open(f"{self.nom_tuto} par {self.auteur}{self.ext}")
            return
        else:
            #no erreur
            self.start_now()            
    
    def start_now(self):
        """Fonction permettant de lancer un document"""
        try:
            os.startfile(self.chemin,"open")
        except Exception as e:
            
            self.Gerer_requete.fail_open()
        else:
            #no erreur
            pass    