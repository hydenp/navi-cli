import click
import os

# create the nav group of commands
@click.group()
def nav() -> None:
    '''
    option to add navigation aliases
    '''
    pass

@nav.command()
# @click.option('--tag', '-', help="Optionally add tags to group your aliases", required=False)
@click.argument('alias')
def add(alias):
    cwd = os.getcwd()
    click.echo(cwd)
    click.echo(alias)

@nav.command()
def update():
    pass
    
@nav.command()
def remove():
    pass

@nav.command()
def list():
    pass

if __name__ == '__main__':
    nav()
