from User import *

class DAO:
    def __init__(self, db: DBLayer):
        self.db = db

    def get_positions(self):
        template = "SELECT * FROM positions"
        result = self.db.execute(template)
        if not result:
            return None
        positions = [Position(*x) for x in result]
        return positions

    def read(self, _arg):
        template = "SELECT user.id, user.name, user.birthday, positions.name, user.phone, departments.name FROM user " \
                   "inner join positions on user.pos_id = positions.id " \
                   "inner join departments_users as du on du.user_id = user.id " \
                   "inner join departments on du.department_id = departments.id " \
                   "WHERE user.id = ?"
        result = self.db.execute(template, str(_arg))
        if not result:
            return None
        user = User(*result[0])
        return user

    def delete(self, _id):
        template = "DELETE  FROM user WHERE id = ?"
        result = self.db.execute(template, str(_id))

    def create(self, user: User):
        template = "INSERT INTO user (name, birthday, pos_id, phone) VALUES (?, ?, ?, ?)"
        result = self.db.execute(template, (user.name, user.birthday, user.position, user.phone))
        last_id = self.db.cursor.lastrowid
        user._id = last_id
        dep = self.db.execute("INSERT INTO departments_users VALUES(?, ?)", (user.department, user._id))

    def update(self, user: User):
        template = "UPDATE user SET name = ?, birthday = ?, pos_id = ?, phone = ?  WHERE id = ?"
        self.db.execute(template, (user.name, user.birthday, user.position, user.phone, user._id))
        dep = self.db.execute("UPDATE departments_users SET department_id = ? WHERE user_id = ?", (user.department, user._id))
        return user

    def all(self):
        template = "SELECT user.id, user.name, user.birthday, positions.name, user.phone, departments.name FROM user " \
                   "inner join positions on user.pos_id = positions.id " \
                   "inner join departments_users as du on du.user_id = user.id " \
                   "inner join departments on du.department_id = departments.id " \
                   "ORDER BY user.id"
        result = self.db.execute(template)
        if not result:
            return None
        users = [User(*x) for x in result]
        return users

    def search_by_name(self, string):
        template = "SELECT user.id, user.name, user.birthday, positions.name, user.phone, departments.name FROM user " \
                   "inner join positions on user.pos_id = positions.id " \
                   "inner join departments_users as du on du.user_id = user.id " \
                   "inner join departments on du.department_id = departments.id " \
                   "WHERE user.name LIKE '%%%s%%' " \
                   "ORDER BY user.id" % (string)
        result = self.db.execute(template)
        if not result:
            return None
        users = [User(*x) for x in result]
        return users

    def search_by_phone(self, string):
        template = "SELECT user.id, user.name, user.birthday, positions.name, user.phone, departments.name FROM user " \
                   "inner join positions on user.pos_id = positions.id " \
                   "inner join departments_users as du on du.user_id = user.id " \
                   "inner join departments on du.department_id = departments.id " \
                   "WHERE user.phone LIKE '%%%s%%' " \
                   "ORDER BY user.id" % (string)
        result = self.db.execute(template)
        if not result:
            return None
        users = [User(*x) for x in result]
        return users

    def search_by_department(self, string):
        template = "SELECT user.id, user.name, user.birthday, positions.name, user.phone, departments.name FROM user " \
                   "inner join positions on user.pos_id = positions.id " \
                   "inner join departments_users as du on du.user_id = user.id " \
                   "inner join departments on du.department_id = departments.id " \
                   "WHERE departments.name LIKE '%%%s%%' " \
                   "ORDER BY user.id" % (string)
        result = self.db.execute(template)
        if not result:
            return None
        users = [User(*x) for x in result]
        return users

    def search_by_pos(self, string):
        template = "SELECT user.id, user.name, user.birthday, positions.name, user.phone, departments.name FROM user " \
                   "inner join positions on user.pos_id = positions.id " \
                   "inner join departments_users as du on du.user_id = user.id " \
                   "inner join departments on du.department_id = departments.id " \
                   "WHERE positions.name LIKE '%%%s%%' " \
                   "ORDER BY user.id" % (string)
        result = self.db.execute(template)
        if not result:
            return None
        users = [User(*x) for x in result]
        return users


