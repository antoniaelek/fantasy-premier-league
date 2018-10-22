from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import layout, Row, Column, widgetbox, gridplot
from bokeh.models import ColumnDataSource, CategoricalColorMapper
from bokeh.models.widgets import Select, Div
from bokeh.palettes import d3
from pathlib import Path
import os
import pandas
import functions

# Parameters
# SEASON = os.environ["FPL_SEASON"]
SEASON = "2018-19"

# Get data
APP_ROOT = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)   # refers to application_top
BASE_PATH = APP_ROOT + "/"

NO_CIRCLES = 40

AGG_DF = pandas.read_csv(BASE_PATH + 'bokeh/data/aggregate_data.csv', encoding='latin_1', sep=';')
RAW_DF = functions.get_raw_data(BASE_PATH + 'scraper/', SEASON)

DF_ALL = pandas.merge(AGG_DF, RAW_DF, on='name', how='outer')
DF_GKP = DF_ALL[DF_ALL.position == 'Goalkeeper']
DF_DEF = DF_ALL[DF_ALL.position == 'Defender']
DF_MID = DF_ALL[DF_ALL.position == 'Midfielder']
DF_FWD = DF_ALL[DF_ALL.position == 'Forward']
DF = DF_ALL

x_metric = "ict_index"
y_metric = "total_points"
x_agg_func = "average"
y_agg_func = "average"


def to_pretty(x):
    return " ".join([e.capitalize() for e in x.split('_')])


def from_pretty(x):
    return str.lower(x.replace(' ', '_'))


def update_data(attrname, old, new):
    global DF, DF_ALL, DF_GKP, DF_DEF, DF_MID, DF_FWD
    if new == "Goalkeepers":
        DF = DF_GKP
    elif new == "Defenders":
        DF = DF_DEF
    elif new == "Midfielders":
        DF = DF_MID
    elif new == "Forwards":
        DF = DF_FWD
    else:
        DF = DF_ALL

    source.data=dict(
        name=DF['name'],
        x=DF[from_pretty(x_agg_func + ' ' + x_metric)],
        y=DF[from_pretty(y_agg_func + ' ' + y_metric)],
        x_title=[to_pretty((x_agg_func + "_" + x_metric))]*len(DF['name']),
        y_title=[to_pretty((y_agg_func + "_" + y_metric))]*len(DF['name']),
        position=DF['position'],
        circle_size=[circle_size]*len(DF['name']),
        fill_alpha=[0.3]*len(DF['name']))


def update_x_agg_func(attrname, old, new):
    global x_agg_func, p, circle_size
    x_agg_func = from_pretty(new)
    circle_size = (DF[from_pretty(x_agg_func + ' ' + x_metric)].max() -
                   DF[from_pretty(x_agg_func + ' ' + x_metric)].min()) / NO_CIRCLES
    source.data=dict(
        name=DF['name'],
        x=DF[from_pretty(x_agg_func + ' ' + x_metric)],
        y=DF[from_pretty(y_agg_func + ' ' + y_metric)],
        x_title=[to_pretty(x_agg_func + "_" + x_metric)]*len(DF['name']),
        y_title=[to_pretty(y_agg_func + "_" + y_metric)]*len(DF['name']),
        position=DF['position'],
        circle_size=[circle_size]*len(DF['name']),
        fill_alpha=[0.3]*len(DF['name']))

    p.xaxis.axis_label = to_pretty(x_agg_func + "_" + x_metric)
    p.yaxis.axis_label = to_pretty(y_agg_func + "_" + y_metric)


def update_y_agg_func(attrname, old, new):
    global y_agg_func, p, circle_size
    y_agg_func = from_pretty(new)
    circle_size = (DF[from_pretty(x_agg_func + ' ' + x_metric)].max() -
                   DF[from_pretty(x_agg_func + ' ' + x_metric)].min()) / NO_CIRCLES
    source.data=dict(
        name=DF['name'],
        x=DF[from_pretty(x_agg_func + ' ' + x_metric)],
        y=DF[from_pretty(y_agg_func + ' ' + y_metric)],
        x_title=[to_pretty((x_agg_func + "_" + x_metric))]*len(DF['name']),
        y_title=[to_pretty((y_agg_func + "_" + y_metric))]*len(DF['name']),
        position=DF['position'],
        circle_size=[circle_size]*len(DF['name']),
        fill_alpha=[0.3]*len(DF['name']))

    p.xaxis.axis_label = to_pretty(x_agg_func + "_" + x_metric)
    p.yaxis.axis_label = to_pretty(y_agg_func + "_" + y_metric)


def update_x_metric(attrname, old, new):
    global x_metric, p, circle_size
    x_metric = from_pretty(new)
    circle_size = (DF[from_pretty(x_agg_func + ' ' + x_metric)].max() -
                   DF[from_pretty(x_agg_func + ' ' + x_metric)].min()) / NO_CIRCLES
    source.data=dict(
        name=DF['name'],
        x=DF[from_pretty(x_agg_func + ' ' + x_metric)],
        y=DF[from_pretty(y_agg_func + ' ' + y_metric)],
        x_title=[to_pretty((x_agg_func + "_" + x_metric))]*len(DF['name']),
        y_title=[to_pretty((y_agg_func + "_" + y_metric))]*len(DF['name']),
        position=DF['position'],
        circle_size=[circle_size]*len(DF['name']),
        fill_alpha=[0.3]*len(DF['name']))

    p.xaxis.axis_label = to_pretty(x_agg_func + "_" + x_metric)
    p.yaxis.axis_label = to_pretty(y_agg_func + "_" + y_metric)


def update_y_metric(attrname, old, new):
    global y_metric, p, circle_size
    y_metric = from_pretty(new)
    circle_size = (DF[from_pretty(x_agg_func + ' ' + x_metric)].max() -
                   DF[from_pretty(x_agg_func + ' ' + x_metric)].min()) / 40
    source.data=dict(
        name=DF['name'],
        x=DF[from_pretty(x_agg_func + ' ' + x_metric)],
        y=DF[from_pretty(y_agg_func + ' ' + y_metric)],
        x_title=[to_pretty((x_agg_func + "_" + x_metric))]*len(DF['name']),
        y_title=[to_pretty((y_agg_func + "_" + y_metric))]*len(DF['name']),
        position=DF['position'],
        circle_size=[circle_size]*len(DF['name']),
        fill_alpha=[0.3]*len(DF['name']))

    p.xaxis.axis_label = to_pretty(x_agg_func + "_" + x_metric)
    p.yaxis.axis_label = to_pretty(y_agg_func + "_" + y_metric)


features = functions.get_features_for_aggregation()
aggregates = functions.get_aggregate_functions()

position_div = Div(text="""<h3>Filter by Player Position</h3>""")
palette = d3['Category10'][4]
color_map = CategoricalColorMapper(factors=['Goalkeeper', 'Defender', 'Midfielder', 'Forward'], palette=palette)
select_position = Select(options=['All', 'Goalkeepers', 'Defenders', 'Midfielders', 'Forwards'])

x_agg_div = Div(text="""<h3>X Metrics</h3>""")
select_agg_func_x = Select(options=[to_pretty(a) for a in aggregates], value=to_pretty(x_agg_func))

y_agg_div = Div(text="""<h3>Y Metrics</h3>""")
select_agg_func_y = Select(options=[to_pretty(a) for a in aggregates], value=to_pretty(y_agg_func))

select_metric_x = Select(options=[to_pretty(f) for f in features], value=to_pretty(x_metric))
select_metric_y = Select(options=[to_pretty(f) for f in features], value=to_pretty(y_metric))

select_position.on_change('value', update_data)
select_agg_func_x.on_change('value', update_x_agg_func)
select_agg_func_y.on_change('value', update_y_agg_func)
select_metric_x.on_change('value', update_x_metric)
select_metric_y.on_change('value', update_y_metric)

# set data source for visual
circle_size = (DF[from_pretty(x_agg_func + ' ' + x_metric)].max() -
               DF[from_pretty(x_agg_func + ' ' + x_metric)].min()) / NO_CIRCLES

source = ColumnDataSource(data=dict(
    name=DF['name'],
    x=DF[from_pretty(x_agg_func + ' ' + x_metric)],
    y=DF[from_pretty(y_agg_func + ' ' + y_metric)],
    x_title=[to_pretty(x_agg_func + "_" + x_metric)]*len(DF['name']),
    y_title=[to_pretty(y_agg_func + "_" + y_metric)]*len(DF['name']),
    position=DF['position'],
    circle_size=[circle_size]*len(DF['name']),
    fill_alpha=[0.3]*len(DF['name'])))

tools = "hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom," \
        "undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"
p = figure(tools=tools, x_axis_label=to_pretty(x_agg_func + "_" + x_metric), y_axis_label=to_pretty(y_agg_func + "_" + y_metric))
p.hover.tooltips = """<table>
<tr style="line-height: 0.8; font-size: 17px; font-weight: bold; padding:0; margin: 0">
    <td colspan=2">@name</td>
</tr>
<tr style="line-height: 0.8; font-size: 12px; padding:0; margin: 0">
    <td style="font-weight: bold;">@x_title</td>
    <td>@x</td>
</tr>
<tr style="line-height: 0.8; font-size: 12px; padding:0; margin: 0">
    <td style="font-weight: bold;">@y_title</td>
    <td>@y</td>
</tr>
</table>
"""
p.scatter(x='x', y='y',
          radius='circle_size', fill_alpha='fill_alpha',
          color={'field': 'position', 'transform': color_map},
          source=source)

selects = layout([[position_div],
                  [widgetbox(select_position)],
                  [x_agg_div],
                  [widgetbox(select_agg_func_x)],
                  [widgetbox(select_metric_x)],
                  [y_agg_div],
                  [widgetbox(select_agg_func_y)],
                  [widgetbox(select_metric_y)]])
curdoc().add_root(layout([[selects, p]], sizing_mode='scale_height'))
