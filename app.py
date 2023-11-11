from flask import Flask, g, render_template, request, redirect, url_for, flash, make_response
import os
import sqlite3
from FDataBase import FDataBase
from UserLogin import UserLogin
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
import config

app = Flask(__name__)

db = None

app.config.from_object(config)  # Файл конфига
app.config.update(dict(DATABASE=os.path.join(app.root_path, "users.db")))

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам!"
login_manager.login_message_category = "error"


@login_manager.user_loader
def load_user(user_id):
    print("user load")
    return UserLogin().fromDB(user_id, db)


@app.before_request  # Выполнение перед запросом
def db():
    global db
    db = FDataBase(get_database())


# Connect database
def connect_db():
    connect = sqlite3.connect(app.config["DATABASE"])
    connect.row_factory = sqlite3.Row
    return connect


# Create database
def create_db():
    db = connect_db()
    with app.open_resource("script.sql", mode="r") as file:
        db.cursor().executescript(file.read())
    db.commit()
    db.close()


# Close database
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()


# Get database
def get_database():
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db


# Main page
@app.route("/")
def index():
    return render_template("index.html", posts=db.getPosts())


@app.route("/showPost/<int:id>")
@login_required  # Если пользователь авторизован показать статью
def showPost(id):
    title, text = db.getPost(id)  # получаем статью по id

    return render_template("showPost.html", title=title, text=text)


# Авторизация
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        user = db.getUserByEmail(request.form["email"])
        if user and request.form["password"] == user["password"]:
            user_login = UserLogin().create(user)
            rm = True if request.form.get("auth") else False
            login_user(user_login, remember=rm)
            return redirect(request.args.get("next") or url_for("profile"))
        else:
            flash("Неверный логин/пароль!", "error")

    return render_template("login.html")


# Регистрация
@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        db.addUser(str(request.form["username"]), str(request.form["email"]), str(request.form["pass1"]))
        return redirect("/login")
    else:
        return render_template("registration.html")


# Добавление поста
@app.route("/addPost", methods=["POST", "GET"])
@login_required
def addPost():
    if request.method == "POST":
        db.addPost(request.form["title"], request.form["text"])
        return redirect("/")

    return render_template("addPost.html")


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/userava")
@login_required
def userava():
    img = current_user.getAvatar(app)
    if not img:
        return ""

    h = make_response(img)
    h.headers["Content-Type"] = "image/png"
    return h


@app.route("/upload_file", methods=["GET", "POST"])
@login_required
def upload_file():
    if request.method == "POST":
        file = request.files['file']
        if file:
            try:
                img = file.read()
                res = db.updateUserAvatar(img, current_user.get_id())
                if not res:
                    redirect("/")
            except FileNotFoundError as e:
                print("Error " + str(e))

    return redirect(url_for("profile"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
