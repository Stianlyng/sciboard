from datetime import datetime, timedelta
from flask import render_template
from flask_login import current_user, login_required
from sqlalchemy import desc
from app import db
from app.models import DocumentHasMetadata,Catalog,TagCategory,CatalogHasTagCategory,User
from app.main import bp



@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()



@bp.route('/', methods=['GET', 'POST'])
@bp.route('/frontpage', methods=['GET', 'POST'])
@login_required
def frontpage():
    metadata = db.session.query(
        DocumentHasMetadata.fk_idDokument,
        DocumentHasMetadata.title,
        DocumentHasMetadata.description,
        DocumentHasMetadata.uploadDate,
        DocumentHasMetadata.views,
        DocumentHasMetadata.votes,
        DocumentHasMetadata.comments,
        User.first_name,
        User.last_name,
        User.id
    ).join(
        User, User.id == DocumentHasMetadata.fk_idUser, isouter=True
    ).order_by(desc(DocumentHasMetadata.uploadDate)
    ).all()

    catalogs = Catalog.query.all()
    categories = db.session.query(TagCategory.categoryName,TagCategory.idTagCategory, CatalogHasTagCategory.fk_idCatalog).join(TagCategory, TagCategory.idTagCategory == CatalogHasTagCategory.fk_idTagCategory).all()

    return render_template('main/frontpage.html', metadata=metadata, catalogs=catalogs, categories=categories)




@bp.route('/popular', methods=['GET', 'POST'])
@login_required
def popular():
    metadata = db.session.query(
        DocumentHasMetadata.fk_idDokument,
        DocumentHasMetadata.title,
        DocumentHasMetadata.description,
        DocumentHasMetadata.uploadDate,
        DocumentHasMetadata.views,
        DocumentHasMetadata.comments,
        User.first_name,
        User.last_name,
        User.id
    ).join(
        User, User.id == DocumentHasMetadata.fk_idUser, isouter=True
    ).order_by(DocumentHasMetadata.views.desc()
    ).all()

    catalogs = Catalog.query.all()
    categories = db.session.query(TagCategory.categoryName,TagCategory.idTagCategory, CatalogHasTagCategory.fk_idCatalog).join(TagCategory, TagCategory.idTagCategory == CatalogHasTagCategory.fk_idTagCategory).all()

    return render_template('main/frontpage.html', metadata=metadata, catalogs=catalogs, categories=categories)


@bp.route('/category/<cat_id>', methods=['GET', 'POST'])
@login_required
def category(cat_id=None):
    metadata = db.session.query(
        TagCategory.idTagCategory,
        DocumentHasMetadata.fk_idDokument,
        DocumentHasMetadata.title,
        DocumentHasMetadata.description,
        DocumentHasMetadata.uploadDate,
        DocumentHasMetadata.views,
        DocumentHasMetadata.comments,
    ).join(
        CatalogHasTagCategory, TagCategory.idTagCategory == CatalogHasTagCategory.fk_idTagCategory
    ).join(
        Catalog, CatalogHasTagCategory.fk_idCatalog == Catalog.idCatalog
    ).join(
        DocumentHasMetadata, Catalog.idCatalog == DocumentHasMetadata.fk_idCatalog
    ).filter(
        TagCategory.idTagCategory == cat_id
    ).all()


    catalogs = Catalog.query.all()
    categories = db.session.query(TagCategory.categoryName,TagCategory.idTagCategory, CatalogHasTagCategory.fk_idCatalog).join(TagCategory, TagCategory.idTagCategory == CatalogHasTagCategory.fk_idTagCategory).all()

    return render_template('main/frontpage.html', metadata=metadata, catalogs=catalogs, categories=categories)

@bp.route('/trending', methods=['GET', 'POST'])
@login_required
def trending():
    today = datetime.utcnow()
    minusDays = timedelta(days=1)
    prevDate = today - minusDays



    metadata = db.session.query(
        DocumentHasMetadata.fk_idDokument,
        DocumentHasMetadata.title,
        DocumentHasMetadata.description,
        DocumentHasMetadata.uploadDate,
        DocumentHasMetadata.views,
        DocumentHasMetadata.comments,
        User.first_name,
        User.last_name,
        User.id
    ).join(
        User, User.id == DocumentHasMetadata.fk_idUser, isouter=True
    ).filter(
        DocumentHasMetadata.uploadDate <= today
    ).filter(
        DocumentHasMetadata.uploadDate >= prevDate
    ).order_by(
        DocumentHasMetadata.views.desc()
    ).all()

    catalogs = Catalog.query.all()
    categories = db.session.query(TagCategory.categoryName,TagCategory.idTagCategory, CatalogHasTagCategory.fk_idCatalog).join(TagCategory, TagCategory.idTagCategory == CatalogHasTagCategory.fk_idTagCategory).all()

    return render_template('main/frontpage.html', metadata=metadata, catalogs=catalogs, categories=categories)





