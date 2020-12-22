import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from flask_session import Session
from flask_socketio import SocketIO, emit
from datetime import date
import json
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from models import Student, Subject, Attendance, AttendanceByDate
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# from eventlet import wsgi
# import eventlet

# app.config["SECRET_KEY"] = 'this-really-needs-to-be-changed'
# socketio = SocketIO(app)

@app.route("/")
def index():
    if "username" in session:
        if "chat_id" in session:
            return redirect(url_for('chatroom', chat_id=session["chat_id"]))
        return redirect(url_for('messages'))
    
    return render_template("index.html")


@app.route("/attendance/<roll_no>", methods=["GET", "POST"])
def attendance(roll_no):
    student = Student.query.filter_by(roll_no=roll_no).first()
    attendances = Attendance.query.filter_by(roll_no=roll_no).all()
    return render_template('attendance.html', attendances=attendances, student=student)


@app.route("/submitattendance", methods=["GET", "POST"])
def submit_attendance():
    if request.method == "POST":
        subject = request.form.get("subject")
        return redirect(url_for('submit_subject_attendance', subject = subject))
    
    subjects = Subject.query.all()
    return render_template('submit_attendance.html', subjects=subjects)
    
@app.route("/submitattendance/<subject>", methods=["GET", "POST"])
def submit_subject_attendance(subject):
    students = Student.query.all()

    if request.method == "POST":
        presentees = request.form.getlist('vehicle')    
        for student in students:
            if student.roll_no in presentees:
                attendance_by_date=AttendanceByDate(
                    date=f'{date.today().day}-{date.today().month}-{date.today().year}',
                    subject=subject,
                    students_present=json.dumps(presentees)
                )
                db.session.add(attendance_by_date)
                db.session.commit()


                attendance = Attendance.query.filter_by(roll_no=student.roll_no, subject=subject).first()
                attendance.days_present += 1
                attendance.total_days += 1
                db.session.commit()
        # return render_template("error.html", message=presentees)

        return redirect(url_for('submit_attendance'))
    
    return render_template("submit_subject_attendance.html", subject=subject, students=students)


@app.route("/getattendance", methods=["GET", "POST"])
def get_attendance():
    if request.method == "POST":
        day = request.form.get("day")
        month = request.form.get("month")
        year = request.form.get("year")
        
        date = f'{day}-{month}-{year}'

        sort_by_subject = {}
        subjects = Subject.query.all()

        for subject in subjects:
            attendances = AttendanceByDate.query.filter_by(date=date, subject=subject.name).first()
            sort_by_subject[subject.name] = json.loads(attendances.students_present)
        # print(sort_by_subject)
        return render_template("get_attendance.html", attendances=sort_by_subject, date=date)

    return render_template("get_attendance.html")


@app.route("/alsoerror", methods=["GET", "POST"])
def alsoerror():
    # if request.method == "POST":

    
    
    # students = Students.query.all()
    return render_template("submit_subject_attendance.html")

@app.route("/error", methods=["GET", "POST"])
def error():
    # if request.method == "POST":
    f = request.form.getlist('vehicle')    
    return render_template('error.html', message = f)
