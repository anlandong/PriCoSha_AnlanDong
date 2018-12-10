from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
##Initialize the app from Flask    
#app = Flask(__name__)

##Configure MySQL

#conn = pymysql.connect(host='localhost',
#                       port=3306,
#                       user='root',
#                       password='',
#                       db='pricosha',
#                       charset='utf8mb4',
#                       cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)
#engine = create_engine('mysql+mysqlconnector://root:@localhost/pricosha')
#connection = engine.connect()
app.config['SECRET_KEY'] = '62258ec2ae3075a22c3406cca7c90f35'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/pricosha'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'



import DBProject.views


