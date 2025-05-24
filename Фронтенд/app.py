# app.py
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, abort
from models import db
from operations import *
from security import *
from database_setup import populate_database, test_database_operations
from datetime import date

app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:C0ck1ya@localhost:5432/Cnyak'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Главная страница
# @app.route('/')
# def index():
#     bookings = []
#     booking_stats = []
#     equipment_stats = []
#     current_date = date.today()
#     if 'user_id' in session:
#         user = get_user_by_id(session['user_id'])
#         bookings = get_user_bookings(session['user_id'])
#         booking_stats = get_bookings_last_7_days()
#         equipment_stats = get_equipment_utilization_stats()  # Нужно реализовать эту функцию
        
#         return render_template('index.html', 
#                             user=user, 
#                             bookings=bookings,
#                             booking_stats=booking_stats,
#                             equipment_stats=equipment_stats,
#                             current_date=date.today())
#     return render_template('index.html')
# @app.route('/')
# def index():
#     bookings = []
#     booking_stats = []
#     equipment_stats = []
#     current_date = date.today()
    
#     if 'user_id' in session:
#         user = get_user_by_id(session['user_id'])
#         bookings = get_user_bookings(session['user_id'])
#         booking_stats = get_bookings_last_7_days()
#         equipment_stats = get_equipment_utilization_stats()
        
#         # Добавим логирование для отладки
#         print("Booking stats:", booking_stats)
#         print("Equipment stats:", equipment_stats)
        
#     return render_template('index.html', 
#                         user=user if 'user_id' in session else None, 
#                         bookings=bookings,
#                         booking_stats=booking_stats,
#                         equipment_stats=equipment_stats,
#                         current_date=current_date)
# @app.route('/')
# def index():
#     bookings = []
#     booking_stats = []
#     equipment_stats = []
#     current_date = date.today()
#     user = None
    
#     if 'user_id' in session:
#         user = get_user_by_id(session['user_id'])
#         bookings = get_user_bookings(session['user_id'])
        
#         # Получаем статистику
#         try:
#             booking_stats = get_bookings_last_7_days()
#             equipment_stats = get_equipment_utilization_stats()
#             print("Booking stats:", booking_stats)  # Для отладки
#             print("Equipment stats:", equipment_stats)  # Для отладки
#         except Exception as e:
#             print(f"Error getting stats: {str(e)}")
#             booking_stats = []
#             equipment_stats = []
    
#     return render_template('index.html', 
#                         user=user, 
#                         bookings=bookings,
#                         booking_stats=booking_stats,
#                         equipment_stats=equipment_stats,
#                         current_date=current_date)

@app.route('/')
def index():
    bookings = []
    booking_stats = []
    equipment_stats = []
    current_date = date.today()
    user = None

    if 'user_id' in session:
        user = get_user_by_id(session['user_id'])
        bookings = get_user_bookings(session['user_id'])

        try:
            booking_stats = get_bookings_last_7_days()
            equipment_stats = get_equipment_utilization_stats()
        except Exception as e:
            print(f"Ошибка при получении статистики: {e}")
            booking_stats = []
            equipment_stats = []

    return render_template('index.html',
                           user=user,
                           bookings=bookings,
                           booking_stats=booking_stats,
                           equipment_stats=equipment_stats,
                           current_date=current_date)


# Страница категорий
@app.route('/categories')
def categories():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('categories.html')

# Страница оборудования по категориям
@app.route('/equipment/<category>')
def equipment(category):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    equipments = get_equipment_by_category(category)
    return render_template(f'{category}.html', equipments=equipments)

# Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = authenticate_user(username, password)  # Проверка хеша
        
        if user:
            session['user_id'] = user.user_id
            return redirect(url_for('personal_account'))
        
        return render_template('login.html', error='Неверные данные')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Получаем данные из формы
        username = request.form.get('username')
        password = request.form.get('password')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        role = request.form.get('role')
        
        # Валидация обязательных полей
        if not all([username, password, firstname, lastname, role]):
            return render_template('registration.html', error='Все поля обязательны для заполнения')
        
        # Проверка существования пользователя
        if get_user_by_login(username):
            return render_template('registration.html', error='Логин занят')
        
        # Маппинг ролей
        role_mapping = {
            'student': 'Студент',
            'teacher': 'Преподаватель',
            'unknown': 'Администратор'  # Изменил 'unknown' на 'admin' для ясности
        }
        
        # Проверка валидности роли
        if role not in role_mapping:
            return render_template('registration.html', error='Неверный тип пользователя')
        
        user_role = role_mapping[role]
        
        try:
            # Создаем пользователя с хешированным паролем
            create_user(username, password, firstname, lastname, user_role)
            return redirect(url_for('login'))
            
        except Exception as e:
            return render_template('registration.html', error='Произошла ошибка при регистрации')
    
    # GET-запрос - отображаем форму регистрации
    return render_template('registration.html')

# Личный кабинет
@app.route('/account', methods=['GET', 'POST'])
def personal_account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = get_user_by_id(session['user_id'])
    bookings = get_user_bookings(session['user_id'])
    favorites = get_user_favorites(session['user_id'])
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            # Обновляем только те поля, которые были переданы
            if 'username' in data:
                user.user_login = data['username']
            if 'firstname' in data:
                user.user_name = data['firstname']
            if 'lastname' in data:
                user.user_surname = data['lastname']
            
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Профиль обновлен'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400
    
    return render_template('personal_account.html', 
                         user=user, 
                         bookings=bookings,
                         favorites=favorites,
                         current_date=date.today())
# Управление избранным
# @app.route('/favorites', methods=['POST'])
# def manage_favorites():
#     if 'user_id' not in session:
#         return jsonify({'status': 'error', 'message': 'Не авторизован'})
    
#     data = request.get_json()
#     equipment_id = data.get('equipment_id')
#     action = data.get('action')
    
#     if action == 'add':
#         add_to_favorites(session['user_id'], equipment_id)
#         return jsonify({'status': 'success', 'message': 'Добавлено в избранное'})
#     elif action == 'remove':
#         remove_from_favorites(session['user_id'], equipment_id)
#         return jsonify({'status': 'success', 'message': 'Удалено из избранного'})
    
#     return jsonify({'status': 'error', 'message': 'Неизвестное действие'})
@app.route('/api/check-favorite')
def check_favorite():
    if 'user_id' not in session:
        return jsonify({'is_favorite': False})
    
    user_id = request.args.get('user_id')
    equipment_id = request.args.get('equipment_id')
    
    favorite = Favorites.query.filter_by(
        user_id=user_id,
        object_id=equipment_id
    ).first()
    
    return jsonify({'is_favorite': favorite is not None})

@app.route('/manage_favorites', methods=['POST'])
def manage_favorites():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Не авторизован'})
    
    data = request.get_json()
    equipment_id = data.get('equipment_id')
    action = data.get('action')
    user_id = session['user_id']
    
    try:
        if action == 'add':
            # Проверяем, нет ли уже в избранном
            existing = Favorites.query.filter_by(
                user_id=user_id,
                object_id=equipment_id
            ).first()
            
            if not existing:
                favorite = Favorites(
                    user_id=user_id,
                    object_id=equipment_id
                )
                db.session.add(favorite)
                db.session.commit()
                
        elif action == 'remove':
            Favorites.query.filter_by(
                user_id=user_id,
                object_id=equipment_id
            ).delete()
            db.session.commit()
            
        return jsonify({'status': 'success'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)})

# Бронирование оборудования
@app.route('/book', methods=['POST'])
def book_equipment():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Не авторизован'})
    
    try:
        data = request.get_json()
        equipment_id = data.get('equipment_id')
        room_id = data.get('room_id')
        date_str = data.get('date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        
        booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        start_datetime = datetime.strptime(f"{date_str} {start_time}", '%Y-%m-%d %H:%M')
        end_datetime = datetime.strptime(f"{date_str} {end_time}", '%Y-%m-%d %H:%M')
        
        if not check_availability(equipment_id, room_id, booking_date, start_datetime, end_datetime):
            return jsonify({'status': 'error', 'message': 'Оборудование уже занято в это время'})
        
        create_occupancy(equipment_id, session['user_id'], room_id, booking_date, start_datetime, end_datetime)
        create_booking(equipment_id, session['user_id'], room_id, booking_date)
        
        return jsonify({'status': 'success', 'message': 'Бронирование создано'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    



@app.route('/cancel_booking', methods=['POST'])
def cancel_booking():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Не авторизован'})
    
    data = request.get_json()
    booking_id = data.get('booking_id')
    
    try:
        # Находим бронирование
        booking = BookHistory.query.get(booking_id)
        
        if not booking:
            return jsonify({'status': 'error', 'message': 'Бронирование не найдено'})
        
        # Проверяем, что бронирование принадлежит текущему пользователю
        if booking.user_id != session['user_id']:
            return jsonify({'status': 'error', 'message': 'Нельзя отменить чужое бронирование'})
        
        # Удаляем связанные записи о занятости
        Occupancy.query.filter_by(
            object_id=booking.object_id,
            user_id=booking.user_id,
            room_id=booking.room_id,
            dataa=booking.data_book
        ).delete()
        
        # Удаляем само бронирование
        db.session.delete(booking)
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': 'Бронирование отменено'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)})



# Получение доступных комнат
@app.route('/available_rooms', methods=['GET'])
def available_rooms():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Не авторизован'})
    
    date_str = request.args.get('date')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    
    try:
        booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        start_datetime = datetime.strptime(f"{date_str} {start_time}", '%Y-%m-%d %H:%M')
        end_datetime = datetime.strptime(f"{date_str} {end_time}", '%Y-%m-%d %H:%M')
        
        rooms = get_available_rooms(booking_date, start_datetime, end_datetime)
        rooms_data = [{'room_id': room.room_id, 'room_name': room.room_name} for room in rooms]
        
        return jsonify({'status': 'success', 'rooms': rooms_data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    

@app.route('/equipment') #Херня для фильтров
def equipment_list():
    # Получаем уникальные серии оборудования из базы данных
    series = db.session.query(Equipment.object_series.distinct()).all()
    equipment_series = [s[0] for s in series if s[0]]  # Преобразуем результат
    
    # Получаем уникальные локации (пример - можно адаптировать под вашу структуру)
    locations = db.session.query(Rooms.room_name.distinct()).all()
    equipment_locations = [l[0] for l in locations if l[0]]
    
    return render_template('equipment.html',
                        equipment_series=equipment_series,
                        equipment_locations=equipment_locations)


# Добавьте этот маршрут в app.py
# @app.route('/equipment/<int:equipment_id>')
# def equipment_detail(equipment_id):
#     if 'user_id' not in session:
#         return redirect(url_for('login'))
    
#     equipment = get_equipment_by_id(equipment_id)
#     if not equipment:
#         abort(404)
    
#     # Добавляем информацию о доступности
#     equipment.is_available = check_equipment_availability(equipment_id)
#     equipment.bookings = get_equipment_bookings(equipment_id)
#     equipment.reviews = get_equipment_reviews(equipment_id)
    
#     return render_template('object.html', equipment=equipment)



@app.route('/booking/<int:equipment_id>')
def booking_settings(equipment_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    equipment = get_equipment_by_id(equipment_id)
    if not equipment:
        abort(404)
    
    rooms = get_all_rooms()
    return render_template('settings.html', equipment=equipment, rooms=rooms)

# @app.route('/equipment/details/<int:equipment_id>')
# def equipment_details(equipment_id):
#     if 'user_id' not in session:
#         return redirect(url_for('login'))
    
#     equipment = get_equipment_by_id(equipment_id)
#     if not equipment:
#         abort(404)
    
#     # Получаем информацию о бронированиях и отзывах
#     bookings = get_equipment_bookings(equipment_id)
#     reviews = get_equipment_reviews(equipment_id)
    
#     # Получаем данные пользователей для каждого отзыва
#     reviews_with_users = []
#     for review in reviews:
#         user = get_user_by_id(review.user_id)
#         reviews_with_users.append({
#             'review': review,
#             'user': user
#         })
    
    # return render_template('object.html', 
    #                      equipment=equipment,
    #                      bookings=bookings,
    #                      reviews_with_users=reviews_with_users)

@app.route('/equipment/details/<int:equipment_id>')
def equipment_details(equipment_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    equipment = get_equipment_by_id(equipment_id)
    if not equipment:
        abort(404)
    
    # Получаем текущие бронирования оборудования
    now = datetime.now()
    active_bookings = Occupancy.query.filter(
        Occupancy.object_id == equipment_id,
        Occupancy.time_end >= now
    ).order_by(Occupancy.time_start).all()
    
    # Проверяем доступность оборудования
    is_available = True
    current_booking = None
    for booking in active_bookings:
        if booking.time_start <= now <= booking.time_end:
            is_available = False
            current_booking = booking
            break
    
    # Получаем отзывы с данными пользователей
    reviews = get_equipment_reviews(equipment_id)
    reviews_with_users = []
    for review in reviews:
        user = get_user_by_id(review.user_id)
        reviews_with_users.append({
            'review': review,
            'user': user
        })
    
    return render_template('object.html',
                         equipment=equipment,
                         is_available=is_available,
                         current_booking=current_booking,
                         reviews_with_users=reviews_with_users)

@app.route('/object/<int:equipment_id>/review', methods=['GET', 'POST'])
def review(equipment_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    equipment = get_equipment_by_id(equipment_id)
    if not equipment:
        abort(404)
    
    if request.method == 'POST':
        review_text = request.form.get('review_text')
        if review_text:
            # Сохраняем отзыв в базу данных
            create_review(equipment_id, session['user_id'], review_text)
            return redirect(url_for('equipment_details', equipment_id=equipment_id))
    
    return render_template('review.html', equipment=equipment)

# Вспомогательные функции
def get_equipment_bookings(equipment_id, limit=5):
    """Получить последние бронирования оборудования"""
    return BookHistory.query.filter_by(object_id=equipment_id)\
                           .order_by(BookHistory.data_book.desc())\
                           .limit(limit)\
                           .all()

def get_equipment_reviews(equipment_id):
    """Получить отзывы об оборудовании"""
    return Revievs.query.filter_by(object_id=equipment_id)\
                       .order_by(Revievs.riviev_id.desc())\
                       .all()

def check_equipment_availability(equipment_id):
    """Проверить доступность оборудования"""
    now = datetime.now()
    active_booking = Occupancy.query.filter(
        Occupancy.object_id == equipment_id,
        Occupancy.time_start <= now,
        Occupancy.time_end >= now
    ).first()
    return active_booking is None

def get_equipment_by_id(equipment_id):
    """Получить оборудование по ID"""
    return Equipment.query.get(equipment_id)


# Общий вариант
@app.route('/category/<category>')
def show_category(category):
    equipments = get_equipment_by_category(category)
    template_map = {
        'computers': 'computers.html',
        'input_devices': 'input_devices.html',
        'output_devices' : 'output_devices.html',
        'storage_devices' : 'storage_devices.html',
        'network_equipment' : 'network_equipment.html',
        'media' : 'media.html',
        'printers_scanners' : 'printers_scanners.html',
        'routers_modems' : 'routers_modems.html',
        'monitors' : 'monitors.html',
        'accessories' : 'accessories.html',
        'cables_adapters' : 'cables_adapters.html'
        # добавить другие категории
    }

    return render_template(template_map.get(category, '404.html'), equipments=equipments)



@app.route('/computers')
def computers():
    # Получаем оборудование категории "компьютеры"
    equipments = get_equipment_by_category('computer')
    rooms = get_all_rooms()
    
    # Добавляем информацию о доступности
    for eq in equipments:
        eq.is_available = check_equipment_availability(eq.object_id)
    
    # Получаем уникальные серии и локации
    series = list({eq.object_series for eq in equipments if eq.object_series})
    locations = list({room.room_name for room in rooms if room.room_name})
    
    return render_template('computers.html',
                         equipments=equipments,
                         equipment_series=series,
                         equipment_locations=locations)

# Обновленные маршруты для всех категорий (добавляем получение серий и локаций)

@app.route('/input_devices')
def input_devices():
    equipments = get_equipment_by_category('input')
    rooms = get_all_rooms()
    series = list({eq.object_series for eq in equipments if eq.object_series})
    locations = list({room.room_name for room in rooms if room.room_name})
    
    for eq in equipments:
        eq.is_available = check_equipment_availability(eq.object_id)
    
    return render_template('input_devices.html',
                         equipments=equipments,
                         equipment_series=series,
                         equipment_locations=locations)

@app.route('/output_devices')
def output_devices():
    equipments = get_equipment_by_category('output')
    rooms = get_all_rooms()
    series = list({eq.object_series for eq in equipments if eq.object_series})
    locations = list({room.room_name for room in rooms if room.room_name})
    
    for eq in equipments:
        eq.is_available = check_equipment_availability(eq.object_id)
    
    return render_template('output_devices.html',
                         equipments=equipments,
                         equipment_series=series,
                         equipment_locations=locations)

@app.route('/storage_devices')
def storage_devices():
    equipments = get_equipment_by_category('storage')
    rooms = get_all_rooms()
    series = list({eq.object_series for eq in equipments if eq.object_series})
    locations = list({room.room_name for room in rooms if room.room_name})
    
    for eq in equipments:
        eq.is_available = check_equipment_availability(eq.object_id)
    
    return render_template('storage_devices.html',
                         equipments=equipments,
                         equipment_series=series,
                         equipment_locations=locations)

@app.route('/network_equipment')
def network_equipment():
    equipments = get_equipment_by_category('network')
    rooms = get_all_rooms()
    series = list({eq.object_series for eq in equipments if eq.object_series})
    locations = list({room.room_name for room in rooms if room.room_name})
    
    for eq in equipments:
        eq.is_available = check_equipment_availability(eq.object_id)
    
    return render_template('network_equipment.html',
                         equipments=equipments,
                         equipment_series=series,
                         equipment_locations=locations)

@app.route('/media')
def media():
    equipments = get_equipment_by_category('media')
    rooms = get_all_rooms()
    series = list({eq.object_series for eq in equipments if eq.object_series})
    locations = list({room.room_name for room in rooms if room.room_name})
    
    for eq in equipments:
        eq.is_available = check_equipment_availability(eq.object_id)
    
    return render_template('media.html',
                         equipments=equipments,
                         equipment_series=series,
                         equipment_locations=locations)

@app.route('/printers_scanners')
def printers_scanners():
    equipments = get_equipment_by_category('printers')
    rooms = get_all_rooms()
    series = list({eq.object_series for eq in equipments if eq.object_series})
    locations = list({room.room_name for room in rooms if room.room_name})
    
    for eq in equipments:
        eq.is_available = check_equipment_availability(eq.object_id)
    
    return render_template('printers_scanners.html',
                         equipments=equipments,
                         equipment_series=series,
                         equipment_locations=locations)

@app.route('/routers_modems')
def routers_modems():
    equipments = get_equipment_by_category('routers')
    rooms = get_all_rooms()
    series = list({eq.object_series for eq in equipments if eq.object_series})
    locations = list({room.room_name for room in rooms if room.room_name})
    
    for eq in equipments:
        eq.is_available = check_equipment_availability(eq.object_id)
    
    return render_template('routers_modems.html',
                         equipments=equipments,
                         equipment_series=series,
                         equipment_locations=locations)

@app.route('/monitors')
def monitors():
    equipments = get_equipment_by_category('monitors')
    rooms = get_all_rooms()
    series = list({eq.object_series for eq in equipments if eq.object_series})
    locations = list({room.room_name for room in rooms if room.room_name})
    
    for eq in equipments:
        eq.is_available = check_equipment_availability(eq.object_id)
    
    return render_template('monitors.html',
                         equipments=equipments,
                         equipment_series=series,
                         equipment_locations=locations)

@app.route('/accessories')
def accessories():
    equipments = get_equipment_by_category('accessories')
    rooms = get_all_rooms()
    series = list({eq.object_series for eq in equipments if eq.object_series})
    locations = list({room.room_name for room in rooms if room.room_name})
    
    for eq in equipments:
        eq.is_available = check_equipment_availability(eq.object_id)
    
    return render_template('accessories.html',
                         equipments=equipments,
                         equipment_series=series,
                         equipment_locations=locations)

@app.route('/cables_adapters')
def cables_adapters():
    equipments = get_equipment_by_category('cables')
    rooms = get_all_rooms()
    series = list({eq.object_series for eq in equipments if eq.object_series})
    locations = list({room.room_name for room in rooms if room.room_name})
    
    for eq in equipments:
        eq.is_available = check_equipment_availability(eq.object_id)
    
    return render_template('cables_adapters.html',
                         equipments=equipments,
                         equipment_series=series,
                         equipment_locations=locations)

# Выход
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def initialize_database():
    with app.app_context():
        drop_tables()
        create_tables()
        populate_database()
        # test_database_operations()

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)