#!/bin/sh

GIT_REPOSITORY=https://github.com/Yassine-cheffai/twitter_data_set_builder_api.git
echo $GIT_REPOSITORY

# access the working directory on the server
docker rm --force tdb-api
git pull
docker build --tag tdb-api:1.0 . 
docker run --detach --publish 8000:80 --name tdb-api tdb-api:1.0