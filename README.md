# navi-cli

Have many different projects you're working on that are constantly changing? Entering the same `cd` command all the time to navigate to the directory in your terminal? navi-cli is here to save you precious seconds...
- Navigate to your project folder and run `navi add <alias>` 
- Reload your terminal session and now easily navigate from anywhere to your project directory by running `<alias>`. 
- Finished with that project? `navi remove <alias>` and the alias is removed!
- Simply run `navi` to see a full list of commands

## Setup
- run `git clone https://github.com/hydenp/navi-cli.git && cd navi-cli && pip install . && cd .. && rm -rf navi-cli`
- add the path to the alias file to your shell config file `source $HOME/.navi-cli/aliases` - likely your `.zshrc` file or `.bashrc` if you are running bash
- reload your terminal session or open a new terminal window/tab and run `navi` to see avialable the commands
## Uninstall
- `pip uninstall navi-cli`

## Next Steps
- Plan is to make navi officially available via Pypi and pip
- Also exploring creating an executable and/or making deliverable via Homebrew
