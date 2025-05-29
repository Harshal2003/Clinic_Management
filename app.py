from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Harsh#4740',
        database='clinic_db'
    )

app = Flask(__name__)
app.secret_key = 'your_secret_key'

ADMIN_ID = 'user'
ADMIN_PASSWORD = 'Admin123'

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_ID and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM patients")
    patients = cursor.fetchall()
    cursor.execute("SELECT id, name FROM doctors")
    doctors = cursor.fetchall()

    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        date = request.form['date']
        time = request.form['time']

        try:
            cursor.execute("""
                INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time)
                VALUES (%s, %s, %s, %s)
            """, (patient_id, doctor_id, date, time))
            conn.commit()
            return redirect(url_for('dashboard'))
        except Exception as e:
            conn.rollback()
            return f"An error occurred: {e}"
        finally:
            conn.close()

    conn.close()
    return render_template('add_appointment.html', patients=patients, doctors=doctors)



@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        disease = request.form['disease']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO patients (name, age, gender, disease) VALUES (%s, %s, %s, %s)", (name, age, gender, disease))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))

    return render_template('add_patient.html')

@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        gender =  request.form['gender']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO doctors (name, specialization, gender) VALUES (%s, %s, %s)", (name, specialization, gender))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))

    return render_template('add_doctor.html')

@app.route('/view_doctors')
def view_doctors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctors")
    doctors = cursor.fetchall()
    conn.close()
    return render_template('view_doctors.html', doctors=doctors)

@app.route('/edit_doctor/<int:doctor_id>', methods=['GET', 'POST'])
def edit_doctor(doctor_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        gender = request.form['gender']

        cursor.execute("""
            UPDATE doctors
            SET name=%s, specialization=%s, gender=%s
            WHERE id=%s
        """, (name, specialization, gender, doctor_id))
        conn.commit()
        conn.close()
        return redirect(url_for('view_doctors'))

    cursor.execute("SELECT * FROM doctors WHERE id=%s", (doctor_id,))
    doctor = cursor.fetchone()
    conn.close()
    return render_template('edit_doctor.html', doctor=doctor)

@app.route('/delete_doctor/<int:doctor_id>')
def delete_doctor(doctor_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM doctors WHERE id=%s", (doctor_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_doctors'))


@app.route('/view_patients')
def view_patients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()
    return render_template('view_patients.html', patients=patients)

@app.route('/edit_patient/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        disease = request.form['disease']

        cursor.execute("""
            UPDATE patients
            SET name=%s, age=%s, gender=%s, disease=%s
            WHERE id=%s
        """, (name, age, gender, disease, patient_id))
        conn.commit()
        conn.close()
        return redirect(url_for('view_patients'))

    cursor.execute("SELECT * FROM patients WHERE id=%s", (patient_id,))
    patient = cursor.fetchone()
    conn.close()
    return render_template('edit_patient.html', patient=patient)

@app.route('/delete_patient/<int:patient_id>')
def delete_patient(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE id=%s", (patient_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_patients'))


@app.route('/view_appointments')
def view_appointments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointments")
    appointments = cursor.fetchall()
    conn.close()
    return render_template('view_appointments.html', appointments=appointments)

@app.route('/edit_appointment/<int:appointment_id>', methods=['GET', 'POST'])
def edit_appointment(appointment_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        date = request.form['date']

        cursor.execute("""
            UPDATE appointments
            SET patient_id=%s, doctor_id=%s, appointment_date=%s
            WHERE id=%s
        """, (patient_id, doctor_id, date, appointment_id))
        conn.commit()
        conn.close()
        return redirect(url_for('view_appointments'))

    cursor.execute("SELECT * FROM appointments WHERE id=%s", (appointment_id,))
    appointment = cursor.fetchone()
    conn.close()
    return render_template('edit_appointment.html', appointment=appointment)

@app.route('/delete_appointment/<int:appointment_id>')
def delete_appointment(appointment_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM appointments WHERE id=%s", (appointment_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_appointments'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
