FROM continuumio/miniconda3

MAINTAINER Antonia Elek <antoniaelek at hotmail.com>


RUN conda install -y nomkl bokeh flask pandas

VOLUME '/app'

EXPOSE 5000

RUN python /app/web/setup.py

ENTRYPOINT ["python","/app/web/app.py"]
