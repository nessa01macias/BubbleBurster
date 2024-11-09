  # Main entry point to run the app
from flask import Flask
from blueprints.feedback import feedback_bp
from blueprints.issues import issues_bp
from blueprints.health import health_bp
from blueprints.chatbot import chatbot_bp
from blueprints.settings import settings_bp
from blueprints.progress_tracker import progress_tracker_bp
from models.database import init_db

app = Flask(__name__)
app.config.from_object('config')

# Register Blueprints
app.register_blueprint(feedback_bp, url_prefix='/feedback')
app.register_blueprint(issues_bp, url_prefix='/issues')
app.register_blueprint(health_bp, url_prefix='/health')
app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
app.register_blueprint(settings_bp, url_prefix='/settings')
app.register_blueprint(progress_tracker_bp, url_prefix='/progress')

# Initialize Database
init_db(app)

if __name__ == '__main__':
    app.run(debug=True)
