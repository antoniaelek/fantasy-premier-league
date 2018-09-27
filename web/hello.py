# Hello, Flask!
from flask import Flask, render_template, request

app = Flask(__name__)


# Index page, no args
@app.route('/')
def index():
    name = request.args.get("name")
    if name is None:
        name = "Edward"
    return render_template("index.html", name=name)


# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    app.run(port=5000, debug=True)

