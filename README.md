# Fantasy Premier League Stats, Visualizations &amp; Analysis

Simple python web app with FPL stats, visualizations and anlysis.
Live at [fantasy.elek.hr](http://fantasy.elek.hr/).

## Running locally
### With Docker
  - Set the value of `IP` environment variable in `variables.env` to `127.0.0.1`
  - Run `docker-compose up`
  - Application will be available at [localhost](http://localhost/)
  
### Natively
  - Run `pip install -r requirements.txt` to install requirements
  - Set the `IP` environment variable to `127.0.0.1` (eq. in PowerShell run `$env:FPL_IP="127.0.0.1"`)
  - Set the `FPL_SEASON` environment variable to `2018-19` (eq. in PowerShell run `$env:FPL_SEASON="2018-19"`)
  - Open up a terminal window and run `python .\web\app.py`. Wait until application starts. 
  - In another termianl window, run `bokeh serve .\bokeh\vpc.py --allow-websocket-origin=localhost:5000`
  - Application will be available at [localhost:5000](http://localhost:5000/)

## Features
Currently, there are two avaliable features, *Players Comparison* & *Points Per Cost Analysis*.

### Players Comparison
Players Comparison is exactly what it sounds it is. Take two players and compare them on number of factors: price, gained points, performance index, in-game stats, or popularity among FPL managers. There are also some handy line plots visualizing the trends in player's price, points, playing time and ICT index.

![comparison](https://raw.githubusercontent.com/antoniaelek/antoniaelek.github.io/master/images/fpl-comparison.png)

### Points Per Cost
Points Per Cost scatter plot visualizes relationship between each player's price and their average points gain. Blue circles on the plot are goalkeepers, orange ones are defenders, midfielders are in green and forwards are red circles. Larger circle means you get better value for your money. It is also possible to filter plot by a certain position, for better visibility.

![points-per-cost](https://raw.githubusercontent.com/antoniaelek/antoniaelek.github.io/master/images/fpl-points-per-cost.png)
