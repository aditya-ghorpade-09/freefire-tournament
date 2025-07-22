from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        branch = request.form['branch']
        year = request.form['year']

        ffid_file = request.files['ffid']
        payment_file = request.files['payment']

        ffid_path = os.path.join(app.config['UPLOAD_FOLDER'], ffid_file.filename)
        payment_path = os.path.join(app.config['UPLOAD_FOLDER'], payment_file.filename)

        ffid_file.save(ffid_path)
        payment_file.save(payment_path)

        with open('players.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, branch, year, ffid_file.filename, payment_file.filename])

        return redirect('/success')
    return render_template('register.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)