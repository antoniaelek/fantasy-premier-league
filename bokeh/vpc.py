from bokeh.models import CategoricalColorMapper
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import column, gridplot
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Select, Div
from bokeh.palettes import d3
from pathlib import Path
import os
import requests
import pandas


def normalize_circle_size(row):
    cs = row['vpc_ratio'] / DF['vpc_ratio'].max()
    if cs > 0.8:
        cs = 0.8
    elif cs < 0.1:
        cs = 0.2
    return cs / 2


def update_data(attrname, old, new):
    if new == "Goalkeepers":
        curr_df = DF_GKP
    elif new == "Defenders":
        curr_df = DF_DEF
    elif new == "Midfielders":
        curr_df = DF_MID
    elif new == "Forwards":
        curr_df = DF_FWD
    else:
        curr_df = DF

    SOURCE.data = dict(
        names=curr_df['display_name'],
        position=curr_df['position'],
        points_per_game=curr_df['total_points'],
        vpc_ratio=curr_df['vpc_ratio'],
        now_cost=curr_df['value'],
        circle_size=curr_df.apply(normalize_circle_size, axis=1),
        fill_alpha=[0.3] * len(curr_df['display_name']))


# Get parameters
SEASON = os.environ["FPL_SEASON"]

# Get current gameweek
URL = "https://fantasy.premierleague.com/drf/bootstrap-static"
DATA = requests.get(URL).json()
CURR_GW = DATA['next-event'] - 1

# Get data
APP_ROOT = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)  # refers to application_top
BASE_PATH = APP_ROOT + "/"

DF = pandas.read_csv(BASE_PATH + 'bokeh/data/vpc_data.csv', encoding='latin_1', sep=';')
DF_GKP = DF[DF.position == 'Goalkeeper']
DF_DEF = DF[DF.position == 'Defender']
DF_MID = DF[DF.position == 'Midfielder']
DF_FWD = DF[DF.position == 'Forward']

COLOR_MAP = CategoricalColorMapper(factors=['Goalkeeper', 'Defender', 'Midfielder', 'Forward'],
                                   palette=d3['Category10'][4])
SELECT = Select(options=['All players', 'Goalkeepers', 'Defenders', 'Midfielders', 'Forwards'])

# set data source for visual
SOURCE = ColumnDataSource(data=dict(
    names=DF['display_name'],
    position=DF['position'],
    points_per_game=DF['total_points'],
    vpc_ratio=DF['vpc_ratio'],
    now_cost=DF['value'],
    circle_size=DF.apply(normalize_circle_size, axis=1),
    fill_alpha=[0.3]*len(DF['display_name'])))


SELECT.on_change('value', update_data)

TOOLS = "hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom," \
        "undo,redo,reset,tap,save,box_select,lasso_select,"

P = figure(tools=TOOLS,
           x_axis_label="Cost",
           y_axis_label="Average Points",
           x_range=(DF['value'].min() - 0.2, DF['value'].max() + 0.4),
           y_range=(DF['total_points'].min() - 0.2, DF['total_points'].max() + 0.4))

P.hover.tooltips = """<table>
<tr style="line-height: 0.8; font-size: 17px; font-weight: bold; padding:0; margin: 0">
    <td colspan=2">@names</td>
</tr>
<tr style="line-height: 0.8; font-size: 12px; padding:0; margin: 0">
    <td style="font-weight: bold;">Position</td>
    <td>@position</td>
</tr>
<tr style="line-height: 0.8; font-size: 12px; padding:0; margin: 0">
    <td style="font-weight: bold;">Cost</td>
    <td>@now_cost &pound;</td>
</tr>
<tr style="line-height: 0.8; font-size: 12px; padding:0; margin: 0">
    <td style="font-weight: bold;">Avg points</td>
    <td>@points_per_game</td>
</tr>
<tr style="line-height: 0.8; font-size: 12px; padding:0; margin: 0">
    <td style="font-weight: bold;">Value per cost</td>
    <td>@vpc_ratio</td>
</tr>
</table>
"""

P.scatter(x='now_cost',
          y='points_per_game',
          radius='circle_size',
          fill_alpha='fill_alpha',
          color={'field': 'position', 'transform': COLOR_MAP},
          source=SOURCE)

curdoc().add_root(column(SELECT, P, width=600, height=600, sizing_mode="scale_width"))