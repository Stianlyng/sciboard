from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app, render_template_string, redirect, url_for, make_response,session
from flask_login import current_user, login_required
from app import db
from app.models import DocumentHasMetadata,Catalog,TagCategory,CatalogHasTagCategory,User, Comment,Tags,Access,DocumentType
from app.explore import bp
from sqlalchemy.sql import or_

@login_required
@bp.route('/all/', methods=['GET', 'POST'])
@bp.route('/all/<catalog_id>', methods=['GET', 'POST'])
def index(catalog_id=None):

    searchWord = request.form.get('search', None)

    search = db.session.query(
        DocumentHasMetadata.title,
        DocumentHasMetadata.description,
        DocumentHasMetadata.creationDate,
        DocumentHasMetadata.fk_idDokument,
        User.username,
        User.first_name,
        User.last_name
    ).join(
        User, User.id == DocumentHasMetadata.fk_idUser
    )

    if searchWord is None and catalog_id is None:
        searchResults = search.all()

    if searchWord is not None:
        searchResults = search.filter(or_(
            DocumentHasMetadata.title.ilike(f'%{searchWord}%'), DocumentHasMetadata.creationDate.ilike(f'%{searchWord}%')
        )).all()

    if catalog_id is not None:
        searchResults = db.session.query(
            TagCategory,
            DocumentHasMetadata.title,
            DocumentHasMetadata.description,
            DocumentHasMetadata.creationDate,
            DocumentHasMetadata.fk_idDokument,
        ).join(
            CatalogHasTagCategory, TagCategory.idTagCategory ==  CatalogHasTagCategory.fk_idTagCategory
        ).join(
            Catalog, CatalogHasTagCategory.fk_idCatalog == Catalog.idCatalog
        ).join(
            DocumentHasMetadata, Catalog.idCatalog == DocumentHasMetadata.fk_idCatalog
        ).filter(
            TagCategory.idTagCategory == catalog_id
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

    return render_template('explore/explore.html',tags=tags, searchResults=searchResults, catalogs=catalogs, categories=categories)
