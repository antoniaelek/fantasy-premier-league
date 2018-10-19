from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import layout
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Select, PreText, Div
import os
import pandas
import functions

# Parameters
# SEASON = os.environ["FPL_SEASON"]
SEASON = "2018-19"

# Get data
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
BASE_PATH = APP_ROOT + "/"

NO_CIRCLES = 40

DF = pandas.read_csv(BASE_PATH + "data/" + SEASON + '/aggregate_data.csv', encoding='latin_1', sep=';')

x_metric = "assists"
y_metric = "assists"
x_agg_func = "mean"
y_agg_func = "mean"


def to_pretty(x):
    return " ".join([e.capitalize() for e in x.split('_')])


def from_pretty(x):
    return str.lower(x.replace(' ', '_'))


def update_x_agg_func(attrname, old, new):
    global x_agg_func, p, circle_size
    x_agg_func = from_pretty(new)
    circle_size = (DF[from_pretty(x_agg_func + ' ' + x_metric)].max() -
                   DF[from_pretty(x_agg_func + ' ' + x_metric)].min())/NO_CIRCLES
    source.data=dict(
        name=DF['name'],
        x=DF[from_pretty(x_agg_func + ' ' + x_metric)],
        y=DF[from_pretty(y_agg_func + ' ' + y_metric)],
        x_title=[to_pretty((x_agg_func + "_" + x_metric))]*len(DF['name']),
        y_title=[to_pretty((y_agg_func + "_" + y_metric))]*len(DF['name']),
        circle_size=[circle_size]*len(DF['name']),
        fill_alpha=[0.3]*len(DF['name']))


def update_y_agg_func(attrname, old, new):
    global y_agg_func, p, circle_size
    y_agg_func = from_pretty(new)
    circle_size = (DF[from_pretty(x_agg_func + ' ' + x_metric)].max() -
                   DF[from_pretty(x_agg_func + ' ' + x_metric)].min())/NO_CIRCLES
    source.data=dict(
        name=DF['name'],
        x=DF[from_pretty(x_agg_func + ' ' + x_metric)],
        y=DF[from_pretty(y_agg_func + ' ' + y_metric)],
        x_title=[to_pretty((x_agg_func + "_" + x_metric))]*len(DF['name']),
        y_title=[to_pretty((y_agg_func + "_" + y_metric))]*len(DF['name']),
        circle_size=[circle_size]*len(DF['name']),
        fill_alpha=[0.3]*len(DF['name']))


def update_x_metric(attrname, old, new):
    global x_metric, p, circle_size
    x_metric = from_pretty(new)
    circle_size = (DF[from_pretty(x_agg_func + ' ' + x_metric)].max() -
                   DF[from_pretty(x_agg_func + ' ' + x_metric)].min())/NO_CIRCLES
    source.data=dict(
        name=DF['name'],
        x=DF[from_pretty(x_agg_func + ' ' + x_metric)],
        y=DF[from_pretty(y_agg_func + ' ' + y_metric)],
        x_title=[to_pretty((x_agg_func + "_" + x_metric))]*len(DF['name']),
        y_title=[to_pretty((y_agg_func + "_" + y_metric))]*len(DF['name']),
        circle_size=[circle_size]*len(DF['name']),
        fill_alpha=[0.3]*len(DF['name']))


def update_y_metric(attrname, old, new):
    global y_metric, p, circle_size
    y_metric = from_pretty(new)
    circle_size = (DF[from_pretty(x_agg_func + ' ' + x_metric)].max() -
                   DF[from_pretty(x_agg_func + ' ' + x_metric)].min())/40
    source.data=dict(
        name=DF['name'],
        x=DF[from_pretty(x_agg_func + ' ' + x_metric)],
        y=DF[from_pretty(y_agg_func + ' ' + y_metric)],
        x_title=[to_pretty((x_agg_func + "_" + x_metric))]*len(DF['name']),
        y_title=[to_pretty((y_agg_func + "_" + y_metric))]*len(DF['name']),
        circle_size=[circle_size]*len(DF['name']),
        fill_alpha=[0.3]*len(DF['name']))


features = functions.get_features_for_aggregation()
aggregates = functions.get_aggregate_functions()

x_agg_div = Div(text="""<h3>X aggregate function</h3>""")
select_agg_func_x = Select(options=[to_pretty(a) for a in aggregates])

y_agg_div = Div(text="""<h3>Y aggregate function</h3?""")
select_agg_func_y = Select(options=[to_pretty(a) for a in aggregates])

select_metric_x = Select(options=[to_pretty(f) for f in features])
select_metric_y = Select(options=[to_pretty(f) for f in features])

select_agg_func_x.on_change('value', update_x_agg_func)
select_agg_func_y.on_change('value', update_y_agg_func)
select_metric_x.on_change('value', update_x_metric)
select_metric_y.on_change('value', update_y_metric)

tools = "hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"

p = figure(tools=tools)
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

# set data source for visual
print(DF[from_pretty(x_agg_func + ' ' + x_metric)].min())
circle_size = (DF[from_pretty(x_agg_func + ' ' + x_metric)].max() -
               DF[from_pretty(x_agg_func + ' ' + x_metric)].min())/NO_CIRCLES
source = ColumnDataSource(data=dict(
    name=DF['name'],
    x=DF[from_pretty(x_agg_func + ' ' + x_metric)],
    y=DF[from_pretty(y_agg_func + ' ' + y_metric)],
    x_title=[to_pretty((x_agg_func + "_" + x_metric))]*len(DF['name']),
    y_title=[to_pretty((y_agg_func + "_" + y_metric))]*len(DF['name']),
    circle_size=[circle_size]*len(DF['name']),
    fill_alpha=[0.3]*len(DF['name'])))
p.scatter(x='x', y='y', radius='circle_size', fill_alpha='fill_alpha', source=source)

curdoc().add_root(layout([[x_agg_div],
                          [select_agg_func_x, select_metric_x],
                          [y_agg_div],
                          [select_agg_func_y, select_metric_y],
                          [p]],
                         width=600, height=600, sizing_mode="scale_width"))