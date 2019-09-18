from functions import get_upcoming_team_fixtures_data
from functions import get_upcoming_fixtures_data
from functions import get_past_fixtures_data
from functions import get_past_team_fixtures_data

import numpy as np

import os
import requests
import pandas

import plotly.offline
import plotly.graph_objects as go

import chart_studio
import chart_studio.plotly as py


def next_fixtures(season, base_path, no_fixtures=6):
    clubs_h = list(get_upcoming_fixtures_data(base_path, season)['team_h'].unique())
    clubs_a = list(get_upcoming_fixtures_data(base_path, season)['team_a'].unique())
    clubs = sorted(set(clubs_h + clubs_a))
    
    fig = go.Figure()
    alldf=pandas.DataFrame()

    for club in clubs:
        df = get_upcoming_team_fixtures_data(club, base_path, season).head(no_fixtures)
        df['team']=club
        df['sum_difficulty'] = df['difficulty'].rolling(min_periods=1, window=no_fixtures).sum()
        alldf = alldf.append(df)
        
    return alldf.set_index(['team'])
    

def form(season, base_path, no_fixtures=6):
    clubs_h = list(get_upcoming_fixtures_data(base_path, season)['team_h'].unique())
    clubs_a = list(get_upcoming_fixtures_data(base_path, season)['team_a'].unique())
    clubs = sorted(set(clubs_h + clubs_a))

    alldf=pandas.DataFrame()
    
    j=0
    for club in clubs:
        df = get_past_team_fixtures_data(club,base_path,season).tail(no_fixtures)
        df['team']=club
        df['location']=df['where']
        df['points']=df.apply(points, axis=1)
        df['result']=df.apply(result, axis=1)
        df['result_type']=df.apply(resultType, axis=1)
        df['description']=df.apply(description, axis=1)
        df['fixture_form']=(df['scored']-df['concieved']+1)*df['relative_difficulty']*0.33
        df['i']=[1 + x * 0.1 for x in range(0,no_fixtures)]
        df['form']=df['i']*df['fixture_form']
        df['form'] = df['form'].rolling(min_periods=1, window=no_fixtures).sum()
        j+=1
                
        alldf = alldf.append(df)
        
    return alldf.set_index(['team'])


def points(row):
    points = 3 if row.scored > row.concieved else 0
    points = 0 if row.scored < row.concieved else points
    points = 1 if row.scored == row.concieved else points
    
    if (row.difficulty < row.difficulty_other):
        points -= (3-points)
    elif (row.difficulty > row.difficulty_other):
        points += (3-points)
    
    return points


def result(row):
    if row.is_home:
        return str(int(row.scored)) + ':' + str(int(row.concieved))
    return str(int(row.concieved)) + ':' + str(int(row.scored))


def resultType(row):
    if row.scored > row.concieved:
        return 'W'
    elif row.scored < row.concieved:
        return 'L'
    return 'D'

def description(row):
    return row.result + ' vs ' + row.opponent + ' (' + row.location + ')'
    

def next_fixtures_plot(season, base_path, data, limit_diff=100.0):
    clubs_h = list(get_upcoming_fixtures_data(base_path, season)['team_h'].unique())
    clubs_a = list(get_upcoming_fixtures_data(base_path, season)['team_a'].unique())
    clubs = sorted(set(clubs_h + clubs_a))
    
    fig = go.Figure()

    for club in clubs:
        df = data.loc[club]

        if (df.iloc[-1]['sum_difficulty']>limit_diff):
            continue
        
        fig.add_trace(go.Scatter(
            x=df['event'], 
            y=df['difficulty'],
            name=club,          
            mode='lines',
            line=dict(shape='spline', width=4, smoothing=1.3),
            text = df['opponent'] + ' (' + df['where'] + ')',
            hoverlabel= dict(
                font=dict(color='#404040'),
                bordercolor='#404040',
                bgcolor='white'
            ),            
            hovertemplate = "<b>"+club+"</b></br></br>vs %{text}</br></br><extra></extra>"))
        
    fig.update_layout(
        hovermode='x',
        legend=go.layout.Legend(
            traceorder="normal",
            font=dict(color="#eee"),
            bgcolor="rgba(0,0,0,0)"
        )
    )
    
    x_min=df[['event']].iloc[0]-1
    x_max=df[['event']].iloc[-1]+1
    fig.update_yaxes(title_text="Difficulty",color='#eee',showgrid=False, zeroline=False, tick0=1, dtick=1, range=[1.5, 5])
    fig.update_xaxes(title_text="Gameweek",color='#eee',showgrid=True, zeroline=True, tick0=1, dtick=1, range=[x_min, x_max])

    fig.update_scenes(bgcolor='rgba(0,0,0,0)')

    fig.layout.update(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    chart_studio.plotly.plot(fig, filename="easiest_schedule", auto_open=False)
    #plotly.offline.iplot(fig)


def form_plot(season, base_path, data, no_fixtures=6,limit_form=-10):
    clubs_h = list(get_upcoming_fixtures_data(base_path, season)['team_h'].unique())
    clubs_a = list(get_upcoming_fixtures_data(base_path, season)['team_a'].unique())
    clubs = sorted(set(clubs_h + clubs_a))
    
    fig = go.Figure()
    alldf=pandas.DataFrame()
    
    j=0
    for club in clubs:
        df = data.loc[club]
        
        if (df['form'].iloc[-1] < limit_form):
            continue        
        
        alldf = alldf.append(df)
        
        fig.add_trace(go.Scatter(
            x=df['event'], 
            y=df['form'],
            name=club,
            text = df['description'],     
            mode='lines+markers',
            line=dict(shape='spline', width=4, smoothing=1.3),
            hoverlabel= dict(font=dict(color='#404040'),
                             bordercolor='#404040',
                             bgcolor='white'
            ),
            hovertemplate = "<b>"+club+"</b></br></br></br>Form: %{y}</br>%{text}</br></br><extra></extra>"))
        
    fig.update_layout(
        hovermode='closest',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        legend=go.layout.Legend(
            traceorder="normal",
            font=dict(color="#eee"),
            bgcolor="rgba(0,0,0,0)"
        )
    )
    
    fig.update_yaxes(title_text="Form",color='#eee',tick0=1,dtick=1,showgrid=False,zeroline=False)
    fig.update_xaxes(title_text="Gameweek",color='#eee',tick0=1,dtick=1,showgrid=True,zeroline=True)

    fig.update_scenes(bgcolor='rgba(0,0,0,0)')

    fig.layout.update(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    chart_studio.plotly.plot(fig, filename="club_form", auto_open=False)
    #plotly.offline.iplot(fig)


def main():
    print('Fetching curr gameweek...')
    URL = "https://fantasy.premierleague.com/api/bootstrap-static/"
    DATA = requests.get(URL).json()
    CURR_GW_OBJS = [x for x in DATA['events'] if x['is_current'] == True]
    if len(CURR_GW_OBJS) == 0:
        CURR_GW_OBJS = DATA['events']        
    CURR_GW = CURR_GW_OBJS[-1]['id']
    SEASON = '2019-20'
    BASE_PATH = './scraper/'
    
    print('Generating teams fixtures plot...')
    fix = next_fixtures(SEASON, BASE_PATH, no_fixtures=4)
    next_fixtures_plot(SEASON, BASE_PATH, fix,limit_diff=10)
    
    print('Generating teams form plot...')
    df_form = form(SEASON, BASE_PATH, no_fixtures=4)
    form_plot(SEASON, BASE_PATH, df_form, limit_form=1.5)
    

if __name__ == '__main__':
    main()
    