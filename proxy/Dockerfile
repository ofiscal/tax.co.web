FROM nginxinc/nginx-unprivileged:1-alpine
#run the container in unprivileged mode in case of compromise
COPY ./default.conf /etc/nginx/conf.d/default.conf
#copies default.conf to the container
COPY ./uwsgi_params /etc/nginx/uwsgi_params
#copies params to the container
USER root
#switches us to root user to create new file
RUN mkdir -p /vol/static
#creates static folder with owner having full access, everyone else read-only
RUN chmod 755 /vol/static

USER nginx
#switch us basic to unprivileged user