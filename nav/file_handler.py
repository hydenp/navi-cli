import os


class FileHandler:
    """class to manage reading and writing to the alias file"""

    # store the name of the file
    file_path = os.path.expanduser("~") + '/.navi-cli/aliases'
    globals_file = os.path.expanduser("~") + '/.navi-cli/navi_globals.txt'

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

    @staticmethod
    def __write_global(global_var, mode):
        """write a global var to the file with the specified write mode"""
        f = open(FileHandler.globals_file, mode)
        f.write(global_var)
        f.close()

    @staticmethod
    def read_globals():
        """read the globals into a dictionary if they exist a"""
        file_exists = os.path.exists(FileHandler.globals_file)
        res = {}
        if file_exists:
            f = open(FileHandler.globals_file, "r+")
            globs = f.read().split('\n')

            for g in globs:
                temp = g.split('=')
                if len(temp) == 2:
                    res[temp[0]] = temp[1]
        return res

    @staticmethod
    def update_global(global_name, new_val):
        """update a given global with the specified value"""
        current_globals = FileHandler.read_globals()
        if current_globals == {}:
            FileHandler.__write_global('{}={}\n'.format(global_name, new_val), 'a+')
        else:
            to_write = ''
            if global_name in current_globals:
                for key in current_globals:
                    if key == global_name:
                        to_write += '{}={}\n'.format(global_name, new_val)
                    else:
                        to_write += '{}={}\n'.format(key, current_globals[key])
                FileHandler.__write_global(to_write, 'w+')
            else:
                FileHandler.__write_global('{}={}\n'.format(global_name, new_val), 'a+')
