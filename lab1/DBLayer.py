import sqlite3
import datetime



class DBLayer:
    def __init__(self, path: str):
        self.connection = sqlite3.connect(path, check_same_thread=False)
        self.logging("INFO: Connection started")
        self.cursor = self.connection.cursor()
        self.logging("INFO: Cursor created")
        self.init_db()

    def logging(self, message):
        now = datetime.datetime.now()
        now = f'{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}'
        with open('log.txt', 'a') as file:
            file.write(f'[+] timestamp: {now}, {message}\n')

    def execute(self, sql: str, attr=()):
        try:
            result = self.cursor.execute(sql, attr).fetchall()
            self.connection.commit()
        except Exception as ex:
            self.connection.rollback()
            result = "[+] ERROR: Wrong query!"
        finally:
            return result

    def close(self):
        if self.cursor:
            self.cursor.close()
            self.logging("INFO: Cursor deleted")
        if self.connection:
            self.connection.close()
            self.logging("INFO: Connection closed\n\n")

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
        self.execute("INSERT INTO user (name, birthday, pos_id, phone ) VALUES ('Григорьев Антон Дмитриевич', '2000-11-03', 1, '+71234567890')")
        self.execute("INSERT INTO user (name, birthday, pos_id, phone ) VALUES ('Ясенев Олег Викторович', '2000-09-26', 2, '+70987654321')")
        self.execute("INSERT INTO user (name, birthday, pos_id, phone ) VALUES ('Кулаков Виктор Олегович', '2000-05-12', 3, '+79251234567')")
        self.execute("INSERT INTO user (name, birthday, pos_id, phone ) VALUES ('Алибабаев Алибаба Алибабаевич', '1989-01-01', 2,'+79251234568' )")
        self.execute("INSERT INTO user (name, birthday, pos_id, phone ) VALUES ('Никонова Анастасия Вадимовна', '2002-01-11', 3,'+79251234569' )")

        self.execute("""CREATE TABLE departments(
                     id integer PRIMARY KEY,
                     name TEXT NOT NULL,
                     head INT NOT NULL,
                     FOREIGN KEY (head) REFERENCES user(id)
                     ON UPDATE CASCADE 
                     ON DELETE CASCADE
                     );
                """)
        self.execute("INSERT INTO departments (name, head) VALUES ('Бухгалтерия', 2);")
        self.execute("INSERT INTO departments (name, head) VALUES ('IT-Отдел', 4);")


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


        self.execute("""CREATE TABLE files(
                    id integer PRIMARY KEY,
                    name TEXT,
                    format VARCHAR(4),
                    load_date DATE,
                    size TEXT,
                    owner INT,
                    FOREIGN KEY (owner) REFERENCES user(id)
                    ON UPDATE CASCADE 
                    ON DELETE CASCADE); 
                    """)

        for i in range(1,21):
            self.execute(f"INSERT INTO files(name, format, load_date, size, owner) VALUES ('{i}.bmp', 'bmp', '2021-11-16', '13', 4);")

        self.logging("INFO: Database initialized")
