####
#### From host system
####

docker run --name webapp -it				\
  -v /home/ec2-user/webapp/apache2/:/mnt/apache2	\
  -v /home/ec2-user/webapp/django/:/mnt/web		\
  -v /home/ec2-user/tax.co/web/:/mnt/tax_co		\
  -p 8000:8000 -d -h 127.0.0.1				\
  -p 443:443 -d -h 127.0.0.1				\
  -p 80:80 -d -h 127.0.0.1				\
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
