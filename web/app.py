from flask import Flask, render_template, request
from bokeh.embed import server_document
from compare import compare_players

SEASON = "2018-19"
CURR_GW = 8

app = Flask(__name__)
# Index page, no args
@app.route('/')
def index():
    vpc = server_document("http://178.128.40.220:5006/vpc")
    return render_template("index.html", vpc=vpc)


# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    compare_players(SEASON, CURR_GW)
    app.run(host='0.0.0.0')

