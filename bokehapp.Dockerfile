FROM continuumio/miniconda3

MAINTAINER Antonia Elek <antoniaelek at hotmail.com>

RUN conda install -y nomkl bokeh numpy pandas

VOLUME '/app'

EXPOSE 5006

ENTRYPOINT ["bokeh","serve","/app/bokeh/vpc.py /app/bokeh/aggregate.py","--allow-websocket-origin=127.0.0.1","--allow-websocket-origin=localhost","--allow-websocket-origin=fantasy.elek.hr","--allow-websocket-origin=fantasy.aelek.me","--allow-websocket-origin=178.128.40.220:80","--address=0.0.0.0"]
