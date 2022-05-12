from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app, render_template_string, redirect, url_for, make_response, session
from flask_login import current_user, login_required
from app import db
from app.models import DocumentHasMetadata, Catalog, TagCategory, CatalogHasTagCategory, Access, DocumentType, User, \
    Comment, Tags
from app.library import bp
from app.library.forms import MetadataForm, CommentForm


@login_required
@bp.route('/document/<doc_id>', methods=['GET', 'POST'])
def document(doc_id=None):
    if doc_id is None:
        pass

    # Sets the active document
    # session['active_document_id'] = doc_id

    # Metadata for document in preview
    metadata = db.session.query(
        DocumentHasMetadata.title,
        DocumentHasMetadata.fk_idDokument,
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
        DocumentHasMetadata.fk_idDokument == doc_id
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
        Comment.fk_idDokument == doc_id
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

    form = CommentForm()
    if form.validate_on_submit():
        commentQuery = Comment(
            comment=form.comment.data,
            fk_idUser=current_user.id,
            fk_idDokument=doc_id
        )
        # Add to commentcounter in metadata
        commentCount = DocumentHasMetadata.query.get(commentQuery.fk_idDokument)
        commentCount.comments += 1
        db.session.add(commentQuery)
        db.session.commit()

        return redirect(request.url)

    return render_template('library/document.html', form=form, tags=tags, catalogs=catalogs, categories=categories,
                           activeDoc=doc_id, commentData=commentData, metadata=metadata)


# Edit Document
@login_required
@bp.route('/document/edit/<doc_id>', methods=['GET', 'POST'])
def editDocument(doc_id=None):
    checkForMeta = DocumentHasMetadata.query.filter(DocumentHasMetadata.fk_idDokument == doc_id).first()

    form = MetadataForm()

    # Choices for the select fields

    # Visibility
    query = Access.query.filter(Access.accessType != 'Admin').all()
    form.access.choices = [(i.idAccess, i.accessType) for i in query]

    # Document Type
    typeQuery = DocumentType.query.all()
    form.type.choices = [(i.idType, i.docType) for i in typeQuery]

    # Subject
    catalogQuery = Catalog.query.all()
    form.catalog.choices = [(i.idCatalog, i.catalogName) for i in catalogQuery]

    # Category
    # This is a the data for a 'dummy' selector what dynamically refreshes with
    # htmx call to url_for('library.getCatalogHasTagCategory')
    CategoryQuery = db.session.query(
        TagCategory.idTagCategory,
        TagCategory.categoryName
    ).join(
        CatalogHasTagCategory, TagCategory.idTagCategory == CatalogHasTagCategory.fk_idTagCategory
    ).filter(
        CatalogHasTagCategory.fk_idCatalog == catalogQuery[0].idCatalog
    ).all()

    # choices = [(i.idTagCategory, i.categoryName) for i in CategoryQuery]

    if form.validate_on_submit():

        print(request.form.get('category', type=int))

        document = DocumentHasMetadata.query.filter_by(fk_idDokument=doc_id).first()
        print(document)
        if document is not None:
            document.title = form.title.data
            document.description = form.description.data
            document.creationDate = form.date.data
            document.uploadDate = document.uploadDate
            document.fk_idCatalog = form.catalog.data
            document.fk_idAccess = form.access.data
            document.fk_idDocumentType = form.type.data
        else:
            addMeta = DocumentHasMetadata(
                title=form.title.data,
                description=form.description.data,
                creationDate=form.date.data,
                fk_idDokument=doc_id,
                fk_idUser=current_user.id,
                fk_idCatalog=form.catalog.data,
                fk_idAccess=form.access.data,
                fk_idDocumentType=form.type.data)
            db.session.add(addMeta)

        db.session.commit()


        return redirect(url_for('library.editDocument', doc_id=doc_id))

        # For sidebar
    catalogs = Catalog.query.all()

    categories = db.session.query(
        TagCategory.categoryName,
        CatalogHasTagCategory.fk_idCatalog
    ).join(
        TagCategory, TagCategory.idTagCategory == CatalogHasTagCategory.fk_idTagCategory
    ).all()

    return render_template('library/edit-document.html', form=form, doc_id=doc_id, CategoryQuery=CategoryQuery,
                           catalogs=catalogs, categories=categories,checkForMeta=checkForMeta)


# Inserts the correct tag category in select
@bp.route('/getCatalogHasTagCategory', methods=['GET'])
def getCatalogHasTagCategory():
    idCatalogArg = request.args.get('catalog')

    # Category
    CategoryQuery = db.session.query(
        TagCategory.idTagCategory,
        TagCategory.categoryName
    ).join(
        CatalogHasTagCategory, TagCategory.idTagCategory == CatalogHasTagCategory.fk_idTagCategory
    ).filter(
        CatalogHasTagCategory.fk_idCatalog == idCatalogArg
    ).all()

    templ = """
            <option value="" disabled>Select A Category</option>
            {% for choice in CategoryQuery %}
            <option value="{{ choice.idTagCategory }}">{{ choice.categoryName }}</option>
            {% endfor %}
            """
    print(CategoryQuery)
    return render_template_string(templ, CategoryQuery=CategoryQuery)


# List of my documents
@login_required
@bp.route('/document/<username>/', methods=['GET', 'POST'])
def myDocuments(username=None):
    # Metadata for document in preview
    metadata = db.session.query(
        DocumentHasMetadata.title,
        DocumentHasMetadata.fk_idDokument,
        DocumentHasMetadata.description,
        DocumentHasMetadata.uploadDate,
        DocumentHasMetadata.creationDate,
        DocumentHasMetadata.views,
        DocumentHasMetadata.votes,
        Catalog.catalogName,
        User.id
    ).join(
        User, User.id == DocumentHasMetadata.fk_idUser
    ).join(
        Catalog, Catalog.idCatalog == DocumentHasMetadata.fk_idCatalog
    ).filter(
        DocumentHasMetadata.fk_idUser == current_user.id
    ).all()

    # For sidebar
    catalogs = Catalog.query.all()

    categories = db.session.query(
        TagCategory.categoryName,
        CatalogHasTagCategory.fk_idCatalog
    ).join(
        TagCategory, TagCategory.idTagCategory == CatalogHasTagCategory.fk_idTagCategory
    ).all()

    return render_template('library/my-documents.html', catalogs=catalogs, categories=categories, metadata=metadata)
