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

class File:
    def __init__(self, id, name, format, load_date, size, owner):
        self._id = id
        self.name = name
        self.format = format
        self.load_date = load_date
        self.size = size
        self.owner = owner

    def __str__(self):
        return f"Файл(id: {self._id}, Название: {self.name}, Формат: {self.format}, Дата загрузки: {self.load_date}, Размер: {self.size}b, Хозяин: {self.owner})"