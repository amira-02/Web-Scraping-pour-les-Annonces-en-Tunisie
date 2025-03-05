# api/database.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///../data/annonces.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()

class Annonce(Base):
    __tablename__ = "annonces"
    
    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String)
    prix = Column(String)
    localisation = Column(String)
    lien = Column(String)

Base.metadata.create_all(bind=engine)
