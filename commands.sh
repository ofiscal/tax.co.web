####
#### Create the Docker container
####

# PITFALL: Run this from the root of the tax.co.web repo,
# which defines paths.json.
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

# Destroy it
docker stop tax.co.web && docker rm tax.co.web


####
#### Once it's been created
####

docker start tax.co.web

# enter docker container as root, set up cron
docker exec -it -u 0 tax.co.web bash
cp /mnt/tax_co/cron/*_cron /etc/cron.d
echo "" > /etc/cron.deny
service cron stop && service cron start

# enter docker container as appuser, set up apache
docker exec -it tax.co.web bash
bash /mnt/apache2/link.sh
service apache2 stop && service apache2 start
cd /mnt/
