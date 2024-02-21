#!/usr/bin/env bash
MODULE=wot_api
API=api.yaml
TARGET=flask_out

#( set -x ; curl -kL dexterindustries.com/update_grovepi | bash )
#( set -x ; curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash )
#export NVM_DIR="$HOME/.nvm"
#[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
#[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
#( set -x ; nvm install --lts )
#( set -x ; sudo apt install default-jre lsof )
#( set -x ; npm install @openapitools/openapi-generator-cli -g )
#( set -x ; pip3 install rdflib pyyaml)
( set -x ; python3 m2m.py )
( set -x ; openapi-generator-cli generate -i ${API} -g python-flask -o ${TARGET} -c config.json)
( set -x ; python3 post_generation.py ${TARGET} ${MODULE} ${API})
( set -x ; cp -r hub.py __main__.py templates/ implementations/ ${TARGET}/${MODULE})
( set -x ; cd flask_out; python3 -m wot_api )