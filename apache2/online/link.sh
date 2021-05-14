#!/bin/bash

away=/etc/apache2/online
home=/mnt/apache2/online

for i in apache2.conf ports.conf; do
    rm    ${away}/$i
    ln -s ${home}/$i ${away}/$i
done
