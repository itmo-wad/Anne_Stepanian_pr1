from flask import Flask, render_template, request, flash, redirect, send_from_directory
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"]="mongodb://localhost:27017/wad"

mongo = PyMongo(app)

@app.route("/")
def home():
    user=mongo.db.users.find({})
    return render_template("index.html",users=user)

@app.route("/signup")
def signup():
    user=mongo.db.users.find({})
    return render_template("signup.html")

@app.route("/auth", methods=["GET","POST"])
def auth():
    if request.method == "GET":
        return render_template("auth.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        user=mongo.db.users.find({"username":username})

        if user and check_password_hash(user["password"],password):
            return render_template("secret.html")
        else:
            return "Error"

    return render_template("auth.html")


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
@app.route("/upload",methods=["GET","POST"])
def upload(): 
    if request.method == "POST":
        myfile = request.files["file"]
        
        if myfile in ALLOWED_EXTENSIONS:
            myfile.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))
            flash("Successfully uploaded")
        else:
            flash("File is not uploaded")
    return render_template("upload.html")

@app.route("/upload/<filename>")
def uploadedfile(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"],filename)


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)