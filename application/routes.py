from application import app
from flask import render_template

@app.route('/')
@app.route('/AboutUs')
def AboutUs():
    return render_template('AboutUs.html')

@app.route('/HelpCenter')
def HelpCenter():
    return render_template('HelpCenter.html')

@app.route('/History')
def History():
    return render_template('History.html')
