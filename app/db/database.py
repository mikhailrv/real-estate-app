from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import urllib.parse

password = "P@ssw0rd"   
encoded_password = urllib.parse.quote(password)

engine = create_engine(f"postgresql://postgres:{encoded_password}@localhost/cian")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

try:
    with engine.connect() as connection:
        print("norm")
except Exception as e:
    print("ne norm", e)

