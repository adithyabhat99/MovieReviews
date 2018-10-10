from flask import Flask,render_template,request,session
#from werkzeug import generate_password_hash, check_password_hash
from flask_session import Session
from flaskext.mysql import MySQL
app=Flask(__name__)
mysql = MySQL(app)
SESSION_TYPE='memcache'
app.secret_key='secret'
app.config['SESSION_TYPE']='filesystem'
sess=Session()
sess.init_app(app)
adpass='123654654'

Session(app)
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123654654'
app.config['MYSQL_DATABASE_DB'] = 'users'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def hello():
	return(render_template('index.html'))

@app.route('/login.html')
def login():
	return(render_template('login.html'))
@app.route('/sign.html')
def signin():
	return(render_template("sign.html"))
@app.route('/signin',methods=['POST','GET'])
def sign():
	if request.method=='POST':
		fusr=request.form['usr']
		fpassw=request.form['passw']
		if fusr and fpassw:
			conn = mysql.connect()
			cursor=conn.cursor()
			#hashed_password = generate_password_hash(fpassw)
			query="insert into users.user(usr,passw) values('{0}','{1}');".format(fusr,fpassw)
			cursor.execute(query)
			data=cursor.fetchall()
			if len(data) is 0:
				conn.commit()
				return '<h1>Success</h1><br><a href="page1.html">Click to continue</a>'
			else:
				return '<h1>Error</h1>'
		else:
			return '<h1>Enter all the fields</h1>'
@app.route('/login',methods=['POST','GET'])
def log():
	fusr=request.form['usr']
	fpassw=request.form['passw']
	if fusr and fpassw:
		conn=mysql.connect()
		cursor=conn.cursor()
		#hashed_password = generate_password_hash(fpassw)
		query="select * from users.user where usr='{0}' and passw='{1}'".format(fusr,fpassw)
		cursor.execute(query)
		data=cursor.fetchone()
		if data is None:
			return '<h1>Username or Password is wrong</h1><br><a href="login.html">Login</a><br><a href="signin.html"</a>'
		else:
			session['usr']=fusr
			return(render_template('page1.html',usr=fusr))
	else:
		return '<h1>Enter all the fields</h1><br><a href="login.html">Login</a><br><a href="signin.html"</a>'


@app.route('/page1.html')
def page1():
	return(render_template('page1.html'))

@app.route('/feedback',methods=['POST','GET'])
def feed():
	feedback=request.form['feedback']
	conn=mysql.connect()
	cursor=conn.cursor()
	query="insert into users.feedback(usr,feedback) values('{0}','{1}')".format(session['usr'],feedback)
	try:
		cursor.execute(query)
		conn.commit()
		return '<h1>Feedback sent succesfully :)</h1>'
	except:
		return '<h1>Eroor :(</h1>'

@app.route('/adminlog.html')
def adlog():
	return(render_template('adminlog.html'))

@app.route('/admin',methods=['POST'])
def admin():
	passw=request.form['passw']
	if passw==adpass:
		return(render_template('admin.html'))
	else:
		return "<h1>Wrong Password</h1>"
@app.route('/review',methods=['POST'])
def review():
	ftitle=request.form['title']
	freview=request.form['review']
	conn=mysql.connect()
	cursor=conn.cursor()
	query="insert into users.reviews(title,review) values('{0}','{1}')".format(ftitle,freview)
	cursor.execute(query)
	data=cursor.fetchall()
	if ftitle and freview:
		if len(data) is 0:
			conn.commit()
			return '<h1>Success</h1>'
		else:
			return '<h1>Error</h1>'
	else:
		return "<h1>Enter all the fields</h1>"


if __name__=='__main__':
	app.run(debug=True)
