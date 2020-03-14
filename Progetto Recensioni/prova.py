from datetime import timedelta

from flask import Flask, redirect, url_for, render_template, session, request, flash

app = Flask(__name__)
app.secret_key = "privatekey"  # chiave cript
#app.permanent_session_lifetime = timedelta(hours=1)


@app.route("/home")  # Base html per ogni pagina
def home():
        return render_template("Home.html")


@app.route("/login", methods=["POST", "GET"])  # pagina di Login
def login():
    if "POST" == request.method:  # se user si autentica e sessione non  è ancora aperta
        user = request.form["nm"]  # prelevo Username
        password = request.form["pass"]
        session["user"] = user  # creazione nuova sessione
        flash("Hai effettuato con successo il login")
        file = open("db_temp.txt", "a+")
        file.write("username:"+str(user)+";"+"password:"+str(password)+"\n")
        file.close()
        return redirect(url_for("profile"))  # reindirizzo a pagine personale
    else:
        if "user" in session:
            return redirect(url_for("logout"))

        return render_template("login.html")  # se user non si è mai registrato rendero pagina Login


@app.route("/user", methods=["POST", "GET"])
def profile():  # funzione per pagina personale utente
    email = None
    if "user" in session:  # se l'utente esiste e ha sessione aperta
        un = session["user"]  # prendo nome

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            flash("Email salvata con successo")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("profile.html", email=email)  # renderizzo pagina profilo
    else:
        flash("Non hai effettuato il login")
        return redirect(url_for("login"))  # altrimenti reindirizzo a pagina login


@app.route("/logout")  # pagina di Logout in fase di aggiornamento
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"Hai effettuato il logout, {user}", "warning")
        output = []
        file = open("db_temp.txt", "r+")
        for riga in file:
            array = riga.split(";")
            username = array[0].split(":")
            if session["user"] != username[1]:
                output.append(riga)
        file.close()
        file = open("db_temp.txt", "w")
        file.writelines(output)
        file.close()
        
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

