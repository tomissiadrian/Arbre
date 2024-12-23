from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Individu as IndividuModel, Relation  # Import des modèles SQLAlchemy
from schemas import Individu as IndividuSchema, IndividuCreate  # Import des schémas Pydantic
import logging
from datetime import date

# Configuration des logs pour faciliter le débogage
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = FastAPI(
    title="API Arbre Généalogique",
    description="API pour gérer un arbre généalogique avec individus et relations familiales",
    version="1.0.0"
)

# Création des tables dans la base de données
Base.metadata.create_all(bind=engine)

# Dépendance pour gérer la session de base de données
def get_db():
    """
    Crée une nouvelle session de base de données pour chaque requête.
    La session est automatiquement fermée à la fin de la requête.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        ((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((()))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))

@app.post("/individus/", response_model=IndividuSchema)
def create_individu(individu: IndividuCreate, db: Session = Depends(get_db)):
    """
    Crée un nouvel individu dans la base de données.
    
    Args:
        individu: Les données de l'individu à créer
        db: La session de base de données
    
    Returns:
        L'individu créé avec son ID
    """


    try:
        logger.debug(f"Tentative de création d'un individu : {individu}")

        # Vérification des dates
        if individu.date_mort is not None and individu.date_naissance >= individu.date_mort:
            logger.warning("Tentative de création avec date de naissance postérieure à la date de mort")
            raise HTTPException(
                status_code=400,
                detail="La date de naissance doit être antérieure à la date de mort."
            )

        # Création de l'instance du modèle SQLAlchemy
        db_individu = IndividuModel(
            prenom=individu.prenom,
            noms=individu.noms,
            date_naissance=individu.date_naissance,
            date_mort=individu.date_mort
        )

        # Sauvegarde dans la base de données
        db.add(db_individu)
        db.commit()
        db.refresh(db_individu)

        logger.info(f"Individu créé avec succès : ID {db_individu.id}")
        return db_individu

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la création de l'individu : {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création : {str(e)}")
    
    ((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((()))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))

@app.get("/individus/{individu_id}", response_model=IndividuSchema)
def read_individu(individu_id: int, db: Session = Depends(get_db)):
    """
    Récupère les informations d'un individu par son ID.
    
    Args:
        individu_id: L'identifiant unique de l'individu
        db: La session de base de données
    
    Returns:
        Les informations de l'individu
    """
    try:
        logger.debug(f"Tentative de récupération de l'individu avec l'ID: {individu_id}")
        
        # Recherche de l'individu
        db_individu = db.query(IndividuModel).filter(IndividuModel.id == individu_id).first()
        
        if db_individu is None:
            logger.warning(f"Individu avec l'ID {individu_id} non trouvé")
            raise HTTPException(
                status_code=404,
                detail=f"Individu avec l'ID {individu_id} non trouvé dans la base de données."
            )
            
        logger.info(f"Individu {individu_id} trouvé avec succès")
        return db_individu
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'individu {individu_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")
    
((((((((((((((((((((((((((((((((((((((((((((((((((((((((((()))))))))))))))))))))))))))))))))))))))))))))))))))))))))))


@app.delete("/individus/{individu_id}")
def delete_individu(individu_id: int, db: Session = Depends(get_db)):
    """
    Supprime un individu de la base de données.
    
    Args:
        individu_id: L'identifiant unique de l'individu à supprimer
        db: La session de base de données
    
    Returns:
        Un message de confirmation de la suppression
    """
    try:
        logger.debug(f"Tentative de suppression de l'individu avec l'ID: {individu_id}")
        
        # Recherche de l'individu
        db_individu = db.query(IndividuModel).filter(IndividuModel.id == individu_id).first()
        
        if db_individu is None:
            logger.warning(f"Tentative de suppression d'un individu inexistant (ID: {individu_id})")
            raise HTTPException(
                status_code=404,
                detail=f"Individu avec l'ID {individu_id} non trouvé dans la base de données."
            )
        
        # Vérification des relations existantes
        relations = db.query(Relation).filter(
            (Relation.parent_id == individu_id) | (Relation.enfant_id == individu_id)
        ).first()
        
        if relations:
            logger.warning(f"Impossible de supprimer l'individu {individu_id}: relations existantes")
            raise HTTPException(
                status_code=400,
                detail="Impossible de supprimer cet individu car il a des relations familiales. Supprimez d'abord les relations."
            )
            
        # Suppression de l'individu
        db.delete(db_individu)
        db.commit()
        
        logger.info(f"Individu {individu_id} supprimé avec succès")
        return {
            "status": "success",
            "message": f"Individu avec l'ID {individu_id} supprimé avec succès.",
            "deleted_id": individu_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la suppression de l'individu {individu_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression: {str(e)}")

# Point d'entrée pour le démarrage de l'application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)

((((((((((((((((((((((((((((((((((((((((((((((((((()))))))))))))))))))))))))))))))))))))))))))))))))))

@app.patch("/individus/{individu_id}", response_model=IndividuSchema)
def update_individu(individu_id: int, individu_update: IndividuCreate, db: Session = Depends(get_db)):
    """
    Met à jour partiellement les informations d'un individu.
    
    Args:
        individu_id: L'identifiant unique de l'individu à mettre à jour
        individu_update: Les nouvelles données de l'individu (partielles ou complètes)
        db: La session de base de données
    
    Returns:
        Les informations mises à jour de l'individu
    """
    try:
        logger.debug(f"Tentative de mise à jour de l'individu avec l'ID: {individu_id}")
        
        # Recherche de l'individu
        db_individu = db.query(IndividuModel).filter(IndividuModel.id == individu_id).first()
        
        if db_individu is None:
            logger.warning(f"Individu avec l'ID {individu_id} non trouvé")
            raise HTTPException(
                status_code=404,
                detail=f"Individu avec l'ID {individu_id} non trouvé dans la base de données."
            )
        
        # Mise à jour des champs, uniquement si des valeurs sont fournies
        if individu_update.prenom is not None:
            db_individu.prenom = individu_update.prenom
        if individu_update.noms is not None:
            db_individu.noms = individu_update.noms
        if individu_update.date_naissance is not None:
            db_individu.date_naissance = individu_update.date_naissance
        if individu_update.date_mort is not None:
            if individu_update.date_naissance and individu_update.date_naissance >= individu_update.date_mort:
                raise HTTPException(
                    status_code=400,
                    detail="La date de naissance doit être antérieure à la date de mort."
                )
            db_individu.date_mort = individu_update.date_mort
        
        # Sauvegarde des modifications
        db.commit()
        db.refresh(db_individu)

        logger.info(f"Individu {individu_id} mis à jour avec succès")
        return db_individu
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour de l'individu {individu_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la mise à jour: {str(e)}")
