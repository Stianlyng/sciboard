from flask import render_template, redirect, url_for,current_app
from flask_login import current_user,login_required
from app import db
from app.admin import bp
from app.models import User,Comment,DeletedComment, DocumentHasMetadata




@login_required
@bp.route('/', methods=['GET', 'POST'])
@bp.route('/comments', methods=['GET', 'POST'])
def comments():
    if current_user.email not in current_app.config['ADMINS']:
        return redirect(url_for('main.frontpage'))

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


@login_required
@bp.route('/deleted-comments', methods=['GET', 'POST'])
def deletedComments():
    if current_user.email not in current_app.config['ADMINS']:
        return redirect(url_for('main.frontpage'))
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



@login_required
@bp.route('/delete-comment/<comment_id>', methods=['GET', 'POST'])
def deleteComment(comment_id=None):
    if current_user.email not in current_app.config['ADMINS']:
        return redirect(url_for('main.frontpage'))

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


@login_required
@bp.route('/users', methods=['GET', 'POST'])
def users():
    if current_user.email not in current_app.config['ADMINS']:
        return redirect(url_for('main.frontpage'))
    metadata = User.query.all()

    return render_template('admin/users.html',
                           metadata=metadata,
                           activeTab='all-users',)


@login_required
@bp.route('/delete-user/<user_id>', methods=['GET', 'POST'])
def deleteUser(user_id=None):
    if current_user.email not in current_app.config['ADMINS']:
        return redirect(url_for('main.frontpage'))

    commentToDelete = User.query.get(user_id)
    db.session.delete(commentToDelete)
    db.session.commit()

    return redirect(url_for('admin.users'))