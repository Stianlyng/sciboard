from flask import render_template_string
from app import db
from app.models import User,DocumentHasMetadata
from app.api import bp
from sqlalchemy import func




@bp.route('/top-users/<int:count>', methods=['GET'])
def getTopUsers(count) -> int:
    # Get sum of views pr user
    top_users = db.session.query(
            func.sum(DocumentHasMetadata.views),
            DocumentHasMetadata.fk_idUser,
            User.first_name,
            User.last_name,
            User.username
        ).join(
            User, User.id == DocumentHasMetadata.fk_idUser
        ).group_by(
            DocumentHasMetadata.fk_idUser
        ).limit(
            count
        ).all()

    templ = """
            {% for user in top_users %}
            {% include 'components/top-user.html' %}
            {% endfor %}
            """

    return render_template_string(templ,top_users=top_users)


