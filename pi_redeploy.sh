#!/usr/bin/env bash
MODULE=wot_api
API=api.yaml
TARGET=flask_out

( set -x ; python3 m2m.py )
( set -x ; openapi-generator-cli generate -i ${API} -g python-flask -o ${TARGET} -c config.json )
( set -x ; python3 post_generation.py ${TARGET} ${MODULE} ${API} )
( set -x ; cp -r __main__.py implementations/ ${TARGET}/${MODULE} )
