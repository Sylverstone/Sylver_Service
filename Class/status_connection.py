
import threading
import time
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
        self.connection = connection_principale         
        threading.Thread(target = self.affiche_status_connexion, daemon=True).start()
          
    def affiche_status_connexion(self):
        """Fonction permettant de vérifier le status de la connetion, une bonne connexion est transcrite par le dessin d'un rond vert sur une 
        surface, une connexion impossible est transcrite par un rond rouge. des tentatives de reconnexion seront faites si celle-ci échoue
        """
        while self.running:            
            if self.connection is None:
                pygame.draw.rect(self.screen,(255,0,0),(0,0,5,5), 0,50)
                self.connection = connect_to_database()
                if self.connection != None:
                    pygame.draw.rect(self.screen,(0,255,0),(0,0,5,5), 0,50)
                else:
                    pygame.draw.rect(self.screen,(255,0,0),(0,0,5,5), 0,50)                    
            else:   
                try:
                    self.connection.ping(False)
                    pygame.draw.rect(self.screen,(0,255,0),(0,0,5,5), 0,50)
                except:
                    pygame.draw.rect(self.screen,(255,0,0),(0,0,5,5), 0,50)
                    self.connection = None
            time.sleep(20)
                    

         
def look_for_connection(con = connection_principale):
    """Fonction verifiant si la connexion est apte a être utilisé, si Non : return False, si Oui : return True

    Returns:
        bool: Return True quand la connexion est disponible, sinon False
    """
    lock = threading.Lock()
    with lock:
        if con is None:
            new_connection = connect_to_database()
            if(new_connection == None):
                return False
            try:
                new_connection.ping(reconnect=False)
                return True
            except Exception:
                return False
        else:
            try:
                con.ping(reconnect=False)
                return True
            except Exception as e:
                return False