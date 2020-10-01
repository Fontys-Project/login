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

## Usage

The service exposes multiple HTTP endpoints which have to be described.

To run the service, use

```
loginapi run
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## known issues
If you encounter `OSError: mysql_config not found` while installing requirements, please run `sudo apt install libmysqlclient-dev`
