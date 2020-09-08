#!/bin/bash
set -xe

# Generate file with database config
cat > $TRAVIS_BUILD_DIR/country_tools_api/.database << EOL
    COUNTRY_TOOLS_DB_USER='${COUNTRY_TOOLS_DB_USER}'
    COUNTRY_TOOLS_DB_PASS='${COUNTRY_TOOLS_DB_PASS}'
    COUNTRY_TOOLS_DB_HOST='${COUNTRY_TOOLS_DB_HOST}'
    COUNTRY_TOOLS_DB_NAME='${COUNTRY_TOOLS_DB_NAME}'
EOL

# Copy Travis build
rsync -rq --delete --rsync-path="mkdir -p $APP_DIR/api && rsync" $TRAVIS_BUILD_DIR/country_tools_api/ $WEBSERVER_USER@$WEBSERVER_ADDRESS:$APP_DIR/api
scp ./requirements.txt $WEBSERVER_USER@$WEBSERVER_ADDRESS:$APP_DIR/

ssh $WEBSERVER_USER@$WEBSERVER_ADDRESS <<- EOF
    sudo apt update
    sudo apt install -y python3.7
    sudo apt install -y python3-venv
    cd $APP_DIR
    python3 -m venv env
    . ./env/bin/activate
    pip install -r requirements.txt
    sudo cp $APP_DIR/api/gunicorn/api.service /etc/systemd/system
    sudo cp $APP_DIR/api/gunicorn/api.ini /etc/systemd/system
    sudo systemctl enable api
    sudo systemctl restart api
EOF
