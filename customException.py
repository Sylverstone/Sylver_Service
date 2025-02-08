class UserNotExist(Exception):
    """Class reprensentant que aucun Utilisateur n'a été trouvé

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


class noCategorie(Exception):
    """Class representant une erreur de recherche de categorie

        Args:
            what (str): Message d'erreur
    """
    def __init__(self, what) -> None:
        
        self.what = what
        super().__init__(self.what)

class cannotSignal(Exception):
    def __init__(self, what) -> None:    
        self.what = what
        super().__init__(self.what)
        
class noFileException(Exception):
    """Class reprensentant aucun fichier choisi

        Args:
            what (str): Message d'erreur
    """   
    def __init__(self, what : str) -> None:
        self.what = what
        super().__init__(self.what)