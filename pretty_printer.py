class Printer:
    """
    Class to handler printing information

    ...

    more to come here

    """

    @staticmethod
    def pretty_print(headings, data):
        """Print out aliases and the directory they point to"""
        longest_alias = max(list(map(lambda t: len(t[0]), data))) + 5
        # print the headings
        for h in headings:
            print(h + ' '*(longest_alias-7), end='')
        print()
        # print('-' * len(self.headings[0]) + ' '*(self.longest_alias-7) + '-'*10)
        
        for x in data:
            print(x[0] + ' ' * (longest_alias - len(x[0])), end='')
            print(x[1])