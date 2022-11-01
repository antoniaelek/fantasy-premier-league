from urllib import response
import requests , json, csv
import pandas as pd
import os

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

    df = get_top_picks_df(base_path=BASE_PATH, season=SEASON, overallLeagueID=OVERALL_LEAGUE_ID, top_n=TOP_N, curr_gw=CURR_GW)
    print(df)


if __name__ == '__main__':
    main()