#!/bin/bash

lockfile="/tmp/nass.lockfile"
cd /var/www/html/nass
if test -f "${lockfile}"; then
	echo "NASS Server is up and runnning"
else
	echo "NASS server is down. bringing up"
	touch "${lockfile}"
	python3.7 /var/www/html/nass/manage.py runserver 0.0.0.0:8002
fi
