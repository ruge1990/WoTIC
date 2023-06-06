#!/usr/bin/env bash
PORT=9000
TARGET=flask_out
MODULE=wot_api
API=api.yaml
PI_IP=192.168.178.22

( set -x ; pipenv run python m2m.py )
( set -x ; openapi-generator-cli generate -i ${API} -g python-flask -o ${TARGET} -c config.json )
( set -x ; pipenv run python post_generation.py ${TARGET} ${MODULE} ${API} )
( set -x ; pipenv run python coap_generation.py)

( set -x ; scp -r server.py flask_out/ pi@${PI_IP}:/home/pi/api)

( set -x ; ssh -t pi@${PI_IP} "cd /home/pi/api/flask_out;
lsof -ti tcp:9000 | xargs kill;
lsof -ti udp:5683 | xargs kill;
python3 -m wot_api & python3 ../server.py
" )
