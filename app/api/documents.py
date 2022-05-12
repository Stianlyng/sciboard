from flask import jsonify, request, url_for, abort, render_template_string, session, make_response,redirect
from app import db
from app.models import User, DocumentHasMetadata, Document,Comment,Tags,DocumentHasTags
from app.api import bp
from app.api.forms import UploadDocumentForm

from werkzeug.utils import secure_filename

@bp.route('/docs/<id>/views', methods=['GET', 'POST'])
def getView(id=None):
    if id is not None:
        voo = db.session.query(
            DocumentHasMetadata.idMetadata,
            DocumentHasMetadata.views,
            DocumentHasMetadata.comments,
            DocumentHasMetadata.votes
        ).all()
        return render_template_string(voo)



@bp.route('/docs/<vote>/<doc_id>', methods=['GET', 'POST'])
def docVote(doc_id=None,vote=None):

    voteCounter = DocumentHasMetadata.query.filter(DocumentHasMetadata.fk_idDokument == doc_id).first()
    if vote == "up":
        voteCounter.votes += 1
    if vote == "down":
        voteCounter.votes += -1
    db.session.commit()
    data = voteCounter.votes


    return render_template_string(str(data))



@bp.route('/docs/search/', methods=['POST'])
@bp.route('/docs/search/<tag_id>', methods=['POST'])
def documentSearch(tag_id=None):
    templ = """
                {% for result in searchResults %}
                <li class="relative bg-white py-5 px-4 hover:bg-gray-50 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600">
                    <div class="flex justify-between space-x-3">
                        <div class="min-w-0 flex-1">
                            <a href="{{ url_for('library.document', doc_id=result.fk_idDokument ) }}" class="block focus:outline-none">
                                <span class="absolute inset-0" aria-hidden="true"></span>
                                <p class="text-sm font-medium text-gray-900 truncate">{{ result.title }}</p>
                                <p class="text-sm text-gray-500 truncate">@{{ result.username }}</p>
                            </a>
                        </div>
                        <time class="flex-shrink-0 whitespace-nowrap text-sm text-gray-500">
                            {{ moment(result.creationDate).fromNow() }}
                        </time>
                    </div>
                    <div class="mt-1">
                        <p class="line-clamp-2 text-sm text-gray-600">{{ result.description }}</p>
                    </div>
                </li>
            {% endfor %}
        """
    # Gets the current chars in search input
    searchWord = request.form.get('search', None)

    # The default search results
    searchResults = db.session.query(
        DocumentHasMetadata.idMetadata,
        DocumentHasMetadata.title,
        DocumentHasMetadata.description,
        DocumentHasMetadata.creationDate,
        DocumentHasMetadata.fk_idDokument,
        )
    # Filter by the search input
    if searchWord is not None:
        searchResults = searchResults.filter(
            DocumentHasMetadata.title.ilike(f'%{searchWord}%')
            )
    # Filter by tags with the filtericon
    if tag_id is not None:
        searchResults = searchResults.join(
            DocumentHasTags, DocumentHasTags.fk_idDokument == DocumentHasMetadata.fk_idDokument
        ).filter(
            DocumentHasTags.fk_idTags == tag_id
        )

    # The returned results
    searchResults = searchResults.all()
    print(searchResults)
    # if the search params does not yield any results show this str instead..
    if not searchResults:
        templ = """<p class="ml-6 mt-6"> No results matching your criteria...</p>"""

    return render_template_string(templ, searchResults=searchResults)


# Get PDF From database
@bp.route('/pdf/<id>', methods=['GET'])
def getPDF(id=None):
    if id is not None:
        session['active_document_id'] = id
        # Add a view to a Document
        docCount = DocumentHasMetadata.query.get(id)
        if docCount is not None:
            docCount.views += 1
            db.session.commit()

        # File handler
        binary_pdf = Document.query.filter(Document.idDocument == id).first()
        response = make_response(binary_pdf.document)
        response.headers.set('Content-Type', binary_pdf.mimetype)
        response.headers.set('Content-Length', binary_pdf.size)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers.set('Content-Disposition', 'inline', filename=binary_pdf.idDocument)
        return response




@bp.route('/upload-modal', methods=['GET', 'POST'])
def upload_modal():
    form = UploadDocumentForm()
    if form.validate_on_submit():

        # File Upload
        fileData = form.file.data
        fileName = secure_filename(fileData.filename)
        mimeType = fileData.mimetype

        # More stuff for db
        blob = fileData.read()
        size = len(blob)

        # Add file to database
        doc = Document(size=size, mimetype=mimeType, filename=fileName, document=blob)
        db.session.add(doc)
        db.session.commit()
        return redirect(url_for('library.editDocument', doc_id=doc.idDocument))

    templ = "{% include 'components/modals/upload-modal.html' %}"
    return render_template_string(templ, form=form)


@bp.route('/delete', methods=['GET'])
def delete():
    return render_template_string('<div class="hidden"></div>')