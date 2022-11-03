import glob
import os
import pandas
import sys

def calc_goals_conceded_per_game(row):
    val = 0
    if row['minutes'] > 0:
        val = row['goals_conceded'] / (row['minutes'] / 90)
    return val


def calc_saves_per_game(row):
    val = 0
    if row['minutes'] > 0:
        val = row['saves'] / (row['minutes'] / 90)
    return val


def calc_in_game_stats(row):
    if row['position'] == 'Goalkeeper':
        val = row['clean_sheets']*4 + row['saves_per_game']/3 - row['goals_conceded_per_game']/2 + row['penalties_saved']*2
    elif row['position'] == 'Defender':
        val = row['clean_sheets']*4 - row['own_goals'] - row['goals_conceded_per_game']/2
    elif row['position'] == 'Midfielder':
        val = row['goals_scored']*5 + row['assists']*3 - row['penalties_missed']
    elif row['position'] == 'Forward':
        val = row['goals_scored']*4 + row['assists']*3 - row['penalties_missed']
    return val


def calc_basic_stats(row):
    if row['minutes'] == 0:
        val = 0
    else:
        val = (row['total_points'] + row['bonus']) / (row['minutes'] / 90) + row['points_per_game'] + row['dreamteam_count']
    return round(val, 2)


def calc_popularity(row):
    val = (row['transfers_balance'] + row['transfers_balance_event'] + row['selected_by_percent'] * 50000)
    return round(val, 2)


def calc_relative_difficulty(row):
    diff = row['difficulty']-row['difficulty_other']
    diff = diff + 1 if diff >= 0 else 1/((0-diff)+1)
    return diff


def map_position(row):
    if row['element_type'] == 1:
        val = 'Goalkeeper'
    elif row['element_type'] == 2:
        val = 'Defender'
    elif row['element_type'] == 3:
        val = 'Midfielder'
    else:
        val = 'Forward'
    return val


def map_status(row):
    if row['status'] == 'a':
        val = 'Avaliable'
    elif row['status'] == 'd':
        val = 'Questionable'
    elif row['status'] == 'i':
        val = 'Injured'
    elif row['status'] == 's':
        val = 'Suspended'
    else:
        val = 'Unknown'
    return val


def map_team(row):
    if row['team_code'] == 1:
        val = 'Man Utd'
    elif row['team_code'] == 3:
        val = 'Arsenal'
    elif row['team_code'] == 4:
        val = 'Newcastle'
    elif row['team_code'] == 6:
        val = 'Spurs'
    elif row['team_code'] == 7:
        val = 'Aston Villa'
    elif row['team_code'] == 8:
        val = 'Chelsea'
    elif row['team_code'] == 11:
        val = 'Everton'
    elif row['team_code'] == 13:
        val = 'Leicester'
    elif row['team_code'] == 14:
        val = 'Liverpool'
    elif row['team_code'] == 20:
        val = 'Southampton'
    elif row['team_code'] == 21:
        val = 'West Ham'
    elif row['team_code'] == 31:
        val = 'Crystal Palace'
    elif row['team_code'] == 36:
        val = 'Brighton'
    elif row['team_code'] == 38:
        val = 'Huddersfield'
    elif row['team_code'] == 39:
        val = 'Wolves'
    elif row['team_code'] == 43:
        val = 'Man City'
    elif row['team_code'] == 45:
        val = 'Norwich'
    elif row['team_code'] == 49:
        val = 'Sheffield Utd'
    elif row['team_code'] == 54:
        val = 'Fulham'
    elif row['team_code'] == 57:
        val = 'Watford'
    elif row['team_code'] == 91:
        val = 'Bournemouth'
    elif row['team_code'] == 90:
        val = 'Burnley'
    elif row['team_code'] == 97:
        val = 'Cardiff'
    else:
        val = 'Unknown'
    return val


def map_team_19_20(row):
    teams = ['Arsenal', 'Aston Villa', 'Bournemouth', 'Brighton', 'Burnley', 'Chelsea', 'Crystal Palace', 
             'Everton', 'Leicester', 'Liverpool', 'Man City', 'Man Utd', 'Newcastle', 'Norwich', 
             'Sheffield Utd', 'Southampton', 'Spurs', 'Watford', 'West Ham', 'Wolves']
    idx = row['team_id']-1
    return teams[idx]


def map_code_to_str(row):
    return str(row['code'])


def map_id_to_str(row):
    return str(row['id'])

    
def get_fixtures_data(base_path, season):
    fix_path = base_path + "data/" + season + "/fixtures.csv"
    df = pandas.read_csv(open(fix_path, 'r'))
    df['team_id']=df['team_a']
    df["team_a"] = df.apply(map_team_19_20, axis=1)
    df['team_id']=df['team_h']
    df["team_h"] = df.apply(map_team_19_20, axis=1)
    return df[['code','event','started','finished','kickoff_time',
               'team_h','team_h_score','team_h_difficulty',
               'team_a','team_a_score','team_a_difficulty']]


def get_team_fixtures_data(team, base_path, season):
    fix = get_fixtures_data(base_path, season)
    fix = fix[(fix['team_h']==team) | (fix['team_a']==team)]
    fix['is_home'] = fix['team_h']==team
    fix['where'] = fix.apply(lambda row: 'H' if row.is_home else 'A', axis=1)
    
    opponents = []
    difficulty = []
    difficulty_other = []
    scored = []
    concieved = []
    for x in range(0, len(fix)):
        curr=fix.iloc[x]
        opponents.append(curr['team_a'] if curr['is_home'] == True else curr['team_h'])
        concieved.append(curr['team_a_score'] if curr['is_home'] == True else curr['team_h_score'])
        scored.append(curr['team_h_score'] if curr['is_home'] == True else curr['team_a_score'])
        difficulty.append(curr['team_h_difficulty'] if curr['is_home'] == True else curr['team_a_difficulty'])
        difficulty_other.append(curr['team_a_difficulty'] if curr['is_home'] == True else curr['team_h_difficulty'])
        
    fix['opponent'] = opponents
    fix['difficulty'] = difficulty
    fix['difficulty_other'] = difficulty_other
    fix['relative_difficulty']=fix.apply(calc_relative_difficulty, axis=1)
    fix['scored'] = scored
    fix['concieved'] = concieved
    return fix[['code','event','started','finished','kickoff_time','is_home','where',
                'opponent','difficulty','difficulty_other','relative_difficulty',
                'scored','concieved']]
    
    
def get_upcoming_fixtures_data(base_path, season):
    df = get_fixtures_data(base_path, season)
    df = df[df['started']==False]
    return df[['code','event','kickoff_time','team_h','team_h_difficulty','team_a','team_a_difficulty']]


def get_upcoming_fixtures_by_team(base_path, season,no_fixtures=6):
    clubs = get_upcoming_fixtures_data(base_path, season)['team_a'].unique()
    alldf=pandas.DataFrame()

    for club in clubs:
        df = get_upcoming_team_fixtures_data(club, base_path, season).head(no_fixtures)
        df['team']=club

        alldf = alldf.append(df)
    return alldf


def get_upcoming_team_fixtures_data(team, base_path, season):
    df = get_team_fixtures_data(team, base_path, season)
    df = df[df['started']==False]
    return df[['code','event','kickoff_time','is_home','where','opponent','difficulty','difficulty_other','relative_difficulty']]


def get_past_fixtures_data(base_path, season):
    df = get_fixtures_data(base_path, season)
    df = df[df['finished']==True]
    return df[['code','event','kickoff_time',
               'team_h','team_h_difficulty','team_h_score',
               'team_a','team_a_score','team_a_difficulty']]


def get_past_team_fixtures_data(team, base_path, season):
    df = get_team_fixtures_data(team, base_path, season)
    df = df[df['finished']==True]
    return df[['code','event','kickoff_time','opponent','is_home','where',
               'difficulty','difficulty_other','relative_difficulty','scored','concieved']]
        
               
def get_player_data(base_path, player, season, range_start=1, range_end=-1):
    pl_path = base_path + "data/" + season + "/players/" + player + "/gw.csv"
    df = pandas.read_csv(open(pl_path, 'r'))
    x = [x * 1 for x in range(1, len(df) + 1)]
    df['gw'] = x
    if range_end == -1:
        range_end = len(df['gw'])

    df = df[range_start - 1:range_end]
    return df


def get_cumulative_data(base_path, season):
    # all data csv path
    all_path = base_path + "data/" + season + "/players_raw.csv"

    # Get all players
    alldf = pandas.read_csv(all_path)
    alldf["code2"] = alldf.apply(map_code_to_str, axis=1)
    alldf["id2"] = alldf.apply(map_id_to_str, axis=1)
    alldf["lower_name"] = alldf["first_name"].str.lower() + " " + alldf["second_name"].str.lower()
    alldf["full_name"] = alldf["first_name"] + " " + alldf["second_name"]
    alldf["full_name_underscore"] = alldf["first_name"] + "_" + alldf["second_name"]
    alldf["full_name_code"] = alldf["first_name"] + " " + alldf["second_name"] + "_" + alldf["code2"]
    alldf["full_name_id"] = alldf["first_name"] + "_" + alldf["second_name"] + "_" + alldf["id2"]
    alldf["price"] = alldf["now_cost"] / 10
    alldf["position"] = alldf.apply(map_position, axis=1)
    alldf["avail_status"] = alldf.apply(map_status, axis=1)
    alldf["team_name"] = alldf.apply(map_team, axis=1)
    alldf['basic_stats'] = alldf.apply(calc_basic_stats, axis=1)
    alldf['quality'] = alldf['ict_index'] + alldf['form']

    alldf['goals_conceded_per_game'] = alldf.apply(calc_goals_conceded_per_game, axis=1)
    alldf['saves_per_game'] = alldf.apply(calc_saves_per_game, axis=1)
    alldf['in_game_stats'] = alldf.apply(calc_in_game_stats, axis=1)

    alldf['transfers_balance'] = alldf['transfers_in'] - alldf['transfers_out']
    alldf['transfers_balance_event'] = alldf['transfers_in_event'] - alldf['transfers_out_event']
    alldf['popularity'] = alldf.apply(calc_popularity, axis=1)

    return alldf

    
def get_gameweek_data(base_path, season, curr_gw):
    df1 = pandas.DataFrame()
    for f in glob.glob(base_path + 'data/'+season+'/gws/gw*'):
        gw = int(f[-5:-4])
        df_tmp = pandas.read_csv(f, encoding='latin_1')
        df_tmp['name'] = df_tmp['name'].str.replace('_', ' ')
        df_tmp['gw'] = gw
        df_tmp['bonus_weighted'] = df_tmp['bonus']/(curr_gw + 1 - gw)
        df_tmp['bps_weighted'] = df_tmp['bps']/(curr_gw + 1 - gw)
        df_tmp['total_points_weighted'] = df_tmp['total_points']/(curr_gw + 1 - gw)
        df_tmp['gw'] = df_tmp['gw']/(curr_gw + 1 - gw)
        df1 = df1.append(df_tmp)
    return df1


def get_raw_data(base_path, season):
    df1 = pandas.read_csv(base_path + 'data/' + season + '/players_raw.csv', encoding='utf8')
    df1['name'] = df1['first_name'] + ' ' + df1['second_name']
    df1["position"] = df1.apply(map_position, axis=1)
    df1 = df1.sort_values(['name'], ascending=True)
    return df1

if os.name == 'nt':
    sys._enablelegacywindowsfsencoding()