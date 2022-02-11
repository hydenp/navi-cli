import click
import os

from nav.alias_db import AliasDB
from nav.pretty_printer import Printer
from nav.file_handler import FileHandler


def refresh_session():
    """
    function to reload the session if auto_reload has been set to true
    """

    global_vars = FileHandler.read_globals()
    if 'auto_reload' not in global_vars:
        global_vars['auto_reload'] = 'false'

    if global_vars['auto_reload'] == 'true':
        if global_vars['shell'] == 'zsh':
            click.echo('Refreshing session...')
            os.system('zsh $HOME/.zshrc')
        elif global_vars['shell'] == 'bash':
            click.echo('Refreshing session...')
            os.system('bash ~/.bashrc')
        else:
            click.echo('navi is not configured to refresh your session, please do so manually!')


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
        click.echo(f'Alias {alias} added successfully')
        refresh_session()


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
        click.echo(f'Alias updated, new alias to cwd is {alias}')
        refresh_session()
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
            click.echo(f'Alias {query_res[0]} for the cwd removed successfully')
            refresh_session()
        else:
            click.echo('There is no alias to remove for the cwd')
    else:
        if AliasDB.delete(alias):
            cmds = AliasDB.fetch_all()
            FileHandler.refresh(cmds)
            click.echo(f'Alias {alias} removed successfully')
            refresh_session()


@nav.command()
def list():
    """
    List all aliases
    """

    # fetch all the aliases and print them out
    headers = ['Alias', 'Directory']
    cmds = AliasDB.fetch_all()
    if len(cmds) == 0:
        click.echo('No aliases currently setup with navi')
    else:
        Printer.pretty_print(headers, cmds, True)


@nav.command()
def search():
    """
    Search for if there is an alias for the current working directory
    """

    query_res = AliasDB.search_cwd(os.getcwd())
    if query_res is None:
        click.echo('No alias for found the current working directory')
    else:
        click.echo(f'{query_res[0]} is the alias for the current working directory')


@nav.command()
@click.argument('show', default='')
def config(show):
    """
    configure if you're using zsh or bash and weather to auto reload the shell
    """

    if show in ['show', 's']:
        # showing the global vars
        gls = FileHandler.read_globals()
        if gls != {}:
            data = []
            headings = ['Global', 'Value']
            for k in gls:
                data.append((k, gls[k]))
            Printer.pretty_print(headings, data)
        else:
            click.echo('No globals currently configured. Run navi config or navi set <global> <value> to set them.')
    else:
        # setting up shell choice
        shell = os.getenv('SHELL')
        shell_choice = True
        if 'zsh' in shell:
            FileHandler.update_global('shell', 'zsh')
            click.echo('We detected you are running zsh. navi shell type has been configured.')
            shell_choice = False
        elif 'bash' in shell:
            FileHandler.update_global('shell', 'bash')
            click.echo('We detected you are running bash. navi shell type has been configured.')
            shell_choice = False
        else:
            click.echo('Uh oh, not sure what type of terminal you are running')

        # if shell can't be figured out automatically
        while shell_choice:
            click.echo('Are you using zsh or bash? Please enter 1 or 2')
            click.echo('1: zsh\n2: bash')
            value = click.prompt('>', type=int)
            if value == 1:
                FileHandler.update_global('shell', 'zsh')
                click.echo('navi has been configured for zsh.')
                shell_choice = False
            elif value == 2:
                FileHandler.update_global('shell', 'bash')
                click.echo('navi has been configured for bash.')
                shell_choice = False
            else:
                click.echo('Please enter a valid option')

        # setting up auto_reload choice
        auto_load_choice = True
        while auto_load_choice:
            click.echo('Would you like to auto-reload your shell after add/update/remove commands?')
            click.echo('1: Yes, auto-reload\n2: No, don\'t auto-reload\n3: What does this mean...')
            choice = click.prompt('>', type=int)
            if choice == 1:
                FileHandler.update_global('auto_reload', 'true')
                click.echo('navi has been configured for auto-reload')
                auto_load_choice = False
            elif choice == 2:
                FileHandler.update_global('auto_reload', 'false')
                click.echo('navi has been configured not to auto-reload')
                auto_load_choice = False
            elif choice == 3:
                click.echo('''
                In order for your alias to work, you need to reload your terminal session.
                Ff you select yes, the command will run automatically after you add/update/remove.
                This will slow down navi but it won't be any faster to run it yourself.
                ''')
            else:
                click.echo('Please enter a valid option')


@nav.command()
@click.argument('global_to_set', nargs=2)
def set(global_to_set):
    """
    set the shell type and auto_reload configs without using the config command
    """

    if global_to_set[0] in ['auto_reload', 'ar'] :
        if global_to_set[1] in ['true', 'false']:
            FileHandler.update_global('auto_reload', global_to_set[1])
            click.echo(f'auto_reload has been set to {global_to_set[1]}')
        else:
            click.echo('Invalid auto_reload arg, accepted inputs are:\ntrue\nfalse')
    elif global_to_set[0] == 'shell':
        if global_to_set[1] in ['bash', 'zsh']:
            FileHandler.update_global(global_to_set[0], global_to_set[1])
            click.echo(f'shell has been set to {global_to_set[1]}')
        else:
            click.echo('Invalid shell type, accepted inputs are:\nzsh\nbash')
    else:
        click.echo('There is no global for that in navi')


if __name__ == '__main__':
    nav()
