import sqlite3
import os


class AliasDB:
    """
    Class to manage sqlite3 database
    """
    file_path = '/Users/hydenpolikoff/Code/projects/navi-cli/aliases.db'
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()

    @staticmethod
    def verify_table():
        AliasDB.cursor.execute('''
                    SELECT count(name) 
                    FROM sqlite_master 
                    WHERE type='table' AND name='nav_aliases'
                ''')
        if AliasDB.cursor.fetchone()[0] != 1:
            print('table doesn\'t exist, creating it now!')

            AliasDB.cursor.execute('''
            CREATE TABLE nav_aliases 
            (alias text PRIMARY KEY,
            directory text, 
            tag text DEFAULT NULL)
            ''')
            AliasDB.conn.commit()

    @staticmethod
    def insert(alias, cwd, tag=None):
        """
        Insert new alias into the table

        Returns
        -------
        False:
            alias already exists
        True:
            alias successfully inserted
        """
        AliasDB.verify_table()
        params = (alias, cwd, tag)

        # Try and insert new alias, catch if it's not unique
        try:
            AliasDB.conn.execute('''
                INSERT INTO nav_aliases (alias, directory, tag)
                VALUES (?, ?, ?)
                ''', params)
            AliasDB.conn.commit()
        except sqlite3.IntegrityError:
            print('That alias is already in use!')
            return False
        else:
            return True

    @staticmethod
    def delete(alias):
        """
        delete a given alias from the table

        Returns
        -------
        False:
            error executing query
        True:
            alias successfully delete
        """
        AliasDB.verify_table()
        try:
            AliasDB.conn.execute('''
                DELETE FROM nav_aliases 
                WHERE alias=?
                ''', (alias,))
            AliasDB.conn.commit()
        except:
            return False
        else:
            return True

    @staticmethod
    def update(old_alias, new_alias, cwd):
        AliasDB.verify_table()
        params = (cwd, new_alias, old_alias)
        try:
            AliasDB.conn.execute('''
                UPDATE nav_aliases 
                SET alias = ? ,
                    directory = ?
                WHERE alias = ?
                ''', params)
            AliasDB.conn.commit()
        except:
            return False
        else:
            return True

    @staticmethod
    def fetch_all():
        """
        fetch all the records from the table

        Returns
        -------
        query_res: list of records as tuples
        """
        AliasDB.verify_table()
        return AliasDB.conn.execute('''
            SELECT * FROM nav_aliases
            ''').fetchall()

    @staticmethod
    def search_cwd(cwd):
        """
        search for a directory in database

        Returns
        -------
        query: list of records as tuples
        """

        AliasDB.verify_table()
        params = (cwd,)
        return AliasDB.conn.execute('''
            SELECT * FROM nav_aliases
            WHERE directory = ?
            ''', params).fetchone()

    @staticmethod
    def search_alias(alias):
        """
        search for an alias in database

        Returns
        -------
        query: list of records as tuples
        """
        AliasDB.verify_table()
        params = (alias,)
        return AliasDB.conn.execute('''
            SELECT * FROM nav_aliases
            WHERE alias = ?
            ''', params).fetchall()