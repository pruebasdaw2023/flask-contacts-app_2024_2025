from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from os import getenv
from flask_mysqldb import MySQL

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = getenv('MYSQL_DB')
app.secret_key = getenv('SECRET_KEY')

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    #print(data)
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)', (fullname,phone,email))

        # SI SE HACE CON EL CONECTOR DE MYSQL-CONNECTOR-PYTHON
        # cur.execute('INSERT INTO contacts VALUES (NULL, ?, ?, ?)', (fullname, phone, email))

        mysql.connection.commit()
        flash('Contact Added Successfully')

        return redirect(url_for('index'))

    return "ADD CONTACT"

@app.route('/edit')
def edit_contact():

    return "EDIT CONTACT"

@app.route('/update')
def update_contact():

    return "UPDATE CONTACT"

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id= %s', (id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('index'))


if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')