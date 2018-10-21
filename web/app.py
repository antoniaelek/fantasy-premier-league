import sys, os
from pathlib import Path
import setup

# Add bokeh folder to path
SCRAPER_BASE_PATH = str(Path(os.path.dirname(os.path.abspath(__file__))).parent) + "/"
sys.path.append(os.path.abspath(os.path.join(SCRAPER_BASE_PATH, 'bokeh')))

from flask import Flask, render_template
from bokeh.embed import server_document

SEASON = os.environ["FPL_SEASON"]
IP = os.environ["FPL_IP"]
BASE_PATH = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)
SCRAPER_BASE_PATH = BASE_PATH + "/scraper/"
BOKEH_BASE_PATH = BASE_PATH + "/bokeh/"


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
    if len(sys.argv) < 2 or sys.argv[1] != "--skip-init":
        setup.main()
    app.run(host='0.0.0.0')

