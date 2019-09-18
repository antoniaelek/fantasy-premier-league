from functions import get_raw_data

import glob
import os
import pandas
import sys
import requests

import plotly.graph_objs as go
import plotly.offline

import chart_studio
import chart_studio.plotly as py


points_metrics = ['goals_scored','assists','own_goals','clean_sheetes','goals_conceded',
                  'penalties_missed','penalties_saved','minutes','yellow_cards']

defensive_metrics = ['clean_sheets','saves','penalties_saved','recoveries','clearances_blocks_interceptions','tackles',
                     'goals_conceded','own_goals','penalties_conceded','errors_leading_to_goal','errors_leading_to_goal_attempt']

creativity_metrics=['assists','big_chances_created','big_chances_missed',
                    'attempted_passes','completed_passes','key_passes','dribbles','open_play_crosses']

attack_metrics=['goals_scored','winning_goals','penalties_missed','target_missed','tackled','offside']

general_metrics=['minutes','red_cards','yellow_cards','fouls',
               'bonus','bps','total_points','ea_index','ict_index','influence','creativity','threat']

other_metrics=['cost','selected','loaned_in','loaned_out','transfers_in','transfers_out','transfers_balance']

points = {'assists':3,
          'own_goals':-2,
          'penalties_missed':-2,
          'minutes':1/45,
          'yellow_cards':-1,
          'red_cards':-3}


def to_pretty_print(input_str):
    return input_str.replace('_', ' ').capitalize()


def from_pretty_print(input_str):
    return input_str.replace(' ', '_').lower()
    

def get_aggregate_functions():
    return ['average', 'median', 'sum', 'count', 'min', 'max']


def get_features_for_aggregation():
    return ['assists', 'bonus', 'bps',
            'clean_sheets', 'cost', 'creativity',
            'goals_conceded', 'goals_scored', 'ict_index', 'influence',
            'minutes', 'own_goals',
            'penalties_missed', 'penalties_saved', 'red_cards', 'saves', 'selected',
            'threat', 'total_points', 'transfers_balance',
            'transfers_in', 'transfers_out', 'yellow_cards']


def get_aggregate_features():
    features = get_features_for_aggregation()
    aggregates = get_aggregate_functions()

    features_out = ['name_id', 'id', 'name']
    for feature in features:
        for aggregate in aggregates:
            features_out.append(aggregate + "_" + feature)

    return features_out


def get_detailed_aggregate_data(base_path, season):
    features_in = get_features_for_aggregation()
    features_out = get_aggregate_features()
    features_out.append('cost')

    df_out = pandas.DataFrame(columns=features_out)
    df_out.set_index('id')

    for file in glob.glob(base_path + 'data/' + season + '/players/*/gw.csv'):
        try:
            df_in = pandas.read_csv(file, encoding='latin_1')
            df_in['value'] = df_in['value']/10
            df_in.rename(columns={'value': 'cost'}, inplace=True)

            element_id = df_in['element'][0]
            name_id = file.replace('/', '\\').split('\\')[-2]
            name = name_id[:int(name_id.rfind("_"))]
            name = name.replace("_", " ")

            features_out_dict = {}
            for feature in features_in:
                features_out_dict["average_" + feature] = df_in[feature].mean()
                features_out_dict["median_" + feature] = df_in[feature].median()
                features_out_dict["sum_" + feature] = df_in[feature].sum()
                features_out_dict["count_" + feature] = df_in[feature].count()
                features_out_dict["min_" + feature] = df_in[feature].min()
                features_out_dict["max_" + feature] = df_in[feature].max()


            features_out_dict['cost'] = df_in['cost']    
            features_out_dict['name_id'] = name_id
            features_out_dict['id'] = element_id
            features_out_dict['name'] = name
            df_out.loc[name_id] = pandas.Series(features_out_dict)
        except:
            print('error reading file: ' + file)
    
    df_out = df_out.fillna(0)
    return df_out


def get_agg_features(features, aggregates):
    agg_features = []
    for feature in features:
        for agg in aggregates:
            agg_features.append(agg + '_' + feature)
    return agg_features


def get_trace(df, x_metrics, y_metrics, color):
    return go.Bar(
        x = df[x_metrics],        
        y = df[y_metrics],
        text = df['name'],        
        #mode = 'markers',        
        marker=dict(color=color),
        hovertemplate = "<b>%{text}</b><br><br>" +
            y_metrics+": %{y:.2f}</br>"+
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


def get_layout(df, x_metrics, y_metrics, title, show_dropdown=True):  
    buttons=[]
    i = 0
    for x in x_metrics.keys():
        for y in y_metrics.keys():
            template = [False] * len(y_metrics)
            template[i] = True
            buttons.append(dict(label = y_metrics[y], method = 'update', args = [{'visible': template}]))        
            i+=1
        
    updatemenus = list([
        dict(active=0,
             bgcolor = 'rgba(255,255,255,100)',
             pad = {'r': 0, 't': 10},
             x = 0,
             y = 1.18,
             xanchor = 'left',
             buttons=buttons)])
    
    if show_dropdown==False:
        updatemenus=None
    
    layout = go.Layout(
        hovermode = 'closest',
        showlegend=False,
        updatemenus=updatemenus, 
        modebar={'bgcolor': 'rgba(0,0,0,0)'},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=go.layout.XAxis(
            color='white',
            title=go.layout.xaxis.Title(
                text='',
                font=dict(
                    size=18
                )
            )
        ),
        yaxis=go.layout.YAxis(
            color='white',
            title=go.layout.yaxis.Title(
                text='',
                font=dict(
                    size=18
                )
            )
        )
    )
    return layout


def get_figure(df, x_metrics, y_metrics, title = '', color='rgba(101,255,71, 0.4)', show_dropdown=True):    
    data = get_data(df, x_metrics, y_metrics, color)
    layout = get_layout(df, x_metrics, y_metrics, title, show_dropdown)
    
    return go.Figure(data=data, layout=layout)


def generate_performance_plots(points_dict, df, position, aggregate="average"):
    if aggregate != "" and aggregate[-1] != "_":
        aggregate += "_"

    df = df.copy(deep=True)

    df['achievements'] = get_achievements(df, points_dict)
    df['errors'] = get_errors(df, points_dict)
    df['value'] = df['achievements'] - df['errors']
    df = df[(df['sum_minutes'] > 0)]# & (df['errors'] > 0) & (df['value'] > 0)]
    
    plot3 = get_figure(df, {'web_name':'Name'}, {'value':'Value'}, 'value', 'white', show_dropdown=True)
#     plotly.offline.iplot(plot3)
    chart_studio.plotly.plot(plot3, filename=(position+"value"))
    
    y1 = {'achievements':'Achievements'}
    for a in filter_achievements(points_dict).keys(): y1[aggregate + a]=to_pretty_print(aggregate + a)
    plot1 = get_figure(df, {'web_name':'Name'}, y1, 'achievements', 'white', show_dropdown=True)
#     plotly.offline.iplot(plot1)
    chart_studio.plotly.plot(plot1, filename=(position+"achievements"))

    y2 = {'errors':'Errors'}
    for e in filter_errors(points_dict).keys(): y2[aggregate + e]=to_pretty_print(aggregate + e)
    plot2 = get_figure(df, {'web_name':'Name'}, y2, 'errors', 'white', show_dropdown=True)
#     plotly.offline.iplot(plot2)
    chart_studio.plotly.plot(plot2, filename=(position+"errors"))

    return df
    
    
def filter_achievements(points_dict):
    return {k:v for (k,v) in points_dict.items() if  v > 0}


def filter_errors(points_dict):
    return {k:v for (k,v) in points_dict.items() if  v < 0}


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
    
def get_performance_data(season, base_path):    
    agg_data = get_detailed_aggregate_data(base_path, season)
    raw_data = get_raw_data(base_path, season)
    raw_data.drop(columns=['name'],inplace=True)
    df = pandas.merge(agg_data, raw_data, on='id', how='outer')
    df['minutes_points'] = df['minutes']/45
    df["web_name_lower"] = df["web_name"].str.lower()
    df.sort_values(by="web_name_lower", inplace=True)
    return df
    

def gk_plot(df):
    game_metrics_gkp = points_metrics + general_metrics + defensive_metrics
    game_metrics_gkp = set(game_metrics_gkp)
    game_metrics_gkp = get_agg_features(game_metrics_gkp, ['sum','average'])

    points_gkp = points.copy()
    points_gkp['goals_scored']=6
    points_gkp['saves']=0.5
    points_gkp['penalties_saved'] = 5
    points_gkp['clean_sheets']=4
    points_gkp['goals_conceded']=-1

    generate_performance_plots(points_gkp, df, 'Goalkeeper')

    
def def_plot(df):
    game_metrics_def = points_metrics + general_metrics + defensive_metrics
    game_metrics_def = set(game_metrics_def)
    game_metrics_def = get_agg_features(game_metrics_def, ['sum','average'])

    points_def = points.copy()
    points_def['goals_scored']=6
    points_def['clean_sheets']=4
    points_def['goals_conceded']=-1

    generate_performance_plots(points_def, df, 'Defender')

    
def mid_plot(df):
    game_metrics_mid = points_metrics + general_metrics + creativity_metrics + attack_metrics
    game_metrics_mid = set(game_metrics_mid)

    game_metrics_mid = get_agg_features(game_metrics_mid, ['sum','average'])

    points_mid = points.copy()
    points_mid['goals_scored']=5
    points_mid['clean_sheets']=1
    points_mid['goals_conceded']=0

    generate_performance_plots(points_mid, df, 'Midfielder')
    
    
def fwd_plot(df):    
    game_metrics_fwd = points_metrics + general_metrics + creativity_metrics + attack_metrics
    game_metrics_fwd = set(game_metrics_fwd)
    game_metrics_fwd = get_agg_features(game_metrics_fwd, ['sum', 'average'])

    points_fwd = points.copy()
    points_fwd['goals_scored'] = 4
    points_fwd['clean_sheets'] = 0
    points_fwd['goals_conceded'] = 0

    generate_performance_plots(points_fwd, df, 'Forward')