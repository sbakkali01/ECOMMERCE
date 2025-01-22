import os
from time import sleep

from flask import Flask, render_template, request, redirect, flash, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "/home/sami/PycharmProjects/Smart Import/upload"
ALLOWED_EXTENSIONS = {'pdf'}

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SECRET_KEY"]="ayo"


def allowed_file(filename: str):
    return '.' in filename and filename.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)
@app.route('/', methods=["GET", "POST"])
def main_page():
    if request.method == "POST":
        if 'file_input' not in request.files:
            flash("No file was sent !")
            return redirect(url_for("main_page"))
        file = request.files["file_input"]
        if not allowed_file(file.filename):
            flash("The file format is not supported !")
            return redirect(url_for("main_page"))
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('download_file', name=filename))
    else:
        return render_template("index.html")