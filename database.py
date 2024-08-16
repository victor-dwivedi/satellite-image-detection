from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:shre_1588%40@localhost:3306/isro_feedback"
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Feedback(Base):
    __tablename__ = "feedbacki"

    id = Column(Integer, primary_key=True, index=True)
    image_filename = Column(String, index=True)
    feedback = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
