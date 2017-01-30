class User():
    def __init__(self, row):
        self.user_name = row[1]
        self.password = row[2]
        self.email = row[3]
        self.first_name = row[4]
        self.last_name = row[5]
        self.address = row[6]
        self.city = row[7]
        self.phone = row[8]