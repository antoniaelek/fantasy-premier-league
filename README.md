# Fantasy Premier League Stats, Visualizations &amp; Analysis

Simple python web app with FPL stats, visualizations and anlysis.
Live at [fantasy.aelek.me](http://fantasy.aelek.me/).

## Running locally
- Natively
  - Open up a terminal and run `bokeh serve .\bokeh\vpc.py --allow-websocket-origin=localhost`
  - In another termianl window, run `python .\web\app.py`

- With Docker
  - Run `docker-compose up`.

Application will be available at [127.0.0.1](http://127.0.0.1/)

## Features
Currently, there are two avaliable features, *Players Comparison* & *Points Per Cost Analysis*.

### Players Comparison
Players Comparison is exactly what it sounds it is. Take two players and compare them on number of factors: price, gained points, performance index, in-game stats, or popularity among FPL managers. There are also some handy line plots visualizing the trends in player's price, points, playing time and ICT index.

![comparison](https://raw.githubusercontent.com/antoniaelek/antoniaelek.github.io/master/images/fpl-comparison.png)

### Points Per Cost
Points Per Cost scatter plot visualizes relationship between each player's price and their average points gain. Blue circles on the plot are goalkeepers, orange ones are defenders, midfielders are in green and forwards are red circles. Larger circle means you get better value for your money. It is also possible to filter plot by a certain position, for better visibility.

![points-per-cost](https://raw.githubusercontent.com/antoniaelek/antoniaelek.github.io/master/images/fpl-points-per-cost.png)

All still rather basic right now, however I will be pushing more contents with new features as I go along.
