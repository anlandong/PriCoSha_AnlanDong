#Import Flask Library
import hashlib
from wtforms import ValidationError
from forms import RegistrationForm, LoginForm, PostForm, FriendGroupForm, AddMemForm, RateForm, TagForm,TagApprovalForm
from DBProject import app, db
from flask import Flask, render_template, request, session, url_for, redirect, flash, redirect, abort
from flask_login import login_user, current_user, logout_user, login_required
from DBProject.model import User, Post, FriendGroup, belong, rate, share, tag
import pymysql.cursors


###Initialize the app from Flask    
##app = Flask(__name__)

#Configure MySQL

conn = pymysql.connect(host='localhost',
                       port = 3306,
                       user='root',
                       password='',
                       db='pricosha',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
    print('hello')
    return render_template('index.html')

@app.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    posts = Post.query.filter_by(is_public=1).all()
    ratings = rate.query.all()
    tags = tag.query.filter_by(status = 'Approved').all()
    pending_tags = tag.query.filter_by(tagged=current_user.get_id(), status="Pending").all()
    fgs_own = FriendGroup.query.filter_by(id = current_user.get_id()).all()
    belongs = belong.query.filter_by(email = current_user.get_id()).all()
    return render_template('home.html', posts = posts, fgs_own = fgs_own, belongs = belongs, pending_tags = pending_tags, ratings = ratings, tags = tags)

@app.route('/register', methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    print('register')
    if form.validate_on_submit():
        print('viewsvalidated')
        hashed_passward = hashlib.sha256(form.password.data.encode('utf-8')).hexdigest()
        print(hashed_passward)
        user = User(id=form.email.data, password=hashed_passward,fname=form.first_name.data, 
                    lname=form.last_name.data)
        print('usr created')
        db.session.add(user)
        db.session.commit()
        print('usr commited')
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register', form=form)

@app.route('/login', methods = ['GET','POST'])
def login():
    print('login')
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm() 
    if form.validate_on_submit():
        print('validating')
        hashed_passward = hashlib.sha256(form.password.data.encode('utf-8')).hexdigest()
        user = User.query.filter_by(id = form.email.data).first()
        if user and (user.password == hashed_passward):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    print('error')
    return render_template('login.html',title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('hello'))

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    fgs_own = FriendGroup.query.filter_by(id = current_user.get_id()).all()
    belongs = belong.query.filter_by(email = current_user.get_id()).all()
    form = PostForm()
    if form.validate_on_submit():
        post = Post(email = current_user.get_id(), file_path=form.file_path.data,
                   item_name = form.item_name.data, is_public=form.is_public.data)
        db.session.add(post)
        db.session.commit()
        item_id = post.id
        if not form.shared_group.data:
           share_to = share(owner_email = current_user.get_id(), item_id = item_id, fg_name = form.shared_group.data)
           db.session.add(share_to)
           db.seession.commit()
        flash('Your post has been created!', 'Success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post', fgs_own = fgs_own, belongs = belongs)

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title='post.item_name', post=post)

@app.route('/create_fg', methods=['GET', 'POST'])
@login_required
def new_fg():
    form = FriendGroupForm()
    if form.validate_on_submit():
        fg = FriendGroup(id = current_user.get_id(), fg_name=form.fg_name.data , desicription=form.description.data)
        db.session.add(fg)
        db.session.commit()
        flash('Your friend group has been created!', 'Success')
        return redirect(url_for('home'))
    return render_template('create_fg.html', title='New Post', form=form)

@app.route('/add_people/<fg_name>', methods=['GET', 'POST'])
def add_people(fg_name):
    print('add_ppl')
    fg_name1 = fg_name
    form = AddMemForm()
    if form.validate_on_submit():
        member = belong(email = form.email.data, owner_email = current_user.get_id(), fg_name = fg_name1)
        db.session.add(member)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_member.html', title= 'New member', form = form)

@app.route('/post_manage/<user_id>', methods=['GET', 'POST'])
def post_manage(user_id):
     posts = Post.query.filter_by(email = user_id).all()
     return render_template('yourpost.html', posts = posts)

@app.route('/post/<int:post_id>/update', methods =['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.email != current_user.get_id():
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.item_name = form.item_name.data
        post.file_path = form.file_path.data
        post.is_public = form.is_public.data
        item_id = post.id
        update_share = form.shared_group.data
        if not update_share:
            share_to = share(owner_email = current_user.get_id(), item_id = item_id , fg_name = form.shared_group.data)
        db.session.add(share_to)
        db.session.commit()
    elif request.method == 'GET':
        form.item_name.data = post.item_name
        form.file_path.data = post.file_path
        form.is_public.data = post.is_public
    return render_template('create_post.html', title='Update Post', form = form, legend = 'Update Post')

@app.route('/post/<int:item_id>/rate', methods = ['GET', 'POST'])
@login_required
def add_rate(item_id):
    form = RateForm()
    if form.validate_on_submit():
        addrate = rate(item_id = item_id, emoji = form.emoji.data, id = current_user.get_id())
        db.session.add(addrate)
        db.session.commit()
        flash('Your rating is submitted', 'Success')
        return redirect(url_for('home'))
    return render_template('add_rating.html', title='New Rating', form = form)

@app.route('/post/<int:item_id>/tag', methods = ['GET', 'POST'])
@login_required
def add_tag(item_id):
    form = TagForm()
    if form.validate_on_submit():
        addtag = tag(tagged = form.tagged.data, tagger = current_user.get_id(), item_id=item_id)
        db.session.add(addtag)
        db.session.commit()
        flash('Your Tag is submitted. Waiting on Approval', 'Success')
        return redirect(url_for('home'))
    return render_template('add_tagging.html', title='New Tag', form = form)

@app.route('/post/<int:item_id>/tag_reaction', methods = ['GET', 'POST'])
@login_required
def tagged_action(item_id):
    form = TagApprovalForm()
    tagged = tag.query.filter_by(tagged = current_user.get_id(), item_id = item_id).first()
    if form.validate_on_submit():
        tagged.status = form.status.data
        db.session.commit()
        flash('Your Tag Action is confirmed.', 'Success')
        return redirect(url_for('home'))
    return render_template('tag_action.html', title='Confirm Tag', form = form)



#Individual Fucntions:
