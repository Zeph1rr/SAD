from UserDAOImpl import *
from DBLayer import *
from User import  *


def main():
    database = DBLayer(":memory:")
    user_dao = DAO(database)
    while True:
        command = input("command: ")
        if command == "create":
            user = User(None, input("ФИО: "), input("Дата рождения: "), input("Должность: "), input("Номер телефона: "), input("Отдел: "))
            user_dao.create(user)
            print(user_dao.read(user._id))
        elif command == "read":
            user = user_dao.read(input("id = "))
            if not user:
                print('[ERROR]: User not found!')
            else:
                print(user)
        elif command == "delete":
            id = input("id = ")
            print(user_dao.read(id))
            accessment = input("Are yoy sure to want delete this user? (y/n): ")
            if accessment == 'y':
                user_dao.delete(id)
        elif command == "all":
            users = user_dao.all()
            if not users:
                print('[ERROR]: There are no users in the database!')
            else:
                for user in users:
                    print(user)
        elif command == "update":
            user = User(input("id: "), input("ФИО: "), input("Дата рождения: "), input("Должность: "), input("Номер телефона: "), input("Отдел: "))
            user = user_dao.update(user)
            print(user_dao.read(user._id))
        elif command == "positions":
            positions = user_dao.get_positions()
            if not positions:
                print('[ERROR]: There are no users in the database!')
            else:
                for position in positions:
                    print(position)
        elif command == "name":
            users = user_dao.search_by_name(input("Name: "))
            if not users:
                print('[ERROR]: There are no users in the database!')
            else:
                for user in users:
                    print(user)
        elif command == "phone":
            users = user_dao.search_by_phone(input("Phone: "))
            if not users:
                print('[ERROR]: There are no users in the database!')
            else:
                for user in users:
                    print(user)
        elif command == "department":
            users = user_dao.search_by_department(input("Department: "))
            if not users:
                print('[ERROR]: There are no users in the database!')
            else:
                for user in users:
                    print(user)
        elif command == "position":
            users = user_dao.search_by_pos(input("Position: "))
            if not users:
                print('[ERROR]: There are no users in the database!')
            else:
                for user in users:
                    print(user)
        elif command == "exit":
            user_dao.db.close()
            break
        else:
            print("Unknown command, try again")

if __name__ == '__main__':
    main()