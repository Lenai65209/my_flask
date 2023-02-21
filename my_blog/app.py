from flask import Flask, render_template
from my_blog.views.users import users_app
from my_blog.views.articles import articles_app


app = Flask(__name__)
app.register_blueprint(users_app)
app.register_blueprint(articles_app, url_prefix="/articles")

# @app.route("/")
# def index():
#     return "Hello web!"

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
