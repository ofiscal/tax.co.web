#base docker image off of python alpine
FROM python:3.8-alpine
#this would add scripts in our PATH of the container
ENV PATH="/scripts:${PATH}"
#this will copy requirements to our docker image
COPY ./requirements.txt /requirements.txt
#this are required alpine packages to install uWSGI. apk is alpine package manager command
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
#this will pip install dependencies in our requirements
RUN pip install -r /requirements.txt
#remove the set of requirements created in line 8 like gcc libc-dev linux-headers
#because they are needed for the installation in line 10. after that we try to keep it light
RUN apk del .tmp
#creates app directory
RUN mkdir /django
#copies contents of our app called django into our dockerfile
COPY ./django /django
# change directory to our working directory
WORKDIR /django
#scripts useful for our dockerimage
COPY ./scripts /scripts
#any scripts can be executable
RUN chmod +x /scripts/*
#create new directories inside our docker image
RUN mkdir -p /vol/web/tax_co
RUN mkdir -p /vol/web/static
#create a user in the image. I guess its like app_user in your case
RUN adduser -D user
#this sets the owner of the volume directories in line 25,26
RUN chown -R user:user /vol
#user has full access the group and others have read access
RUN chmod -R 755 /vol/web
#switch to the user
USER user
#start our application and run uWSGI
CMD ["entrypoint.sh"]