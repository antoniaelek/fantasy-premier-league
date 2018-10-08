from flask import Flask, render_template, request
from bokeh.embed import server_document
from compare import compare_players
import os

SEASON = os.environ["FPL_SEASON"]
CURR_GW = int(os.environ["FPL_CURR_GW"])
IP = os.environ["FPL_IP"]

app = Flask(__name__)
# Index page, no args
@app.route('/')
def index():
    vpc = server_document("http://" + IP + ":5006/vpc")
    return render_template("index.html", vpc=vpc)


# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    compare_players(SEASON, CURR_GW)
    app.run(host='0.0.0.0')

