# Flask application for the sale and purchase of books of the Ukrainian and not only publishing house

## Install all dependencies:
```bash
pip install -r requirements.txt
```

## Export environment variables:
```shell
FLASK_APP="bookshop:create_app(ENV_NAME)"
FLASK_ENV="development"
```

*ENV_NAME - 'prod' | 'test' | 'dev'

## Compile translations
```shell
pybabel compile -d bookshop/translations
```
or use flask cli:
```shell
flask translate compile
```

## Start pytest:
```shell
pytest
pytest --cov-report term-missing --cov=bookshop
```

## Commands for Working with db
```shell
flask db init

flask db migrate -m 'Commit message'
flask db upgrade
```