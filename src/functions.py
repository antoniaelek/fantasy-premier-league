#=============================================================================#
#                                    Functions                                #
#=============================================================================#

import glob
import pandas


def get_player_data(base_path, player, season="2018-19", range_start=1, range_end=-1):
    pl_path = base_path + "data/" + season + "/players/" + player + "/gw.csv"
    # Get player dataset
    df = pandas.read_csv(open(pl_path, 'r'))
    x = [x * 1 for x in range(1, len(df) + 1)]
    df['gw'] = x
    if range_end == -1:
        range_end = len(df['gw'])

    df = df[range_start - 1:range_end]
    return df


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
    if row['team_code'] == 3:
        val = 'Arsenal'
    elif row['team_code'] == 91:
        val = 'Bournemouth'
    elif row['team_code'] == 36:
        val = 'Brighton'
    elif row['team_code'] == 90:
        val = 'Burnley'
    elif row['team_code'] == 97:
        val = 'Cardiff'
    elif row['team_code'] == 8:
        val = 'Chelsea'
    elif row['team_code'] == 31:
        val = 'Crystal Palace'
    elif row['team_code'] == 11:
        val = 'Everton'
    elif row['team_code'] == 54:
        val = 'Fulham'
    elif row['team_code'] == 38:
        val = 'Huddersfield'
    elif row['team_code'] == 13:
        val = 'Leicester'
    elif row['team_code'] == 14:
        val = 'Liverpool'
    elif row['team_code'] == 43:
        val = 'Man City'
    elif row['team_code'] == 1:
        val = 'Man Utd'
    elif row['team_code'] == 4:
        val = 'Newcastle'
    elif row['team_code'] == 20:
        val = 'Southampton'
    elif row['team_code'] == 6:
        val = 'Spurs'
    elif row['team_code'] == 57:
        val = 'Watford'
    elif row['team_code'] == 21:
        val = 'West Ham'
    elif row['team_code'] == 39:
        val = 'Wolves'
    else:
        val = 'Unknown'
    return val


def map_code_to_str(row):
    return str(row['code'])


def get_cumulative_data(base_path, season="2018-19"):
    # all data csv path
    all_path = base_path + "data/" + season + "/players_raw.csv"

    # Get all players
    alldf = pandas.read_csv(all_path)
    alldf["code2"] = alldf.apply(map_code_to_str, axis=1)
    alldf["lower_name"] = alldf["first_name"].str.lower() + " " + alldf["second_name"].str.lower()
    alldf["full_name"] = alldf["first_name"] + " " + alldf["second_name"]
    alldf["full_name2"] = alldf["first_name"] + "_" + alldf["second_name"]
    alldf["full_name3"] = alldf["first_name"] + " " + alldf["second_name"] + "_" + alldf["code2"]
    alldf["price"] = alldf["now_cost"] / 10
    alldf["position"] = alldf.apply(map_position, axis=1)
    alldf["avail_status"] = alldf.apply(map_status, axis=1)
    alldf["team_name"] = alldf.apply(map_team, axis=1)
    alldf['basic_stats'] = round(
        (alldf['total_points'] + alldf['bonus']) / (alldf['minutes'] / 90) + alldf['points_per_game'] + alldf[
            'dreamteam_count'], 2)
    alldf['quality'] = round(
        (alldf['creativity'] + alldf['ict_index'] + alldf['threat']) * 0.2 + alldf['influence'] * 0.2 + alldf[
            'form'] * 0.6, 2)
    alldf['in_game_stats'] = round((alldf['goals_scored'] - alldf['goals_conceded'] + alldf['assists'] + alldf[
        'clean_sheets'] + alldf['saves'] - alldf['own_goals'] - alldf['penalties_missed'] + alldf['penalties_saved'] -
                                    alldf['yellow_cards'] * 0.2 - alldf['red_cards'] * 0.6) / (alldf['minutes'] / 90),
                                   2)
    alldf['popularity'] = round(((alldf['transfers_in'] - alldf['transfers_out']) + (
            alldf['transfers_in_event'] - alldf['transfers_out_event']) + alldf['selected_by_percent'] * 50000) / 1000,
                                2)

    return alldf


def points_per_appearance(base_path, season):
    # data by gws for each player
    df0 = pandas.DataFrame()
    for f in glob.glob(base_path + 'data/'+season+'/gws/*'):
        dftmp = pandas.read_csv(f, encoding='ansi')
        dftmp['name'] = dftmp['name'].str.replace('_', ' ')
        df0 = df0.append(dftmp)

    # group by player and calculate ratio - df2
    df2 = df0.groupby(['name']).median()
    df2['value'] = df2['value'] / 10
    df2['vpc_ratio'] = df2['total_points'] / df2['value']
    df2 = df2[(df2['total_points'] > 0) & (df2['vpc_ratio'] > 0)]
    df2['name'] = df2.index.values
    df2 = df2.set_index('name')
    df2 = df2.sort_values(['name'], ascending=True)

    # add cleaned data - df1
    df1 = pandas.read_csv(base_path + 'data/'+season+'/players_raw.csv', encoding='utf8')
    df1['name'] = df1['first_name'] + ' ' + df1['second_name']
    df1["position"] = df1.apply(map_position, axis=1)
    df1 = df1.sort_values(['name'], ascending=True)

    # merge
    df = pandas.merge(df1, df2, on='name', how='outer')
    df.to_csv('out.csv', encoding='utf8')

    return df
