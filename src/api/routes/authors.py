import os
from flask import Blueprint, request, url_for, current_app
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.authors import Author, AuthorSchema
from api.utils.database import db

allowed_extensions = set(['image/jpeg', 'image/png', 'jpeg'])

def allowed_file(filetype):
    return filetype in allowed_extensions


author_routes = Blueprint("author_routes", __name__)

@author_routes.route('/', methods=['POST'])
@jwt_required()
def create_author():
    """
        Create author endpoint
        ---
        parameters:
            - in: body
              name: body
              schema:
                id: Author
                required:
                    - first_name
                    - last_name
                    - books
                properties:
                    first_name:
                        type: string
                        description: First name of the author
                        default: John
                    last_name:
                        type: string
                        description: Last name of the author
                        default: "Doe"
            - in: header
              name: authorization
              type: string
              required: true
        security:
            - Bearer: []
        responses:
            200:
                description: Author successfully created
                schema:
                    id: AuthorCreated
                    properties:
                        code:
                            type: string
                        message:
                            type: string
                        value:
                            schema:
                                id: AuthorFull
                                properties:
                                    first_name:
                                        type: string
                                    last_name:
                                        type: string
                                    books:
                                        type: array
                                        items:
                                            schema:
                                                id: BookSchema
            422:
                description: Invalid input arguments
                schema:
                    id: invalidInput
                    properties:
                        code:
                            type: string
                        message:
                            type: string
    """

    try:
        data = request.get_json()
        author_schema = AuthorSchema(load_instance=True)
        author = author_schema.load(data)
        result = author_schema.dump(author.create())
        return response_with(resp.SUCCESS_201, value={"author": result})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@author_routes.route('/', methods=['GET'])
def get_author_list():
    fetched = Author.query.all()
    author_schema = AuthorSchema(many=True, only=['first_name', 'last_name', 'id'])
    authors = author_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"authors": authors})


@author_routes.route('/<int:author_id>', methods=['GET'])
def get_author_detail(author_id):
    fetched = Author.query.get_or_404(author_id)
    author_schema = AuthorSchema()
    author = author_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route('/<int:author_id>', methods=['PATCH'])
@jwt_required()
def update_author_detail(author_id):
    data = request.get_json()
    get_author = Author.query.get_or_404(author_id)
    if data.get('first_name', None):
        get_author.first_name = data['first_name']
    if data.get('last_name', None):
        get_author.last_name = data['last_name']
    db.session.add(get_author)
    db.session.commit()
    author_schema = AuthorSchema()
    author = author_schema.dump(get_author)
    return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route('/<int:author_id>', methods=['DELETE'])
@jwt_required()
def delete_author(author_id):
    get_author = Author.query.get_or_404(author_id)
    db.session.delete(get_author)
    db.session.commit()
    return response_with(resp.SUCCESS_204)


@author_routes.route('/avatar/<int:author_id>', methods=['POST'])
@jwt_required()
def upsert_author_avatar(author_id):
    """
    Upsert author avatar
    ---
    parameters:
        - in: body
          name: body
          schema:
            id: Author2
            required:
                - avatar
            properties:
                avatar:
                    type: file
                    description: Image file
        - name: author_id
          in: path
          description: ID of the author
          required: true
          schema:
            type: integer
    responses:
        200:
            description: Author avatar successfully upserted
            schema:
                id: AuthorCreated
                properties:
                    code:
                        type: string
                    message:
                        type: string
                    value:
                        schema:
                            id: AuthorFull
                            properties:
                                first_name:
                                    type: string
                                last_name:
                                    type: string
                                books:
                                    type: array
                                    items:
                                        schema:
                                            id: BookSchema
        422:
            description: Invalid input arguments
            schema:
                id: invalidInput
                properties:
                    code:
                        type: string
                    message:
                        types: string
    """
    try:
        file = request.files['avatar']
        get_author = Author.query.get_or_404(author_id)
        if file and allowed_file(file.content_type):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        get_author.avatar = url_for('uploaded_file', filename=filename, _external=True)
        db.session.add(get_author)
        db.session.commit()
        author_schema = AuthorSchema()
        author = author_schema.dump(get_author)
        return response_with(resp.SUCCESS_200, value={"author": author})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)
