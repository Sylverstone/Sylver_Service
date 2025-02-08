class Tuto:
    
    def __init__(self,id_auteur,nom,date,doc,contenu,id_,auteur,extension,nb_signalement,
                 type_tuto,categorie,is_annonce):
        
        self.id_auteur = id_auteur 
        self.nom = nom
        self.date = date
        self.doc = doc
        self.contenu = contenu
        self.id_ = id_
        self.auteur = auteur
        self.extension = extension
        self.nb_signalement = nb_signalement
        self.type_tuto = type_tuto
        self.categorie = categorie
        self.is_annonce = is_annonce
    
    def get_tuto_as_list(self):
        return [self.nom,self.date,"doc",self.contenu,self.auteur,self.extension,
                self.nb_signalement,self.type_tuto,self.categorie,self.is_annonce,self.id_auteur]