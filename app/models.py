import base64
from datetime import datetime, timedelta,date
from hashlib import md5
import json
import os
from time import time
from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
#import redis
#import rq
from app import db, login


class User(UserMixin, db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    first_name = db.Column(db.String(40),nullable=False)
    last_name = db.Column(db.String(40),nullable=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    vertified = db.Column(db.Boolean, unique=False, default=False)


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Author(db.Model):
    __tablename__ = 'Author'

    idAuthor = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(80), nullable=False)
    firstname = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"Author('{self.idAuthor}', '{self.firstname}', '{self.lastname}')"

class Access(db.Model):
    __tablename__ = 'Access'

    idAccess = db.Column(db.Integer, primary_key=True)
    accessType = db.Column(db.String(45), nullable=False)


    def __repr__(self):
        return f"Access('{self.idAccess}', '{self.accessType}')"

class Catalog(db.Model):
    __tablename__ = 'Catalog'
    idCatalog = db.Column(db.Integer, primary_key=True)
    catalogName = db.Column(db.String(80), nullable=False)

    fk_idAccess = db.Column(db.Integer, db.ForeignKey("Access.idAccess"),  default=1)
    fk_Access = db.relationship("Access")
    def __repr__(self):
        return f"Catalog('{self.idCatalog}', '{self.catalogName}', '{self.fk_idAccess}')"


class Document(db.Model):
    __tablename__ = 'Document'
    idDocument = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(10), nullable=False)
    mimetype = db.Column(db.String(50), nullable=False)
    filename = db.Column(db.String(250), nullable=False)
    document = db.Column(db.LargeBinary(length=(2**32)-1)) # Vises som BLOB, må kanskje endres til LONGBLOB

    def __repr__(self):
        return f"Document('{self.idDocument}', '{self.size}', '{self.mimetype}', '{self.filename}', '{self.document}')"

class Thumbnail(db.Model):
    __tablename__ = 'Thumbnail'

    idThumbnail = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(10), nullable=False)
    mimetype = db.Column(db.String(50), nullable=False)
    filename = db.Column(db.String(250), nullable=False)
    image = db.Column(db.LargeBinary(length=(2**32)-1)) # Vises som BLOB, må kanskje endres til LONGBLOB

    fk_idUser = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    fk_user = db.relationship("User")

    def __repr__(self):
        return f"Document('{self.idThumbnail}', '{self.size}', '{self.mimetype}', '{self.filename}', '{self.image}', '{self.fk_idUser}')"


class DocumentHasAuthor(db.Model):

    __tablename__ = 'DocumentHasAuthor'

    __table_args__ = (
        db.PrimaryKeyConstraint('fk_idDokument', 'fk_idAuthor'),
    )

    fk_idDokument = db.Column(db.Integer,db.ForeignKey("Document.idDocument"), primary_key=True,  nullable=False)
    fk_document = db.relationship("Document")

    fk_idAuthor = db.Column(db.Integer, db.ForeignKey("Author.idAuthor"), nullable=False)
    fk_author = db.relationship("Author")

    def __repr__(self):
        return f"DocumentHasAuthor('{self.fk_idDokument}', '{self.fk_idAuthor}', '{self.fk_idAccess}')"

class TagCategory(db.Model):
    __tablename__ = 'TagCategory'

    idTagCategory = db.Column(db.Integer, primary_key=True)
    categoryName = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"TagCategory('{self.idTagCategory}', '{self.categoryName}')"


class Tags(db.Model):
    __tablename__ = 'Tags'

    idTags = db.Column(db.Integer, primary_key=True)
    tagName = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Tags('{self.idTags}', '{self.tagName}')"


class TagCategoryHasTags(db.Model):
    __tablename__ = 'TagCategoryHasTags'

    __table_args__ = (
        db.PrimaryKeyConstraint('fk_idTagCategory', 'fk_idTags'),
    )

    fk_idTagCategory = db.Column(db.Integer, db.ForeignKey("TagCategory.idTagCategory"), primary_key=True, nullable=False)
    fk_tagCategory = db.relationship("TagCategory")

    fk_idTags = db.Column(db.Integer, db.ForeignKey("Tags.idTags"), nullable=False)
    fk_document = db.relationship("Tags")



    def __repr__(self):
        return f"TagCategoryHasTags('{self.fk_idTagCategory}', '{self.fk_idTags}')"

class CatalogHasTagCategory(db.Model):
    __tablename__ = 'CatalogHasTagCategory'

    __table_args__ = (
        db.PrimaryKeyConstraint('fk_idCatalog', 'fk_idTagCategory'),
    )

    fk_idCatalog = db.Column(db.Integer, db.ForeignKey("Catalog.idCatalog"), primary_key=True, nullable=False)
    fk_Catalog = db.relationship("Catalog")

    fk_idTagCategory = db.Column(db.Integer,db.ForeignKey("TagCategory.idTagCategory"), nullable=False)
    fk_TagCategory = db.relationship("TagCategory")

    def __repr__(self):
        return f"CatalogHasTagCategory('{self.fk_idCatalog}', '{self.fk_idTagCategory}')"




class Comment(db.Model):
    __tablename__ = 'Comment'

    idComment = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    comment = db.Column(db.Text(500), nullable=False) #Sjekk denne

    fk_idUser = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    fk_user = db.relationship("User")

    fk_idDokument = db.Column(db.Integer, db.ForeignKey("Document.idDocument"), nullable=False)
    fk_document = db.relationship("Document")

    fk_idComment = db.Column(db.Integer, db.ForeignKey("Comment.idComment"))
    fk_comment = db.relationship("Comment")

    def __repr__(self):
        return f"Comment('{self.idComment}', '{self.date}', '{self.title}', '{self.comment}', '{self.fk_idUser}', '{self.fk_idDokument}')"

class DeletedComment(db.Model):
    __tablename__ = 'DeletedComment'

    idComment = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    comment = db.Column(db.Text(500), nullable=False) #Sjekk denne

    fk_idUser = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    fk_user = db.relationship("User")

    fk_idDokument = db.Column(db.Integer, db.ForeignKey("Document.idDocument"), nullable=False)
    fk_document = db.relationship("Document")

    fk_idComment = db.Column(db.Integer, db.ForeignKey("DeletedComment.idComment"))
    fk_comment = db.relationship("DeletedComment")

    def __repr__(self):
        return f"Comment('{self.idComment}', '{self.date}', '{self.title}', '{self.comment}', '{self.fk_idUser}', '{self.fk_idDokument}')"





class DocumentHasTags(db.Model):
    __tablename__ = 'DocumentHasTags'

    __table_args__ = (
        db.PrimaryKeyConstraint('fk_idDokument', 'fk_idTags'),
    )

    fk_idDokument = db.Column(db.Integer, db.ForeignKey("Document.idDocument"), primary_key=True, nullable=False)
    fk_document = db.relationship("Document")

    fk_idTags = db.Column(db.Integer, db.ForeignKey("Tags.idTags"), nullable=False)
    fk_document = db.relationship("Tags")

    def __repr__(self):
        return f"DocumentHasTags('{self.fk_idDokument}', '{self.fk_idTags}')"


class DocumentHasMetadata(db.Model):
    __tablename__ = 'DocumentHasMetadata'

    idMetadata = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=False)
    uploadDate = db.Column(db.DateTime, default=datetime.utcnow)
    creationDate = db.Column(db.Date, nullable=False)
    views = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    votes = db.Column(db.Integer, default=0)

    fk_idDokument = db.Column(db.Integer, db.ForeignKey("Document.idDocument"),  nullable=False)
    fk_document = db.relationship("Document")

    fk_idDocumentType = db.Column(db.Integer, db.ForeignKey("DocumentType.idType"), nullable=False)
    fk_DocumentType = db.relationship("DocumentType")

    fk_idUser = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    fk_user = db.relationship("User")

    fk_idCatalog = db.Column(db.Integer, db.ForeignKey("Catalog.idCatalog"), nullable=False)
    fk_Catalog = db.relationship("Catalog")

    fk_idAccess = db.Column(db.Integer, db.ForeignKey("Access.idAccess"),nullable=False)
    fk_Access = db.relationship("Access")

    def __repr__(self):
        return f"DocumentHasMetadata('{self.idMetadata}', '{self.title}', '{self.description}', '{self.creationDate}', '{self.uploadDate}', '{self.fk_idDokument}', '{self.fk_idUser}', '{self.fk_idCatalog}', '{self.fk_idAccess}')"

class DocumentType(db.Model):
    __tablename__ = 'DocumentType'

    idType = db.Column(db.Integer, primary_key=True)
    docType = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return f"DocumentType('{self.idType}', '{self.docType}')"
