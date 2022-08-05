from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/images/'

app.secret_key="secret key"
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png'])

def allowed_file(filename):
    return '.' in filename and filename.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
@app.route("/index")
def index():
    con = sql.connect("db_web.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from badges")
    data = cur.fetchall()
    return render_template("index.html", datas=data)


@app.route("/add_badge", methods=['POST', 'GET'])
def add_badge():

    if request.method == 'POST':
        badge_name = request.form['badge_name']
        badge_description = request.form['badge_description']
        upload_badge = request.files['upload_badge']

        if upload_badge.filename == '':
            flash("No image selected for uploading")
            return redirect(url_for("add_badge"))
        if upload_badge and allowed_file(upload_badge.filename):
            filename = secure_filename(upload_badge.filename)
            upload_badge.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            flash("Image successfully uploaded!")
        else:
            flash("Allowed image types are:- .png")

        eligible_students = request.form['eligible_students']
        con = sql.connect("db_web.db")
        cur = con.cursor()
        cur.execute(
            "insert into badges(BADGE_NAME, BADGE_DESCRIPTION, UPLOAD_BADGE, ELIGIBLE_STUDENTS) values (?,?,?,?)",
            (badge_name, badge_description, filename, eligible_students))
        con.commit()
        flash('Badge Added', 'success')
        return redirect(url_for("index"))
    return render_template("add_badge.html")

@app.route("/edit_badge/<string:bid>", methods=['POST', 'GET'])
def edit_badge(bid):
    if request.method=="POST":
        badge_name=request.form['badge_name']
        badge_description=request.form['badge_description']
        upload_badge = request.files['upload_badge']

        if upload_badge.filename == '':
            flash("No image selected for uploading")
            return redirect(url_for("add_badge"))
        if upload_badge and allowed_file(upload_badge.filename):
            filename = secure_filename(upload_badge.filename)
            upload_badge.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            flash("Image successfully updated!")
        else:
            flash("Allowed image types are:- .png")

        eligible_students=request.form['eligible_students']
        con=sql.connect("db_web.db")
        cur=con.cursor()
        cur.execute("update badges set BADGE_NAME=?, BADGE_DESCRIPTION=?, UPLOAD_BADGE=?, ELIGIBLE_STUDENTS=? where BID=?",
                    (badge_name, badge_description, filename, eligible_students, bid))
        con.commit()
        flash("Badge updated", "success")
        return redirect(url_for("index"))
    con=sql.connect("db_web.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from badges where BID=?", (bid))
    data=cur.fetchone()
    return render_template("edit_badge.html", datas=data)

@app.route("/delete_badge/<string:bid>", methods=['GET'])
def delete_badge(bid):
    con=sql.connect("db_web.db")
    cur=con.cursor()
    cur.execute("delete from badges where BID=?", (bid))
    con.commit()
    flash("Badge deleted", "warning")
    return redirect(url_for("index"))

@app.route("/badge", methods=['POST', 'GET'])
def badge():
    if request.method == 'POST':
        badge_name = request.form['badge_name']
        email_id = request.form['email_id']
        con=sql.connect("db_web.db")
        cur=con.cursor()
        cur.execute("select upload_badge from badges where badge_name='"+badge_name+"' and eligible_students LIKE "+"'%" + email_id +"%'")
        con.commit()
        data = cur.fetchall()

        data=[value[0] for value in data]

        return render_template("badge.html", datas=data)
    return render_template("badge.html")

if __name__=='__main__':
    app.run(debug=True, port=8082)