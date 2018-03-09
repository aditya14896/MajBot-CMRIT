from flask import Flask,redirect,url_for,request, render_template, request, jsonify,session
from functools import wraps
from flask_restful import Resource, Api
import json
import sqlite3
import aiml
import os
with open('config.json') as data_file:
    config = json.load(data_file)

app = Flask(__name__)
api = Api(app)
app.secret_key= "my precious"

def login_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            win32api.MessageBox(0, 'YOU NEED TO LOGIN FIRST!', 'LOGIN Error',0x00001000)
            return render_template('index.html')
    return wrap

@app.route("/")
def hello():
    return render_template('index.html')


@app.route('/register',methods=['GET','POST'])
def register():
    error= None
    return render_template('chat.html')
    if 'logged_in' in session:
        return render_template('chat.html')
    if request.method == 'POST':
        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']
        sql="SELECT COUNT(1) FROM userdetail WHERE username= ?;"
        con = sqlite3.connect('majbot.sqlite3')
        cur = con.cursor()
        cur.execute(sql, [(username)])
        if cur.fetchone()[0]:
            win32api.MessageBox(0, 'This username already exists', 'Error',0x00001000)
            return render_template('index.html')
        if password1 != password2:
            win32api.MessageBox(0, 'passwords do not match.please check!!', 'Check passwords',0x00001000)
            return render_template('index.html')
        data=[username,firstname,lastname,email,0,password2]
        sql="INSERT INTO userdetail(username,first_name,last_name,email_id,dob,user_type,mob_no,password) VALUES(?,?,?,?,?,?,?,?)"
        cur.execute(sql, data)
        con.commit()
        win32api.MessageBox(0, 'Successfully Registered!!', 'Welcome to MediWare',0x00001000)
        session['logged_in']= True
        session['user']=username
        return render_template('chat.html')
    return render_template('index.html')


@app.route("/ask", methods=['POST'])
def ask():
	message = str(request.form['messageText'])

	kernel = aiml.Kernel()

	if os.path.isfile("bot_brain.brn"):
	    kernel.bootstrap(brainFile = "bot_brain.brn")
	else:
	    kernel.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands = "load aiml b")
	    kernel.saveBrain("bot_brain.brn")

	# kernel now ready for use
	while True:
	    if message == "quit":
	        exit()
	    elif message == "save":
	        kernel.saveBrain("bot_brain.brn")
	    else:
	        bot_response = kernel.respond(message)
	        # print bot_response
	        return jsonify({'status':'OK','answer':bot_response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
