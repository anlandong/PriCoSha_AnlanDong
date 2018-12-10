
from datetime import datetime
from DBProject import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_email):
    return User.query.get(user_email)

class User(db.Model, UserMixin):
    __tablename__ = 'person'
    id = db.Column('email', db.String(50),primary_key=True)
    password = db.Column('password', db.String(50))
    fname = db.Column('fname', db.String(20))
    lname = db.Column('lname', db.String(20))
    def __repr__(self):
        return f"User('{self.email}', '{self.fname}', '{self.lname}')"

class Post(db.Model):
    __tablename__ = 'contentitem'
    id = db.Column('item_id', db.Integer, primary_key = True, autoincrement=True)
    email = db.Column('email_post', db.String(50))
    post_time = db.Column('post_time', db.TIMESTAMP, default=datetime.utcnow)
    file_path = db.Column('file_path', db.String(100))
    item_name = db.Column('item_name', db.String(20)) 
    is_public = db.Column('is_pub', db.Integer) #0 for private; 1 for public
    
    def __repr__(self):
        return f"Post('{self.id}', '{self.email}', '{self.file_path}')"

class FriendGroup(db.Model):
    __tablename__ = 'friendgroup'
    id = db.Column('owner_email',db.String(50), primary_key=True)
    fg_name = db.Column('fg_name', db.String(20), primary_key=True)
    desicription = db.Column('description', db.String(1000))

    def __repr__(self):
        return f"Post('{self.id}', '{self.fg_name}')"

class belong(db.Model):
    __tablename__ = 'belong'
    email = db.Column('email', db.String(50), primary_key=True)
    owner_email = db.Column('owner_email', db.String(50), primary_key=True)
    fg_name = db.Column('fg_name', db.String(20), primary_key=True)

    def __repr__(self):
        return f"Post('{self.id}', '{self.fg_name}')"

class rate(db.Model):
    __tablename__ = 'rate'
    id = db.Column('email', db.String(50), primary_key=True)
    item_id = db.Column('item_id', db.Integer, primary_key=True)
    rate_time = db.Column('rate_time', db.TIMESTAMP, default=datetime.utcnow)
    emoji = db.Column('emoji', db.String(20))

    def __repr__(self):
        return f"Post('{self.email}', '{self.item_id}')"

class share(db.Model):
    __tablename__ = 'share'
    owner_email = db.Column('owner_email', db.String(50), primary_key=True)
    item_id = db.Column('item_id', db.Integer, primary_key=True)
    fg_name = db.Column('fg_name', db.String(20), primary_key=True)

    def __repr__(self):
        return f"Post('{self.ower_email}', '{self.item_id}', '{self.fg_name}')"

class tag(db.Model):
    __tablename__ = 'tag'
    tagger = db.Column('email_tagger', db.String(50), primary_key=True)
    tagged = db.Column('email_tagged', db.String(50), primary_key=True)
    item_id = db.Column('item_id', db.Integer, primary_key=True)
    status = db.Column('status', db.String(20), default='Pending')

    def __repr__(self):
        return f"Post('{self.tagger}', '{self.tagged}', '{self.item_id}', '{self.status}')"

