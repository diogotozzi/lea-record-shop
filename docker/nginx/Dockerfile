FROM nginx:1.23.2-alpine

RUN rm -Rf /etc/nginx/config.d/*

COPY templates/default.conf /etc/nginx/conf.d/default.conf

RUN mkdir /etc/nginx/ssl

COPY files/dev-ssl-bundle.crt /etc/nginx/ssl/ssl-bundle.crt

COPY files/dev-ssl.key /etc/nginx/ssl/ssl.key
