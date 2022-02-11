import os


class Printer:
    """
    Class to handler printing information

    ...

    more to come here

    """

    @staticmethod
    def pretty_print(headings, data, is_dir=False):
        """Print out aliases and the directory they point to"""
        longest_alias = max(list(map(lambda t: len(t[0]), data)))

        # manage edge case where all aliases are very short
        if longest_alias < len(headings[0]):
            longest_alias += (len(headings[0]) - longest_alias)

        # set the min distance between columns
        longest_alias += 3

        # print the headings
        for h in headings:
            print(h + ' ' * (longest_alias - len(headings[0])), end='')
        print()

        # print out all the entries without the home directory
        home = 0
        if is_dir:
            home = len(os.path.expanduser("~"))
        for x in data:
            print(x[0] + ' ' * (longest_alias - len(x[0])), end='')
            print(x[1][home:])
