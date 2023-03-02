import os

from flask import Flask, render_template
from flask_migrate import Migrate

from .configs import DevConfig
from .models.database import db
from .security import flask_bcrypt
from .views.articles import articles_app
from .views.auth import login_manager, auth_app
from .views.users import users_app

app = Flask(__name__)
app.register_blueprint(users_app)
app.register_blueprint(articles_app, url_prefix="/articles")

# from my_blog.configs import DevConfig
app.config.from_object(DevConfig)
# app.config.from_pyfile('config.cfg')

# app.config["CONFIG_NAME"] = "DevConfig"
# cfg_name = os.environ.get("CONFIG_NAME") or "ProductionConfig"
# app.config.from_object(f"my_flask.configs.{cfg_name}")
# app.config.from_object(config.get("CONFIG_NAME" or "ProductionConfig"))
# app.config.from_object(os.environ.get("FLASK_CONFIG") or "ProductionConfig")

file_path = os.path.abspath(os.getcwd()) + "\database.db"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/blog.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

app.config["SECRET_KEY"] = "123456"
app.register_blueprint(auth_app, url_prefix="/auth")
login_manager.init_app(app)

flask_bcrypt.init_app(app)

migrate = Migrate(app, db, compare_type=True, render_as_batch=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


# @app.cli.command("init-db")
# def init_db():
#     """
#     Run in your terminal:
#     flask init-db
#     """
#     db.create_all()
#     print("done!")


@app.cli.command("create-users")
def create_users():
    """
    Run in your terminal:
    flask create-users
    > done! created users: <User #1 'admin'> <User #2 'james'>
    """
    from my_blog.models.user import User
    ivan = User(username="admin", is_staff=True, password="1")
    james = User(username="james", password="2")
    db.session.add(ivan)
    db.session.add(james)
    db.session.commit()
    print("done! created users:", ivan, james)


@app.cli.command("create-admin")
def create_admin():
    """
    Run in your terminal:
    ➜ flask create-admin
    > created admin: <User #1 'admin'>
    """
    from my_blog.models.user import User
    admin = User(username="admin", is_staff=True)
    admin.password = os.environ.get("ADMIN_PASSWORD") or "adminpass"
    db.session.add(admin)
    db.session.commit()
    print("created admin:", admin)
