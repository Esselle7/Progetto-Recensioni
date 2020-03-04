from flask import Flask, redirect, url_for, render_template, session, request

app = Flask(__name__)
app.secret_key = "privatekey" # chiave cript

cont: int = 0


@app.route("/")  # Base html per ogni pagina
def home():
    return render_template("base.html")


@app.route("/login", methods=["POST", "GET"])  # pagina di Login
def login():
    if "POST" == request.method:  # se user si autentica e sessione non  è ancora aperta
        user = request.form["nm"]  # prelevo Username
        session[str(user)] = user  # creazione nuova sessione
        return redirect(url_for("profile", usr=user)) #reindirizzo a pagine personale
    else:
        return render_template("login.html") #se user non si è mai registrato rendero pagina Login


@app.route("/<usr>")
def profile(usr): # funzione per pagina personale utente, passo come parametro username
    if usr in session: #se l'utente esiste e ha sessione aperta
        un = session[usr] #prendo nome
        return render_template("profile.html", name=usr) #renderizzo pagina profilo
    else:
        redirect(url_for("login")) #altrimenti reindirizzo a pagina login


@app.route("/logout")  # pagina di Logout in fase di aggiornamento
def logout(usr):
    session.pop(usr)
    return redirect(url_for("login"))



if __name__ == "__main__":
    app.run(debug=True)
