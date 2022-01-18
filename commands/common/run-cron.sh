cp /mnt/tax_co/cron/*_cron /etc/cron.d
echo "" > /etc/cron.deny
service cron stop && service cron start
