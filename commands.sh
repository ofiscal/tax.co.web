####
#### From host system
####

docker run --name webapp -it                    \
  -v /home/jeff/of/webapp/apache2/:/mnt/apache2 \
  -v /home/jeff/of/webapp/django/:/mnt/web      \
  -v /home/jeff/of/tax.co/web/:/mnt/tax_co      \
  -p 8000:8000 -d -h 127.0.0.1                  \
  ofiscal/tax.co:latest

docker start webapp
docker exec -it webapp bash

docker stop webapp && docker rm webapp


####
#### From within Docker container
####

# initialize & restart
bash /mnt/apache2/link.sh
cd /mnt/
service apache2 stop && service apache2 start
