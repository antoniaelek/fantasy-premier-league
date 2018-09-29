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
SEASON = "2018-19"
CURR_GW = 6

# Get data
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
BASE_PATH = APP_ROOT + "/"

df = functions.calc_vpc(BASE_PATH, SEASON, CURR_GW)
df_gkp = df[df.position == 'Goalkeeper']
df_def = df[df.position == 'Defender']
df_mid = df[df.position == 'Midfielder']
df_fwd = df[df.position == 'Forward']

palette = d3['Category10'][4]
color_map = CategoricalColorMapper(factors=['Goalkeeper', 'Defender', 'Midfielder', 'Forward'], palette=palette)
select = Select(options=['All', 'Goalkeepers', 'Defenders', 'Midfielders', 'Forwards'])

# set data source for visual
source = ColumnDataSource(data=dict(
    names=df['display_name'],
    position=df['position'],
    points_per_game=df['total_points'],
    vpc_ratio=df['vpc_ratio'],
    now_cost=df['value'],
    circle_size=df['vpc_ratio'] / 2,
    fill_alpha=df['vpc_ratio'] / 2))


def update_data(attrname, old, new):
    if new == "Goalkeepers":
        curr_df = df_gkp
    elif new == "Defenders":
        curr_df = df_def
    elif new == "Midfielders":
        curr_df = df_mid
    elif new == "Forwards":
        curr_df = df_fwd
    else:
        curr_df = df

    source.data = dict(
        names=curr_df['display_name'],
        position=curr_df['position'],
        points_per_game=curr_df['total_points'],
        vpc_ratio=curr_df['vpc_ratio'],
        now_cost=curr_df['value'],
        circle_size=curr_df['vpc_ratio'] / 2,
        fill_alpha=curr_df['vpc_ratio'] / 2)


select.on_change('value', update_data)

tools = "hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"

p = figure(tools=tools, x_axis_label="cost", y_axis_label="avg points", x_range=(3, 15), y_range=(0, 10))
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
