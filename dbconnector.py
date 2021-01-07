import mysql.connector
from mysql.connector import Error, DataError

class DBConnector:

    """ 
    This class handles the communication with the MySQL database.
    Use: instantiate, connect(), execute your queries, disconnect()
    """

    def __init__(self):
        # Data about tables in DB
        self.table_name = "trademarks"
        self.cols = '{}, {}, {}, {}, {}'.format("application_date",
                                                "application_lang_code",
                                                "second_lang_code",
                                                "mark_feature",
                                                "mark_verb_ele_text")

    def connect(self):
        """ Connect to MySQL DB """
        try:
            print("Trying to connect to database", flush=True)

            self.conn = mysql.connector.connect(host='db',
                                            database='db',
                                            user='user',
                                            password='password')
            print("Connected to database", flush=True)
            return True

        except Error as e:
            print(e, flush=True)

    def disconnect(self):
        if self.conn:
            if self.conn.is_connected():
                self.conn.close()

    def select(self):
        """
        Returns last 5 rows from the trademarks table.
        For debugging.
        """
        try:
            if self.conn:
                if self.conn.is_connected():
                    cursor = self.conn.cursor()

                    cursor.execute("SELECT * FROM {} ORDER BY id desc "\
                                   "LIMIT 5 ;".format(self.table_name))
                
                    result = []

                    row = cursor.fetchone()
                    while row:
                        result.append(row)
                        row = cursor.fetchone()

                    return result

        except Error as e:
            print(e, flush=True)

        finally:
            cursor.close()

    def select_where(self, trademark, case_sensitive=True):
        """ 
        Returns a list of rows where 'mark_verb_ele_text' matches the trademark 
        parameter.
        Case sensitive if case_sensitive is True. Exact match apart from that.
        """
        try:
            if self.conn:
                if self.conn.is_connected():
                    cursor = self.conn.cursor()

                    if case_sensitive:
                        query = 'SELECT * FROM {} WHERE mark_verb_ele_text'\
                                'LIKE BINARY "{}" ;'\
                                .format(self.table_name, trademark)
                    else:
                        query = 'SELECT * FROM {} WHERE mark_verb_ele_text'\
                                'LIKE "{}" ;'\
                                .format(self.table_name, trademark)

                    cursor.execute(query)

                    result = []

                    row = cursor.fetchone()
                    while row:
                        result.append(row)
                        row = cursor.fetchone()

                    return result

        except Error as e:
            print(e, flush=True)

        finally:
            cursor.close()
    
    def insert_one(self, trademark):
        try:
            query = 'INSERT INTO {0}({1}) '\
                    'VALUES(%s, %s, %s, %s, %s) ;'.format(self.table_name, 
                                                          self.cols)

            cursor = self.conn.cursor()
            cursor.execute(query, trademark)
            self.conn.commit()

        except Error as e:
            print(e, flush=True)

        finally:
            cursor.close()

    def insert_many(self, trademarks):
        try:
            query = 'INSERT INTO {0}({1}) '\
                    'VALUES(%s, %s, %s, %s, %s) ;'.format(self.table_name, 
                                                          self.cols)

            cursor = self.conn.cursor()
            cursor.executemany(query, trademarks)
            self.conn.commit()

        except DataError as e:
            print(e, flush=True)
            print("Query: {}".format(query), flush=True)
            print("Trademarks: {}".format(trademarks), flush=True)
        except Error as e:
            print(e, flush=True)

        finally:
            cursor.close()

        
if __name__ == '__main__':
    ttm = ("al", "al", "sl", "mf", "mvet")

    connector = DBConnector()
    connector.connect()

    #connector.insert_one(ttm)
    for r in connector.select():
        print(r, flush=True)

    connector.disconnect()
