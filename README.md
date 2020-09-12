# twitter_data_set_builder_api

## local server
`uvicorn main:app --reload`
`gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker`

## docker
`docker build --tag tdb:1.0 . `
`docker run --publish 8000:8000 --name tdb tdb:1.0`
`docker rm --force tdb`
