from DAO import *
from DBLayer import *
from ORM import  *
from datetime import date
from os import path
from os import makedirs
from os import environ
from os import remove
from shutil import copy
from time import sleep


def commands(command, user_dao, file_dao):
    if command == "3":
        user = User(None, input("ФИО: "), input("Дата рождения: "), input("Должность: "), input("Номер телефона: "), input("Отдел: "))
        user_dao.create(user)
        print(user_dao.read(user._id))
    elif command == "2":
        user = user_dao.read(input("id = "))
        if not user:
            print('[ОШИБКА]: Ничего не найдено!')
        else:
            print(user)
    elif command == "4":
        id = input("id = ")
        print(user_dao.read(id))
        accessment = input("Вы уверены, что хотите удалить данного пользователя?\n1.Да\n2.Нет: ")
        if accessment == '1':
            user_dao.delete(id)
    elif command == "1":
        users = user_dao.all()
        if not users:
            print('[ОШИБКА]: Ничего не найдено!')
        else:
            for user in users:
                print(user)
    elif command == "5":
        user = User(input("id: "), input("ФИО: "), input("Дата рождения: "), input("Должность: "), input("Номер телефона: "), input("Отдел: "))
        user = user_dao.update(user)
        print(user_dao.read(user._id))
    elif command == "6":
        positions = user_dao.get_positions()
        if not positions:
            print('[ОШИБКА]: Ничего не найдено!')
        else:
            for position in positions:
                print(position)
    elif command == "7":
        users = user_dao.search_by_name(input("Name: "))
        if not users:
            print('[ОШИБКА]: Ничего не найдено!')
        else:
            for user in users:
                print(user)
    elif command == "8":
        users = user_dao.search_by_phone(input("Phone: "))
        if not users:
            print('[ОШИБКА]: Ничего не найдено!')
        else:
            for user in users:
                print(user)
    elif command == "9":
        users = user_dao.search_by_department(input("Department: "))
        if not users:
            print('[ОШИБКА]: Ничего не найдено!')
        else:
            for user in users:
                print(user)
    elif command == "10":
        users = user_dao.search_by_pos(input("Position: "))
        if not users:
            print('[ОШИБКА]: Ничего не найдено!')
        else:
            for user in users:
                print(user)
    elif command == "13":
        file = input("Абсолютный путь к файлу: ")
        try:
            allowed_format = ['jpeg', 'png', 'bmp', 'gif']
            new_file = File(None, path.split(file)[1], file.split('.')[-1], date.today(), path.getsize(file), None)
            if new_file.size > 10485760:
                print('[ОШИБКА] Файл слишком велик!')
                return None
            if new_file.format not in allowed_format:
                print('[ОШИБКА] Недопустимый формат!')
                return None
            new_file.owner = input("Владелец: ")
            file_dao.create(new_file)
            try:
                copy(file, path.join('uploads', new_file.owner, new_file.name))
                print(file_dao.read(new_file._id))
            except FileNotFoundError:
                makedirs(path.join('uploads', new_file.owner))
                copy(file, path.join('uploads', new_file.owner, new_file.name))
        except FileNotFoundError:
            print('[ОШИБКА] Такого файла не существует!')
    elif command == "14":
        file = file_dao.read(input('id = '))
        print(file)
        file.owner = file_dao.get_owner_id(file._id)
        filepath = input('Абсолютный путь к папке выгрузки: ')
        if not path.isdir(filepath):
            makedirs(filepath)
        try:
            copy(path.join('uploads', str(file.owner), str(file.name)), filepath)
        except FileNotFoundError:
            print('[ОШИБКА] Файл не найден')
            file_dao.delete(file._id)
    elif command == "15":
        file = file_dao.read(input('id = '))
        print(file)
        accessment = input("Вы уверены, что хотите удалить данный файл?\n1.Да\n2.Нет:  ")
        if accessment == '1':
            file.owner = file_dao.get_owner_id(file._id)
            file_dao.delete(file._id)
            filepath = path.join('uploads', str(file.owner), str(file.name))
            if path.isfile(filepath):
                remove(filepath)
    elif command == "11":
        files = file_dao.all()
        if not files:
            print('[ОШИБКА]: Ничего не найдено!')
        else:
            for file in files:
                print(file)
    elif command == '12':
        file = file_dao.read(input("id = "))
        if not file:
            print('[ОШИБКА]: Ничего не найдено!')
        else:
            print(file)
    elif command == "16":
        user_dao.db.close()
        return False
    else:
        print("Unknown command, try again")

def main():
    database = DBLayer(":memory:")
    user_dao = UserDao(database)
    file_dao = FileDAO(database)
    menu = """Выберите действие:
    1. Просмотр всех пользователей
    2. Просмотр конкретного пользователя по id
    3. Создание пользователя
    4. Удаление пользователя
    5. Обновить всю информацию о конкретном пользователе
    6. Просмотр всех должностей
    7. Поиск пользователя по части ФИО
    8. Поиск пользователя по части телефона
    9. Поиск пользователя по части названия отдела
    10. Поиск пользователя по части дожности
    11. Просмотр всех файлов
    12. Просмотр конкретного файла по id
    13. Загрузка файла
    14. Выгрузка файла
    15. Удаление файла
    16. Выйти из программы"""
    while True:
        print(menu)
        command = input("Действие: ")
        result = commands(command, user_dao, file_dao)
        if result == False:
            break
        input('Для продолжения нажмите клавишу Enter...')

if __name__ == '__main__':
    main()
