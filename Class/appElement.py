import pygame

class appElement:
    def __init__(self,Surface : pygame.Surface, Rect : pygame.Rect):
        self.__surface__ = Surface
        self.__pos__ = Rect

    def setRect(self,newPos : pygame.Rect):
        if not isinstance(newPos, pygame.Rect):
            raise ValueError("Le rectangle doit être un objet de type pygame.Rect")
        self.__pos__ = newPos
    
    def setSurface(self,newSurface : pygame.Surface):
        if not isinstance(newSurface, pygame.Surface):
            raise ValueError("La surface doit être un objet de type pygame.Surface")
        self.__surface__ = newSurface
    
    def get_pos(self):
        return self.__pos__

    def get_surface(self):
        return self.__surface__
        
    