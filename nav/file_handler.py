import os


class FileHandler:
    """
    class to manage reading and writing to the alias file
    ...

    Methods
    -------
    write_cd()
    clear_file()
    refresh()
    read_globals()
    update_global()
    """

    # store the name of the file
    file_path = os.path.expanduser("~") + '/.navi-cli/aliases'

    @staticmethod
    def write_cd(alias, path):
        """Write a cd command to the file"""

        to_write = "alias {}=\"cd {}\"\n".format(alias, path)
        f = open(FileHandler.file_path, "a")
        f.write(to_write)
        f.close()

    @staticmethod
    def clear_file():
        """Delete all contests from the file"""
        f = open(FileHandler.file_path, "r+")
        f.seek(0)
        f.truncate()
        f.close()

    @staticmethod
    def refresh(cmds):
        """Delete all data from the file then write all given cmds in"""
        FileHandler.clear_file()
        for cmd in cmds:
            FileHandler.write_cd(cmd[0], cmd[1])
