#from MySQLConnector import MySQLConnector

#class UserController():

#    def __init__(self):
#        return

#    def insert_user(username, password):
#        query = "INSERT INTO tb_users(username,password) " \
#            "VALUES(%s,%s)"
#        args = (username, password)
 
#        try:
#            conn = MySQLConnection(**db_config)
 
#            cursor = conn.cursor()
#            cursor.execute(query, args)
 
#            if cursor.lastrowid:
#                print('last insert id', cursor.lastrowid)
#            else:
#                print('last insert id not found')
 
#            conn.commit()
#    #except Error as error:
#            print(error)
 
#        finally:
#            cursor.close()
#            conn.close()

#    def login_page(userName,password):
#        ##reg exp
#        ##send to MySQLConnector
#        params = (userName,password)
#        row = MySQLConnector.ExecuteSPParams('sp_get_user',params)
#        print("the beach is beautiful!")
#        if(len(row) == 0):
#            return -1
#        return 0

from MySQLConnector import MySQLConnector
import re

class UserController():

    def __init__(self):
        return

    def login_page(userName,password):
        ##reg exp
        psswdMatch = re.compile(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{8,}$')
        ispswdMatch = psswdMatch.match(password)

        userMatch = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{6,15}$')
        isnameMatch = userMatch.match(userName)
        ##send to MySQLConnector
        if(ispswdMatch is not None and isnameMatch is not None):
            params = (userName,password)
            row = MySQLConnector.ExecuteSP_Params('sp_get_user',params)
            if(len(row) == 0):
                return -1
        else:
            return 100
        return 0
       