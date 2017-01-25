#from students_dbconfig import read_db_config

import pymysql


class MySQLConnector():

    def __init__(self):
        return

    def ExecuteAddUserParams(params):
        try:
            print("Connecting to MySQL...")
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='Squ135vfe!@#', db='edoa')
            cursor = conn.cursor()
            print("Connection succeed...")

            cursor.execute("select distinct edoa from tb_users order by 1")
            print("Tal Sratim")
            
        except:
            print("Error at connection")

        finally:
            conn.commit()
            conn.close()
            print('Connection closed.')

    def ExecuteSPParams(stored_proc, params):
        try:
            print("Connecting to MySQL...")
            cnx = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='Squ135vfe!@#', db='edoa')
            curr = cnx.cursor()
            print("Connection succeed...")
            curr.callproc(stored_proc, params)
            for i in range(0,len(curr._rows)):
                print(curr._rows[i])    
            return curr._rows
        except:
            print("Error at connection")

        finally:
            cnx.close()
            print('Connection closed.')

    def ExecuteSP(stored_proc):
        try:
            print("Connecting to MySQL...")
            cnx = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='Squ135vfe!@#', db='edoa')
            curr = cnx.cursor()
            print("Connection succeed...")
            curr.callproc(stored_proc)
            for i in range(0,len(curr._rows)):
                print(curr._rows[i])    
            return curr._rows
        except:
            print("Error at connection")
        finally:
            cnx.close()
            print('Connection closed.')





