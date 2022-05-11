from flask import jsonify, request, url_for, abort,render_template_string
from app import db
from app.models import User,Document,DocumentHasMetadata
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from sqlalchemy import func

@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)



@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    if token_auth.current_user().id != id:
        abort(403)
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())


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


