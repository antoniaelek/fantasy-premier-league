import sys, os
from pathlib import Path

# Add bokeh folder to path
BASE_PATH = str(Path(os.path.dirname(os.path.abspath(__file__))).parent) + "/"
sys.path.append(os.path.abspath(os.path.join(BASE_PATH, 'bokeh')))

from flask import Flask, render_template
from bokeh.embed import server_document
from functions import calc_vpc
from functions import get_detailed_aggregate_data
import compare
import requests


SEASON = os.environ["FPL_SEASON"]
IP = os.environ["FPL_IP"]
BASE_PATH = str(Path(os.path.dirname(os.path.abspath(__file__))).parent) + "/bokeh/"
URL = "https://fantasy.premierleague.com/drf/bootstrap-static"

app = Flask(__name__)
# Index page, no args
@app.route('/')
def index():
    vpc = server_document("http://" + IP + ":5006/vpc")
    aggregate = server_document("http://" + IP + ":5006/aggregate")
    return render_template("index.html", vpc=vpc, aggregate=aggregate)


# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    print("Fetching current gameweek...")
    json = requests.get(URL).json()
    curr_gameweek = json['next-event'] - 1

    # Generate html files with players data
    print("Generating html stats for players comparison...")
    compare.compare_players(SEASON, curr_gameweek)

    # Save vpc data to csv
    print("Generating value-per-cost data...")
    vpc_data = calc_vpc(BASE_PATH, SEASON, curr_gameweek)
    vpc_data.to_csv(BASE_PATH + "/data/" + SEASON + '/vpc_data.csv', sep=';', encoding='latin_1', index=False)

    # Save aggregate data to csv
    print("Generating aggregate data...")
    agg_data = get_detailed_aggregate_data(BASE_PATH, SEASON)
    agg_data.to_csv(BASE_PATH + "/data/" + SEASON + '/aggregate_data.csv', sep=';', encoding='latin_1', index=False)

    app.run(host='0.0.0.0')

