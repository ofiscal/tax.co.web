# USAGE:
# Run the `jq` and `docker` commands from the host system,
# from the root of tax.co.web.
# The other commands are for running inside the docker container.

# PITFALL: By "offline" I mean the *website* is offline --
# available at 127.0.0.1:8000, not connected to the internet.
# But the code still has internet access, and will send email,
# provided email credentials are available in tax.co.web/apache2/secret/
# (see python/email.py in the tax.co repo for details).


####
#### Create the Docker container
####

# PITFALL: Run this from the root of the tax.co.web repo,
# which defines paths.json.
eval "$(jq -r '.paths | to_entries | .[] | .key + "=\"" + .value + "\""' < paths/paths.json)"

# Running locally, without connection to internet.
docker run --name tax.co.web -it                     \
  -v $base_system_tax_co_web/paths/:$docker_paths    \
  -v $base_system_tax_co_web/apache2/:$docker_apache \
  -v $base_system_tax_co_web/django/:$docker_django  \
  -v $base_system_tax_co/:$docker_tax_co             \
  -p 8000:8000                                       \
  -d -h 127.0.0.1                                    \
  ofiscal/tax.co:latest

# Serving to the internet.
docker run --name tax.co.web -it                     \
  -v $base_system_tax_co_web/paths/:$docker_paths    \
  -v $base_system_tax_co_web/apache2/:$docker_apache \
  -v $base_system_tax_co_web/django/:$docker_django  \
  -v $base_system_tax_co/:$docker_tax_co             \
  -p 8000:8000                                       \
  -d -h 127.0.0.1                                    \
  -p 443:443                                         \
  -p 80:80                                           \
  ofiscal/tax.co:latest

# Destroy it
docker stop tax.co.web && docker rm tax.co.web


####
#### Once it's been created
####

docker start tax.co.web

# Enter Docker container as root, set up cron.
docker exec -it -u 0 tax.co.web bash
cp /mnt/tax_co/cron/*_cron /etc/cron.d
echo "" > /etc/cron.deny
service cron stop && service cron start

# ONLINE use:
# Enter Docker container as appuser, set up Apache.
docker exec -it tax.co.web bash
bash /mnt/apache2/online/link.sh
service apache2 stop && service apache2 start
cd /mnt/

# OFFLINE use:
# Enter Docker container as appuser, set up Apache.
docker exec -it tax.co.web bash
bash /mnt/apache2/offline/link.sh
service apache2 stop && service apache2 start
cd /mnt/
