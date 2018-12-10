from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, ValidationError
from DBProject import app, db
from wtforms.validators import DataRequired, Length, Email, EqualTo
from DBProject.model import User, Post, FriendGroup, belong, rate, share, tag
import DBProject.views 
from flask_login import login_user, current_user, logout_user, login_required

class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators = [ DataRequired(), Email()])
    first_name = StringField('Frist Name',
                                     validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name',
                                     validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(id=email.data).first()
        if user: 
            raise ValidationError('An Account with this email already exists. Please choose a different one')
        print('form_validated')
        


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    item_name = StringField('Title', validators=[DataRequired()])
    file_path = StringField('FilePath', validators=[DataRequired()])
    shared_group = StringField('Share To Friend Groups')
    is_public = SelectField('Visibility:', choices=[(1,'Public'),(0,'Private')], coerce=int)
    
    submit = SubmitField('Post')

    #def validate_group_ownership(self, shared_group):
    #    groups = FriendGroup.query.filter_by(fg_name = shared_group).all()
    #    group_owner = [gp.id for gp in groups] 
    #    if (current_user.get_id() not in group_owner)
    #        raise ValidationError('You do not own this group!')
    #    print('form_validated')

    


class FriendGroupForm(FlaskForm):
    fg_name = StringField('Friend Group Name', 
                          validators = [ DataRequired()])
    description = StringField('Description(1000 Words Max)')
    submit = SubmitField('Create Group')

class AddMemForm(FlaskForm):
    email = StringField('Email for the person to be added', 
                        validators = [DataRequired(), Email()])
    submit = SubmitField('Add Member')

    def validate_email(self, email):
        user = belong.query.filter_by(email = email.data).first()
        if user:
            raise VaildationError('User is already a member')

class RateForm(FlaskForm):
    emoji = StringField('Emoji', validators = [DataRequired()])
    
    submit = SubmitField('Rate')

class TagForm(FlaskForm):
    tagged = StringField('Tag by email', validators = [DataRequired(), Email()])
    submit = SubmitField('Tag')

class TagApprovalForm(FlaskForm):
    status = SelectField('Action:', choices=[('Approved','Approve'),('Denied','Deny')])
    submit = SubmitField('Confirm')