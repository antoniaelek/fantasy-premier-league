from flask import Flask, render_template, request
from bokeh.embed import server_document
from compare import compare_players
import os
import requests

SEASON = os.environ["FPL_SEASON"]
IP = os.environ["FPL_IP"]

url = "https://fantasy.premierleague.com/drf/bootstrap-static"

app = Flask(__name__)
# Index page, no args
@app.route('/')
def index():
    vpc = server_document("http://" + IP + ":5006/vpc")
    return render_template("index.html", vpc=vpc)


# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    data = requests.get(url).json()
    curr_gameweek = data['next-event'] - 1
    compare_players(SEASON, curr_gameweek)
    app.run(host='0.0.0.0')

