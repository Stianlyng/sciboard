from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app, render_template_string, redirect, url_for, make_response,session
from flask_login import current_user, login_required
from app import db
from app.models import DocumentHasMetadata,Catalog,TagCategory,CatalogHasTagCategory,User, Comment,Tags,Access,DocumentType
from app.explore import bp


@bp.route('/all/', methods=['GET', 'POST'])
@bp.route('/all/<doc_id>', methods=['GET', 'POST'])
@bp.route('catalog/<catalog_id>', methods=['GET', 'POST'])
@login_required
def index(doc_id=None,catalog_id=None):
    if catalog_id is None:
        searchResults = db.session.query(
            DocumentHasMetadata.title,
            DocumentHasMetadata.description,
            DocumentHasMetadata.creationDate,
            DocumentHasMetadata.fk_idDokument,
            User.username,
            User.first_name,
            User.last_name
        ).join(
            User, User.id == DocumentHasMetadata.fk_idUser
        ).all()

    else:
        searchResults = db.session.query(
            DocumentHasMetadata.title,
            DocumentHasMetadata.description,
            DocumentHasMetadata.creationDate,
            DocumentHasMetadata.fk_idDokument,
            User.username,
            User.first_name,
            User.last_name
        ).join(
            User, User.id == DocumentHasMetadata.fk_idUser
        ).join(
            Catalog, Catalog.idCatalog == DocumentHasMetadata.fk_idCatalog
        ).filter(
            DocumentHasMetadata.fk_idCatalog == catalog_id
        ).all()

    if doc_id is None:
        # Gets the id of the first document under the searchbar
        activeDoc = searchResults[0].fk_idDokument
    else:
        activeDoc = doc_id
    # Sets the active document
    session['active_document_id'] = activeDoc

    # Metadata for document in preview
    metadata = db.session.query(
        DocumentHasMetadata.title,
        DocumentHasMetadata.description,
        DocumentHasMetadata.uploadDate,
        DocumentHasMetadata.creationDate,
        DocumentHasMetadata.views,
        DocumentHasMetadata.votes,
        User.username,
        User.first_name,
        User.last_name,
        User.id
    ).join(
        User, User.id == DocumentHasMetadata.fk_idUser
    ).filter(
        DocumentHasMetadata.fk_idDokument == activeDoc
    ).first()

    # Comments for the document in preview
    commentData = db.session.query(
        Comment.date,
        Comment.comment,
        User.first_name,
        User.last_name,
        User.id
    ).join(
        User, User.id == Comment.fk_idUser
    ).filter(
        Comment.fk_idDokument == activeDoc
    ).all()

    # Get all tags for the filter button
    tags = Tags.query.all()

    # For sidebar
    catalogs = Catalog.query.all()

    categories = db.session.query(
        TagCategory.categoryName,
        CatalogHasTagCategory.fk_idCatalog
    ).join(
        TagCategory, TagCategory.idTagCategory == CatalogHasTagCategory.fk_idTagCategory
    ).all()

    return render_template('explore/explore.html',tags=tags, searchResults=searchResults, catalogs=catalogs, categories=categories, activeDoc=activeDoc, commentData=commentData, metadata=metadata)
