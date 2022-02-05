import sqlite3
from pathlib import Path
import os


class Alias_DB():
    """
    Class to manage sqlite3 database

    ...

    Attributes
    ----------
    conn : obj
        database connection
    cursor : obj
        database cursor

    Methods
    -------
    """

    def __init__(self):

        self.file_path = '/Users/hydenpolikoff/Code/projects/navi-cli/aliases.db'
        self.conn = sqlite3.connect(self.file_path)
        self.cursor = self.conn.cursor()

        # check if the table exists
        self.cursor.execute('''
            SELECT count(name) 
            FROM sqlite_master 
            WHERE type='table' AND name='nav_aliases'
        ''')

        # create the table if it doesn't exist
        if self.cursor.fetchone()[0] != 1:
            print('table doesn\'t exist, creating it now!')

            self.cursor.execute('''
            CREATE TABLE nav_aliases 
            (alias text PRIMARY KEY,
            directory text, 
            tag text DEFAULT NULL)
            ''')
            self.conn.commit()

    # try to insert a certain alias
    def insert(self, alias, cwd, tag=None):
        """
        Insert new alias into the table

        Returns
        -------
        False:
            alias already exists
        True:
            alias successfully inserted
        """
        params = (alias, cwd, tag)

        # Try and insert new alias, catch if it's not unique
        try:
            self.conn.execute('''
                INSERT INTO nav_aliases (alias, directory, tag)
                VALUES (?, ?, ?)
                ''', params)
            self.conn.commit()
        except sqlite3.IntegrityError:
            print('That alias is already in use!')
            return False
        else:
            return True

    def delete(self, alias):
        """
        delete a given alias from the table

        Returns
        -------
        False:
            error executing query
        True:
            alias successfully delete
        """
        try:
            self.conn.execute('''
                DELETE FROM nav_aliases 
                WHERE alias=?
                ''',
                              (alias,))
            self.conn.commit()
        except e:
            print(e)
            return False
        else:
            return True

    def update(self, old_alias, new_alias, cwd):
        params = (cwd, new_alias, old_alias)
        try:
            self.conn.execute('''
                UPDATE nav_aliases 
                SET alias = ? ,
                    directory = ?
                WHERE alias = ?
                ''', params)
            self.conn.commit()
        except e:
            print(e)
            return False
        else:
            return True

    def fetch_all(self):
        """
        fetch all the records from the table

        Returns
        -------
        query_res: list of records as tuples
        """
        return self.conn.execute('''
            SELECT * FROM nav_aliases
            ''').fetchall()

    def search_cwd(self, cwd):
        """
        search for a directory in database

        Returns
        -------
        query: list of records as tuples
        """
        params = (cwd,)
        return self.conn.execute('''
            SELECT * FROM nav_aliases
            WHERE directory = ?
            ''', params).fetchone()

    def search_alias(self, alias):
        """
        search for an alias in database

        Returns
        -------
        query: list of records as tuples
        """
        params = (alias,)
        return self.conn.execute('''
            SELECT * FROM nav_aliases
            WHERE alias = ?
            ''', params).fetchall()


# if __name__ == '__main__':
#     db = Alias_DB()
#     # db.insert("dev", 'test')
#     db.insert("eeee", "/Users/hydenpolikoff", 'test_tag')
#     # db.insert("yuu", "/Users/hydenpolikoff")
#     # db.search_cwd('home')
#
#     print(db.fetch_all())
#     db.delete("home")
#
#     print(db.fetch_all())
    # heads = ['Aliases', 'Directory']
    # test = [('home', '/Users/hydenpolikoff', 'test_tag'), ('devvv', '/Users/hydenpolikoff/Code/projects/navi-cli', None)]

    # pp = Printer(heads, test)
    # pp.pretty_print()
