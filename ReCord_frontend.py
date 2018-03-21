from flask import Flask, render_template, request
from wtforms import TextAreaField, SubmitField, RadioField, SelectField, validators, ValidationError, Form
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
    expressive_terms = RadioField('expressive_terms', choices=["stacatto", "allegro", "allegrissimo", ])
    submit = SubmitField("Submit")

# home page
@app.route('/', methods=['POST', 'GET'])
def front_page():
    form = xml_form(request.form)
    if request.method == 'POST' and form.validate():
        # this is faking for the result since second input is missing
        result = search(form.data, form.data)
        return render_template('ReChord_result.html', result=result)
    elif request.method == 'GET'and form.validate():
        result = search(form.data, form.data)
        return render_template('ReChord_result.html', result=result)
    return render_template('search_test_2.html', form=form)


if __name__ == "__main__":
    app.run()

