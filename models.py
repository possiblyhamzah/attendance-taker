from app import db

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    roll_no = db.Column(db.String())
    name = db.Column(db.String())
    
    def __init__(self, roll_no, name):
        self.roll_no = roll_no
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.roll_no)
    
    def serialize(self):
        return {
            'roll no': self.roll_no,
            'name': self.name,
            'password': self.password
        }

class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name
        }

class Attendance(db.Model):
    __tablename__ = 'attendances'

    id = db.Column(db.Integer, primary_key=True)
    roll_no = db.Column(db.String())
    subject = db.Column(db.String())
    days_present = db.Column(db.Integer)
    total_days = db.Column(db.Integer)

    def __init__(self, roll_no, subject, days_present, total_days):
        self.roll_no = roll_no
        self.subject = subject
        self.days_present = days_present
        self.total_days = total_days

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'roll_no': self.roll_no,
            'subject': self.subject,
            'days_present':self.days_present,
            'total_days':self.total_days
        }

class AttendanceByDate(db.Model):
    __tablename__ = 'attendancebydate'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String())
    subject = db.Column(db.String())
    students_present = db.Column(db.String())

    def __init__(self, date, subject, students_present):
        self.date = date
        self.subject = subject
        self.students_present = students_present

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'date': self.date,
            'subject': self.subject,
            'students_present': self.students_present
        }