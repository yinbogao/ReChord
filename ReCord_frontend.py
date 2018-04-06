from search import *
from lxml import etree
from flask import Flask, request, render_template, flash, redirect, url_for, send_from_directory
from io import BytesIO
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'xml', 'mei'}

# initiate the app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = '\x82\xebT\x17\x07\xbbx\xd9\xe1dxR\x11\x8b\x0ci\xe1\xb7\xa8\x97\n\xd6\x01\x99'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def my_form():
    """render front page template
        Argument: N/A
        Return: rendered front page 'ReChord_front.html' """
    return render_template('ReChord_front.html')


@app.route('/', methods=['POST'])
def my_form_post():
    """the view function which return the result page by using the input pass to the back end
        Arguments: form submitted in ReChord_front.html
        Return: rendered result page 'ReChord_result.html' """

    # todo: Need to iterate multiple user submitted files

    # tab1 snippet search
    if request.form['submit'] == 'Search Snippet In Our Database':
        tree, root = prepare_tree('database/Chopin.xml')
        return search_snippet(request.form['text'], tree)

    # tab1 snippet search using user submitted library
    if request.form['submit'] == 'Upload and Search Your Snippet':
        filename = upload_file('base_file')
        tree, root = prepare_tree(str('uploads/' + filename))
        return search_snippet(request.form['text'], tree)

    # tab2 terms search
    if request.form['submit'] == 'Search Parameter':
        tag = request.form['term']
        para = request.form['parameter']
        tree, root = prepare_tree('database/Chopin.xml')
        return search_terms(tag, para, tree)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


# Helper function


def search_snippet(snippet, tree):
    """search the snippet from the given database"""
    # todo: prepare the database
    # get_mei_from_database('database/MEI_Complete_examples')

    xml = BytesIO(snippet.encode())
    inputXML = etree.parse(xml)
    input_root = inputXML.getroot()

    snippet_measure = search(input_root, tree)
    title = get_title(tree)
    creator = get_creator(tree)
    return render_template('ReChord_result.html', results=snippet_measure, title=title, creator=creator)


def search_terms(tag, para, tree):
    """ search terms in the database"""

    if tag == 'Expressive Terms':
        # todo: do search on expressive terms
        result = find_artic(tree, para)
    elif tag == 'Articulation':
        result = find_expressive_term(tree.root, para)

    # todo: Integrate more term search
    # elif tag == 'Tempo Marking':
    # elif tag == 'Dynamic Marking':
    # elif tag == 'Piano Fingerings':
    # elif tag == 'Pedal Marking':
    # elif tag == 'Hairpin':
    # elif tag == 'Slur/Ligatures':
    # elif tag == 'Ornaments':
    # elif tag == 'Notes':
    # elif tag == 'Accidental':
    return render_template('ReChord_result.html', result=result)


def upload_file(name_tag):
    """pass the upload file and store it in uploads folder"""

    # check if the post request has the file part
    if 'base_file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    else:
        file = request.files[name_tag]

        # if user does not select file, browser also submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # if properly uploaded
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # todo handle return
            return filename


if __name__ == "__main__":
    app.run()
