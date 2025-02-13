
import threading
import pygame
import pymysql as sql 
from connection_fonction import connect_to_database
from get_co import connection_principale



class status_connection:
    """Class permettant de gerer le status de la connection

        Args:
            screen (pygame.Surface): surface sur laquelle sera dessiné le rond indiquant la connection
    """
    def __init__(self,screen):
        
        self.screen = screen
        self.running = True
        self.connection_principale = connection_principale         
        threading.Thread(target = self.affiche_status_connexion, daemon=True).start()
          
    def affiche_status_connexion(self):
        """Fonction permettant de vérifier le status de la connetion, une bonne connexion est transcrite par le dessin d'un rond vert sur une 
        surface, une connexion impossible est transcrite par un rond rouge. des tentatives de reconnexion seront faites si celle-ci échoue
        """
        connection_principale = self.connection_principale
        while self.running:            
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
                    self.connection_principale = conn
                    pygame.draw.rect(self.screen,(0,255,0),(0,0,5,5), 0,50)
                else:
                    self.connection_principale = None
                    pygame.draw.rect(self.screen,(255,0,0),(0,0,5,5), 0,50)
                    

         
def look_for_connection(con = connection_principale):
    """Fonction verifiant si la connexion est apte a être utilisé, si Non : return False, si Oui : return True

    Returns:
        bool: Return True quand la connexion est disponible, sinon False
    """
    lock = threading.Lock()
    connection_principale = con
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
                connection_principale.ping(reconnect=True)
                return True
            except sql.Error as e:
                
                connection_principale = None
                return False