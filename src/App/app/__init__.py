from flask import Flask
from flask_cors import CORS
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:root@localhost:3306/ffbs_database")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    CORS(app)

    # Configure file paths
    app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "uploads")
    app.config["EXPORT_FOLDER"] = os.path.join(os.getcwd(), "exports")

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["EXPORT_FOLDER"], exist_ok=True)

    # Register routes dynamically
    from app.routes import register_routes
    register_routes(app)

    return app

def init_db():
    """Initialize SQLAlchemy database structure"""
    import app.models  # Ensure models are loaded
    Base.metadata.create_all(engine)