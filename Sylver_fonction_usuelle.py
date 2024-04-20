import pygame

def draw_text_(text, font = "Comic Sans Ms", color = (0,0,0), x = 0, y = 0,reference_center_x = None,contener = None,size = 20,importer = False, center_multi_line_y = False, ombre = False,center_multi_line = False):
    """Fonction affichant un texte a l'écran

    Args:
        text (str): texte a image_userr
        font (str, optional): nom de la police a image_userr. Defaults to "Comic Sans Ms".
        color (tuple, optional): couleur du texte a image_userr. Defaults to (0,0,0).
        x (int, optional): position en x du texte a image_userr. Defaults to 0.
        y (int, optional): position en y du texte a image_userr. Defaults to 0.
        reference_center_x (pygame.Surface, optional): Surface sur laquelle le texte doit être centré en x. Defaults to None.
        contener (pygame.Surface, optional): Surface sur laquelle le texte doit être image_userr. Defaults to screen.
        size (int, optional): taille du texte a image_userr. Defaults to 20.
        importer (bool, optional): Variable indiquant si la varible n'est pas native a pygame ou non. Defaults to False.
        center_multi_line_y (bool, optional): Variable indiquant si le texte est centrer en y (pour les textes avec \\n). Defaults to False.
        ombre (bool, optional): Variable indiquant si le texte doit comporter une ombre. Defaults to False.
        center_multi_line (bool, optional): Variable indiquant si le texte est centrer en x (pour les textes avec \\n). Defaults to False.
    """
    
    text = str(text) #transformer le texte en str 
    all_text = text.split("\n")
    if not importer:
        font_ = pygame.font.SysFont(font, size)
    else:
        font_ = pygame.font.Font(font,size)
    #boucle pour image_userr tout les textes de all_text
    
    for enum,text in enumerate(all_text):
        if center_multi_line:
            if reference_center_x==None:
                x = contener.get_rect()[2]/2 - font_.size(text)[0]/2
            else:
                x = reference_center_x.get_rect()[2]/2 - font_.size(text)[0]/2
        if center_multi_line_y:
            y = contener.get_rect()[3]/2 - font_.size(text)[1] * len(all_text)/2
        if ombre:
            text_ = font_.render(str(text), True, (0,0,0))            
            contener.blit(text_, (x+1,y+(size+2)*enum))
        text_ = font_.render(str(text), True, color)
        contener.blit(text_, (x,y+(size + 2)*enum))
        
def font(font_name,size,importer = False):
    if not importer:
        return pygame.font.SysFont(font_name,size)
    return pygame.font.Font(font_name,size)

def verification_size(contenaire : pygame.Rect, nom_font : pygame.font, size : int, texte : str,importer : bool = True, id = 0):
        """Fonction récursive permettant de reduire la taille d'un texte si il est trop grand

        Args:
            contenaire (pygame.Rect): Rect que le texte ne doit pas dépasser
            nom_font (pygame.font): nom de la police utilisée
            size (int): taille du texte original
            texte (str): texte a image_userr
        """
        if id == 0:
            if contenaire.w <= font(nom_font,size,importer).size(texte)[0]:
                size -= 2
                return verification_size(contenaire,nom_font,size,texte,importer)
            else:
                return size       
 
def make_line(text : str,font : pygame.font,size_max : int):
    """Fonction permettant de faire le coupage d'un texte par rapport a son contenaire,
    renvoie le nombre de ligne du texte et ses zones de coupages en plus de sa hauteur

    # Args:
        text (str): text que l'on choisi
        font (pygame.font): la police attribué a ce text
        size_max (int): la taille maximum a ne pas depasser

    # Returns:
        (list,int,float): Renvoie la liste de coupages des caractères, renvoie le nombre de ligne qu'occupe le texte, renvoie la hauteur qu'occupe le texte
    
    * Liste de coupages : liste comportant les indices où une nouvelle ligne commence pour le texte
    """
    coupage = [0]
    line = 1
    start = 0
    i = 0
    while i < len(text):
        size = font.size(text[start:i])[0]
        if size + 5 > size_max:
            w = -1
            while text[start:i][w] != " " and abs(w) < len(text[start:i]):
                w -= 1
            if abs(w) == len(text[start:i]):
                #dans le cas ou il n'y a pas d'espace avant le mot
                w = -1
            i += w #i recule jusqua la position de l'espace, pour eviter de couper un mot
            start = i
            coupage.append(start)
            line+=1
        elif text[start:i][-1:] == "\n": #i recule jusqua la position de l'espace, pour eviter de couper un mot
            start = i
            coupage.append(start)
            line+=1
        i+=1
    y = 0
    for i in range(line):
        y = font.size(text)[1] + font.size(text)[1] * i
    return coupage,line,y

def make_line_n(text : str,font : pygame.font,size_max : int):
    """Fonction permettant de faire le coupage d'un texte par rapport a son contenaire,
    dans cette version de make_line, des \n sont ajouter au texte

    # Args:
        text (str): text que l'on choisi
        font (pygame.font): la police attribué a ce text
        size_max (int): la taille maximum a ne pas depasser

    # Returns:
        (list,int,float): Renvoie la liste de coupages des caractères, renvoie le nombre de ligne qu'occupe le texte, renvoie la hauteur qu'occupe le texte
    
    * Liste de coupages : liste comportant les indices où une nouvelle ligne commence pour le texte
    """
    line = 1
    start = 0
    i = 0
    while i < len(text):
        size = font.size(text[start:i])[0]
        if size + 20 > size_max:
            
            w = -1
            while text[start:i][w] != " " and abs(w) < len(text[start:i]):
                w -= 1
            if abs(w) == len(text[start:i]):
                #dans le cas ou il n'y a pas d'espace avant le mot
                w = -1
            i += w #i recule jusqua la position de l'espace, pour eviter de couper un mot
            start = i
            line+=1
            text = text[0:i] + "\n" + text[i:]
        elif text[start:i][-1:] == "\n":
            line += 1
            start = i
        i+=1            
    
    y = font.size(text)[1] + font.size(text)[1] * (line-1)
    return text,line,y

def calcul_height(text, all_text : list,font : pygame.font):
    """Fonction permettant de calculer la taille de plusieur text

    Args:
        text (str): Le texte étudié en total
        all_text (list): chaque ligne du texte
        font (pygame.font): la police attribué au texte

    Returns:
        float: hauteur du texte
    """
    return font.size(text)[1] * len(all_text)
    
    
def draw_line(line :int,coupage : list,text :str,size : int,contener : pygame.Surface,font : str ,fontz : pygame.font,importer : bool = True,x : float=0,y : float=0):
    """Fonction permmettant d'image_userr un texte contenant plusieurs ligne grace a son coupage de texte

    Args:
        line (int): nombre de line utilisé
        coupage (list): Liste précisant les coupures du texte
        text (str): text que l'on ecrit
        size (int): la taille du texte
        contener (pygame.Surface): la surface sur laquel on ecrit le texte
        font (str): le nom de la font
        fontz (pygame.font): la font du texte
        importer (bool, optional): Indique si la font est une font importer Defaults to True.
        x (float, optional): Position x. Defaults to 0.
        y (float, optional): Position y. Defaults to 0.
    """
    back_x = x
    for i in range(line):
        start = coupage[i]
        if i != line - 1:
            limite = coupage[i+1]
        else:
            limite = len(text)
        if back_x == True:
            x = contener.get_width()/2 - fontz.size(f"{text[start:limite]}")[0]/2
        y = y + fontz.size(text)[1] * i
        draw_text_(contener = contener, x = x,
                y = y,
                text = f"{text[start:limite]}",
                size = size, importer = importer, font = font)   

def decoupe_text(coupage : list ,line : int,text_info : str) :
    """Decouper un texte selon son coupage en le mettant dans une liste

    Args:
        coupage (list): liste contenant toute les coupure du texte
        line (int): nombre de ligne du texte
        text_info (str): text utilisé
    Returns:
        list : Represente toutes les lignes du texte
    """
    all_text = []
    for i in range(line):
        start = coupage[i]
        try:
            limite = coupage[i+1]
        except:
            limite = len(text_info)
        all_text.append(text_info[start:limite].strip())
    return all_text

