from functions import  calc_vpc
from visuals import map_position_to_color
from visuals import colors
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

from common import BASE_PATH
from common import SEASON
from common import CURR_GW


def get_trace(df, position):
    return go.Scatter(
        x = df['value'],
        y = df['total_points'],
        name= (position+'s'),
        text = df['display_name'],
        mode = 'markers',
        marker=dict(color = map_position_to_color(position),
                    size = df['vpc_ratio'],
                    sizeref = 0.001,
                    sizemode = 'area'),
        hovertemplate = "<b>%{text}</b><br><br>" +
            "Value: %{y:.2f}</br>"+
            "Cost: %{x:.2f}£</br>"+
            "<extra></extra>")

vpc = calc_vpc(BASE_PATH, SEASON, CURR_GW)

goalkeepers = vpc[(vpc['position']=='Goalkeeper') & (vpc['total_points']>0.1)]
defenders = vpc[(vpc['position']=='Defender') & (vpc['total_points']>0.1)]
midfielders = vpc[(vpc['position']=='Midfielder') & (vpc['total_points']>0.1)]
forwards = vpc[(vpc['position']=='Forward') & (vpc['total_points']>0.1)]

trace_gkp = get_trace(goalkeepers,'Goalkeeper')
trace_def = get_trace(defenders,'Defender')
trace_mid = get_trace(midfielders,'Midfielder')
trace_fwd = get_trace(forwards,'Forward')

data = [trace_gkp,trace_def,trace_mid,trace_fwd]

updatemenus = list([
    dict(active=0,
         pad = {'r': 0, 't': 10},
         x = 0,
         y = 1.18,
         xanchor = 'left',
         buttons=list([
            dict(label = 'All',
                 method = 'update',
                 args = [{'visible': [True, True, True, True]}]),
            dict(label = 'Goalkeepers',
                 method = 'update',
                 args = [{'visible': [True, False, False, False]}]),
            dict(label = 'Defenders',
                 method = 'update',
                 args = [{'visible': [False, True, False, False]}]),
            dict(label = 'Forwards',
                 method = 'update',
                 args = [{'visible': [False, False, False, True]}])
        ]),
    )
])

layout = go.Layout(
    hovermode = 'closest',
    showlegend=False,
    updatemenus=updatemenus,
    title=go.layout.Title(
        text='Value Per Cost',
            font=dict(
                size=21
            )
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Cost',
            font=dict(
                size=18
            )
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Value',
            font=dict(
                size=18
            )
        )
    )
)

fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig,filename='out/vpc.html')


