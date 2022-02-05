import click
import os

from sqlite_db import Alias_DB
from pretty_printer import Printer
from file_handler import FileHandler


# create the nav group of commands
@click.group()
def nav() -> None:
    """
    Manage navigation aliases
    """
    pass


@nav.command()
@click.argument('alias', type=str)
def add(alias):
    """
    Add alias to navigate to current directory with alias as argument
    """

    # get the current working directory
    cwd = os.getcwd()

    # add the alias to the db and then write to the file
    db = Alias_DB()
    if db.insert(alias, cwd, None):
        FileHandler.write_cd(alias, cwd)
        click.echo('Alias added successfully')


@nav.command()
@click.argument('alias', type=str)
def update(alias):
    """
    If an alias exists for the current working directory, update it with the argument provided
    """
    db = Alias_DB()
    res = db.search_cwd(os.getcwd())
    if res is not None:
        db.update(res[0], os.getcwd(), alias)
        cmds = db.fetch_all()
        FileHandler.refresh(cmds)
        click.echo('Alias updated, alias to cwd is {}'.format(alias))
    else:
        click.echo('No aliases to the current directory')


@nav.command()
@click.argument('alias', type=str, required=False)
def remove(alias):
    """
    Remove alias to current directory if no argument provided.
    If alias is provided, remove the provided alias
    """

    db = Alias_DB()

    if alias is None:
        query_res = db.search_cwd(os.getcwd())
        if query_res is not None:
            db.delete(query_res[0])
            click.echo('Alias removed successfully')
        else:
            click.echo('There is no alias to remove for the cwd!')
    else:
        if db.delete(alias):
            cmds = db.fetch_all()
            FileHandler.refresh(cmds)
            click.echo('Alias {} removed successfully'.format(alias))


@nav.command()
def list():
    """
    List all aliases
    """

    # fetch all the aliases and print them out
    headers = ['Aliases', 'Directory']
    db = Alias_DB()
    cmds = db.fetch_all()
    if len(cmds) == 0:
        click.echo('You don\'t currently have any aliases setup with navi')
    else:
        Printer.pretty_print(headers, cmds)


@nav.command()
def search():
    """
    Search for if there is an alias for the current working directory
    """
    db = Alias_DB()
    query_res = db.search_cwd(os.getcwd())
    if query_res is None:
        click.echo('No alias for the current working directory')
    else:
        click.echo('{} is the alias for the current working directory'.format(query_res[0]))

