from flask import Blueprint
import click
import os

translate_command = Blueprint('translate', __name__, 
                            cli_group='translate')


@translate_command.cli.command('update')
def update():
    """Update all languages."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot ./bookshop/'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i messages.pot -d bookshop/translations'):
        raise RuntimeError('update command failed')
    os.remove('./messages.pot')

@translate_command.cli.command('compile')
def compile():
    """Compile all languages."""
    if os.system('pybabel compile -d bookshop/translations'):
        raise RuntimeError('compile command failed')

@translate_command.cli.command('init')
@click.argument('lang')
def init(lang):
    """Initialize a new language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot ./bookshop/'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel init -i messages.pot -d bookshop/translations -l ' + lang):
        raise RuntimeError('init command failed')
    os.remove('./messages.pot')
