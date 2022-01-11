# # #
# # # USAGE
# # #
# This can't be evaluated as a script
# (although it *can* be evaluated as commands for tmux -- see tmux-setup.sh)
# because some of the commands it contains are
# for the Docker container it launches.
# It must instead be copied and pasted into the shell.

docker start tax.co.web

# Enter Docker container as root, set up cron, exit.
docker exec -it -u 0 tax.co.web bash
cp /mnt/tax_co/cron/*_cron /etc/cron.d
echo "" > /etc/cron.deny
service cron stop && service cron start
exit

# Enter Docker container as jeff, set up Apache, stay in Docker.
docker exec -it tax.co.web bash
bash /mnt/apache2/offline/link.sh
service apache2 stop && service apache2 start
cd /mnt/
