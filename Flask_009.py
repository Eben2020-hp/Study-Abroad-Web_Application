from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_cors import cross_origin
import pandas as pd
import pyodbc

employee = {"Priyanka" : "priyanka", "Smitha" : "smitha", "Eldho" : "eldho", "Baslin" : "baslin", "Annabel" : "annabel"}

#connection to database
conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=DESKTOP-T8B1PTQ;'
                      'Database=Eben_2048009;'
                      'Trusted_Connection=yes;')


app = Flask(__name__)
app.secret_key = 'hello'    #Secret key.


@app.route('/')             #This is a decorator.
@cross_origin()
def home():
    return render_template('index.html')



@app.route('/login', methods=['POST','GET']) 
@cross_origin()
def login():
    flag = 0
    if request.method == 'POST':
        user = request.form['name']   #'name' is the name in the dictionary key.
        pwd = request.form['password']
        for key, value in employee.items():
            if key == user and value == pwd:
                session['user'] = user      #'user' is the name in the dictionary key.
                #flash("Login Succesful!")
                return redirect(url_for("Details"))
                flag = 1
                break
        if flag == 0:
            flash("INCORRECT USERNAME or PASSWORD !!")
            return redirect(url_for('login'))
    else:
        if 'user' in session:       #Check notes 446-448.
            flash("Already logged in")
            return redirect(url_for('Details'))

        return render_template('login.html')


@app.route('/user')
@cross_origin()
def user():
    if 'user' in session:
        user = session['user']
        return render_template('user.html', user = user)
    else:
        flash("You are not logged in yet.")
        return redirect(url_for('login'))


@app.route('/logout')
@cross_origin()
def logout():
    #The next 3 lines of code is for checking if the user is in the session. And if he is there then we will logout with the user name.
    if 'user' in session:
        user = session['user']
        flash(f"You have succesfully logged out, {user}.","info")
    session.pop('user',None)    #Remove the user data from our sessions. None is a message associated with removing that data.
    return redirect(url_for('home'))



@app.route("/Employees", methods = ["GET", "POST"])
@cross_origin()
def Employees():
    data1 = pd.read_sql("SELECT * FROM EMPLOYEES", conn)
    result=data1.to_html()
    return result


@app.route("/Students", methods = ["GET", "POST"])
@cross_origin()
def Students():
    data2 = pd.read_sql("SELECT * FROM STUDENTS", conn)
    result=data2.to_html()
    return result


@app.route("/Branches", methods = ["GET", "POST"])
@cross_origin()
def Branches():
    data3 = pd.read_sql("SELECT * FROM BRANCHES", conn)
    result=data3.to_html()
    return result


@app.route("/Details", methods = ["GET", "POST"])
@cross_origin()
def Details():
    data4 = pd.read_sql("SELECT * FROM Details", conn)
    result=data4.to_html()
    return result





@app.route('/insert', methods=['POST','GET']) 
@cross_origin()
def insert():
    if request.method == 'POST':
        return redirect(url_for('DML'))
    
    return render_template('insert.html')



@app.route("/DML", methods = ["GET", "POST"])
@cross_origin()
def DML():
    option = request.form['Eben']

    if  option == 'opt1':
        v1= request.form['first']
        v2= request.form['second']
        v3= request.form['third']
        v4= request.form['fourth']
        record=[v1,v2,v3,v4]
        cursor=conn.cursor()
        insert="INSERT INTO STUDENTS VALUES(?,?,?,?);"
        cursor.execute(insert,record)
        data = pd.read_sql("SELECT * FROM STUDENTS", conn)
        result=data.to_html()


    elif  option == 'opt2':
        v1= request.form['first_del']
        cursor=conn.cursor()
        kick="DELETE FROM Details WHERE Student_ID = ?;"
        cursor.execute(kick,v1)
        data = pd.read_sql("SELECT * FROM Details", conn)
        result=data.to_html()


    elif  option == 'opt3':
        v1= request.form['first_up']
        v2= request.form['second_up']
        record=[v1,v2]
        cursor=conn.cursor()
        update="UPDATE STUDENTS SET Email_ID = ? WHERE Student_Name = ?;"
        cursor.execute(update,record)
        data = pd.read_sql("SELECT * FROM STUDENTS", conn)
        result=data.to_html()


    else:
        result="PLEASE SELECT AN OPTION!!"
    return result






@app.route("/Visuals", methods = ["GET", "POST"])
@cross_origin()
def Visuals():
    return render_template('visuals.html')





if __name__ == '__main__':
    app.run(host='127.0.0.1', port=1234, debug = True) 
#The "debug = True" will make the server update by itself and make the changes for us.