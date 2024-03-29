# Fantasy Premier League Stats, Visualizations &amp; Analysis

## Features
  - Top Managers' Picks Analysis
  - Value vs Cost Analysis
  - Player Position Analysis
    - Goalkeepers ranked by achievements and errors
    - Defenders ranked by achievements and errors
    - Midfielders ranked by achievements and errors
    - Forwards ranked by achievements and errors

## Getting started

Clone the repository and submodules

```
git clone --recurse-submodules https://github.com/antoniaelek/fantasy-premier-league.git
```

Setup python environment

```
cd ./fantasy-premier-league
mkdir env
py -m venv ./env
./env/Scripts/activate
pip install -r requirements.txt
```

Create .env file in repository root with the following contents (replace [CHANGEME] placeholder with your own values)
```
CHARTS_API_KEY=[CHANGEME]
CHARTS_USER=[CHANGEME]
```

## Updating submodules

```
git submodule foreach git checkout master
git submodule foreach git pull origin master
```

## Acknowledgements
- Data by [vaastav](https://github.com/vaastav/Fantasy-Premier-League/)
- Images by [footyrenders](https://footyrenders.com) & [premierleague](https://premierleague.com)
- Theme by [beautiful-jekyll](https://deanattali.com/beautiful-jekyll/)
