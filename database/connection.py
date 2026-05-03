from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

DB_URL = os.getenv("DATABASE_URL")
engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if __name__ == "__main__":
    if DB_URL is None:
        print("❌ Error: DB_URL is still None.")
    else:
        try:
            with engine.connect() as connection:
                print("✅ Successfully connected to the RigRadar database!")
        except Exception as e:
            print(f"❌ Connection failed: {e}")