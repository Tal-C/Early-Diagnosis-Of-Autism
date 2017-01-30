##from students_dbconfig import read_db_config
#import pymysql

#class MySQLConnector():

#    def __init__(self):
#        return

#    def ExecuteSPParams(stored_proc, params):
#        try:
#            print("Connecting to MySQL...")
#            cnx = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='Squ135vfe!@#', db='edoa')
#            curr = cnx.cursor()
#            print("Connection succeed...")
#            curr.callproc(stored_proc, params)
#            for i in range(0,len(curr._rows)):
#                print(curr._rows[i])    
#            return curr._rows
#        except:
#            print("Error at connection")

#        finally:
#            cnx.close()
#            print('Connection closed.')

#    def ExecuteSP(stored_proc):
#        try:
#            print("Connecting to MySQL...")
#            cnx = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='Squ135vfe!@#', db='edoa')
#            curr = cnx.cursor()
#            print("Connection succeed...")
#            curr.callproc(stored_proc)
#            for i in range(0,len(curr._rows)):
#                print(curr._rows[i])    
#            return curr._rows
#        except:
#            print("Error at connection")
#        finally:
#            cnx.close()
#            print('Connection closed.')

from students_dbconfig import read_db_config
import pymysql

class MySQLConnector():

    def __init__(self):
        return

   
    def ExecuteSP_Params(stored_proc,params):
        try:
            db_config = read_db_config()
            db_config = read_db_config()
            cnx = pymysql.connect(host=db_config['host'], port=int(db_config['port']),
                                  user=db_config['user'], passwd=db_config['password'], db=db_config['database'])
            curr = cnx.cursor()
            curr.callproc(stored_proc,params)
            for i in range(0,len(curr._rows)):
                print(curr._rows[i])    
            return curr._rows
        except:
            print("Error at connection")
            if(cnx == None):
                return None
        finally:
            cnx.close()
            

    def ExecuteSP(stored_proc):
        try:
            cnx = None
            db_config = read_db_config()
            cnx = pymysql.connect(host=db_config['host'], port=int(db_config['port']),
                                  user=db_config['user'], passwd=db_config['password'], db=db_config['database'])
            curr = cnx.cursor()
            curr.callproc(stored_proc)
            for i in range(0,len(curr._rows)):
                print(curr._rows[i])    
            return curr._rows
        except:
            print("Error at connection")
            if(cnx == None):
                return None
        finally:
            cnx.close()





