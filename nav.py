import click
import os

from sqlite_db import Alias_DB
from pretty_printer import Printer
from file_handler import FileHandler

# create the nav group of commands
@click.group()
def nav() -> None:
    '''
    Add navigation aliases
    '''
    pass

@nav.command()
@click.argument('alias', type=str)
def add(alias):
    '''
    Add alias to navigate to current directory with alias as argument
    '''

    # get the current working directory
    cwd = os.getcwd()

    # add the alias to the db and then write to the file
    db = Alias_DB()
    if db.insert(alias, cwd, None):
        FileHandler.write_cd(alias, cwd)


@nav.command()
def update():
    pass
    
@nav.command()
@click.argument('alias', type=str)
def remove(alias):
    '''
    Remove alias to current directory
    '''

    # delete the alias from the database and then refresh the alias file
    db = Alias_DB()
    if db.delete(alias):
        cmds = db.fetch_all()
        FileHandler.refresh(cmds)
    

@nav.command()
def list():
    '''
    List all aliases
    '''

    # fetch all the aliases and print them out
    headers = ['Aliases', 'Directory']
    db = Alias_DB()
    cmds = db.fetch_all()
    if len(cmds) == 0:
        print("You don't currently have any aliases")
    else:
        Printer.pretty_print(headers, cmds)


if __name__ == '__main__':
    nav()
