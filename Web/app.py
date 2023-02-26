from flask import Flask, send_file, Response, make_response, render_template
import os

MYPHOTO = os.path.join("static","myphoto")
app = Flask(__name__, static_folder = "static")

# app.config['UPLOAD_FOLDER'] = MYPHOTO


@app.route("/")
# @app.route("/index")
def start():
    # return send_file('static/myphoto/me.JPG', mimetype='image/jpeg')
    return make_response("Hello! This is start page :).")

@app.route("/photo")
# @app.route("/index")
def photo():
    # return send_file('static/myphoto/me.JPG', mimetype='image/jpeg')
    # return make_response("This is photo page.")
    # return send_file('static/myphoto/me.JPG', mimetype='image/jpeg')
    filename = os.path.join("static/myphoto","me.jpg")
    return render_template("index.html", image = filename)

    
if __name__ == "__main__":
    app.run()