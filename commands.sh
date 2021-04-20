####
#### From host system
####

eval "$(jq -r '.paths | to_entries | .[] | .key + "=\"" + .value + "\""' < paths.json)"

# Running locally, without connection to internet.
docker run --name tax.co.web -it                   \
  -v $base_system_tax_co_web/apache2/:/mnt/apache2 \
  -v $base_system_tax_co_web/django/:/mnt/django   \
  -v $base_system_tax_co/:/mnt/tax_co              \
  -p 8000:8000                                     \
  -d -h 127.0.0.1                                  \
  ofiscal/tax.co:latest

# Serving to the internet.
docker run --name tax.co.web -it                   \
  -v $base_system_tax_co_web/apache2/:/mnt/apache2 \
  -v $base_system_tax_co_web/django/:/mnt/django   \
  -v $base_system_tax_co/:/mnt/tax_co              \
  -p 8000:8000                                     \
  -d -h 127.0.0.1                                  \
  -p 443:443                                       \
  -p 80:80                                         \
  ofiscal/tax.co:latest

docker start tax.co.web
docker exec -it tax.co.web bash

docker stop tax.co.web && docker rm tax.co.web


####
#### From within Docker container
####

# initialize & restart
bash /mnt/apache2/link.sh
cd /mnt/
service apache2 stop && service apache2 start
