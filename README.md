# twitter_data_set_builder_api

## local server
`uvicorn main:app --reload`  
`gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker`

## docker
`docker build --tag tdb-api:1.0 . `  
`docker run --detach --publish 8000:80 --name tdb-api tdb-api:1.0`  
`docker rm --force tdb-api`  
