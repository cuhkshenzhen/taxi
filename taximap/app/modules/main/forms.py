from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, FileField, RadioField, HiddenField, SelectMultipleField, DateTimeField, IntegerField, widgets, DateField
from flask_wtf.file import FileAllowed
from wtforms.validators import Required, Length, Email, Regexp, URL, Optional
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ...models import *
from flask_login import current_user


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class EditProfileForm(Form):
    first_name = StringField(
        'First Name *', validators=[Required(), Length(1, 64)])
    last_name = StringField(
        'Last Name *', validators=[Required(), Length(1, 64)])
    organization = StringField(
        'Organization *', validators=[Required(), Length(1, 64)])
    country = StringField('Country *', validators=[Required()])
    state = StringField('State/Province', validators=[Length(0, 64)])
    location = StringField('City *', validators=[Required(), Length(1, 64)])
    website = StringField('Website')
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    confirmed = BooleanField('Confirmed')
    # a bug here
    # role = SelectField('Role', coerce=int)
    first_name = StringField('First Name', validators=[
                             Required(), Length(0, 64)])
    last_name = StringField('Last Name', validators=[
                            Required(), Length(0, 64)])
    location = StringField('City', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        # self.role.choices = [(role.id, role.name)
        # for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                Student.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class PostForm(Form):
    body = PageDownField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')


class CommentForm(Form):
    body = StringField('Enter your comment', validators=[Required()])
    submit = SubmitField('Submit')


class TicketOrderForm(Form):
    collection_type = RadioField('Collection type', choices=[('basic_info', 'Basic information'),
                                                             ('buy_only', 'Buyer only'), ('each_attendee', 'Each Attendee')], validators=[Required()])
    ticket_type = SelectMultipleField('Select information by ticket type', choices=[('early_acad', 'Early academic'),
                                                                                    ('early_stud', 'Early student')], validators=[Required()])
    email = StringField('Email', validators=[
                        Required(), Length(1, 64), Email()])


class RegistrationForm(Form):
    card_number = StringField('Credit card number', validators=[Required()])
    holder_name = StringField('Name on card', validators=[
                              Required(), Length(1, 128)])
    security_code = IntegerField('Security code', validators=[Required()])
    # expire_date = StringField('Expire date', validators=[
    #                           Required(), Length(1, 7)])
    month = SelectField('Month:', choices=[('1', 'Jan'), ('2', 'Feb'), ('3', 'Mar'), ('4', 'Apr'), ('5', 'May'),
                                           ('6', 'June'), ('7', 'July'), ('8', 'Aug'), ('9', 'Sept'), ('10', 'Oct'), ('11', 'Nov'), ('12', 'Dec')], validators=[Required()])
    year = SelectField('Year:', choices=[('2016', '2016'), ('2017', '2017'), ('2018', '2018'), (
        '2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025')], validators=[Required()])
    street = StringField('Street', validators=[Required(), Length(1, 128)])
    city = StringField('City', validators=[Required(), Length(1, 128)])
    state = StringField(
        'State/Province', validators=[Length(0, 128)])
    zipcode = IntegerField('Zip', validators=[Optional()])
    country = StringField('Country', validators=[Required()])
    # email = StringField('Buyer\'s mail', validators=[Required(), Email()])
    submit_button = SubmitField('Confirm')
    attendee_first_name = StringField('First name', validators=[
        Required(), Length(1, 128)])
    attendee_last_name = StringField('Last name', validators=[
        Required(), Length(1, 128)])
    attendee_email = StringField(
        'Email', validators=[Required(), Email()])
    attendee_affiliation = StringField('Affiliation', validators=[
        Required(), Length(1, 128)])
    tickets = RadioField(coerce=int, validators=[Required()])
    products = SelectMultipleField(coerce=int)
    promo_code = HiddenField()
    stripeToken = HiddenField()
