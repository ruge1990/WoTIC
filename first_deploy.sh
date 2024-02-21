#!/usr/bin/env bash
PORT=9000
TARGET=flask_out
MODULE=wot_api
API=api.yaml
PI_IP=192.168.178.22

echo initialize raspberry pi
# ( set -x ; ssh -t pi@${PI_IP} "sudo apt update; sudo apt upgrade;
# curl -kL dexterindustries.com/update_grovepi | bash;
# sudo apt install lsof" )

# ( set -x ; ssh -t pi@${PI_IP} "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh;
# sudo apt install libssl-dev;
# pip3 install --upgrade 'aiocoap[all]'")

( set -x ; pipenv run python m2m.py )
( set -x ; openapi-generator-cli generate -i ${API} -g python-flask -o ${TARGET} -c config.json)
( set -x ; pipenv run python post_generation.py ${TARGET} ${MODULE} ${API})
( set -x ; cp -r hub.py implementations/ ${TARGET}/${MODULE})
( set -x ; pipenv run python coap_generation.py)

( set -x ; scp -r server.py flask_out/ pi@${PI_IP}:/home/pi/api)
( set -x ; ssh -t pi@${PI_IP} "cd /home/pi/api/flask_out;
python3 -m wot_api & python3 ../server.py" )
# ( set -x ; ssh -t pi@${PI_IP} "cd /home/pi/api/flask_out;
# pip3 install -r requirements.txt;
# python3 -m wot_api & python3 ../server.py" )
