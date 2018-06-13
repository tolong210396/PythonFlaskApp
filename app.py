from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask,render_template,jsonify,json,request
#from fabric.api import *

import bcrypt

app= Flask(__name__)

client = MongoClient('localhost:27017')
db = client.bankaccount

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route("/getaccount", methods = ['POST'])
def getaccount():
    try:
        listdb = db.AC.find()
        accountlist = []
        for ac in listdb:
            print ac
            acItem = {
                'account_number':ac['account_number'],
                'firstname':ac['firstname'],
                'lastname':ac['lastname'],
                'email':ac['email'],
                'address':ac['address'],
                'id': str(ac['_id'])
                }
            accountlist.append(acItem)
    except Exception,e:
        return str(e)
    return json.dumps(accountlist)

@app.route('/login', methods = ['POST'])
def login():
    login_user = db.AC.find_one({'email' : request.form['email']})

    if  login_user:
        # if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            passwd = db.AC.find_one({'password' : request.form['pass']})
            if passwd:
                return redirect(url_for('home'))
    return 'Invalid email/password combination'

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
         existing_user = db.AC.find_one({'username' : request.form['email']})

         if existing_user is None:

             name = request.form['name']
             hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
             users.insert({'name': request.form['name'], 'username' : request.form['email'], 'password' : hashpass})
             session['email'] = request.form['email']
             return redirect(url_for('find'))

         return ('that username already exists!')
    return render_template('register.html')  
    

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)