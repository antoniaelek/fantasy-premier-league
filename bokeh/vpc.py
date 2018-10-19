from bokeh.models import CategoricalColorMapper
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Select
from bokeh.palettes import d3
import os
import requests
import pandas

# Parameters
SEASON = os.environ["FPL_SEASON"]

url = "https://fantasy.premierleague.com/drf/bootstrap-static"
data = requests.get(url).json()
CURR_GW = data['next-event'] - 1

# Get data
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
BASE_PATH = APP_ROOT + "/"

DF = pandas.read_csv(BASE_PATH + "data/" + SEASON + '/vpc_data.csv', encoding='latin_1', sep=';')
DF_GKP = DF[DF.position == 'Goalkeeper']
DF_DEF = DF[DF.position == 'Defender']
DF_MID = DF[DF.position == 'Midfielder']
DF_FWD = DF[DF.position == 'Forward']

palette = d3['Category10'][4]
color_map = CategoricalColorMapper(factors=['Goalkeeper', 'Defender', 'Midfielder', 'Forward'], palette=palette)
select = Select(options=['All', 'Goalkeepers', 'Defenders', 'Midfielders', 'Forwards'])


def normalize_circle_size(row):
    cs = row['vpc_ratio'] / 2
    if cs > 1:
        cs = 1
    elif cs < 0.1:
        cs = 0.1
    return cs


def normalize_fill_alpha(row):
    cs = row['vpc_ratio'] / 2
    if cs > 0.8:
        cs = 0.8
    elif cs < 0.1:
        cs = 0.1
    return normalize_circle_size(row)/2


# set data source for visual
source = ColumnDataSource(data=dict(
    names=DF['display_name'],
    position=DF['position'],
    points_per_game=DF['total_points'],
    vpc_ratio=DF['vpc_ratio'],
    now_cost=DF['value'],
    circle_size=DF.apply(normalize_circle_size, axis=1),
    fill_alpha=DF.apply(normalize_fill_alpha, axis=1)))


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

    source.data = dict(
        names=curr_df['display_name'],
        position=curr_df['position'],
        points_per_game=curr_df['total_points'],
        vpc_ratio=curr_df['vpc_ratio'],
        now_cost=curr_df['value'],
        circle_size=curr_df.apply(normalize_circle_size, axis=1),
        fill_alpha=curr_df.apply(normalize_fill_alpha, axis=1))


select.on_change('value', update_data)

tools = "hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"

p = figure(tools=tools, x_axis_label="cost", y_axis_label="avg points", x_range=(3, 14), y_range=(0, 14))
p.hover.tooltips = """<table>
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

p.scatter(x='now_cost', y='points_per_game', radius='circle_size', fill_alpha='fill_alpha',
          color={'field': 'position', 'transform': color_map}, source=source)

curdoc().add_root(column(select, p, width=600, height=600, sizing_mode="scale_width"))
