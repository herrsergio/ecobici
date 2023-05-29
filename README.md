# ecobici
Script to query the Ecobici data

```
cd empty-stations
npm i serverless@3.28.1  # There is a bug with latest version 3.31 and local-schedule
serverless plugin install -n serverless-local-schedule
serverless plugin install -n serverless-python-requirements
export AWS_SECRET_ACCESS_KEY=xxxx
export AWS_ACCESS_KEY_ID=xxxxx
serverless deploy
```
