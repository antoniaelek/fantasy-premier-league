FROM continuumio/miniconda

MAINTAINER Antonia Elek <antoniaelek at hotmail.com>

RUN conda install -y flask bokeh

## Scripts are in here.
VOLUME ['/app']

EXPOSE 5000

WORKDIR /app

ENTRYPOINT ["python","/app/app.py"]
