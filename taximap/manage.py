#!/usr/bin/env python
import os
import shutil
import glob
from app import create_app, db
from app.models import *
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
from config import config, Config

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]


# get config
app = create_app(os.getenv('CONF_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


@migrate.configure
def configure_alembic(c):
    # modify config object
    c.set_main_option('compare_type', 'True')
    return c


def make_shell_context():
    return dict(app=app, db=db, Taxi=Taxi)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
# manager.add_command('runserver', Server(threaded=True))


@manager.command
def test_logging():
    """test logging"""
    app.logger.error('This is a error log test')
    app.logger.info('This is a info log test')


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    # run the app in tesing configration
    app.config.from_object(config['testing'])
    config['testing'].init_app(app)
    # Remove the sqlite database files if exist
    for fl in glob.glob("data-test.sqlite"):
        os.remove(fl)
        print("old test sqlite database removed")

    deploy()  # redeploy the database
    fakedata()  # generate the fakedata
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests).wasSuccessful()

    # the exit code is used for CircleCI
    import sys

    if result:  # tests passed
        sys.exit(0)
    else:  # tests failed
        sys.exit(1)

    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/calendar.html' % covdir)
        COV.erase()

    # Remove the sqlite database files if exist after test
    for fl in glob.glob("data-test.sqlite"):
        os.remove(fl)
        print("testing sqlite database removed")


@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


# run the db migration script
# this creates all tables when first run, after that
# if the database has no changes, nothing happens
@manager.command
def deploy():
    """initialize the database and populate init data"""
    from flask_migrate import init, migrate, upgrade

    upgrade()  # upgrade to the latest db schema



# Caution!!!: this reset db migration and related sqlite files
# The name is designed on purpose to highlight the potential danger
@manager.command
def reset_db_danger():
    """reset db migration and delete all related files"""
    from flask_migrate import init, migrate, upgrade
    # Remove the migration folder if exist
    if os.path.exists("migrations"):
        shutil.rmtree("migrations")

    # Remove the sqlite database files if exist
    for fl in glob.glob("*.sqlite"):
        os.remove(fl)

    # Reset Migration Database
    init()

    # migrate database to latest revision
    migrate(message='init')


@manager.command
def testconfs(email='harryjwang@gmail.com'):
    """Generate fake pending confs"""
    Conference.generate_fake_confs(10, email)  # create 10 pending conferences


@manager.command
def fakedata():
    """Generate fake testing data"""
    if Student.query.filter_by(email='chair@conferency.com').first():
        print("fake data already generated")
    else:
        Course.generate_fake_courses()
        Timeslot.generate_fake_timeslots()
        Student.generate_fake_users()


if __name__ == '__main__':
    manager.run()
