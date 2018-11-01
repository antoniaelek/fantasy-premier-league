# -*- coding: utf-8 -*-
from pathlib import Path
from bokeh.models import CategoricalColorMapper
from bokeh.io import output_file, save
from bokeh.plotting import figure
from bokeh.layouts import gridplot, row
from bokeh.models import ColumnDataSource
from bokeh.palettes import d3
import functions
import os


def compare_players(season, curr_gw):
    # Get data
    base_path = str(Path(os.path.dirname(os.path.abspath(__file__))).parent) + "/"

    df = functions.get_cumulative_data(base_path=base_path + "scraper/", season=season)
    df = df.fillna(0)

    #player_stats(df, base_path)
    player_plots(df, base_path, curr_gw)


def player_stats(df, base_path):
    players = df["full_name_id"].values.tolist()
    players3 = df["full_name_code"].values.tolist()
    players4 = df["full_name_id"].values.tolist()

    df = df.set_index(['full_name_id'])

    for i in range(0, len(players)):
        player3 = players3[i]
        player4 = players4[i]

        val = (df[df.index.str.startswith(player4)])

        md_file = base_path + 'web/static/assets/bokeh/player_stats/' + player3 + '_text.html'

        dirname = os.path.dirname(md_file)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        print("Generating " + md_file + "...")
        with open(md_file, 'w', encoding='utf8') as f:
            f.write('<head><style>' +
                    'body, table, td { font-family: "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif; color: #444; line-height: 0.8; font-size: 12px; } ' +
                    'h1, h2, h3, h4, h5, h6 { margin: 10px 0 5px 0 !important; font-family: Helvetica, Arial, sans-serif; color: #34465d; font-weight: bold; line-height: 0.8; } ' +
                    'h1{font-size:20px} h2{font-size:18px} h3{font-size:16px} h4{font-size:14px} h5{font-size:12px} h6{font-size:12px} ' +
                    'td{ padding: 2px 5px 2px 5px; }</style></head>')
            f.write('<body><h1>' + val['full_name'][0] + '</h1>')
            f.write('<table><tr><td colspan=2><h3>' + str(val['position'][0]) + ', ' + str(
                val['price'][0]) + ' £</h3></td><td></td></tr>')
            f.write('<tr><td><b>Team: </b>' + str(val['team_name'][0]) + '</td>' +
                    '<td><b>Status:</b> ' + str(val['avail_status'][0]) + '</td></tr>')

            f.write('<tr><td colspan=2><h3>Basic Stats</h3></td><td id="basic_stats" style="display:none;">' + str(
                val['basic_stats'][0]) + '</td><td></td></tr>')
            f.write('<tr><td><b>Minutes played:</b> ' + str(val['minutes'][0]) + '</td>' +
                    '<td><b>Total Points:</b> ' + str(val['total_points'][0]) + '</td></tr>' +
                    '<tr><td><b>Bonus Points:</b> ' + str(val['bonus'][0]) + '</td>' +
                    '<td><b>BPS:</b> ' + str(val['bps'][0]) + '</td></tr>' +
                    '<tr><td><b>Points Per Game:</b> ' + str(val['points_per_game'][0]) + '</td>' +
                    '<td><b>Times in Dream Team:</b> ' + str(val['dreamteam_count'][0]) + '</td></tr>')

            f.write('<tr><td colspan=2><h3>Quality indexes:</h3></td><td id="quality" style="display:none;">' + str(
                val['quality'][0]) + '</td><td></td></tr>')
            f.write('<tr><td><b>ICT index:</b> ' + str(val['ict_index'][0]) + '</td>' +
                    '<td><b>Form:</b> ' + str(val['form'][0]) + '</td></tr>' +
                    '<tr><td><b>Influence:</b> ' + str(val['influence'][0]) + '</td>' +
                    '<td><b>Threat:</b> ' + str(val['threat'][0]) + '</td></tr>' +
                    '<tr><td><b>Creativity:</b> ' + str(val['creativity'][0]) + '</td>' +
                    '<td></td></tr>')

            f.write('<tr><td colspan=2><h3>In-Game Stats</h3></td><td id="in_game_stats" style="display:none;">' + str(
                val['in_game_stats'][0]) + '</td><td></td></tr>')
            f.write('<tr><td><b>Goals Scored:</b> ' + str(val['goals_scored'][0]) + '</td>' +
                    '<td><b>Assists:</b> ' + str(val['assists'][0]) + '</td></tr>' +
                    '<tr><td><b>Goals Conceded:</b> ' + str(val['goals_conceded'][0]) + '</td>' +
                    '<td><b>Clean Sheets:</b> ' + str(val['clean_sheets'][0]) + '</td></tr>' +
                    '<tr><td><b>Saves:</b> ' + str(val['saves'][0]) + '</td>' +
                    '<td><b>Own Goals:</b> ' + str(val['own_goals'][0]) + '</td></tr>' +
                    '<tr><td><b>Penalties Missed:</b> ' + str(val['penalties_missed'][0]) + '</td>' +
                    '<td><b>Penalties Saved:</b> ' + str(val['penalties_saved'][0]) + '</td></tr>' +
                    '<tr><td><b>Yellow Cards:</b> ' + str(val['yellow_cards'][0]) + '</td>' +
                    '<td><b>Red Cards:</b> ' + str(val['red_cards'][0]) + '</td></tr>')

            f.write('<tr><td colspan=2><h3>Popularity</td><td id="popularity" style="display:none;">' + str(
                val['popularity'][0]) + '</td><td></td></tr>')
            f.write('<tr><td><b>Transfers Balance:</b> ' + str(val['transfers_balance'][0]) + '</td>' +
                    '<td><b>GW Transfers Balance:</b> ' + str(val['transfers_balance_event'][0]) + '</td></tr>' +
                    '<tr><td><b>Selected by managers:</b> ' + str(val['selected_by_percent'][0]) + '% </td>' +
                    '<td></td></tr></table></body>')


def player_plots(df, base_path, gw_cnt):
    players = df["full_name_id"].values.tolist()
    players3 = df["full_name_code"].values.tolist()
    players4 = df["full_name_id"].values.tolist()
    tools = "hover"
    tooltips = """<table style="padding: 5px; color: #888;">
            <tr style="line-height: 0.8; font-size: 17px; font-weight: bold; padding:10; margin: 0">
                <td colspan=3" style="padding:5px;">@name</td>
            </tr>
            <tr style="line-height: 0.8; font-size: 12px; padding:5px !important; margin: 5px;">
                <td style="font-weight: bold; padding:5px;">Gameweek</td>
                <td style="padding:5px;">@x</td>
            </tr>
            <tr style="line-height: 0.8; font-size: 12px; padding:5px !important; margin: 5px;">
                <td style="font-weight: bold; padding:5px;">Price</td>
                <td style="padding:5px;">@y_value £</td>
            </tr>
            <tr style="line-height: 0.8; font-size: 12px; padding:5px !important; margin: 5px;">
                <td style="font-weight: bold; padding:5px;">Points</td>
                <td style="padding:5px;">@y_pts</td>
            </tr>
            <tr style="line-height: 0.8; font-size: 12px; padding:5px !important; margin: 5px;">
                <td style="font-weight: bold; padding:5px;">Minutes</td>
                <td style="padding:5px;">@y_mins</td>
            </tr>
            <tr style="line-height: 0.8; font-size: 12px; padding:5px !important; margin: 5px;">
                <td style="font-weight: bold; padding:5px;">ICT</td>
                <td style="padding:5px;">@y_ict</td>
            </tr>
        </table>
        """

    for i in range(0, len(players)):
        player3 = players3[i]
        player4 = players4[i]

        # get plots data
        val = functions.get_player_data(base_path=base_path+"scraper/", player=player4)
        source = ColumnDataSource(
            data=dict(name=([player3[:player3.index('_')]] * len(val['gw'])),
                      x=val['gw'],
                      y_value=val['value'] / 10,
                      y_pts=val['total_points'],
                      y_mins=val['minutes'],
                      y_ict=val['ict_index']))

        # plots
        p_price = figure(y_axis_label='£', tools=tools, x_range=(1, gw_cnt))
        p_price.line('x', 'y_value', source=source, line_width=2)
        p_price.hover.tooltips = tooltips

        p_pts = figure(y_axis_label='Points', tools=tools, x_range=(1, gw_cnt))
        p_pts.line('x', 'y_pts', source=source, line_width=2)
        p_pts.hover.tooltips = tooltips

        p_mins = figure(y_axis_label='Minutes', tools=tools, x_range=(1, gw_cnt), y_range=(0, 100))
        p_mins.line('x', 'y_mins', source=source, line_width=2)
        p_mins.hover.tooltips = tooltips

        p_ict = figure(x_axis_label='GW', y_axis_label='ICT', tools=tools, x_range=(1, gw_cnt))
        p_ict.line('x', 'y_ict', source=source, line_width=2)
        p_ict.hover.tooltips = tooltips

        p = gridplot([p_price, p_pts, p_mins, p_ict], ncols=1, plot_width=300, plot_height=120, toolbox=None,
                     toolbar_options={'logo': None})

        fig = row(p)

        md_file = base_path + 'web/static/assets/bokeh/player_stats/' + player3 + '.html'
        print("Generating " + md_file + "...")
        output_file(md_file)
        save(fig)


def display_vpc(df, out_file):
    palette = d3['Category10'][4]
    color_map = CategoricalColorMapper(factors=['Goalkeeper','Defender','Midfielder','Forward'], palette=palette)

    # set data source for visual
    source = ColumnDataSource(data=dict(
        names=df['display_name'],
        position=df['position'],
        points_per_game=df['total_points'],
        vpc_ratio=df['vpc_ratio'],
        now_cost=df['value'],
        circle_size=df['vpc_ratio']/2,
        fill_alpha=df['vpc_ratio']/2))

    tools = "hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"

    p = figure(tools=tools, x_axis_label="cost", y_axis_label="avg points", x_range=(3, 15), y_range=(0, 10))
    p.hover.tooltips = [
        ("Name", "@names"),
        ("Position", "@position"),
        ("Cost", "@now_cost" + ' £'),
        ("Avg points", "@points_per_game"),
        ("Value per cost", "@vpc_ratio")
    ]

    p.scatter(x='now_cost',
              y='points_per_game',
              radius='circle_size',
              fill_alpha='fill_alpha',
              color={'field': 'position', 'transform': color_map},
              source=source,
              toolbar_options={'logo': None})

    fig = row(p)
    # show(fig)
    output_file(out_file)
    save(fig)
