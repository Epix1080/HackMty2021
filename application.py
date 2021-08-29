from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import hashlib
import sqlite3
import re
from tempfile import mkdtemp
from .login_req import login_required
from .pillHandler import url_decifer
from .pdfqr import crear_pdf
from HACKMTY import app

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_FILE_THRESHHOLD"] = 600
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = mkdtemp()
Session(app)

@app.after_request
def after_request(response):
    response.headers["Expires"] = 0
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET"])
@login_required
def index():
    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def loginUser():
    if request.method == "POST":
        session.clear()
        user = request.form.get("username").upper()
        password = request.form.get("password")

        if user == "" or password == "":
            flash("Espacios vacios")
            return render_template("login.html")
        else:
            comp = hashlib.sha256(password.encode()).hexdigest()
            conn = sqlite3.connect("HACKMTY/infoManager50.db")
            cur = conn.cursor()
            db_user = conn.execute("SELECT * FROM users WHERE UPPER(user)=?", (user,)).fetchall()
            if len(db_user) != 0:
                if comp == db_user[0][2]:
                    session["user_id"] = db_user[0][0]
                    if db_user[0][3] == 'FALSE':
                        return redirect("/userCalendar")
                    else:
                        return redirect("/patients")
                else:
                    flash("Contraseña incorrecta")
                    return render_template("login.html")
            else:
                flash("Usurario no existe")
                return render_template("login.html")
    else:
        return render_template("login.html")


@app.route("/patients", methods=["GET", "POST"])
@login_required
def patients():
    if request.method == "POST":
        pass
    else:
        return render_template("pacientes.html")
    

@app.route("/pillSetup", methods=["GET", "POST"])
@login_required
def pillSetup():
    if request.method == "POST":
        user = request.form.get("username")
        return redirect("/pillSetup" + '?user=' + user)
    else:
        username = request.args['user']
        return render_template("recetariodoctor.html", items=username)


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    session.clear()
    return redirect("/")


@app.route("/userCalendar", methods=["GET", "POST"])
@login_required
def userCalendar():
    if request.method == "POST":
        pass
    else:
        return render_template("recetariopaciente.html")

@app.route("/verificar", methods=["GET"])
def verificar():
    conn = sqlite3.connect("HACKMTY/infoManager50.db")
    cur = conn.cursor()
    key = request.args['key']
    temp = re.findall(r'\d+', key)
    id_paciente = str(temp[0])
    usrstring = (key.replace(temp[0],'')).strip()
    db_user = conn.execute("SELECT receta_string FROM pacientes WHERE id_paciente=?", (id_paciente,)).fetchall()

    if db_user[0][0] == 'FALSO':
        conn.close()
        return render_template("verIncorrecto.html")
    elif db_user[0][0] == usrstring:
        db_user = cur.execute("UPDATE pacientes SET receta_string=? WHERE id_paciente=?", ("FALSO", id_paciente))
        conn.commit()
        return render_template("verCorrecto.html")
    else:
        conn.close()
        return render_template("verIncorrecto.html")


@app.route("/pdf", methods=["POST"])
@login_required
def pdf():
    conn = sqlite3.connect("HACKMTY/infoManager50.db")
    cur = conn.cursor()
    db_user = conn.execute("SELECT receta_string FROM pacientes WHERE id_paciente=?", (session["user_id"],)).fetchall()
    receta = conn.execute("SELECT nombre,cantidad,descripcion FROM receta WHERE id_paciente=?", (session["user_id"],)).fetchall()
    paciente = conn.execute("SELECT * FROM pacientes WHERE id_paciente=?", (session["user_id"],)).fetchall()
    if len(paciente) != 0:
        doctor = conn.execute("SELECT * FROM doctores WHERE id_doctor=?", (paciente[0][6],)).fetchall()
    
    if len(db_user) != 0:
        print()
        crear_pdf('http://localhost:60491/' + 'verificar?key=' + str(session["user_id"]) + db_user[0][0], receta, doctor, paciente)
        return redirect("/userCalendar")
    else:
        return redirect("/userCalendar")