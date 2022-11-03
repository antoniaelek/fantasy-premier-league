from urllib import response
import requests , json, csv
import pandas as pd
import os
import numpy as np

import plotly.graph_objs as go

import chart_studio
import chart_studio.plotly as pys

def get_top_picks_df(base_path: str, season: str, overallLeagueID: int, top_n: int, curr_gw: int):
    players_ids_df = pd.read_csv(base_path + 'data/' + season + '/player_idlist.csv') 
    players_ids_df.rename({'id': 'player_id'}, axis=1, inplace=True)
    players_ids_df['full_name'] = players_ids_df['first_name'] + ' ' + players_ids_df['second_name']
    players_ids_df.drop('first_name', axis=1, inplace=True)
    players_ids_df.drop('second_name', axis=1, inplace=True)

    players_stats_df = pd.read_csv(base_path + 'data/' + season + '/cleaned_players.csv') 
    players_stats_df['full_name'] = players_stats_df['first_name'] + ' ' + players_stats_df['second_name']
    players_stats_df.drop('first_name', axis=1, inplace=True)
    players_stats_df.drop('second_name', axis=1, inplace=True)

    players_df = players_ids_df.merge(players_stats_df, on=['full_name'])

    picks_df = top_managers_gw_picks_df(overallLeagueID=overallLeagueID, top_n=top_n, curr_gw=curr_gw)
    
    merged = picks_df.merge(players_df, on=['player_id'])
    merged=merged.sort_values(by=['team_id', 'gw', 'position'])
    return merged


def top_managers_gw_picks_df(overallLeagueID: int, top_n: int, curr_gw: int):
    count = 0
    picks = []
    for manager in get_top_managers_from_api(overallLeagueID):
        if count >= top_n:
            break
        count +=1
        teamID = manager['entry']
        cols =  ['team_id','gw','player_id','position','multiplier']
        parsed = get_gw_picks_from_api(teamID=teamID, gw=curr_gw)
        for i in range(len(parsed['picks'])):
            try:
                currPicks = {
                    'team_id':teamID,
                    'gw':curr_gw, 
                    'player_id':parsed['picks'][i]['element'], 
                    'position':parsed['picks'][i]['position'],
                    'multiplier':parsed['picks'][i]['multiplier']
                    }
                picks.append(currPicks)
            except:
                continue
    
    return pd.DataFrame(picks, columns = cols)


def top_managers_gw_infos_df(overallLeagueID: int, top_n: int, curr_gw: int):
    count = 0
    infos = []
    for manager in get_top_managers_from_api(overallLeagueID):
        if count >= top_n:
            break
        count +=1
        teamID = manager['entry']
        cols = ['team_id','gw','points','bench','gw_rank','transfers','hits','total_points','overall_rank','team_value','chip']
        for gw in range(1,curr_gw):
            parsed = get_gw_picks_from_api(teamID=teamID, gw=gw)
            try:
                currInfo = {
                    'team_id':teamID,
                    'gw':gw, 
                    'points':parsed['entry_history']['points'], 
                    'bench':parsed['entry_history']['points_on_bench'],
                    'gw_rank':parsed['entry_history']['rank'], 
                    'transfers':parsed['entry_history']['event_transfers'],
                    'hits':parsed['entry_history']['event_transfers_cost'], 
                    'total_points':parsed['entry_history']['total_points'],
                    'overall_rank':parsed['entry_history']['overall_rank'], 
                    'team_value':int(parsed['entry_history']['value'])/10, 
                    'chip':parsed['active_chip']
                    }
                infos.append(currInfo)
            except:
                continue
    
    return pd.DataFrame(infos, columns = cols)


def top_managers_df(overallLeagueID: int, top_n: int):
    ids = []
    managers = []
    cols  = ['rank','entry','player_name','entry_name','total']
    count = 0
    for manager in get_top_managers_from_api(overallLeagueID):
        if count >= top_n:
            break
        count +=1
        currManager = {
            'rank': manager['rank'],
            'entry': manager['entry'],
            'player_name': manager['player_name'],
            'entry_name': manager['entry_name'],
            'total': manager['total']}
        managers.append(currManager)
        ids.append(manager['entry'])

    return pd.DataFrame(managers, index=ids, columns = cols)

def get_top_managers_from_api(overallLeagueID: int):
    url = "https://fantasy.premierleague.com/api/leagues-classic/"+str(overallLeagueID)+"/standings/"
    response = requests.get(url)
    data = response.text
    parsed = json.loads(data)
    return parsed['standings']['results']


def get_gw_picks_from_api(teamID: int, gw: int):
    url = "https://fantasy.premierleague.com/api/entry/"+str(teamID)+"/event/"+str(gw)+"/picks/"
    response = requests.get(url)
    data = response.text
    return json.loads(data)


def plot_df(df):
    goalkeepers = df[(df['element_type']=='GK')]
    defenders = df[(df['element_type']=='DEF')]
    midfielders = df[(df['element_type']=='MID')]
    forwards = df[(df['element_type']=='FWD')]

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
                text='Picked by',
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
                text='Total points',
                font=dict(
                    size=18,
                    color='white'
                )
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    return fig


def get_trace(df, position):
    return go.Scatter(
        x = df['picked_by_percent'],        
        y = df['total_points'],
        name= (position+'s'),
        text = df['full_name'] + ' (£' + (df['now_cost']/10).map(str) + ')',
        mode = 'markers',        
        marker=dict(color = map_position_to_color(position),
                    size = 1/df['now_cost'], 
                    sizeref = 0.00003, 
                    sizemode = 'area'),
        hoverlabel= dict(
            font=dict(color='#404040'),
            bordercolor='#404040',
            bgcolor='white'
        ),
        hovertemplate = "<b>%{text}</b><br><br>" +
            "Total points: %{y:f}</br>"+
            "Picked by: %{x:.2f}%</br>"+
            "<extra></extra>")
            
    
def map_position_to_color(position):
    if position == 'Goalkeeper':
        return 'rgba(0,53,166, 0.8)'
    elif position == 'Defender':
        return 'rgba(101,255,71, 0.8)'
    elif position == 'Midfielder':
        return 'rgba(254,213,0, 0.8)'
    else:
        return 'rgba(236,0,0, 0.8)'


def main():
    print('Fetching curr gameweek...')
    URL = "https://fantasy.premierleague.com/api/bootstrap-static/"
    DATA = requests.get(URL).json()
    CURR_GW_OBJS = [x for x in DATA['events'] if x['is_current'] == True]
    if len(CURR_GW_OBJS) == 0:
        CURR_GW_OBJS = DATA['events']        
    CURR_GW = CURR_GW_OBJS[-1]['id']
    
    # Overall FPL league ID is 314
    OVERALL_LEAGUE_ID = 314
    TOP_N = 10
    BASE_PATH = './scraper/'
    SEASON = '2022-23'

    print('Fetching top picks...')
    df = get_top_picks_df(base_path=BASE_PATH, season=SEASON, overallLeagueID=OVERALL_LEAGUE_ID, top_n=TOP_N, curr_gw=CURR_GW)
    df['picked_by'] = df['player_id'].apply(lambda x: (df['player_id'] == x).sum())
    df = df[['element_type','player_id','full_name','picked_by','total_points','now_cost','multiplier']]
    df = df.drop_duplicates(subset='player_id', keep="last")
    df['picked_by_percent'] = df['picked_by']*100/TOP_N
    df = df[df.picked_by_percent >= 5]
    df.sort_values(by="picked_by_percent", ascending=False, inplace=False)
    print(df)

    print('Generating plot...')
    fig = plot_df(df)
    chart_studio.plotly.plot(fig,filename="top-picked")


if __name__ == '__main__':
    main()