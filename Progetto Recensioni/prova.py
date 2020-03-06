from datetime import timedelta

from flask_sqlalchemy import SQLalchemy
from flask import Flask, redirect, url_for, render_template, session, request, flash

app = Flask(__name__)
app.secret_key = "privatekey"  # chiave cript
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(hours=1)

db = sqlalchemy(app)


class users(db.Model):
    _id = db.Column("id", db.integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, name, password):
        self.name = name
        self.password = password


@app.route("/")  # Base html per ogni pagina
def home():
    return render_template("base.html")


@app.route("/login", methods=["POST", "GET"])  # pagina di Login
def login():
    if "POST" == request.method:  # se user si autentica e sessione non  è ancora aperta
        user = request.form["nm"]  # prelevo Username
        session["user"] = user  # creazione nuova sessione
        flash("Hai effettuato con successo il login")
        return redirect(url_for("profile"))  # reindirizzo a pagine personale
    else:
        if "user" in session:
            flash("Hai già effettuato il login")
            return redirect(url_for("profile"))

        return render_template("login.html")  # se user non si è mai registrato rendero pagina Login


@app.route("/user")
def profile():  # funzione per pagina personale utente, passo come parametro username
    if "user" in session:  # se l'utente esiste e ha sessione aperta
        un = session["user"]  # prendo nome
        return render_template("profile.html")  # renderizzo pagina profilo
    else:
        flash("Non hai effettuato il login")
        return redirect(url_for("login"))  # altrimenti reindirizzo a pagina login


@app.route("/logout")  # pagina di Logout in fase di aggiornamento
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"Hai effettuato il logout, {user}", "warning")

    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
