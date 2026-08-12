from flask import Flask
from dotenv import load_dotenv

load_dotenv()

from config import Config
from database import db

from routes.auth import auth
from routes.member import member
from routes.trainer import trainer
from routes.admin import admin

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Import models
from models.user import User
from models.user import Notice

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(member)
app.register_blueprint(trainer)
app.register_blueprint(admin)

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=False)