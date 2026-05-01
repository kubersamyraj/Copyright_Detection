from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from pipeline import process_file

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file uploaded"
    
    file = request.files["file"]

    if file.filename == "":
        return "No selected file"
    
    filename = secure_filename(file.filename)
    custom_name = request.form.get("custom_name", "").strip()
    if custom_name:
        custom_name = secure_filename(custom_name)
        if custom_name:
            extension = os.path.splitext(filename)[1]
            if os.path.splitext(custom_name)[1] == "":
                filename = custom_name + extension
            else:
                filename = custom_name

    path = os.path.abspath(os.path.join(UPLOAD_FOLDER, filename))
    file.save(path)

    print("File saved:", path)

    result = process_file(path)

    return render_template(
        "result.html",
        filename=filename,
        audio_score=round(result["audio_score"] * 100, 2),
        video_score=round(result["video_score"] * 100, 2),
        final_score=round(result["final_score"] * 100, 2),
        detected=result["detected"],
        message=result["message"],
        tx_hash=result["tx_hash"],
        matched_file=result.get("matched_file"),
        stats=result.get("stats", {})
    )

if __name__ == "__main__":
    app.run(debug=True)