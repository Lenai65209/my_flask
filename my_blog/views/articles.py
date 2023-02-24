from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

from .users import USERS


articles_app = Blueprint("articles_app", __name__)
ARTICLES = {
    1: {'title': "Flask", "text": "text Flask", "author": 1},
    2: {'title': "Django", "text": "text Django", "author": 2},
    3: {'title': "JSON:APIo", "text": "text JSON:API", "author": 3},
}


@articles_app.route("/", endpoint="list")
def articles_list():
    return render_template("articles/list.html", articles=ARTICLES)


@articles_app.route("/<int:article_id>/", endpoint="details")
def article_details(article_id: int):
    try:
        article_text = ARTICLES[article_id]['text']
        article_author_id = ARTICLES[article_id]['author']
        article_name = ARTICLES[article_id]['title']
        article_author = USERS[article_author_id]
    except KeyError:
        raise NotFound(f"Article #{article_id} doesn't exist!")
    return render_template('articles/details.html', article_id=article_id,
                           article_name=article_name, article_text=article_text,
                           article_author=article_author,
                           article_author_id=article_author_id)
