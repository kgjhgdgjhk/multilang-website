# database.py - نسخة بدون SQLAlchemy

# قاعدة بيانات وهمية في الذاكرة
fake_db = {"users": []}


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
    yield db_instance

def init_db():
    pass

