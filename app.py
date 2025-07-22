from flask import Flask, render_template, request, redirect
import os
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Setup Google Sheets connection
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("tournament-website-466716-62b67624d91e.json", scope)
client = gspread.authorize(creds)

# Open your sheet
sheet = client.open("Free Fire Tournament Registrations").sheet1

# File upload folder
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

        # Add row to Google Sheet
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([name, branch, year, ffid_file.filename, payment_file.filename, timestamp])

        return redirect('/success')
    return render_template('register.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)