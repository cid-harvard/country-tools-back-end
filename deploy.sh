#!/bin/bash
set -xe

SERVER_ADDRESS=$1

# Copy Travis build
rsync -rq --delete --rsync-path="mkdir -p $APP_DIR/api && rsync" $TRAVIS_BUILD_DIR/country_tools_api/ $SERVER_USER@$SERVER_ADDRESS:$APP_DIR/api
scp ./requirements.txt $SERVER_USER@$SERVER_ADDRESS:$APP_DIR/

ssh $SERVER_USER@$SERVER_ADDRESS <<- EOF
	sudo apt update
	sudo apt install -y python3.7
	sudo apt install -y python3-venv
	cd $APP_DIR
	python3 -m venv env
	. ./env/bin/activate
	pip install -r requirements.txt
	export COUNTRY_TOOLS_DB_USER=$COUNTRY_TOOLS_DB_USER
	export COUNTRY_TOOLS_DB_PASS=$COUNTRY_TOOLS_DB_PASS
	export COUNTRY_TOOLS_DB_HOST=$COUNTRY_TOOLS_DB_HOST
	export COUNTRY_TOOLS_DB_NAME=$COUNTRY_TOOLS_DB_NAME
	sudo cp $APP_DIR/api/gunicorn/api.service /etc/systemd/system
	sudo cp $APP_DIR/api/gunicorn/api.ini /etc/systemd/system
	sudo systemctl reload api
EOF
