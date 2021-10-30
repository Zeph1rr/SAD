from DBLayer import *

class User:
    def __init__(self, id, name, birthday, position, phone, department):
        self._id = id
        self.name = name
        self.birthday = birthday
        self.position = position
        self.phone = phone
        self.department = department

    def __str__(self):
        return f"Пользователь(id: {self._id}, ФИО: {self.name}, Дата рождения: {self.birthday}, Должность: {self.position}, Номер телефона: {self.phone}, Отдел: {self.department})"

class Position:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f"Должность(id: {self.id}, Название: {self.name})"