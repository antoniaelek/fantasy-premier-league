from functions import get_raw_data
from functions import get_gameweek_data
from functions import map_id_to_str

import os
import requests
import pandas

from vpc import calc_vpc
from vpc import plot_vpc

from teams import next_fixtures
from teams import next_fixtures_plot

from teams import form
from teams import form_plot

from performance import get_performance_data
from performance import gk_plot
from performance import def_plot
from performance import mid_plot
from performance import fwd_plot

import plotly.graph_objs as go

import chart_studio
import chart_studio.plotly as py


def main():
    print('Fetching curr gameweek...')
    URL = "https://fantasy.premierleague.com/api/bootstrap-static/"
    DATA = requests.get(URL).json()
    CURR_GW_OBJS = [x for x in DATA['events'] if x['is_current'] == True]
    if len(CURR_GW_OBJS) == 0:
        CURR_GW_OBJS = DATA['events']        
    CURR_GW = CURR_GW_OBJS[-1]['id']
    SEASON = '2022-23'
    BASE_PATH = './scraper/'
    CHARTS_USER = config('CHARTS_USER')
    CHARTS_API_KEY = config('CHARTS_API_KEY')
    chart_studio.tools.set_credentials_file(username=CHARTS_USER, api_key=CHARTS_API_KEY)
    
    print('Getting performance data...')
    df=get_performance_data(SEASON, BASE_PATH)

    print('Generating goalkeepers performance plots...')
    gk_plot(df[df.position == 'Goalkeeper'])
    
    print('Generating defenders performance plots...')
    def_plot(df[df.position == 'Defender'])
    
    print('Generating midfielders performance plots...')
    mid_plot(df[df.position == 'Midfielder'])
    
    print('Generating forwards performance plots...')
    fwd_plot(df[df.position == 'Forward'])
    
    print('Generating VPC plot...')
    vpc = calc_vpc(BASE_PATH, SEASON, CURR_GW)
    fig = plot_vpc(vpc)
    chart_studio.plotly.plot(fig, filename="vpc", auto_open=False)
    
    print('Generating teams fixtures plot...')
    fix = next_fixtures(SEASON, BASE_PATH, no_fixtures=4)
    next_fixtures_plot(SEASON, BASE_PATH, fix,limit_diff=10)
    
    print('Generating teams form plot...')
    df_form = form(SEASON, BASE_PATH, no_fixtures=4)
    form_plot(SEASON, BASE_PATH, df_form, limit_form=1.5)
    

if __name__ == '__main__':
    main()
    