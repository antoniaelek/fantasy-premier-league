import numpy as np
import glob
import pandas
from bokeh.io import *
from bokeh.plotting import figure, show, output_file, ColumnDataSource

def parse_data():
    """ Parse and store all the data
    """
    df = pandas.DataFrame()
    for f in glob.glob("C:\\Users\\aelek\\source\\repos\\FantaSeaViz\\data\\2016-17\\gws\\*"):
        dftmp = pandas.read_csv(f, index_col='name', encoding='ansi')
        dftmp = dftmp[['value', 'total_points']]
        df = df.append(dftmp)

    # group by player
    res = df.groupby(['name']).sum()

    # calculate ratio
    res['ratio'] = res['value'] / res['total_points']
    res = res[res['ratio'] > 1]
    res = res.sort_values(['total_points'], ascending=False)

    x = res['value']/10
    y = res['total_points']
    radii = 10#res['ratio']/100

    source = ColumnDataSource(
        data=dict(
            x=x,
            y=y,
            radii=radii,
            name=res.index.values,
        )
    )

    colors = [
        "#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(50+2*x, 30+2*y)
    ]

    TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"

    p = figure(tools=TOOLS)
    p.hover.tooltips = [
        ("name", "@name"),
        ("name2", "")
    ]
    p.scatter(x='x', y='y', radius='radii', source=source,
              fill_color=colors, fill_alpha=0.6,
              line_color=None)

    # output_file("color_scatter.html", title="color_scatter.py example")
    output_notebook()
    show(p)

def main():
    parse_data()

if __name__ == "__main__":
    main()