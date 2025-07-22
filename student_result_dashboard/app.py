from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database initialization
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Create students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT UNIQUE NOT NULL,
            class_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create subjects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            max_marks INTEGER DEFAULT 100
        )
    ''')
    
    # Create marks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject_id INTEGER,
            marks INTEGER NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (subject_id) REFERENCES subjects (id),
            UNIQUE(student_id, subject_id)
        )
    ''')
    
    # Insert default subjects if not exists
    default_subjects = [
        ('Mathematics', 100),
        ('Science', 100),
        ('English', 100),
        ('Social Studies', 100),
        ('Computer Science', 100)
    ]
    
    for subject, max_marks in default_subjects:
        cursor.execute('INSERT OR IGNORE INTO subjects (name, max_marks) VALUES (?, ?)', 
                      (subject, max_marks))
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def calculate_grade(percentage):
    if percentage >= 90:
        return 'A+'
    elif percentage >= 80:
        return 'A'
    elif percentage >= 70:
        return 'B+'
    elif percentage >= 60:
        return 'B'
    elif percentage >= 50:
        return 'C'
    elif percentage >= 40:
        return 'D'
    else:
        return 'F'

@app.route('/')
def index():
    conn = get_db_connection()
    
    # Get total students
    total_students = conn.execute('SELECT COUNT(*) as count FROM students').fetchone()['count']
    
    # Get recent results
    recent_results = conn.execute('''
        SELECT s.name, s.roll_no, s.class_name,
               AVG(m.marks) as avg_marks,
               COUNT(m.marks) as subjects_count
        FROM students s
        LEFT JOIN marks m ON s.id = m.student_id
        GROUP BY s.id
        ORDER BY s.created_at DESC
        LIMIT 5
    ''').fetchall()
    
    conn.close()
    
    return render_template('index.html', 
                         total_students=total_students,
                         recent_results=recent_results)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll_no = request.form['roll_no']
        class_name = request.form['class_name']
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO students (name, roll_no, class_name) VALUES (?, ?, ?)',
                        (name, roll_no, class_name))
            conn.commit()
            flash('Student added successfully!', 'success')
        except sqlite3.IntegrityError:
            flash('Roll number already exists!', 'error')
        finally:
            conn.close()
        
        return redirect(url_for('add_student'))
    
    return render_template('add_student.html')

@app.route('/enter_marks', methods=['GET', 'POST'])
def enter_marks():
    conn = get_db_connection()
    
    if request.method == 'POST':
        student_id = request.form['student_id']
        
        # Delete existing marks for this student
        conn.execute('DELETE FROM marks WHERE student_id = ?', (student_id,))
        
        # Insert new marks
        subjects = conn.execute('SELECT * FROM subjects').fetchall()
        for subject in subjects:
            marks = request.form.get(f'marks_{subject["id"]}')
            if marks and marks.strip():
                conn.execute('INSERT INTO marks (student_id, subject_id, marks) VALUES (?, ?, ?)',
                           (student_id, subject['id'], int(marks)))
        
        conn.commit()
        flash('Marks entered successfully!', 'success')
        conn.close()
        return redirect(url_for('enter_marks'))
    
    students = conn.execute('SELECT * FROM students ORDER BY name').fetchall()
    subjects = conn.execute('SELECT * FROM subjects ORDER BY name').fetchall()
    conn.close()
    
    return render_template('enter_marks.html', students=students, subjects=subjects)

@app.route('/results')
def results():
    conn = get_db_connection()
    
    # Get all students with their results
    results_data = conn.execute('''
        SELECT s.id, s.name, s.roll_no, s.class_name,
               COALESCE(SUM(m.marks), 0) as total_marks,
               COALESCE(COUNT(m.marks), 0) as subjects_count,
               COALESCE(AVG(m.marks), 0) as avg_marks
        FROM students s
        LEFT JOIN marks m ON s.id = m.student_id
        GROUP BY s.id
        ORDER BY avg_marks DESC
    ''').fetchall()
    
    # Calculate percentage, grade, and rank
    processed_results = []
    for i, result in enumerate(results_data):
        if result['subjects_count'] > 0:
            percentage = (result['total_marks'] / (result['subjects_count'] * 100)) * 100
            grade = calculate_grade(percentage)
            rank = i + 1
        else:
            percentage = 0
            grade = 'N/A'
            rank = 'N/A'
        
        processed_results.append({
            'id': result['id'],
            'name': result['name'],
            'roll_no': result['roll_no'],
            'class_name': result['class_name'],
            'total_marks': result['total_marks'],
            'subjects_count': result['subjects_count'],
            'percentage': round(percentage, 2),
            'grade': grade,
            'rank': rank
        })
    
    conn.close()
    return render_template('results.html', results=processed_results)

@app.route('/student_detail/<int:student_id>')
def student_detail(student_id):
    conn = get_db_connection()
    
    # Get student info
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    
    # Get student marks with subject details
    marks_data = conn.execute('''
        SELECT sub.name as subject_name, sub.max_marks, m.marks
        FROM marks m
        JOIN subjects sub ON m.subject_id = sub.id
        WHERE m.student_id = ?
        ORDER BY sub.name
    ''', (student_id,)).fetchall()
    
    conn.close()
    
    if not student:
        flash('Student not found!', 'error')
        return redirect(url_for('results'))
    
    # Calculate totals
    total_marks = sum(mark['marks'] for mark in marks_data)
    total_max_marks = sum(mark['max_marks'] for mark in marks_data)
    percentage = (total_marks / total_max_marks * 100) if total_max_marks > 0 else 0
    grade = calculate_grade(percentage)
    
    return render_template('student_detail.html', 
                         student=student,
                         marks_data=marks_data,
                         total_marks=total_marks,
                         total_max_marks=total_max_marks,
                         percentage=round(percentage, 2),
                         grade=grade)

@app.route('/api/chart_data')
def chart_data():
    conn = get_db_connection()
    
    # Grade distribution
    grade_data = {}
    results = conn.execute('''
        SELECT s.id, AVG(m.marks) as avg_marks
        FROM students s
        LEFT JOIN marks m ON s.id = m.student_id
        GROUP BY s.id
        HAVING COUNT(m.marks) > 0
    ''').fetchall()
    
    for result in results:
        percentage = result['avg_marks']
        grade = calculate_grade(percentage)
        grade_data[grade] = grade_data.get(grade, 0) + 1
    
    # Subject-wise average
    subject_avg = conn.execute('''
        SELECT sub.name, AVG(m.marks) as avg_marks
        FROM subjects sub
        LEFT JOIN marks m ON sub.id = m.subject_id
        GROUP BY sub.id, sub.name
        ORDER BY sub.name
    ''').fetchall()
    
    conn.close()
    
    return jsonify({
        'grade_distribution': grade_data,
        'subject_averages': {row['name']: round(row['avg_marks'] or 0, 2) for row in subject_avg}
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
