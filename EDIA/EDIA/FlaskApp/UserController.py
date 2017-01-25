from MySQLConnector import MySQLConnector

class UserController():

    def __init__(self):
        return

    def insert_user(username, password):
        query = "INSERT INTO tb_users(username,password) " \
            "VALUES(%s,%s)"
    args = (username, password)
 
    try:
        conn = MySQLConnection(**db_config)
 
        cursor = conn.cursor()
        cursor.execute(query, args)
 
        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')
 
        conn.commit()
    except Error as error:
        print(error)
 
    finally:
        cursor.close()
        conn.close()

    def login_page(userName,password):
        ##reg exp
        ##send to MySQLConnector
        params = (userName,password)
        row = MySQLConnector.ExecuteSPParams('sp_get_user',params)
        print("the beach is beautiful!")
        if(len(row) == 0):
            return -1
        return 0
       