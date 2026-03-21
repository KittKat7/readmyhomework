# save this as app.py
from flask import Flask, render_template

app: Flask = Flask(__name__)

@app.route("/")
def hello():
    return render_template('app.html')

