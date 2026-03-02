/* =========================================================
   1) Base de données
========================================================= */
IF DB_ID('FormationDB') IS NULL
    CREATE DATABASE FormationDB;
GO

USE FormationDB;
GO

/* =========================================================
   1) Nettoyage (si tu relances le script)
========================================================= */
IF OBJECT_ID('dbo.Obtenir', 'U') IS NOT NULL DROP TABLE dbo.Obtenir;
IF OBJECT_ID('dbo.Passer',  'U') IS NOT NULL DROP TABLE dbo.Passer;
IF OBJECT_ID('dbo.Resultats','U') IS NOT NULL DROP TABLE dbo.Resultats;

IF OBJECT_ID('dbo.Inscrire','U') IS NOT NULL DROP TABLE dbo.Inscrire;
IF OBJECT_ID('dbo.SessionFormations','U') IS NOT NULL DROP TABLE dbo.SessionFormations;

IF OBJECT_ID('dbo.Suggerer','U') IS NOT NULL DROP TABLE dbo.Suggerer;
IF OBJECT_ID('dbo.Recommander','U') IS NOT NULL DROP TABLE dbo.Recommander;
IF OBJECT_ID('dbo.RecommandationsIA','U') IS NOT NULL DROP TABLE dbo.RecommandationsIA;

IF OBJECT_ID('dbo.Posseder','U') IS NOT NULL DROP TABLE dbo.Posseder;
IF OBJECT_ID('dbo.ModulesFormations','U') IS NOT NULL DROP TABLE dbo.ModulesFormations;
IF OBJECT_ID('dbo.Formations','U') IS NOT NULL DROP TABLE dbo.Formations;

IF OBJECT_ID('dbo.Utilisateurs','U') IS NOT NULL DROP TABLE dbo.Utilisateurs;
GO

/* =========================================================
   2) Tables “principales”
========================================================= */

CREATE TABLE dbo.Formations (
    id_formation INT IDENTITY(1,1) NOT NULL,
    titre        VARCHAR(255) NOT NULL,
    description  VARCHAR(1000) NOT NULL,
    duree        CHAR(20) NULL,
    CONSTRAINT PK_Formations PRIMARY KEY (id_formation)
);
GO

CREATE TABLE dbo.ModulesFormations (
    id_module INT IDENTITY(1,1) NOT NULL,
    titre     VARCHAR(255) NOT NULL,
    contenu   VARCHAR(2000) NOT NULL,
    duree     CHAR(20) NULL,
    CONSTRAINT PK_ModulesFormations PRIMARY KEY (id_module)
);
GO

CREATE TABLE dbo.Utilisateurs (
    id_utilisateur INT IDENTITY(1,1) NOT NULL,
    nom            CHAR(60) NOT NULL,
    prenom         CHAR(60) NOT NULL,
    email          CHAR(120) NOT NULL,
    CONSTRAINT PK_Utilisateurs PRIMARY KEY (id_utilisateur)
);
GO

CREATE TABLE dbo.RecommandationsIA (
    id_recommandation INT IDENTITY(1,1) NOT NULL,
    date_reco         CHAR(20) NOT NULL,
    score_pertinence  INT NOT NULL,
    motif             VARCHAR(1000) NULL,
    CONSTRAINT PK_RecommandationsIA PRIMARY KEY (id_recommandation)
);
GO

CREATE TABLE dbo.SessionFormations (
    id_session   INT IDENTITY(1,1) NOT NULL,
    id_formation INT NOT NULL,
    date_debut   CHAR(20) NOT NULL,
    date_fin     CHAR(20) NOT NULL,
    lieu         VARCHAR(255) NOT NULL,
    capacite     INT NOT NULL,
    mode_presentiel TINYINT NULL,
    CONSTRAINT PK_SessionFormations PRIMARY KEY (id_session),
    CONSTRAINT FK_SessionFormations_Formations
        FOREIGN KEY (id_formation) REFERENCES dbo.Formations(id_formation)
);
GO

CREATE TABLE dbo.Resultats (
    id_resultats INT IDENTITY(1,1) NOT NULL,
    id_module    INT NOT NULL,
    note         INT NULL,
    reussite     TINYINT NULL,
    date_passage CHAR(20) NOT NULL,
    tentative    TINYINT NULL,
    CONSTRAINT PK_Resultats PRIMARY KEY (id_resultats),
    CONSTRAINT FK_Resultats_ModulesFormations
        FOREIGN KEY (id_module) REFERENCES dbo.ModulesFormations(id_module)
);
GO

/* =========================================================
   4) Tables d’association (N-N)
========================================================= */

-- Posseder : Formations <-> ModulesFormations
CREATE TABLE dbo.Posseder (
    id_module    INT NOT NULL,
    id_formation INT NOT NULL,
    CONSTRAINT PK_Posseder PRIMARY KEY (id_module, id_formation),
    CONSTRAINT FK_Posseder_Module FOREIGN KEY (id_module)
        REFERENCES dbo.ModulesFormations(id_module),
    CONSTRAINT FK_Posseder_Formation FOREIGN KEY (id_formation)
        REFERENCES dbo.Formations(id_formation)
);
GO

-- Suggerer : RecommandationsIA <-> Formations
CREATE TABLE dbo.Suggerer (
    id_recommandation INT NOT NULL,
    id_formation      INT NOT NULL,
    CONSTRAINT PK_Suggerer PRIMARY KEY (id_recommandation, id_formation),
    CONSTRAINT FK_Suggerer_Reco FOREIGN KEY (id_recommandation)
        REFERENCES dbo.RecommandationsIA(id_recommandation),
    CONSTRAINT FK_Suggerer_Formation FOREIGN KEY (id_formation)
        REFERENCES dbo.Formations(id_formation)
);
GO

-- Recommander : Utilisateurs <-> RecommandationsIA
CREATE TABLE dbo.Recommander (
    id_utilisateur     INT NOT NULL,
    id_recommandation  INT NOT NULL,
    CONSTRAINT PK_Recommander PRIMARY KEY (id_utilisateur, id_recommandation),
    CONSTRAINT FK_Recommander_User FOREIGN KEY (id_utilisateur)
        REFERENCES dbo.Utilisateurs(id_utilisateur),
    CONSTRAINT FK_Recommander_Reco FOREIGN KEY (id_recommandation)
        REFERENCES dbo.RecommandationsIA(id_recommandation)
);
GO

-- Inscrire : Utilisateurs <-> SessionFormations (avec date_inscription)
CREATE TABLE dbo.Inscrire (
    id_utilisateur   INT NOT NULL,
    id_session       INT NOT NULL,
    date_inscription CHAR(20) NOT NULL,
    CONSTRAINT PK_Inscrire PRIMARY KEY (id_utilisateur, id_session),
    CONSTRAINT FK_Inscrire_User FOREIGN KEY (id_utilisateur)
        REFERENCES dbo.Utilisateurs(id_utilisateur),
    CONSTRAINT FK_Inscrire_Session FOREIGN KEY (id_session)
        REFERENCES dbo.SessionFormations(id_session)
);
GO

-- Passer : Utilisateurs <-> Resultats
CREATE TABLE dbo.Passer (
    id_utilisateur INT NOT NULL,
    id_resultats   INT NOT NULL,
    CONSTRAINT PK_Passer PRIMARY KEY (id_utilisateur, id_resultats),
    CONSTRAINT FK_Passer_User FOREIGN KEY (id_utilisateur)
        REFERENCES dbo.Utilisateurs(id_utilisateur),
    CONSTRAINT FK_Passer_Resultats FOREIGN KEY (id_resultats)
        REFERENCES dbo.Resultats(id_resultats)
);
GO

-- Obtenir : Utilisateurs <-> Resultats (tel que sur ton schéma)
CREATE TABLE dbo.Obtenir (
    id_utilisateur INT NOT NULL,
    id_resultats   INT NOT NULL,
    CONSTRAINT PK_Obtenir PRIMARY KEY (id_utilisateur, id_resultats),
    CONSTRAINT FK_Obtenir_User FOREIGN KEY (id_utilisateur)
        REFERENCES dbo.Utilisateurs(id_utilisateur),
    CONSTRAINT FK_Obtenir_Resultats FOREIGN KEY (id_resultats)
        REFERENCES dbo.Resultats(id_resultats)
);
GO
