from MySQLConnector import MySQLConnector

class UserController():

    def __init__(self):
        return

    def login_page(userName,password):
        ##reg exp
        ##send to MySQLConnector
        params= (userName,password)
        row = MySQLConnector.ExecuteSPParams('sp_get_user',params)
        print("the beach is beautiful!")
        if(len(row) == 0):
            return -1
        return 0
       