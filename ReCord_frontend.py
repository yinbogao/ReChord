from flask import Flask, render_template, request
from WTForms import TextAreaField, SubmitField, RadioField, TextField, validators, ValidationError, Form, StringField
from flask_bootstrap import Bootstrap
from search import prepare_tree, search, find_artic,get_measure
from lxml import etree

"""Create the Flask app"""
DEBUG = True
app = Flask(__name__)
app.config['SECRET_KEY'] = 'DontTellAnyone'
Bootstrap(app)

class xml_form(Form):
    snippet_box = TextAreaField('Snippet',[validators.DataRequired()])
    submit = SubmitField("Submit")

class term_form(Form):
    expressive_terms = StringField('expressive_terms',[validators.DataRequired()])
    submit = SubmitField("Submit")

# home page
@app.route('/', methods=['POST', 'GET'])
def front_page():
    form = xml_form(request.form)
    if request.method == 'POST' and form.validate():
        result = search_demo(form.data)
        return render_template('ReChord_result.html', result=result)
    elif request.method == 'GET'and form.validate():
        result = search_demo(form.data)
        return render_template('ReChord_result.html', result=result)
    return render_template('ReChord_Boot.html', form=form)


# this is a temporary function to get around database
def search_demo(formData):
    tree, _ = prepare_tree('database/Chopin.xml')
    inputXML = etree.parse(formData)
    result = search(inputXML, tree)
    return result


if __name__ == "__main__":
    app.run()

