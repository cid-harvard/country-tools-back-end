#!/bin/bash
set -xe

# Copy Travis build
scp ./requirements.txt $SERVER_USER@$SERVER_ADDRESS:$APP_DIR/api
rsync -rq --delete --rsync-path="mkdir -p $APP_DIR/api && rsync" $TRAVIS_BUILD_DIR/country_tools_api $SERVER_USER@$SERVER_ADDRESS:$APP_DIR/api

ssh $SERVER_USER@$SERVER_ADDRESS <<- EOF
	sudo apt update
    sudo apt install -y python3.7
    sudo apt install -y python3-venv
    cd $APP_DIR/api
    python3 -m venv env
    . ./env/bin/activate
    pip install -r requirements.txt
    python flask_app.py
EOF
