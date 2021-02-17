#!/bin/bash

target=/etc/apache2/apache2.conf

rm    $target
ln -s /mnt/apache2/apache2.conf $target
