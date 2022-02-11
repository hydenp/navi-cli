# Navi-CLI

Have many different projects you're working on that are constantly changing? Entering the same `cd` command all the time? navi-cli is here to save you precious seconds!
- Navigate to your project folder and run `navi add <alias>` 
- Reload your terminal and now easily navigate from anywhere to your project directory by running `<alias>`. 
- Finished with that project? `navi remove <alias>` and the alias is removed!
- Simply run `navi` to see a full list of commands

## Setup
- run `git clone git@github.com:hydenp/navi-cli.git && cd navi-cli && pip install . && cd .. && rm -rf navi-cli`
- add the path to the alias file to your shell config file `source $HOME/.navi-cli/aliases` or similar
- refresh your terminal session or open a new terminal and run `navi` to see avialable commands
