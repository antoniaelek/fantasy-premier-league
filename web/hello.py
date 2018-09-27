from flask import Flask, render_template, request
from bokeh.io import *
from bokeh.embed import components
from bokeh.layouts import row
from bokeh.embed import server_document
import functions
import plots

app = Flask(__name__)
# Index page, no args
@app.route('/')
def index():
    # base_path = "C:/Users/aelek/source/antoniaelek/fantasy-premier-league/"
    # season = "2018-19"
    # gw_cnt = 6

    # ppa = functions.calc_vpc(base_path, season, gw_cnt)
    # plot = plots.display_vpc(ppa)

    # Embed plot into HTML via Flask Render
    # script, div = components(plot)
    script = server_document("http://localhost:5006/vpc")

    return render_template("index.html", bokS=script)


# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    app.run(port=5000, debug=True)

