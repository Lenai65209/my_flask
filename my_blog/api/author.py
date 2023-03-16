from flask_combo_jsonapi import ResourceDetail, ResourceList

from ..schemas.author import AuthorSchema
from ..models.database import db
from ..models.author import Author


class AuthorList(ResourceList):
    schema = AuthorSchema
    data_layer = {
        "session": db.session,
        "model": Author,
    }


class AuthorDetail(ResourceDetail):
    schema = AuthorSchema
    data_layer = {
        "session": db.session,
        "model": Author,
    }
