# database.py - نسخة بدون SQLAlchemy

# قاعدة بيانات وهمية في الذاكرة
fake_db = {"users": []}

# Session وهمية لتوافق الـ Depends في FastAPI
class Session:
    def __init__(self):
        self.closed = False
    def close(self):
        self.closed = True
    def commit(self):
        pass
    def rollback(self):
        pass

# مثال على كائن واحد يستخدم في get_db
db_instance = Session()

# دالة get_db للتوافق مع Depends
def get_db():
    yield db_instance

# دالة init_db وهمية لتوافق main.py
def init_db():
    pass
