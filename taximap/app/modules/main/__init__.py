from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors

# A context processor is a function that returns a dictionary.
@main.app_context_processor
def inject_permissions():
    return dict()

# @main.app_context_processor
# def inject_session():
	# print "&&&&&&&&&&&"
	# print session['conference_id']
	# conference = Conference.query.filter_by(id=session['conference_id']).first()
	# print conference.id
	# return dict(current_conference=conference)
	# return dict(current_conference_id=session['conference_id'])