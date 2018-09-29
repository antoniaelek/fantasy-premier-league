FROM httpd:2.4

MAINTAINER Antonia Elek <antoniaelek at hotmail.com>

COPY ./httpd/vhost.conf /usr/local/apache2/conf/httpd.conf

VOLUME ['/static']

EXPOSE 80
