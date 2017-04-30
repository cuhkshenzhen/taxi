from collections import OrderedDict
from flask import url_for
from flask_login import current_user


def generate_navigation_bar(current_user):
    navigation_bar = OrderedDict()
    if current_user.is_administrator():
        navigation_bar["dashboard"] = (
            '/dashboard', 'fa fa-tachometer', 'Dashboard', None)
        navigation_bar["conferences"] = ('', 'fa fa-list', 'Conferences',
                                         OrderedDict([
                                             ('admin-requests', (url_for('admin.admin_requests'),
                                              'Conference Requests')),
                                             ('admin-registrations', (url_for('admin.admin_registrations'),
                                              'Conference Registrations'))
                                         ])
                                         )
        navigation_bar['user_search'] = (
            '/user', 'fa fa-search', 'User Directory', None)
    else:
        navigation_bar["dashboard"] = (
            '/dashboard', 'fa fa-tachometer', 'Dashboard', None)
        navigation_bar["submissions"] = ('', 'fa fa-file-text-o', 'Submissions',
                                         OrderedDict([
                                             ("add-submissions",
                                              (url_for('submission.add_submission'), 'Add Submissions')),
                                             ("my-submissions",
                                              (url_for('submission.my_submissions'), 'My Submissions'))
                                         ])
                                         )
        navigation_bar["reviews"] = ('', 'fa fa-star-o', 'Reviews',
                                     OrderedDict([
                                         ('add-reviews', (url_for('review.add_review'),
                                                          'Add/Update Reviews')),
                                         ('my-reviews',
                                          (url_for('review.my_reviews'), 'My Reviews'))
                                     ])
                                     )
        navigation_bar["conferences"] = ('', 'fa fa-list', 'Conferences',
                                         OrderedDict([
                                             ('my-conferences',
                                              (url_for('conference.my_conference'), 'My Conferences')),
                                            #  ('all-conferences',
                                            #   (url_for('conference.all_conference'), 'All Conferences')),
                                             ('request-conferences', (url_for('conference.request_conference'),
                                                                      'Request New Conferences'))
                                         ])
                                         )
        navigation_bar['connections'] = (
            '/followed-by/' + str(current_user.id), 'fa fa-group', 'My Connections', None)
        navigation_bar['user_search'] = (
            '/user', 'fa fa-search', 'User Directory', None)

        if current_user.is_chair(current_user.curr_conf):
            navigation_bar['conferenceRegistration'] = ('', 'fa fa-book', 'Registration',
                                                        OrderedDict([
                                                            ('set_registration', (url_for(
                                                                'conference.set_registration', conference_id=current_user.curr_conf_id), 'Registration Settings')),
                                                            ('set_registration_form', (url_for('conference.set_registration_form',
                                                                                               conference_id=current_user.curr_conf_id), 'Registration Form')),
                                                            ('registration_summary', (url_for('conference.registration_summary',
                                                                                              conference_id=current_user.curr_conf_id), 'Sales Summary')),
                                                            ('registration_recent_orders', (url_for(
                                                                'conference.registration_recent_orders', conference_id=current_user.curr_conf_id), 'Orders'))
                                                        ])
                                                        )
            #navigation_bar['website'] = (url_for('website.website_builder'), 'fa fa-sitemap', 'Website', None
                                        #  OrderedDict([
                                        #      ('index', (url_for(
                                        #          'website.page', page_id=current_user.curr_conf.site.pages.all()[0].id), 'Index'))
                                        #  ])
                                         #)

            navigation_bar['conferenceManagement'] = ('', 'fa fa-cogs', 'Administration',
                                                      OrderedDict([
                                                          # ('all-submissions', (url_for('conference.conferences_submission',
                                                          #                              conference_id=current_user.curr_conf_id), 'All Submissions')),
                                                          ('submission_menu', ('', 'Submission', OrderedDict([
                                                                        ('all-submissions', (url_for('conference.conferences_submission', conference_id=current_user.curr_conf_id), 'All Submissions')),
                                                          ])
                                                          )),
                                                          ('review_menu', ('', 'Review', OrderedDict([
                                                              ('all-reviews', (url_for('conference.conferences_review',
                                                                                       conference_id=current_user.curr_conf_id), 'All Reviews')),
                                                              ('manual-assignment', (url_for('conference.conferences_assignment_manual',
                                                                                             conference_id=current_user.curr_conf_id), 'Review Assignments')),
                                                              ('review-decision', (url_for('conference.conferences_decision_review',
                                                                                           conference_id=current_user.curr_conf_id), 'Review Decisions')),
                                                              ('review_set', (url_for('conference.conference_review_setting',
                                                                                      conference_id=current_user.curr_conf_id), 'Review Form')),
                                                          ])
                                                          )),
                                                          # ('all-reviews', (url_for('conference.conferences_review',
                                                          #                          conference_id=current_user.curr_conf_id), 'All Reviews')),
                                                          # ('manual-assignment', (url_for('conference.conferences_assignment_manual',
                                                          #                                conference_id=current_user.curr_conf_id), 'Review Assignments')),
                                                          # ('review-decision', (url_for('conference.conferences_decision_review',
                                                          #                              conference_id=current_user.curr_conf_id), 'Review Decisions')),
                                                          # ('review_setting', (url_for('conference.conference_review_setting', conference_id=current_user.curr_conf_id), 'Review Settings')),
                                                          ('member-roles', (url_for('conference.conferences_members',
                                                                                    conference_id=current_user.curr_conf_id), 'Members')),
                                                          ('invitations', (url_for(
                                                              'conference.invitations', conference_id=current_user.curr_conf_id), 'Invitations')),
                                                          ('notify', (url_for(
                                                              'conference.send_notification', conference_id=current_user.curr_conf_id), 'Notifications')),
                                                          ('tracks', (url_for(
                                                              'conference.tracks'), 'Tracks')),
                                                          ('setting', (url_for('conference.conferences_setting',
                                                                               conference_id=current_user.curr_conf_id), 'Settings')),
                                                      ])
                                                      )

        if current_user.curr_conf_id == 1:
            navigation_bar['submissions'][3].pop('add-submissions')
            navigation_bar['reviews'][3].pop('add-reviews')

    return navigation_bar


def get_date_str(date):
    date = date + 1
    repr = {1: 'Monday',
            2: 'Tuesday',
            3: 'Wednesday',
            4: 'Thursday',
            5: 'Friday'}
    return repr[date]