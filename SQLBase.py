import pymysql.cursors
import configparser


class SqlBase(object):
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def addnew(self, query: str, parameters: list = []):
        return self.__execute(query, parameters).lastrowid

    def execute(self, query: str, parameters: list = []):
        return self.__execute(query, parameters).rowcount

    def select_all(self, query: str, parameters: list = []):
        cursor = self.__execute(query, parameters)
        return cursor.fetchall()

    def select_one(self, query: str, parameters: list = []):
        cursor = self.__execute(query, parameters)
        return cursor.fetchone()

    def select_count(self, query: str, parameters: list = []):
        cursor = self.__execute(query, parameters)
        if cursor is None:
            return -1
        else:
            return cursor.rowcount

    def __execute(self, query: str, parameters: list = []):
        try:
            with self.__openconnection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, parameters)
                    connection.commit()
                    return cursor
        except pymysql.Error as e:
            print(f"Error while executing query [{query}]: {str(e)}")

    def __openconnection(self):
        try:
            return pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database,
                                   cursorclass=pymysql.cursors.DictCursor)
        except pymysql.Error as e:
            print(f"Error while opening sql connection: {str(e)}")
