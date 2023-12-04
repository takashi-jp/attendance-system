from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import ProductionConfig
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(ProductionConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models
from app.models import Employee
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))

# Import routes and commands
from app import routes, commands

# Register blueprints
app.cli.add_command(commands.create_user)