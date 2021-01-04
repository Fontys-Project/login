# Login Service

Login Service is part of Warehouse Management System (WMS+) which utilizes authentication functionality.

## Installation

The service is based on a [cookiecutter](https://github.com/karec/cookiecutter-flask-restful#installation) instance of Flask-restful.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the login service requirements.

```bash
pip install -r requirements.txt
pip install -e .
```

You have now access to cli commands and you can init your project

```
loginapi db upgrade
loginapi init
```

## Docker-compose
This service has docker-compose to run and manage containers. To run all containers, simply run `docker-compose up -d`  
After all services are up, run `docker-compose exec web loginapi db upgrade` to run every migration to make sure you are up to date.

## Usage

The service exposes multiple HTTP endpoints which have to be described.

To run the service, use

```
loginapi run
```

## Run celery in debug mode
Make sure you have `loginapi run`, db and rabbitmq container running. Celery version must be 4.4.  
Configure celery like the following:
```
Script path: /path/to/venv/bin/celery (or run "$ which celery" to get bin path)
Parameters: -A celery_app worker -l info -n login_worker@%h
Environment variables can be default
Working directory: /path/to/login/LoginService/loginapi
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## known issues
If you encounter `OSError: mysql_config not found` while installing requirements, please run `sudo apt install libmysqlclient-dev`
