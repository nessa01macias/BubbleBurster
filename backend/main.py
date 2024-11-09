# Main entry point to run the app
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config import DATABASE_URL
from blueprints.feedback import feedback_bp
from blueprints.issues import issues_bp
from blueprints.health import health_bp
from blueprints.chatbot import chatbot_bp
from blueprints.settings import settings_bp
from blueprints.progress_tracker import progress_tracker_bp
from models import models  # Ensures models are loaded for database creation

app = Flask(__name__)
app.config.from_object('config')

# Database Setup (formerly in database.py)
engine = create_engine(DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

def init_db():
    # Import models to ensure they are registered with Base
    import models.models
    Base.metadata.create_all(bind=engine)

# Register Blueprints
app.register_blueprint(feedback_bp, url_prefix='/feedback')
app.register_blueprint(issues_bp, url_prefix='/issues')
app.register_blueprint(health_bp, url_prefix='/health')
app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
app.register_blueprint(settings_bp, url_prefix='/settings')
app.register_blueprint(progress_tracker_bp, url_prefix='/progress')

# Initialize Database
with app.app_context():
    init_db()  # Creates tables in the database if they don't exist

# Dependency for database session in views
@app.teardown_appcontext
def shutdown_session(exception=None):
    SessionLocal.remove()

if __name__ == '__main__':
    app.run(debug=True)
