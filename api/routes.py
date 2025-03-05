# api/routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, Annonce

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/annonces")
def get_annonces(db: Session = Depends(get_db)):
    return db.query(Annonce).all()

@router.post("/scrape")
def scrape_and_save(db: Session = Depends(get_db)):
    from scraping.scraper import scrape_annonces
    annonces = scrape_annonces()

    for annonce in annonces:
        new_annonce = Annonce(
            titre=annonce["titre"],
            prix=annonce["prix"],
            localisation=annonce["localisation"],
            lien=annonce["lien"]
        )
        db.add(new_annonce)
    db.commit()

    return {"message": "Scraping terminé", "nombre": len(annonces)}
