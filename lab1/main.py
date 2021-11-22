from DAO import *
from DBLayer import *
from ORM import  *
from datetime import date
from os import path, makedirs, remove, system, name
from shutil import copy, copytree
from logo import get_logo


def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def commands(command, user_dao, file_dao):
    if command == "1":
        users = user_dao.all()
        if not users:
            print('[ОШИБКА]: Ничего не найдено!')
        else:
            for user in users:
                print(user)
    elif command == "2":
        try:
            user = user_dao.read(input("id = "))
        except:
            print('[ОШИБКА]: Ничего не найдено!')
            return None
        if not user:
            print('[ОШИБКА]: Ничего не найдено!')
        else:
            print(user)
            files = file_dao.get_all_by_owner(user._id)
            if not files:
                return None
            print(f'\nФайлы ({file_dao.get_count_by_id(user._id)}/20):')
            for file in files:
                print(file)
    elif command == "3":
        user = User(None, input("ФИО: "), input("Дата рождения: "), input("Должность: "), input("Номер телефона: "), input("Отдел: "))
        user_dao.create(user)
        print(user_dao.read(user._id))
    elif command == "4":
        id = input("id = ")
        if not id or int(id) not in range(1, int(user_dao.get_users_count())+1):
            print('[ОШИБКА]: Ничего не найдено!')
            return None
        print(user_dao.read(id))
        accessment = input("Вы уверены, что хотите удалить данного пользователя?\n1.Да\n2.Нет\n")
        if accessment == '1':
            user_dao.delete(id)
    elif command == "5":
        try:
            user = User(input("id: "), input("ФИО: "), input("Дата рождения: "), input("Должность: "), input("Номер телефона: "), input("Отдел: "))
        except:
            print('[ОШИБКА]: Ничего не найдено!')
            return None
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
        users = user_dao.search_by_name(input("Подстрока ФИО: "))
        if not users:
            print('[ОШИБКА]: Ничего не найдено!')
        else:
            for user in users:
                print(user)
    elif command == "8":
        users = user_dao.search_by_phone(input("Подстрока телефона: "))
        if not users:
            print('[ОШИБКА]: Ничего не найдено!')
        else:
            for user in users:
                print(user)
    elif command == "9":
        users = user_dao.search_by_department(input("Подстрока отдела: "))
        if not users:
            print('[ОШИБКА]: Ничего не найдено!')
        else:
            for user in users:
                print(user)
    elif command == "10":
        users = user_dao.search_by_pos(input("Подстрока должности: "))
        if not users:
            print('[ОШИБКА]: Ничего не найдено!')
        else:
            for user in users:
                print(user)
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
    elif command == "13":
        file = input("Абсолютный путь к файлу: ")
        try:
            allowed_format = ['jpeg', 'png', 'bmp', 'gif']
            new_file = File(None, path.split(file)[1], file.split('.')[-1], date.today(), path.getsize(file), None)
            if new_file.format not in allowed_format:
                print('[ОШИБКА] Недопустимый формат!')
                return None
            if new_file.size > 10485760:
                print('[ОШИБКА] Файл слишком велик!')
                return None
            new_file.owner = input("Владелец: ")
            if not new_file.owner or int(new_file.owner) > int(user_dao.get_users_count()):
                print('[ОШИБКА] Пользователь не найден')
                return None
            if int(file_dao.get_count_by_id(new_file.owner)) >= 20:
                print('[ОШИБКА] Лимит файлов для данного пользователя исчерпан')
                return None
            if path.isfile(path.join('uploads', new_file.owner, new_file.name)):
                print('[ОШИБКА] Файл с таким именем у этого пользователя уже существует!')
                return None
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
        try:
            file = file_dao.read(input('id = '))
        except:
            print('[ОШИБКА]: Ничего не найдено!')
            return None
        if not file:
            print("[ОШИБКА]: Ничего не найдено!")
            return None
        print(file)
        file.owner = file_dao.get_owner_id(file._id)
        print(file.owner)
        filepath = input('Абсолютный путь к папке выгрузки: ')
        if filepath:
            if not path.isdir(filepath):
                makedirs(filepath)
            try:
                copy(path.join('uploads', str(file.owner), str(file.name)), filepath)
            except FileNotFoundError:
                print(f'[ОШИБКА] Файл не найден { path.join("uploads", str(file.owner), str(file.name)) }')
                file_dao.delete(file._id)
    elif command == "15":
        file = file_dao.read(input('id = '))
        print(file)
        accessment = input("Вы уверены, что хотите удалить данный файл?\n1.Да\n2.Нет\n")
        if accessment == '1':
            file.owner = file_dao.get_owner_id(file._id)
            file_dao.delete(file._id)
            filepath = path.join('uploads', str(file.owner), str(file.name))
            if path.isfile(filepath):
                remove(filepath)
    elif command == "16":
        filepath = input('Абсолютный путь к папке выгрузки: ')
        if filepath:
            try:
                copytree('uploads', path.join(filepath, 'uploads'), dirs_exist_ok=True)
            except:
                print("[ОШИБКА]: Ничего не найдено!")
    elif command == "17":
        files = file_dao.search_by_format(input("Формат: "))
        if not files:
            print('[ОШИБКА]: Ничего не найдено!')
        else:
            for file in files:
                print(file)
    elif command == "18":
        print("Диапазон размера в байтах")
        files = file_dao.search_by_size(input("От: "), input("До: "))
        if not files:
            print('[ОШИБКА]: Ничего не найдено!')
        else:
            for file in files:
                print(file)
    elif command == "19":
        user_dao.db.close()
        return False
    else:
        print("Unknown command, try again")


def main():
    database = DBLayer(":memory:")
    user_dao = UserDao(database)
    file_dao = FileDAO(database)
    clear()
    print('Вас приветствует программа "Справочник"')
    input('Для продолжения нажмите Enter...')
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
    16. Выгрузить все файлы
    17. Поиск файлов по формату
    18. Поиск в диапазоне размера
    19. Выйти из программы"""
    while True:
        print(menu)
        command = input("Действие: ")
        result = commands(command, user_dao, file_dao)
        if result == False:
            break
        input('\nДля продолжения нажмите клавишу Enter...')


if __name__ == '__main__':
    main()
    clear()
    print('Спасибо, что воспользовались приложением "Справочник"!')
    print(get_logo())
    input('\nНажмите Enter для выхода из программы...')
