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
fusr=0;

@app.route('/',defaults={'path':''})
def hello(path):
	return(render_template('index.html'))
@app.route('/<path:path>')
def get_dir(path):
	if 'usr' in session:
		return(render_template('{}'.format(path)))
	else:
		return(render_template('login.html'))

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
			query2="select * from users.user where usr='{}';".format(fusr)
			cursor.execute(query2)
			data=cursor.fetchall()
			if len(data) is 0:
				cursor.execute(query)
				data=cursor.fetchall()
				if len(data) is 0:
					conn.commit()
					return '<h1>Success</h1><br><a href="page1.html">Click to continue</a>'
				else:
					return '<h1>Error</h1>'
			else:
				return '<h1>Username already exists</h1>'
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

@app.route('/logout')
def logout():
	session.pop('usr',None)
	x=1
	if x==1:
		return "<h1>Logged out successfully</h1><a href='sign.html'>SignUp</a><br><a href='login.html'>Login</a><br><a href='adminlog.html'>Admin</a><br>"

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
			convert(ftitle,freview)
			return '<h1>Success</h1>'
		else:
			return '<h1>Error</h1>'
	else:
		return "<h1>Enter all the fields</h1>"

@app.route('/admin.html')
def admin_page():
	return(render_template('adminlog.html'))

@app.route('/home.html')
def home():
	conn=mysql.connect()
	cursor=conn.cursor()
	query="select title from users.reviews;"
	cursor.execute(query)
	data=cursor.fetchall()
	return(render_template('home.html',data=data))

@app.route('/feedback.html')
def fee():
	conn=mysql.connect()
	cursor=conn.cursor()
	query="select * from users.feedback"
	cursor.execute(query)
	data=cursor.fetchall()
	return(render_template('feedback.html',data=data))

def convert(title,review):
	x='templates/re{}.html'.format(title)
	y=open(x,'w')
	z="""<!DOCTYPE html><html><head> <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous"></head><body><h1>{0}</h1><h2>{1}</h2><form action='feedback' method='POST' >Feedback<input type='text' name='feedback'><input type='submit' value='feedb'></form><a href='home.html'>Home</a><br><a href='logout'>Logout</a></body></html>""".format(title,review)
	y.write(z)
	y.close()

if __name__=='__main__':
	app.run(debug=True)
