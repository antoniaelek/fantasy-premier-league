import importlib

import functions
import plots

importlib.reload(functions)
importlib.reload(plots)


def main():
    base_path = "C:/Users/aelek/source/antoniaelek/fantasy-premier-league/"
    season = "2018-19"
    gw_cnt = 6

    df = functions.get_cumulative_data(base_path=base_path, season=season)
    df = df.fillna(0)

    ppa = functions.calc_vpc(base_path, season, gw_cnt)
    ppa_gkp = ppa[ppa.position == 'Goalkeeper']
    ppa_def = ppa[ppa.position == 'Defender']
    ppa_mid = ppa[ppa.position == 'Midfielder']
    ppa_fwd = ppa[ppa.position == 'Forward']

    # VPC
    plots.display_vpc(ppa, base_path + '/docs/assets/bokeh/value_per_cost.html')
    plots.display_vpc(ppa_gkp, base_path + '/docs/assets/bokeh/value_per_cost_gkp.html')
    plots.display_vpc(ppa_def, base_path + '/docs/assets/bokeh/value_per_cost_def.html')
    plots.display_vpc(ppa_mid, base_path + '/docs/assets/bokeh/value_per_cost_mid.html')
    plots.display_vpc(ppa_fwd, base_path + '/docs/assets/bokeh/value_per_cost_fwd.html')

    # Stats
    plots.player_stats(df, base_path)
    plots.player_plots(df, base_path, gw_cnt)


if __name__ == "__main__":
    main()