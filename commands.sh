####
#### Start and enter Docker container
####

docker run --name webapp -it                    \
  -v /home/jeff/of/webapp/apache2/:/mnt/apache2 \
  -v /home/jeff/of/webapp/django/:/mnt/web      \
  -v /home/jeff/of/tax.co/web/:/mnt/tax         \
  -p 8000:8000 -d -h 127.0.0.1                  \
  ofiscal/tax.co:latest

docker exec -it webapp bash

docker stop webapp && docker rm webapp


####
#### In Docker container, configure and run apache
####

bash /mnt/apache2/link.sh
service apache2 start


####
#### also handy
####

service apache2 stop && service apache2 start
