#!/bin/sh

GIT_REPOSITORY=https://github.com/Yassine-cheffai/twitter_data_set_builder_api.git
echo $GIT_REPOSITORY

# docker rm --force tdb-api
# git pull
# docker build --tag tdb-api:1.0 . 
# docker run --detach --publish 8000:80 --name tdb-api tdb-api:1.0
# access the working directory on the server

# ssh -t user@domain.com 'cd /some/path; bash -l'
#
#ssh -t root@IP << EOF
#cd ~/twitter_data_set_builder_api   
#git pull
#EOF
# https://serverfault.com/questions/241588/how-to-automate-ssh-login-with-password


echo "deploy using heroku"
