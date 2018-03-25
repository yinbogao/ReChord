from search import prepare_tree, search, find_artic, get_measure
from lxml import etree
from flask import Flask, request, render_template, flash
from io import BytesIO

app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('ReChord_front.html')


@app.route('/', methods=['POST'])
def my_form_post():
    if request.form['submit'] == 'Search Snippet':
        snippet = request.form['text']

        xml = BytesIO(snippet.encode())
        tree, root = prepare_tree('database/Chopin.xml')
        inputXML = etree.parse(xml)
        input_root = inputXML.getroot()

        snippet_measure = search(input_root, tree)
        return render_template('ReChord_result.html', results=snippet_measure)

if __name__ == "__main__":
    app.run()
