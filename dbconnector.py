import mysql.connector
from mysql.connector import Error

class DBConnector:

    """ 
    This class handles the communication with the MySQL database.
    Use: instantiate, connect(), execute your queries, disconnect()
    """

    def __init__(self):
        # Data about tables in DB
        self.table_name = "trademarks3"
        self.cols = '{}, {}, {}, {}, {}'.format("application_date",
                                                "application_lang_code",
                                                "second_lang_code",
                                                "mark_feature",
                                                "wordmark_spec")


    def connect(self):
        """ Connect to MySQL DB """

        try:
            self.conn = mysql.connector.connect(host='localhost',
                                            database='test1',
                                            user='root',
                                            password='root')
            if self.conn.is_connected():
                print('Connected')

        except Error as e:
            print(e)


    def disconnect(self):
        if self.conn:
            if self.conn.is_connected():
                self.conn.close()


    def select(self):
        """
        Prints last 5 rows from the trademarks table.
        For debugging.
        """
        try:
            if self.conn:
                if self.conn.is_connected():
                    cursor = self.conn.cursor()

                    cursor.execute("SELECT * FROM {} ORDER BY id desc "\
                                   "LIMIT 5 ;".format(self.table_name))
                
                    row = cursor.fetchone()

                    while row:
                        print(row)
                        row = cursor.fetchone()

        except Error as e:
            print(e)

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
            print(e)

        finally:
            cursor.close()


    def insert_many(self, trademarks):
        try:
            query = 'INSERT INTO {0}({1}) '\
                    'VALUES(%s, %s, %s, %s, %s) ;'.format(self.table_name, 
                                                          self.cols)

            cursor = self.conn.cursor()
            print("executemany("+query+")")
            cursor.executemany(query, trademarks)
            self.conn.commit()

        except Error as e:
            print(e)

        finally:
            cursor.close()

        
if __name__ == '__main__':
    ttm = ("al", "al", "sl", "mf", "mvet")

    connector = DBConnector()
    connector.connect()

    connector.insert_many(ttm)
    connector.select()

    connector.disconnect()
