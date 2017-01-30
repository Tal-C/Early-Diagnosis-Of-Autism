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
        if(ispswdMatch is not None and isnameMatch is not None ):
            params= (userName,password)
            row = MySQLConnector.ExecuteSP_Params('sp_get_user',params)
        if(len(row) == 0):
            return -1
        else:
            return 100
        return 0
       