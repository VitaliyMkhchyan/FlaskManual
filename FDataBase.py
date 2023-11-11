import sqlite3


class FDataBase:
    def __init__(self, db) -> None:
        self.__db = db
        self.__cursor = db.cursor()

    def addPost(self, title: str, text: str) -> bool:
        try:
            self.__cursor.execute("INSERT INTO posts VALUES(NULL, ?, ?)", (title, text))
            self.__db.commit()
            return True
        except sqlite3.Error as e:
            print("SQLITE Error: " + str(e))
        return False

    def getPost(self, id) -> tuple:
        try:
            self.__cursor.execute(f"SELECT title, text FROM posts WHERE id = {id} LIMIT 1")
            result = self.__cursor.fetchone()
            if result:
                return result
        except sqlite3.Error as e:
            print("SQLITE Error: " + str(e))

        return (False, False)

    def getPosts(self) -> list:
        try:
            self.__cursor.execute("SELECT * FROM posts")
            result = self.__cursor.fetchall()
            if result:
                return result
        except sqlite3.Error as e:
            print("SQLITE Error: " + str(e))

        return []

    def addUser(self, name: str, email: str, password: str) -> bool:
        try:
            self.__cursor.execute(f"SELECT COUNT() as `count` from users WHERE email LIKE '{email}'")
            result = self.__cursor.fetchone()
            if result["count"] > 0:
                print("Пользователь уже существует")
                return False

            self.__cursor.execute(f"INSERT INTO users VALUES(NULL, ?, ?, ?, NULL)", (name, email, password))
            self.__db.commit()
            return True
        except sqlite3.Error as e:
            print("Error: " + str(e))

    def getUser(self, user_id):
        try:
            self.__cursor.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            result = self.__cursor.fetchone()
            if not result:
                print("Пользователь не найден")
                return False

            return result
        except sqlite3.Error as e:
            print("Error: " + str(e))
        return False

    def getUserByEmail(self, email):
        try:
            self.__cursor.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            result = self.__cursor.fetchone()
            if not result:
                print("Пользователь не найден")
                return False

            return result
        except sqlite3.Error as e:
            print("Error: " + str(e))
        return False

    def updateUserAvatar(self, avatar, user_id):
        try:
            binary = sqlite3.Binary(avatar)
            self.__cursor.execute(f"UPDATE users SET avatar = ? WHERE id = ?", (binary, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error " + str(e))
            return False

        return True