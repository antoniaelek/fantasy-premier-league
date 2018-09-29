from flask import Flask, render_template, request
from bokeh.embed import server_document

app = Flask(__name__)
# Index page, no args
@app.route('/')
def index():
    vpc = server_document("http://localhost:5006/vpc")
    return render_template("index.html", vpc=vpc)


# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    app.run(host='0.0.0.0')

