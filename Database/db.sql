CREATE TABLE `categorie` (
  `nom` varchar(100) NOT NULL,
  `description` text,
  `membre` int DEFAULT NULL,
  `tuto_count` int DEFAULT NULL,
  PRIMARY KEY (`nom`)
);

CREATE TABLE `signalements` (
  `id_signalement` int NOT NULL AUTO_INCREMENT,
  `id_tuto_signaler` int NOT NULL,
  `signalement` text NOT NULL,
  `pseudo` text NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`id_signalement`)
);

CREATE TABLE `tuto` (
  `nom` varchar(255) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `doc` mediumblob,
  `text_ctn` text,
  `id` int NOT NULL AUTO_INCREMENT,
  `auteur` varchar(255) DEFAULT NULL,
  `file` varchar(100) DEFAULT NULL,
  `signalement` int DEFAULT '0',
  `type_de_tuto` varchar(100) DEFAULT NULL,
  `categorie` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `utilisateur` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) DEFAULT NULL,
  `prenom` varchar(100) DEFAULT NULL,
  `tuto_transmis` int DEFAULT '0',
  `photo_profil` longblob,
  `age` int DEFAULT NULL,
  `pseudo` varchar(255) DEFAULT NULL,
  `mot_de_passe` varchar(100) DEFAULT NULL,
  `rect_photo_profil` varchar(100) DEFAULT NULL,
  `admin` int DEFAULT '0',
  `categorie` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `pseudo` (`pseudo`)
) ;
