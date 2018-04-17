import uuid
from io import BytesIO
from flask import Flask, request, render_template, flash, redirect
from werkzeug.utils import secure_filename
from lxml import etree
from search import search, prepare_tree, get_title, get_creator,text_box_search_folder, snippet_search_folder, os

ALLOWED_EXTENSIONS = {'xml', 'mei'}

# initiate the app
app = Flask(__name__) # pylint: disable=invalid-name
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
        path = 'database/test_files'
        return search_snippet(path, request.form['text'])

    # tab1 snippet search using user submitted library
    elif request.form['submit'] == 'Upload and Search Your Snippet':
        path = upload_file("base_file")
        return search_snippet(path, request.form['text'])

    # tab2 terms search
    elif request.form['submit'] == 'Search Parameter':
        tag = request.form['term']
        para = request.form['parameter']
        path = 'database'
        return search_terms(path, tag, para)
    return


# Helper functions

def get_mei_from_folder(path):
    """gets a list of MEI files from a given folder path
    Arguments: path [string]: absolute or relative path to folder
    Returns: all_mei_files: List<file>: list of mei files in path
    """
    return [path + "/" + filename for filename in os.listdir(path) if filename.endswith('.mei') or filename.endswith('.xml')]


def search_snippet(path, snippet):
    """search the snippet from the given database
    Arguments:
        snippet of xml that want to search for
        tree of xml base that needed to be searched in
    Return: rendered result page 'ReChord_result.html'
    """
    xml = BytesIO(snippet.encode())
    input_xml_tree = etree.parse(xml)

    origins = snippet_search_folder(path, input_xml_tree)
    result_list = []
    for key, value in origins.items():
        temp = key + value
        result_list.append(temp)

        # times of appearing
        num_appearance = len(value.split(","))

    return render_template('ReChord_result.html', origins=result_list, appearances=num_appearance)


def search_terms(path, tag, para):
    """ search terms in the database
    Arguments:
        tags of term that want to search for
        para(meters) of tags that want to search for
        tree of xml base that needed to be searched in
    Return: rendered result page 'ReChord_result.html'
    """

    return render_template('ReChord_result.html', result=text_box_search_folder(path, tag, para))


def upload_file(name_tag):
    """pass the upload files and store them in uploads folder's unique sub-folder
    Arguments: name_tag that used in html
    Return: upload path name
    """

    # check if the post request has the file part
    if 'base_file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    else:
        files = request.files.getlist(name_tag)
        file_path = make_upload_dir()

        for file in files:
            # if user does not select file, browser also submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            # if properly uploaded
            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(file_path, filename))
        return file_path


def make_upload_dir():
    """return a unique file_path for each upload
    RETURN: unique file path under uploads folder"""

    file_path = r"database/uploads/" + str(uuid.uuid4()) + "/"
    directory = os.path.dirname(file_path)
    os.makedirs(directory)
    return file_path

if __name__ == "__main__":
    app.run()
