from application import app
from flask import Flask, jsonify, request, render_template


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

