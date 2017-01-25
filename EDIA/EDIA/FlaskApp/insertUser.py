from MySQLConnector import MySQLConnection, Error
 
def insert_user(username, password):
    query = "INSERT INTO tb_users(username,password) " \
            "VALUES(%s,%s)"
    args = (username, password)
 
    try:
        db_config = read_db_config()
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