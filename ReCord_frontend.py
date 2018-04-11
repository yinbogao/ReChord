from io import BytesIO
from flask import Flask, request, render_template, flash, redirect
from werkzeug.utils import secure_filename
from lxml import etree
from search import search, prepare_tree, get_title, get_creator,text_box_search, os

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'xml', 'mei'}

# initiate the app
app = Flask(__name__) # pylint: disable=invalid-name
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = '\x82\xebT\x17\x07\xbbx\xd9\xe1dxR\x11\x8b\x0ci\xe1\xb7\xa8\x97\n\xd6\x01\x99'


def allowed_file(filename):
    """check the file name to avoid possible hack
    Arguments: uploaded file's name
    Return: rendered result page 'ReChord_result.html'
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def my_form():
    """render front page template
    Return: rendered front page 'ReChord_front.html'
    """
    return render_template('ReChord_front.html')


@app.route('/', methods=['POST'])
def my_form_post():
    """the view function which return the result page by using the input pass to the back end
    Arguments: forms submitted in ReChord_front.html
    Return: rendered result page 'ReChord_result.html' by call on helper functions
    """

    # todo: Need to iterate multiple user submitted files

    # tab1 snippet search
    if request.form['submit'] == 'Search Snippet In Our Database':
        tree, _ = prepare_tree('database/Chopin.xml')
        return search_snippet(request.form['text'], tree)

    # tab1 snippet search using user submitted library
    elif request.form['submit'] == 'Upload and Search Your Snippet':
        filename = upload_file('base_file')
        tree, _ = prepare_tree(str('uploads/' + filename))
        return search_snippet(request.form['text'], tree)

    # tab2 terms search
    elif request.form['submit'] == 'Search Parameter':
        tag = request.form['term']
        para = request.form['parameter']
        tree, _ = prepare_tree('database/Chopin.xml')
        return search_terms(tag, para, tree)
    return



# Helper functions


def search_snippet(snippet, tree):
    """search the snippet from the given database
    Arguments:
        snippet of xml that want to search for
        tree of xml base that needed to be searched in
    Return: rendered result page 'ReChord_result.html'
    """
    # todo: prepare the database
    # get_mei_from_database('database/MEI_Complete_examples')

    xml = BytesIO(snippet.encode())
    input_xml = etree.parse(xml)
    input_root = input_xml.getroot()

    snippet_measure = search(input_root, tree)
    title = get_title(tree)
    creator = get_creator(tree)
    return render_template('ReChord_result.html', results=snippet_measure, title=title, creator=creator)


def search_terms(tag, para, tree):
    """ search terms in the database
    Arguments:
        tags of term that want to search for
        para(meters) of tags that want to search for
        tree of xml base that needed to be searched in
    Return: rendered result page 'ReChord_result.html'
    """

    return render_template('ReChord_result.html', result=text_box_search(tree.root, tag, para))


def upload_file(name_tag):
    """pass the upload file and store it in uploads folder
    Arguments: name_tag that used in html
    Return: rendered result page 'ReChord_result.html'"""

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
