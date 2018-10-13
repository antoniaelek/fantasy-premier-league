from bokeh.models import CategoricalColorMapper
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import gridplot, column, layout
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Select
from bokeh.palettes import d3
import os
import functions

# Parameters
#SEASON = os.environ["FPL_SEASON"]
SEASON = "2018-19"

# Get data
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
BASE_PATH = APP_ROOT + "/"

df = functions.get_detailed_aggregate_data(BASE_PATH, SEASON)


x_metric = "assists"
y_metric = "assists"
x_agg_func = "mean"
y_agg_func = "mean"


def normalize_circle_size(row):
    return 0.1


def update_x_agg_func(attrname, old, new):
    global x_agg_func, p
    x_agg_func = new
    source.data=dict(
        name=df['name'],
        x=df[x_agg_func + '_' + x_metric],
        y=df[y_agg_func + '_' + y_metric],
        x_title=[x_agg_func + "_" + x_metric]*len(df['name']),
        y_title=[y_agg_func + "_" + y_metric]*len(df['name']),
        circle_size=[p.x_range.default_span/200]*len(df['name']),
        fill_alpha=[0.3]*len(df['name']))


def update_y_agg_func(attrname, old, new):
    global y_agg_func, p
    y_agg_func = new
    source.data=dict(
        name=df['name'],
        x=df[x_agg_func + '_' + x_metric],
        y=df[y_agg_func + '_' + y_metric],
        x_title=[x_agg_func + "_" + x_metric]*len(df['name']),
        y_title=[y_agg_func + "_" + y_metric]*len(df['name']),
        circle_size=[p.x_range.default_span/200]*len(df['name']),
        fill_alpha=[0.3]*len(df['name']))


def update_x_metric(attrname, old, new):
    global x_metric, p
    x_metric = new
    source.data=dict(
        name=df['name'],
        x=df[x_agg_func + '_' + x_metric],
        y=df[y_agg_func + '_' + y_metric],
        x_title=[x_agg_func + "_" + x_metric]*len(df['name']),
        y_title=[y_agg_func + "_" + y_metric]*len(df['name']),
        circle_size=[p.x_range.default_span/200]*len(df['name']),
        fill_alpha=[0.3]*len(df['name']))


def update_y_metric(attrname, old, new):
    global y_metric, p
    y_metric = new
    source.data=dict(
        name=df['name'],
        x=df[x_agg_func + '_' + x_metric],
        y=df[y_agg_func + '_' + new],
        x_title=[x_agg_func + "_" + x_metric]*len(df['name']),
        y_title=[y_agg_func + "_" + new]*len(df['name']),
        circle_size=[p.x_range.default_span/200]*len(df['name']),
        fill_alpha=[0.3]*len(df['name']))


select_agg_func_x = Select(options=functions.get_aggregate_functions())
select_agg_func_y = Select(options=functions.get_aggregate_functions())

select_metric_x = Select(options=functions.get_features_for_aggregation())
select_metric_y = Select(options=functions.get_features_for_aggregation())

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
source = ColumnDataSource(data=dict(
    name=df['name'],
    x=df[x_agg_func + '_' + x_metric],
    y=df[y_agg_func + '_' + y_metric],
    x_title=[x_agg_func + "_" + x_metric]*len(df['name']),
    y_title=[y_agg_func + "_" + y_metric]*len(df['name']),
    circle_size=[p.x_range.default_span/200]*len(df['name'])))
p.scatter(x='x', y='y', radius='circle_size', source=source)

fig = ()

curdoc().add_root(layout([[select_agg_func_x, select_metric_x], [select_agg_func_y, select_metric_y],[p]]))