#!/bin/bash

source /home/student/Documents/linux/config.cfg

psql "host=${db_host} port=${db_port} dbname=${db_name} user=${username} password=${pwd}" -c "\COPY (${queries}) TO '/home/student/Documents/linux/invoices_${year}.csv' (FORMAT csv)"

sed  -i "1i ${columns}" invoices_${year}.csv

echo invoices_${year}.csv | gzip -c > invoices_${year}.gzip
