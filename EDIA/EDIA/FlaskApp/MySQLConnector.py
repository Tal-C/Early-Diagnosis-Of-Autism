from mysql.connector import MySQLConnection, Error
from students_dbconfig import read_db_config

class MySQLConnector():

    def __init__(self):
        return
 
    def connectionToDB():
        dbconfig = read_db_config()

    def ExecuteSP(procedure_name,params):
        #   ##Time -  StopWatch - set timeout in init
        #con.query('SET GLOBAL connect_timeout=28800')
        #con.query('SET GLOBAL wait_timeout=28800')
        #con.query('SET GLOBAL interactive_timeout=28800')
        try:
            db_config = read_db_config()
            conn = MySQLConnection(**db_config)
            cursor = conn.cursor()
            #conn._connection_timeout
            #------------------------#
            i = 0
            for p in params:
                args[i] = p
                i += 1
            #------------------------#
            #args = params????????????
            #args = ['1236400967773', 0]
            result_args = cursor.callproc(procedure_name, args)
 
            return result_args
 
        except Error as e:
            print(e)
 
        finally:
            cursor.close()
            conn.close()

    def query_with_fetchone():
        print("Inside connect")
        dbconfig = read_db_config()
        try:
            print('Connecting to MySQL database...')
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")

            row = cursor.fetchone()
 
            while row is not None:
                print(row)
                row = cursor.fetchone()


            if conn.is_connected():
                print('connection established.')
            else:
                print('connection failed.')
 
        except Error as error:
            print(error)
 
        finally:
            conn.close()
            print('Connection closed.')


    if __name__ == '__main__':
        query_with_fetchone()
        query_with_fetchall()
        query_with_fetchmany()