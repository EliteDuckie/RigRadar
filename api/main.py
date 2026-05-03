from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import sys
import os
from pathlib import Path
import json

# Add the parent directory to Python's path so it can find your database folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from database.models import CPU

# 1. Initialize the FastAPI app
app = FastAPI(title="RigRadar API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 2. A helper function to safely open and close the database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3. The Home Page Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the RigRadar Backend API! 🚀"}

# 4. The Data Endpoint: Get all CPUs
@app.get("/api/cpus")
def get_all_cpus(db: Session = Depends(get_db)):
    # Query the database for every CPU we have saved
    cpus = db.query(CPU).all()
    return cpus

# 5. The Glossary Endpoint: Serve the hardware glossary JSON
@app.get("/api/glossary")
def get_glossary():
    # Construct the path to the JSON file
    file_path = os.path.join("data", "hardware_glossary.json")
    
    try:
        with open(file_path, "r") as f:
            glossary_data = json.load(f)
        return glossary_data
    except FileNotFoundError:
        return {"error": "Glossary file not found."}