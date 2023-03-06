from flask import Blueprint, render_template, request, current_app, redirect, \
    url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

from ..forms.article import CreateArticleForm
from ..models.author import Author
from ..models.article import Article
from ..models.database import db


articles_app = Blueprint("articles_app", __name__)
users_app = Blueprint("users_app", __name__)


@articles_app.route("/", endpoint="list")
def articles_list():
    articles = Article.query.all()
    return render_template("articles/list.html", articles=articles)


@articles_app.route("/<int:article_id>/", endpoint="details")
def article_details(article_id: int):
    article = Article.query.filter_by(id=article_id).one_or_none()
    if article is None:
        raise NotFound
    return render_template("articles/details.html", article=article)


@articles_app.route("/create/", methods=["GET", "POST"], endpoint="create")
@login_required
def create_article():
    error = None
    form = CreateArticleForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        _article = Article(title=form.title.data.strip(), body=form.body.data)
        if current_user.author:
            # use existing author if present
            _author=current_user.author
            _article.author_id = _author.id
        else:
            # otherwise create author record
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.flush()
            _article.author_id = author.id
        db.session.add(_article)
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create a new article!")
            error = "Could not create article!"
        else:
            return redirect(
                url_for("articles_app.details", article_id=_article.id))
    return render_template("articles/create.html", form=form, error=error)
