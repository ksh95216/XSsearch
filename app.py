from core import *
from urllib.parse import urlparse
from urllib.error import URLError, HTTPError
from flask import Flask,request,render_template,url_for,redirect,g,session,url_for
import sqlite3
import hashlib
import json
import os

app = Flask(__name__, static_url_path="/static/", static_folder="./templates/static/")
USER_DATABASE = 'users.db'
REPORT_DATABASE = 'report.db'
app.secret_key = os.urandom(24)

def vaild_url(url):

	url_scheme = urlparse(url).scheme
	url_domain = urlparse(url).netloc

	if(url_scheme == ''):
	
		return False

	if(url_domain == ''):
	
		return False
	
	if(url_scheme == 'http' or url_scheme == 'https'):

		if(url_domain == 'localhost' or url_domain == '127.0.0.1'):

			return False
		else:
			return url

def load_userdb():

	if not hasattr(g, 'users.db'):
	
		db = sqlite3.connect(USER_DATABASE)
	
	db.row_factory = sqlite3.Row
	return db

def load_reportdb():

	if not hasattr(g, 'report.db'):

		db = sqlite3.connect(REPORT_DATABASE)

	db.row_factory = sqlite3.Row
	return db

@app.teardown_appcontext
def close_connection(exception):

	if hasattr(g, 'users.db'):

		g.db.close()


@app.route('/', methods=["GET","POST"])
def index():

        return render_template('index.html')

@app.route('/api/logout', methods=["GET"])
def logout():

	if session.get('user') == None:

		return json.dumps({'success':"false", "msg":"You are not logged"})

	session.pop('user', None)
	return json.dumps({"success":"true", "msg":"Logout Success"})


@app.route('/api/login', methods=["POST"])
def login():

	if session.get('user') != None:

		return json.dumps({'success':"false","msg":"You are already logged"})

	username = request.form.get('username')
	password = request.form.get('password')

	db = load_userdb()
	cursor = db.cursor()
	query = cursor.execute("SELECT username FROM users where username = ? AND password = ?", (username, hashlib.sha256(password.encode()).hexdigest())).fetchone()

	if query:
	
		session['user'] = query['username']
		return json.dumps({"success":"true","msg":"Login Success"});

	else:

		return json.dumps({"success":"false","msg":"Login Fail"});


@app.route('/api/register', methods=["POST"])
def register():

	if session.get('user') != None:

		return json.dumps({'success':"false","msg":"You are already logged"})

	username = request.form.get('username')
	password = request.form.get('password')

	db = load_userdb()
	cursor = db.cursor()
	query = cursor.execute("SELECT * FROM users where username = ?", (username,)).fetchone()

	if query:

		return json.dumps({"success":"false", "msg": "User already exist"});


	query2 = "INSERT INTO users(username, password) VALUES (?,?)"
	query_exec = cursor.execute(query2, (username, hashlib.sha256(password.encode()).hexdigest()))
	db.commit()

	if not query_exec:
	
		return json.dumps({"success":"false","msg":"DB Error"});
	
	return json.dumps({"success":"true", "msg":"Register Success"});

@app.route('/api/search', methods=["POST"])
def search():
    
	if session.get('user') == None:

		return json.dumps({'success':"false","msg":"You are not logged"})
	
	url = request.form.get('url')
	use_cookie = request.form.get('use_cookie')

	check_url = vaild_url(url)

	if(check_url == False):

		return json.dumps({"success":"false", "msg": "Invaild URL"})

	if(use_cookie == 'true'):

		cookie = request.form.get('cookie')
		parser = XSsearch(url=url,cookies=cookie)
		parser.run()
		result = parser.result
		return json.dumps(result)

	else:

		parser = XSsearch(url=url,cookies={})
		parser.run()
		result = parser.result
		return json.dumps(result)


@app.route('/api/status', methods=["GET"])
def status():

	logined = True if session.get('user') else False
	return json.dumps({"success":logined, "msg":"Logged"})
	

@app.route('/api/report', methods=["POST"])
def report():

	if session.get('user') == None:
   
		return json.dumps({'success':"false","msg":"You arg not logged"})
	
	url = request.form.get('url')	

	if(vaild_url(url) == False):
	
		return json.dumps({"success":"false","msg":"Invaild URL"})
	
	
	username = session.get('user')
	db = load_reportdb() 
	cursor = db.cursor()
	
	query = "INSERT INTO report(username, url) VALUES (?,?)"
	query_exec = cursor.execute(query, (username, url))
	db.commit()

	if not query_exec:

		return json.dumps({"success":"false","msg":"DB Error"})
	
	return json.dumps({"success":"true", "msg":"Report Success"})


app.run('0.0.0.0',8080)
