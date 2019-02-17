import sys, os
from pathlib import Path

# Add bokeh folder to path
SCRAPER_BASE_PATH = str(Path(os.path.dirname(os.path.abspath(__file__))).parent) + "/"
sys.path.append(os.path.abspath(os.path.join(SCRAPER_BASE_PATH, 'viz')))

from functions import calc_vpc
from functions import get_detailed_aggregate_data
import compare
import requests

SEASON = os.environ["FPL_SEASON"]
IP = os.environ["FPL_IP"]
BASE_PATH = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)
SCRAPER_BASE_PATH = BASE_PATH + "/scraper/"
BOKEH_BASE_PATH = BASE_PATH + "/viz/"

URL = "https://fantasy.premierleague.com/drf/bootstrap-static"


def main():
    print("Fetching current gameweek...")
    json = requests.get(URL).json()
    curr_gameweek = json['next-event'] - 1
    print("Current gameweek: " + str(curr_gameweek))

    # Generate html files with players data
    print("Generating html stats for players comparison...")
    compare.compare_players(SEASON, curr_gameweek)

    # Save vpc data to csv
    print("Generating value-per-cost data...")
    vpc_data = calc_vpc(SCRAPER_BASE_PATH, SEASON, curr_gameweek)
    vpc_data.to_csv(BOKEH_BASE_PATH + 'data/vpc_data.csv', sep=';', encoding='latin_1', index=False)

    # Save aggregate data to csv
    print("Generating aggregate data...")
    agg_data = get_detailed_aggregate_data(SCRAPER_BASE_PATH, SEASON)
    agg_data.to_csv(BOKEH_BASE_PATH + 'data/aggregate_data.csv', sep=';', encoding='latin_1', index=False)


if __name__ == '__main__':
    main()
