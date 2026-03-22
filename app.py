import os
import wave
import ocrmypdf
import hashlib
from pypdf import PdfReader
from piper import PiperVoice
from flask import Flask, render_template, request, jsonify, redirect, send_file

app: Flask = Flask(__name__)

FILECACHE = "./filecache/"
if not os.path.exists(FILECACHE):
    os.makedirs(FILECACHE)

@app.route("/")
def homePage():
    return render_template("app.html")

@app.route("/<hash>")
def filePage(hash: str):
    if not os.path.isfile(FILECACHE + hash + ".pdf"):
        return redirect("/", 302)

    isConverted: bool = os.path.isfile(FILECACHE + hash + ".wav")

    return render_template("app.html", hash=hash, converted=isConverted)
    
# TODO
@app.errorhandler(404)
def page_not_found(error: str):
    return render_template('404.html', error=error), 404

@app.route("/upload", methods=["POST"]) #type: ignore
def upload_file():
    # Get the file, if it does not exist, return an error
    file = request.files["file"]
    if not file:
        return jsonify({"error": "No file!"}), 400

    hashf = hashlib.new("md5")
    while c := file.stream.read(8192):
        hashf.update(c)
    
    hash: str = hashf.hexdigest()

    file.stream.seek(0)

    filename = "./filecache/" + hash + ".pdf"

    file.save(filename)

    try:
        ocrmypdf.ocr(filename, filename) #type: ignore
    except:
        ""

    print("redir to /" + hash)
    return redirect("/" + hash, code = 302)
    # return jsonify({"msg": "File Uploaded", "hash": hash}), 200
    

@app.route("/pdf/<hash>")
def getPdf(hash: str):
    return send_file(FILECACHE + hash + ".pdf")

@app.route("/wav/<hash>")
def getWav(hash: str):
    return send_file(FILECACHE + hash + ".wav", as_attachment=True)

@app.route("/convert/<hash>")
def convertFile(hash: str):

    filename: str = FILECACHE + hash
    print(filename)
    
    reader = PdfReader(filename + ".pdf")
    text: str = ""
    for page in reader.pages:
        text += page.extract_text()
    
    voice: PiperVoice = PiperVoice.load("./voices/en_US-joe-medium.onnx")

    with wave.open(filename + ".wav", "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)

    return redirect("/" + hash, 302)

