import sqlite3
import traceback


class DBLayer:
    def __init__(self, path: str):
        self.connection = sqlite3.connect(path, check_same_thread=False)
        print("[+] INFO: Connection started")
        self.cursor = self.connection.cursor()
        print("[+] INFO: Cursor created")
        self.init_db()

    def execute(self, sql: str, attr=()):
        try:
            result = self.cursor.execute(sql, attr).fetchall()
            self.connection.commit()
        except Exception as ex:
            self.connection.rollback()
            result = "[+] ERROR: Wrong query!"
            print(ex)
        finally:
            return result

    def close(self):
        if self.cursor:
            self.cursor.close()
            print("[+] INFO: Cursor deleted")
        if self.connection:
            self.connection.close()
            print("[+] INFO: Connection closed")

    def init_db(self):
        self.execute("""CREATE TABLE positions(
                     id integer PRIMARY KEY,
                     name TEXT NOT NULL
                     );
                     """)

        self.execute("INSERT INTO positions (name) VALUES ('Администратор');")
        self.execute("INSERT INTO positions (name) VALUES ('Начальник');")
        self.execute("INSERT INTO positions (name) VALUES ('Сотрудник');")

        self.execute("""CREATE TABLE user(
                    id integer PRIMARY KEY,
                    name TEXT NOT NULL,
                    birthday DATE,
                    pos_id INT,
                    phone VARCHAR(12),
                    FOREIGN KEY (pos_id) REFERENCES positions(id)
                    ON UPDATE CASCADE 
                    ON DELETE CASCADE
                    );
                """)
        self.execute("INSERT INTO user (name, birthday, pos_id, phone ) VALUES ('user1', '2000-11-03', 1, '+79161111111')")
        self.execute("INSERT INTO user (name, birthday, pos_id, phone ) VALUES ('user2', '2000-09-26', 2, '+79161111112')")
        self.execute("INSERT INTO user (name, birthday, pos_id, phone ) VALUES ('user3', '2000-05-12', 3, '+79161111113')")
        self.execute("INSERT INTO user (name, birthday, pos_id, phone ) VALUES ('user4', '1989-01-01', 2, '+79161111114')")
        self.execute("INSERT INTO user (name, birthday, pos_id, phone ) VALUES ('user5', '2002-01-11', 3, '+79161111115')")

        self.execute("""CREATE TABLE departments(
                     id integer PRIMARY KEY,
                     name TEXT NOT NULL,
                     head INT NOT NULL,
                     FOREIGN KEY (head) REFERENCES user(id)
                     ON UPDATE CASCADE 
                     ON DELETE CASCADE
                     );
                """)
        self.execute("INSERT INTO departments (name, head) VALUES ('dep1', 2);")
        self.execute("INSERT INTO departments (name, head) VALUES ('dep2', 4);")

        self.execute("""CREATE TABLE departments_users(
                     department_id integer,
                     user_id integer,
                     PRIMARY KEY(department_id, user_id),
                     FOREIGN KEY (department_id) REFERENCES departments(id)
                     ON UPDATE CASCADE 
                     ON DELETE CASCADE,
                     FOREIGN KEY (user_id) REFERENCES user(id)
                     ON UPDATE CASCADE 
                     ON DELETE CASCADE                     
                     );
                     """)
        self.execute("INSERT INTO departments_users VALUES (1, 2)")
        self.execute("INSERT INTO departments_users VALUES (1, 5)")
        self.execute("INSERT INTO departments_users VALUES (2, 4)")
        self.execute("INSERT INTO departments_users VALUES (2, 3)")
        self.execute("INSERT INTO departments_users VALUES (2, 1)")

        print("[+] INFO: Database initialized")


# db = DBLayer(":memory:")
# sql = "SELECT * FROM user"
# try:
#     print(db.execute(sql).fetchall())
# except:
#     print(db.execute(sql))
#
# db.close()
