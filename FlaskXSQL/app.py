# app.py
from flask import Flask
from models import db
from operations import create_tables, drop_tables
from database_setup import populate_database, test_database_operations

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:C0ck1ya@localhost:5432/Cnyak'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def initialize_database():
    with app.app_context():
        # Удаляем все таблицы
        drop_tables()
        print("Таблицы удалены")
        
        # Создаем таблицы с новой структурой
        create_tables()
        print("Таблицы созданы заново")
        
        # Заполняем данными
        populate_database()
        
        # Запускаем тесты
        test_database_operations()

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)