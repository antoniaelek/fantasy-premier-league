from functions import get_detailed_aggregate_data
from functions import get_raw_data

from visuals import map_position_to_color

from constants import BASE_PATH
from constants import SEASON
from constants import CURR_GW

import plotly
import plotly.graph_objs as go

import pandas


def filter_achievements(points_dict):
    return {k: v for (k, v) in points_dict.items() if v > 0}


def filter_errors(points_dict):
    return {k: v for (k, v) in points_dict.items() if v < 0}


def get_errors(df, points_dict, aggregate="average"):
    errors = pandas.Series()
    for e in filter_errors(points_dict):
        tmp = (df[aggregate + "_" + e]*(0-points_dict[e]))
        errors = errors.add(tmp, fill_value=0)
    return errors


def get_achievements(df, points_dict, aggregate="average"):
    achievements = pandas.Series()
    for e in filter_achievements(points_dict):
        tmp = (df[aggregate + '_' + e]*(points_dict[e]))
        achievements = achievements.add(tmp, fill_value=0)
    return achievements


def get_agg_features(features, aggregates):
    agg_features = []
    for feature in features:
        for agg in aggregates:
            agg_features.append(agg + '_' + feature)
    return agg_features


def get_trace(df, x_metrics, y_metrics, color):
    return go.Bar(
        x=df[x_metrics],
        y=df[y_metrics],
        text=df['name'],
        # mode = 'markers',
        marker=dict(color=color),
        hovertemplate="<b>%{text}</b><br><br>" +
                      y_metrics + ": %{y:.2f}</br>" +
                      #             x_metrics+": %{x}</br>"+
                      "<extra></extra>")


def get_data(df, x_metrics, y_metrics, color):
    data = []
    for x in x_metrics:
        for y in y_metrics:
            data.append(get_trace(df, x, y, color))

    for el in data[1:]:
        el['visible'] = 'legendonly'

    return data


def get_layout(df, x_metrics, y_metrics, title):
    buttons = []
    i = 0
    for x in x_metrics:
        for y in y_metrics:
            template = [False] * len(y_metrics)
            template[i] = True
            buttons.append(dict(label=y, method='update', args=[{'visible': template}]))
            i += 1

    updatemenus = list([
        dict(active=0,
             pad={'r': 0, 't': 10},
             x=0,
             y=1.18,
             xanchor='left',
             buttons=buttons)])

    layout = go.Layout(
        hovermode='closest',
        showlegend=False,
        updatemenus=updatemenus,
        title=go.layout.Title(
            text=title,
            font=dict(
                size=21
            )
        ),
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text='',
                font=dict(
                    size=18
                )
            )
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text='',
                font=dict(
                    size=18
                )
            )
        )
    )
    return layout


def get_figure(df, x_metric, y_metrics, title='', color='rgba(101,255,71, 0.4)'):
    data = get_data(df, [x_metric], y_metrics, color)
    layout = get_layout(df, [x_metric], y_metrics, title)

    return go.Figure(data=data, layout=layout)


def generate_performance_plots(points_dict, df, position, aggregate="average"):
    if aggregate != "" and aggregate[-1] != "_":
        aggregate += "_"

    df = df.copy(deep=True)

    df['achievements'] = get_achievements(df, points_dict)
    df['errors'] = get_errors(df, points_dict)
    df['value'] = df['achievements'] - df['errors']
    df = df[(df['achievements'] > 0) & (df['errors'] > 0) & (df['value'] > 0)]

    plot3 = get_figure(df, 'web_name', ['value'], 'value', map_position_to_color(position))
    plotly.offline.plot(plot3, filename='out/' + position.lower() + 's_value.html', auto_open=False)

    df = df[(df['achievements'] > 0) & (df['errors'] > 0)]
    df['value'] = df['achievements'] - df['errors']

    y1 = ['achievements']
    for a in filter_achievements(points_dict).keys(): y1.append(aggregate + a)
    plot1 = get_figure(df, 'web_name', y1, 'achievements', map_position_to_color(position))
    plotly.offline.plot(plot1, filename='out/' + position.lower() + 's_achievements.html', auto_open=False)

    y2 = ['errors']
    for e in filter_errors(points_dict).keys(): y2.append(aggregate + e)
    plot2 = get_figure(df, 'web_name', y2, 'errors', map_position_to_color(position))
    plotly.offline.plot(plot2, filename='out/' + position.lower() + 's_errors.html', auto_open=False)


points_metrics = ['goals_scored', 'assists', 'own_goals', 'clean_sheetes', 'goals_conceded',
                  'penalties_missed', 'penalties_saved', 'minutes', 'yellow_cards']

defensive_metrics = ['clean_sheets', 'saves', 'penalties_saved',
                     'recoveries', 'clearances_blocks_interceptions', 'tackles',
                     'goals_conceded', 'own_goals', 'penalties_conceded', 'errors_leading_to_goal',
                     'errors_leading_to_goal_attempt']

creativity_metrics = ['assists', 'big_chances_created', 'big_chances_missed',
                      'attempted_passes', 'completed_passes', 'key_passes', 'dribbles', 'open_play_crosses']

attack_metrics = ['goals_scored', 'winning_goals', 'penalties_missed', 'target_missed', 'tackled', 'offside']

general_metrics = ['minutes', 'red_cards', 'yellow_cards', 'fouls',
                   'bonus', 'bps', 'total_points', 'ea_index', 'ict_index', 'influence', 'creativity', 'threat']

other_metrics = ['cost', 'selected', 'loaned_in', 'loaned_out', 'transfers_in', 'transfers_out', 'transfers_balance']

points = {'assists': 3,
          'own_goals': -2,
          'penalties_missed': -2,
          'minutes': 1 / 45,
          'yellow_cards': -1,
          'red_cards': -3}

aggregate = get_detailed_aggregate_data(BASE_PATH, SEASON)
raw = get_raw_data(BASE_PATH, SEASON)
players = pandas.merge(aggregate, raw, on='name', how='outer')
players['minutes_points'] = players['minutes'] / 45
players.sort_values('web_name', inplace=True)

goalkeepers = players[players.position == 'Goalkeeper']
defenders = players[players.position == 'Defender']
midfielders = players[players.position == 'Midfielder']
forwards = players[players.position == 'Forward']

#################
#               #
#  Goalkeepers  #
#               #
#################
game_metrics_gkp = points_metrics + general_metrics + defensive_metrics
game_metrics_gkp = set(game_metrics_gkp)
game_metrics_gkp = get_agg_features(game_metrics_gkp, ['sum', 'average'])

points_gkp = points.copy()
points_gkp['goals_scored'] = 6
points_gkp['penalties_saved'] = 5
points_gkp['saves'] = 0.5
points_gkp['clean_sheets'] = 4
points_gkp['goals_conceded'] = -1

generate_performance_plots(points_gkp, goalkeepers, 'Goalkeeper')

###############
#             #
#  Defenders  #
#             #
###############
game_metrics_def = points_metrics + general_metrics + defensive_metrics
game_metrics_def = set(game_metrics_def)
game_metrics_def = get_agg_features(game_metrics_def, ['sum', 'average'])

points_def = points.copy()
points_def['goals_scored'] = 6
points_def['clean_sheets'] = 4
points_def['goals_conceded'] = -1

generate_performance_plots(points_def, defenders, 'Defender')

#################
#               #
#  Midfielders  #
#               #
#################
game_metrics_mid = points_metrics + general_metrics + creativity_metrics + attack_metrics
game_metrics_mid = set(game_metrics_mid)
game_metrics_mid = get_agg_features(game_metrics_mid, ['sum', 'average'])

points_mid = points.copy()
points_mid['goals_scored'] = 5
points_mid['clean_sheets'] = 1
points_mid['goals_conceded'] = 0

generate_performance_plots(points_mid, midfielders, 'Midfielder')

##############
#            #
#  Forwards  #
#            #
##############
game_metrics_fwd = points_metrics + general_metrics + creativity_metrics + attack_metrics
game_metrics_fwd = set(game_metrics_fwd)
game_metrics_fwd = get_agg_features(game_metrics_fwd, ['sum', 'average'])

points_fwd = points.copy()
points_fwd['goals_scored'] = 4
points_fwd['clean_sheets'] = 0
points_fwd['goals_conceded'] = 0

generate_performance_plots(points_fwd, forwards, 'Forward')
