from search import *
from lxml import etree
from flask import Flask, request, render_template
from io import BytesIO


app = Flask(__name__)


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

    # prepare the database
    # get_mei_from_database('database/MEI_Complete_examples')
    tree, root = prepare_tree('database/Chopin.xml')

    # tab1 snippet search
    if request.form['submit'] == 'Search Snippet':
        snippet = request.form['text']

        xml = BytesIO(snippet.encode())
        inputXML = etree.parse(xml)
        input_root = inputXML.getroot()

        snippet_measure = search(input_root, tree)
        return render_template('ReChord_result.html', results=snippet_measure)

    # tab2 terms search
    if request.form['submit'] == 'Search Parameter':
        tag = request.form['term']
        para = request.form['parameter']
        print(para)
        print(tag)

        if tag == 'Expressive Terms':
            result = find_artic(tree, para)
        elif tag == 'Articulation':
            result = find_expressive_term(root, para)
            print(result)

        # # todo
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

if __name__ == "__main__":
    app.run()
