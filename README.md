# GrowthLab.app Back-End 
## by the Growth Lab at Harvard's Center for International Development
This package is part of Harvard Growth Lab’s portfolio of software packages, digital products and interactive data visualizations. To browse our entire portfolio, please visit growthlab.app. To learn more about our research, please visit [Harvard Growth Lab’s home page](https://growthlab.cid.harvard.edu/).

This codebase handles data ingestion and administering a GraphQL API for the Growth Lab's [GrowthLab.app](https://growthlab.app) endeavor.

Shared under a [Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/) license.

## Overview
This repository is divided into two main segments: individual directories for each country project (e.g., `/albania` and `/country_tools_api`. Individual project directories contain the processes for processing and ingesting raw data into needed formats for the tool to work. Separately, the `country_tools_api` handles all of the functions necessary to connect to a populated PostgreSQL database (where data from individual countries ends up) and serves the data according to the defined models.

## Requirements
This project has two separate requirements files. The first, the standard `requirements.txt`, is the file that ultimately ends up on the webserver responsible for hosting the Flask/Graphene API. The second, `requirements-develop.txt`, is useful for running ingestions and all other aspects of this project that are not necessary to host on the API server.

## Data Ingestion
Data ingestion processes are uniquely defined for individual country projects in corresponding directories within the root of the project. Importantly, most data is not provided in this repository in order to comply with licensing and other data usage agreements. However, if an individual has access to necessesary data to run the processes and format the data correspondingly, this would allow for full usage of this tool set.

Due to the internal arrangement within the Growth Lab, most country project ingestion scripts will likely concern themselves mostly with data transformation rather than computing new values or models. These processes will likely ensure various consistent ID fields are used throughout the data and alter fields to comply with the database models whenever necessary.

## Country Tools GraphQL API
Data through the webserver is accessed via GraphQL queries via the `/graphql` endpoint.

### Configuration
The API is primarily configured through SQLAlchemy and Graphene models. SQLAlchemy models (defined in individual project files within `./country_tools_api/database`) reflect the connected database structure and the data format by which the project-specific ingestion directories should output. This also includes relationships between tables which are then automatically passed through Graphene for allow for sub-querying objects within a single GraphQL request.

Graphene models, defined in `./country_tools_api/schema.py`, then take these SQLAlchemy models and define the ways in which they can be queried through the webserver. This largely directly reflects the database models, but some objects may require specific definitions of query parameters or other custom logic.

The database configuration uses environment variables in order to define the connection. These variables and their implementation can be found in `./country_tools_api/database/base.py`.

### Testing
To start the test server, simply run `python ./country_tools_api/flask_app.py`. This should begin a local server and allow for querying via the `/graphql` endpoint if everything is configured correctly and data is populated on the database server in question.

### Deployment
Our production and development instances are both deployed automatically via TravisCI using `master` and `develop` branches, respectively.

One necessary consideration is due to the separation of the front-end and back-end code bases in this project, care should be given to pushing non-breaking changes whenever at all possible. Removing or changing configurations that the front-end may rely on can cause breaking issues when pushed to the server.

## TravisCI
The TravisCI deployment for this project is done through a custom SSH script using Amazon Web Services EC2, rather than a more plug-and-play service more directly integrated with Travis CI. This was largely to allow for further customization and to allow for both the front and back-ends to be developed separately and hosted within the same server. These scripts can be found at root, including `./.travis.yml` and `./deploy.sh`. Additionally, encrypted SSH keys also live in this directory and are necessary for Travis to complete deployment.

Some variables, both sensitive and not, are configured through the TravisCI dashboard and are invoked throughout the scripts as environment variables. TravisCI allows for both private and public variables, so this has been a useful feature, particuarly in allowing for different variables with identical names in different branch environments.

## Contact
For further information on this project or other works of the Growth Lab of the Center for International Development, please contact [Brendan Leonard](mailto:brendan_leonard@hks.harvard.edu).
