import MySQLConnector
import re

class User_Controller():

    def __init__(self):
        return

    def signin_handler(self,userName,password):
        
        psswdMatch = re.compile(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{8,}$')
        ispswdMatch = psswdMatch.match(password)

        userMatch = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{6,15}$')
        isnameMatch = userMatch.match(userName)
        ##send to MySQLConnector
        if(ispswdMatch is not None and isnameMatch is not None ):
            params= (userName,password)
            mysqlptr = MySQLConnector.MySQL_Connector()
            row = mysqlptr.ExecuteSP_Params('sp_get_user',params)
            if(len(row) == 0):
                return 404#user not found
            else: 
                 return row#OK
        else:
            return 100 #wrong password/username format
       
    def signup_handler(self,uname,pswdf,email,fname,lname,number,address,city,zipCode,comments):
        #validation
        #__reg exp__:
        ##pswd
        psswdMatch = re.compile(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{8,}$')
        ispswdMatch = psswdMatch.match(pswdf)
        if(ispswdMatch is  None ):
            return 'password' 
        ##email
        emailMatch = re.compile(r'(\b[\w.]+@+[\w.]+.+[\w.]\b)')
        isemailMatch = emailMatch.match(email)
        if(isemailMatch is  None ):
            return 'email' 
        ##userName
        userMatch = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{6,15}$')
        isnameMatch = userMatch.match(uname)
        if(isnameMatch is  None ):
            return 'user name' 
        #phone number
        phoneMatch = re.compile(r'(?=.*?\d){10}')
        isphoneMatch = phoneMatch.match(number)
        if(isphoneMatch is  None ):
            return 'phone number' 

        #insertion
        params= (str(uname),str(pswdf),str(email),str(fname),str(lname),str(address),str(city),str(number),str(zipCode),str(comments),2)
        mysqlptr = MySQLConnector.MySQL_Connector()
        id = mysqlptr.ExecuteSP_Params('sp_insert_user',params)
        return id
        
            
        