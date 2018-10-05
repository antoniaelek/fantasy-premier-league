FROM continuumio/miniconda3

MAINTAINER Antonia Elek <antoniaelek at hotmail.com>


RUN conda install -y nomkl bokeh flask pandas

VOLUME '/app'

EXPOSE 5000

ENTRYPOINT ["python","/app/web/app.py"]
