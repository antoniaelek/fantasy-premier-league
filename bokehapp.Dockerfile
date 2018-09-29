FROM continuumio/miniconda

MAINTAINER Antonia Elek <antoniaelek at hotmail.com>


RUN conda install -y bokeh numpy pandas

## Scripts are in here.
VOLUME ['/app']

EXPOSE 5006

ENTRYPOINT ["bokeh","serve","/app/vpc.py","--allow-websocket-origin=*","--address=0.0.0.0"]
