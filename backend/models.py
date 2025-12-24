# models وهمية
class User:
    def __init__(self, username, email, full_name, hashed_password, language="en"):
        self.username = username
        self.email = email
        self.full_name = full_name
        self.hashed_password = hashed_password
        self.language = language

# قاعدة بيانات وهمية في الذاكرة
fake_db = {"users": []}

# دالة get_db وهمية
class Session:
    def __init__(self):
        self.closed = False
    def close(self):
        self.closed = True
    def commit(self):
        pass
    def rollback(self):
        pass
db_instance = Session()

def get_db():
    return db_instance

models = type('Models', (), {'User': User})()
