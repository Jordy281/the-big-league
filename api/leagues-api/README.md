# Leagues API

This microservice API transacts with the Accounts database

[URL](https://Full-Documentation.com/, Full Documentation)


## Installation and Setup
This API is running on App Engine and can be called using the service's [URL](https://partners-api-dot-revenue-reporting-280115.uc.r.appspot.com/).

It can be run locally using:
```bash
pip install -r requirements.txt
python3 main.py
```


## Local Development
### Start mysql server proxy to connect to cloud SQL
```bash
sudo /etc/init.d/mysql stop 
cloud_sql_proxy -instances=cmp-dandelion-dev:us-central1:cmp-dandelion=tcp:3306
```

sudo /etc/init.d/mysql stop 
cloud_sql_proxy -instances=cmp-dandelion-staging:us-central1:cmp-dandelion=tcp:3306

sudo /etc/init.d/mysql stop 
cloud_sql_proxy -instances=cmp-dandelion-production:us-central1:cmp-dandelion=tcp:3306

### Serve API
```bash
python3 main.py
```
### NOTE:
You may need to disable the unix socket in db.py

The config for App engine to connect to the SQL database is for it to use the public IP, and a unix socket

## Team
Created by: Jordan Stirling

Readme Last Edited: 2021/25/01