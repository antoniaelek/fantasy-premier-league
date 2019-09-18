from functions import get_raw_data
from functions import get_gameweek_data
from functions import map_id_to_str

import os
import requests
import pandas

import plotly.graph_objs as go

import chart_studio
import chart_studio.plotly as py


def plot_vpc(vpc):
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
             type = 'buttons',
             font=dict(color='#404040'),
             bgcolor = 'rgba(255,255,255,100)',
             direction = 'right',
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
                dict(label = 'Midfielders',
                     method = 'update',
                     args = [{'visible': [False, False, True, False]}]),
                dict(label = 'Forwards',
                     method = 'update',
                     args = [{'visible': [False, False, False, True]}])
            ]),
        )
    ])

    layout = go.Layout(
        modebar={'bgcolor': 'rgba(0,0,0,0)'},
        hovermode = 'closest',
        showlegend=False,
        updatemenus=updatemenus, 
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=go.layout.XAxis(
            showgrid=True,
            zeroline=False,
            color='rgba(255,255,255,1)',
            showticklabels=False,
            title=go.layout.xaxis.Title(
                text='Cost',
                font=dict(
                    size=18,
                    color='white'
                )
            )
        ),
        yaxis=go.layout.YAxis(  
            showgrid=True,
            zeroline=False,
            color='rgba(255,255,255,10)',
            showticklabels=False,
            title=go.layout.yaxis.Title(
                text='Value',
                font=dict(
                    size=18,
                    color='white'
                )
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    return fig

def calc_vpc(base_path, season, currgw):
    # cleaned data - df1
    df1 = get_raw_data(base_path, season)
    df1['value'] = df1['now_cost']/10
    df1['id_str'] = df1.apply(map_id_to_str, axis=1)
    df1['display_name'] = df1['name']
    df1['name'] = df1['name'] + ' ' + df1['id_str']
    df1 = df1[['value', 'name', 'position', 'display_name']]

    # data by gws for each player
    df2 = get_gameweek_data(base_path, season, currgw)
    df2 = df2[['name', 'bonus', 'bonus_weighted', 'bps', 'bps_weighted', 'total_points', 'total_points_weighted']]

    # df2.to_csv('in.csv', sep='\t')
    # group by player and calculate ratio
    df2 = df2.groupby(['name']).mean()

    # merge
    df = pandas.merge(df1, df2, on='name', how='outer')
    df['vpc_ratio'] = df['total_points'] / df['value']
    df['vpc_ratio_weighted'] = df['total_points_weighted'] / df['value']

    return df


def map_position_to_color(position):
    if position == 'Goalkeeper':
        return 'rgba(0,53,166, 0.8)'
    elif position == 'Defender':
        return 'rgba(101,255,71, 0.8)'
    elif position == 'Midfielder':
        return 'rgba(254,213,0, 0.8)'
    else:
        return 'rgba(236,0,0, 0.8)'


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
        hoverlabel= dict(
            font=dict(color='#404040'),
            bordercolor='#404040',
            bgcolor='white'
        ),
        hovertemplate = "<b>%{text}</b><br><br>" +
            "Value: %{y:.2f}</br>"+
            "Cost: %{x:.2f}£</br>"+
            "<extra></extra>")