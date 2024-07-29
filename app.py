from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session 
import pyrebase
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


app = Flask(__name__)
app.config['SECRET_KEY']="*******"

firebaseConfig = {
  'apiKey': "AIzaSyC8SEDSRYBW0hh3p5rk7YdWvzQcF1--zsI",
  'authDomain': "einar-case-study.firebaseapp.com",
  'projectId': "einar-case-study",
  'storageBucket': "einar-case-study.appspot.com",
  'messagingSenderId': "449189864578",
  'appId': "1:449189864578:web:6bf15a20b73355c015c09b",
  'measurementId': "G-3DLSXW8H7D",
  'databaseURL':"https://einar-case-study-default-rtdb.europe-west1.firebasedatabase.app/"
}

sender_email = "georgeghrayib2008@gmail.com"
password = "iobh zefi phxo riga"
smtp_server = "smtp.gmail.com"
smtp_port = 587

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template("signin.html") 
    else:
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('dashboard'))
        except:
            error = "Womp it failed. Try again!"
            return render_template("signin.html", error=error)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("signin.html") 
    else:
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('dashboard'))
        except:
            error = "Wrong email or password!"
            return render_template("signin.html", error=error)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'GET':
        return render_template("dashboard.html") 
    else:
        subject = request.form['subject']
        body = request.form['message']
        file = request.form['file']
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = "makeoveryourleftovers@gmail.com"
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        attachment = MIMEBase('application', 'octet-stream')
        try:
            with open(file, 'rb') as file:
                attachment.set_payload(file.read())
                encoders.encode_base64(attachment)
                attachment.add_header('Content-Disposition', f'attachment; filename={file}')
                msg.attach(attachment)
        except Exception as e:
            print(f"Failed to attach file {file}. Error: {str(e)}")

        # Send the email
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(sender_email, password)
                server.sendmail(sender_email, msg['To'], msg.as_string())
                print(f"Email sent to {msg['To']}")
                return redirect(url_for('dashboard'))
        except Exception as e:
            print(f"Failed to send email to {msg['To']}. Error: {str(e)}")
            return redirect(url_for('dashboard'))
            
@app.route('/calender', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'GET':
        return render_template("calender.html") 
    
if __name__ == '__main__':
    app.run(debug=True)