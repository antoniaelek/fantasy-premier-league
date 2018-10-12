from bokeh.models import CategoricalColorMapper
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import gridplot, column
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

df = functions.get_detailed_data(BASE_PATH, SEASON)


def normalize_circle_size(row):
    return 0.1


# set data source for visual
source = ColumnDataSource(data=dict(
    name=df['name'],
    mean_ict_index=df['mean_ict_index'],
    mean_value=df['mean_value'],
    circle_size=df.apply(normalize_circle_size, axis=1)))

tools = "hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"

p = figure(tools=tools, x_axis_label="mean_ict_index", y_axis_label="mean_value")
p.hover.tooltips = """<table>
<tr style="line-height: 0.8; font-size: 17px; font-weight: bold; padding:0; margin: 0">
    <td colspan=2">@name</td>
</tr>
<tr style="line-height: 0.8; font-size: 12px; padding:0; margin: 0">
    <td style="font-weight: bold;">mean_ict_index</td>
    <td>@mean_ict_index</td>
</tr>
<tr style="line-height: 0.8; font-size: 12px; padding:0; margin: 0">
    <td style="font-weight: bold;">mean_value</td>
    <td>@mean_value &pound;</td>
</tr>
</table>
"""
p.scatter(x='mean_ict_index', y='mean_value', radius='circle_size', source=source)

curdoc().add_root(column(p, width=600, height=600, sizing_mode="scale_width"))