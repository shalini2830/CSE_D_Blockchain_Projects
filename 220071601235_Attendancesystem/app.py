from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from blockchain import Blockchain
import uuid, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'replace-this-with-a-random-secret-in-production'

db = SQLAlchemy(app)
blockchain = Blockchain()

class Student(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll = db.Column(db.String(50), nullable=False)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), db.ForeignKey('student.id'))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    block_hash = db.Column(db.String(64))

with app.app_context():
    db.create_all()

@app.template_filter('format_datetime')
def format_datetime(value):
    if not value:
        return ""
    return value.strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def index():
    students = Student.query.all()
    # show recent attendance (latest 10)
    recent = db.session.query(Attendance, Student).join(Student).order_by(Attendance.timestamp.desc()).limit(10).all()
    return render_template('index.html', students=students, recent=recent)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name'].strip()
        roll = request.form['roll'].strip()
        if not name or not roll:
            flash('All fields are required', 'danger')
            return render_template('register.html')
        sid = str(uuid.uuid4())
        new_student = Student(id=sid, name=name, roll=roll)
        db.session.add(new_student)
        db.session.commit()
        blockchain.new_transaction(sid, 'register', {'name': name, 'roll': roll})
        blockchain.new_block(proof=12345)
        flash(f'Student {name} registered successfully', 'success')
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    sid = request.form.get('student_id')
    student = Student.query.get(sid)
    if not student:
        flash('Student not found', 'danger')
        return redirect(url_for('index'))

    # Prevent multiple marks per calendar day (server local date)
    today = datetime.datetime.utcnow().date()
    existing = Attendance.query.filter(
        Attendance.student_id == sid,
        db.func.date(Attendance.timestamp) == today
    ).first()

    if existing:
        flash(f'Attendance already marked today for {student.name}', 'warning')
        return redirect(url_for('index'))

    # record in blockchain
    blockchain.new_transaction(sid, 'attendance', {'name': student.name})
    block = blockchain.new_block(proof=9999)
    block_hash = blockchain.hash(block)
    record = Attendance(student_id=sid, block_hash=block_hash)
    db.session.add(record)
    db.session.commit()
    flash(f'Attendance marked successfully for {student.name}', 'success')
    return redirect(url_for('index'))

@app.route('/view_chain')
def view_chain():
    return render_template('view_chain.html', chain=blockchain.chain)

@app.route('/api/chain')
def api_chain():
    return jsonify({'length': len(blockchain.chain), 'chain': blockchain.chain})

@app.route('/attendance_records')
def attendance_records():
    records = db.session.query(Attendance, Student).join(Student).order_by(Attendance.timestamp.desc()).all()
    return render_template('attendance.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)
