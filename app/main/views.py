from flask import render_template
from . import main
from .forms import ExhibitForm

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/exhibit')
def exhibit():
    # name = None
    form = ExhibitForm()
    return render_template('exhibit.html', form = form)
