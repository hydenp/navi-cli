import click
import os
import nav

from nav.alias_db import AliasDB
from nav.pretty_printer import Printer
from nav.file_handler import FileHandler


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

    # add the alias to the db and then write to the file
    if AliasDB.insert(alias, os.getcwd(), None):
        FileHandler.write_cd(alias, os.getcwd())
        click.echo('Alias {} added successfully'.format(alias))


@nav.command()
@click.argument('alias', type=str)
def update(alias):
    """
    If an alias exists for the current working directory, update it with the argument provided
    """

    res = AliasDB.search_cwd(os.getcwd())
    if res is not None:
        AliasDB.update(res[0], os.getcwd(), alias)
        cmds = AliasDB.fetch_all()
        FileHandler.refresh(cmds)
        click.echo('Alias updated, new alias to cwd is {}'.format(alias))
    else:
        click.echo('No alias to update for the current directory')


@nav.command()
@click.argument('alias', type=str, required=False)
def remove(alias):
    """
    Remove alias to current directory if no argument provided, and it exists. If alias arg is provided, remove the
    provided alias
    """

    if alias is None:
        query_res = AliasDB.search_cwd(os.getcwd())
        if query_res is not None:
            AliasDB.delete(query_res[0])
            click.echo('Alias {} for the cwd removed successfully'.format(query_res[0]))
        else:
            click.echo('There is no alias to remove for the cwd')
    else:
        if AliasDB.delete(alias):
            cmds = AliasDB.fetch_all()
            FileHandler.refresh(cmds)
            click.echo('Alias {} removed successfully'.format(alias))


@nav.command()
def list():
    """
    List all aliases
    """

    # fetch all the aliases and print them out
    headers = ['Aliases', 'Directory']
    cmds = AliasDB.fetch_all()
    if len(cmds) == 0:
        click.echo('No aliases currently setup with navi')
    else:
        Printer.pretty_print(headers, cmds)


@nav.command()
def search():
    """
    Search for if there is an alias for the current working directory
    """

    query_res = AliasDB.search_cwd(os.getcwd())
    if query_res is None:
        click.echo('No alias for found the current working directory')
    else:
        click.echo('{} is the alias for the current working directory'.format(query_res[0]))
