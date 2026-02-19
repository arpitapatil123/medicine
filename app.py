from flask import Flask, render_template, request, redirect, url_for
from datetime import date

app = Flask(__name__)

# In-memory data store
patients = {}

# Dummy patient for direct testing
patients['9876543210'] = {
    'name': 'Vaishnavi Test',
    'medicines': []
}

# ---------- ROUTES ---------- #

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/add')
def add():
    return render_template('add.html')


@app.route('/auth')
def auth():
    return render_template('auth.html')


@app.route('/verify', methods=['POST'])
def verify():
    phone = request.form['phone']
    otp = request.form['otp']
    # Simulated OTP check
    if otp == "123456":
        return f"✅ Login successful for {phone}!"
    else:
        return "❌ Invalid OTP, please try again."


@app.route('/save-patient', methods=['POST'])
def save_patient():
    name = request.form['name']
    phone = request.form['phone']
    # Save patient in memory
    patients[phone] = {'name': name, 'medicines': []}
    # Redirect to medicine entry page with phone as param
    return redirect(url_for('medi', phone=phone))


@app.route('/medi')
def medi():
    phone = request.args.get('phone')
    if phone not in patients:
        return "❌ Invalid patient"
    return render_template('medi.html', phone=phone, current_date=date.today())


@app.route('/save-medicine', methods=['POST'])
def save_medicine():
    phone = request.form['phone']
    med_name = request.form['med_name']
    time = request.form['time']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    if phone in patients:
        # Add the new medicine
        patients[phone]['medicines'].append({
            'name': med_name,
            'time': time,
            'start_date': start_date,
            'end_date': end_date
        })

        # Render a confirmation page with all saved medicines
        return render_template(
            'save_medicine.html',
            name=patients[phone]['name'],
            phone=phone,
            medicines=patients[phone]['medicines']
        )
    else:
        return "❌ Patient not found."

# ---------- MAIN ---------- #

if __name__ == '__main__':
    app.run(debug=True)
