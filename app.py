from flask import Flask,render_template,request
from werkzeug import generate_password_hash, check_password_hash
from flaskext.mysql import MySQL
app=Flask(__name__)
mysql = MySQL(app)
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
				return '<h1>Success</h1>'
			else:
				return '<h1>Error</h1>'
		else:
			return '<h1>Enter all the fields</h1>'
if __name__=='__main__':
	app.run(debug=True)
