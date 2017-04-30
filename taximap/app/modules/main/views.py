from flask import render_template, redirect, url_for, abort, flash, request, \
    current_app, make_response, jsonify, json
from flask_sqlalchemy import get_debug_queries
from sqlalchemy import or_, and_
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm, \
    CommentForm, TicketOrderForm, RegistrationForm
from ... import db
from ...models import *
from ...utils.decorators import chair_required, permission_required
from werkzeug.exceptions import RequestEntityTooLarge
from ...utils.email_operation import send_email
from ...utils.macros import split_on_comma_and_trim, check_date
import stripe
import os


# Set cache control to private
@main.after_request
def add_header(response):
    response.cache_control.private = True
    response.cache_control.public = False
    return response


# @main.before_app_first_request
# def before_request():
#     current_user.set_conference_id(1)


# *****Landing Page*****
@main.route('/')
def index():
    # if the user is logged in, redirect to dashboard
    return render_template('/site/calendar.html')


# *****Mapping Page*****
@main.route('/taxi/<int:taxi_id>/<string:_from>')
def map(taxi_id, _from):
    # if the user is logged in, redirect to dashboard
    limit = request.args.get('limit', 50)
    offset = request.args.get('offset', 0)
    from_type = request.args.get('f', 3)
    to_type = request.args.get('t', 5)

    records = Taxi.query.filter_by(id=taxi_id).offset(offset).limit(limit).all()
    return render_template('/site/' + _from + '_map.html', taxi_id=taxi_id, records=records, from_type=from_type, to_type=to_type)
