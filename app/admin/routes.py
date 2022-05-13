from flask import render_template, redirect, url_for, flash, request,current_app
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from app import db
from app.admin import bp
from app.models import User,Comment,DeletedComment, DocumentHasMetadata
from sqlalchemy import func

@bp.route('/comments', methods=['GET', 'POST'])
def comments():
    metadata = db.session.query(
        DocumentHasMetadata.fk_idDokument,
        Comment.idComment,
        Comment.comment,
        Comment.date,
        User.username
    ).join(
        User, User.id == DocumentHasMetadata.fk_idUser
    ).join(
        Comment, Comment.fk_idDokument == DocumentHasMetadata.fk_idDokument
    ).all()

    return render_template('admin/all-comments.html',
                           metadata=metadata,
                           activeTab='all-comments',
                           )


@bp.route('/deleted-comments', methods=['GET', 'POST'])
def deletedComments():
    metadata = db.session.query(
        DocumentHasMetadata.fk_idDokument,
        DeletedComment.idComment,
        DeletedComment.comment,
        DeletedComment.date,
        User.username
    ).join(
        User, User.id == DocumentHasMetadata.fk_idUser
    ).join(
        DeletedComment, DeletedComment.fk_idDokument == DocumentHasMetadata.fk_idDokument
    ).all()

    return render_template('admin/all-comments.html',
                           metadata=metadata,
                           activeTab='deleted-comments'
                           )



@bp.route('/delete-comment/<comment_id>', methods=['GET', 'POST'])
def deleteComment(comment_id=None):

    commentToDelete = Comment.query.get(comment_id)
    commentToAdd = DeletedComment(
        comment=commentToDelete.comment,
        fk_idUser=commentToDelete.fk_idUser,
        fk_idDokument=commentToDelete.fk_idDokument,
        fk_idComment=commentToDelete.fk_idComment
    )
    db.session.add(commentToAdd)
    db.session.delete(commentToDelete)
    db.session.commit()

    return redirect(url_for('admin.comments'))