from MySQLConnector import MySQLConnector

class UserController():

    def __init__(self):
        return

    def login_page(userName,password):
        ##reg exp
        ##send to MySQLConnector
        params= (userName,password)
        row = MySQLConnector.ExecuteSP("sp_get_user",params)
        print("the beach is beautiful!")
        return row
       