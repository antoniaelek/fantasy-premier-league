FROM continuumio/miniconda3

MAINTAINER Antonia Elek <antoniaelek at hotmail.com>

RUN conda install -y nomkl bokeh numpy pandas

VOLUME '/app'

EXPOSE 5006

ENTRYPOINT ["bokeh","serve","/app/bokeh/vpc.py","--allow-websocket-origin=*","--address=0.0.0.0"]
