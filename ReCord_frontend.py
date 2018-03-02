from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from search import prepare_tree, search, find_artic,get_measure
from lxml import etree
"""Create the Flask app"""
DEBUG = True
app = Flask(__name__)

"""Turn user submitted MEI code snippet into xml file."""
def transform_xml(xml_code):
    xml = xml_code.encode()
    f = open('upload.xml', 'wb')
    f.write(xml)
    f.close()

@app.route('/')
def my_form():
    return render_template('search_test_2.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    return transform_xml(text)

if __name__ == "__main__":
    app.run()

