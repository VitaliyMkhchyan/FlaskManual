from flask import url_for


class UserLogin:
    def __init__(self):
        self.__user = None
        
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user["id"])

    def getName(self):
        return str(self.__user["name"])

    def getEmail(self):
        return str(self.__user["email"])

    def getAvatar(self, app):
        img = None
        if not self.__user["avatar"]:
            try:
                with app.open_resource(app.root_path + url_for('static', filename="default.png")) as file:
                    img = file.read()
            except FileNotFoundError as e:
                print("[-] Error " + str(e))
        else:
            img = self.__user["avatar"]
        return img
