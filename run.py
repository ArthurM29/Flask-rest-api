# uwsgi doesn't run app.py, so 'from db import db' won't run in __name__ == '__main__'

from app import app
from db import db

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()
