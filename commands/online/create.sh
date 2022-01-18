eval "$(jq -r '.paths.base_system | to_entries | .[] | "base_system_" + .key + "=\"" + .value + "\""' < paths/paths.json)"
eval "$(jq -r '.paths.docker | to_entries | .[] | "docker_" + .key + "=\"" + .value + "\""' < paths/paths.json)"

docker run --name tax.co.web -it                         \
  -v $base_system_tax_co_web/paths/:$docker_paths        \
  -v $base_system_tax_co_web/apache2/:$docker_apache     \
  -v $base_system_tax_co_web/django/:$docker_django      \
  -v $base_system_tax_co_web/commands/:$docker_commands  \
  -v $base_system_tax_co/:$docker_tax_co                 \
  -p 8000:8000                                           \
  -d -h 127.0.0.1                                        \
  -p 443:443                                             \
  -p 80:80                                               \
  ofiscal/tax.co:latest

/home/ubuntu/tax.co.web/commands/online/run-services.sh
