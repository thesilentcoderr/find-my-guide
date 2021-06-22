from flask import Flask, render_template,request,json,url_for,session,flash

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/bloginfo")
def bloginfo():
    return render_template("bloginfo.html")

if __name__ == "__main__":
    app.run(debug=True)