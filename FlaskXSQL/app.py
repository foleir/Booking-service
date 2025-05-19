from flask import Flask
from models import db
from operations import create_tables

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    create_tables()

if __name__ == '__main__':
    app.run(debug=True)