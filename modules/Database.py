import pyodbc


def GetDatabase(_Database):
    return Mysql() if _Database == 'MySql' else SqlServer('SQL Server', 'DESKTOP-33LB82J\HOSSAM', 'ATTENDENCE_SYSTEM')



class Mysql:
    pass


class SqlServer:

    def __init__(self, Driver, Server, Database):
        self.__Driver = Driver
        self.__Server = Server
        self.__Database = Database
    

    def Connect(self):
        self.__Connection = pyodbc.connect(
            'Driver={SQL Server};'
            'Server=DESKTOP-33LB82J\HOSSAM;'
            'Database=ATTENDENCE_SYSTEM;'
            'Trusted_Connection=yes;'
        )
    

    def Insert(self, query, *args):
        Cursor = self.__Connection.cursor()
        Cursor.execute(query, args)
        Cursor.commit()
    

    def Select(self, query, *args):
        Cursor = self.__Connection.cursor()
        Cursor.execute(query, args)
