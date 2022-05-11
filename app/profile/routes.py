from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app, render_template_string, redirect, url_for, make_response
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from sqlalchemy import desc
from app import db
from app.models import DocumentHasMetadata, Catalog, TagCategory, CatalogHasTagCategory, Document, User, Thumbnail, \
    Access, Tags, DocumentType
from app.profile import bp
from app.profile.forms import UploadThumbnailForm


@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    metadata = db.session.query(
        DocumentHasMetadata.title,
        DocumentHasMetadata.description,
        DocumentHasMetadata.uploadDate,
        User.first_name, User.last_name
    ).join(
        User, User.id == DocumentHasMetadata.fk_idUser
    ).order_by(desc(DocumentHasMetadata.uploadDate)).all()

    catalogs = Catalog.query.all()
    categories = db.session.query(TagCategory.categoryName, CatalogHasTagCategory.fk_idCatalog).join(TagCategory,
                                                                                                     TagCategory.idTagCategory == CatalogHasTagCategory.fk_idTagCategory).all()

    # Fetch Thumbnail

    # Settings Form
    form = UploadThumbnailForm()
    if form.validate_on_submit():
        # File Upload
        fileData = form.image.data
        fileName = secure_filename(fileData.filename)
        mimeType = fileData.mimetype

        # More stuff for db
        blob = fileData.read()
        size = len(blob)

        # Add file to database
        img = Thumbnail(size=size, mimetype=mimeType, filename=fileName, image=blob, fk_idUser=current_user.id)
        db.session.add(img)
        db.session.commit()

        return redirect(url_for('profile.settings'))

    return render_template('profile/settings.html', metadata=metadata, catalogs=catalogs, categories=categories, form=form)


# Get PDF From database
@bp.route('/thumbnail/<id>', methods=['GET'])
def getThumbnail(id=None):
    if id is not None:
        img = Thumbnail.query.filter(Thumbnail.fk_idUser == id).first()
        response = make_response(img.image)
        response.headers.set('Content-Type', img.mimetype)
        response.headers.set('Content-Length', img.size)
        response.headers['Content-Type'] = 'image/jpeg'
        response.headers.set('Content-Disposition', 'inline', filename=img.filename)
        return response




