import os

from flask import Flask, render_template

from my_blog.models.database import db
from my_blog.views.articles import articles_app
from my_blog.views.auth import login_manager, auth_app
from my_blog.views.users import users_app

app = Flask(__name__)
app.register_blueprint(users_app)
app.register_blueprint(articles_app, url_prefix="/articles")

file_path = os.path.abspath(os.getcwd()) + "\database.db"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/blog.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

app.config["SECRET_KEY"] = "123456"
app.register_blueprint(auth_app, url_prefix="/auth")
login_manager.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.cli.command("init-db")
def init_db():
    """
    Run in your terminal:
    flask init-db
    """
    db.create_all()
    print("done!")


@app.cli.command("create-users")
def create_users():
    """
    Run in your terminal:
    flask create-users
    > done! created users: <User #1 'admin'> <User #2 'james'>
    """
    from my_blog.models.user import User
    admin = User(username="admin", is_staff=True)
    james = User(username="james")
    db.session.add(admin)
    db.session.add(james)
    db.session.commit()
    print("done! created users:", admin, james)
