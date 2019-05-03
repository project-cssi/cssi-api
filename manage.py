#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) Copyright 2019 Brion Mario.
# (c) This file is part of the CSSI REST API and is made available under MIT license.
# (c) For more information, see https://github.com/brionmario/cssi-api/blob/master/LICENSE.txt
# (c) Please forward any queries to the given email address. email: brion@apareciumlabs.com

"""
Brief:   REST API for the CSSI library

Author:  Brion Mario
"""

import os
import subprocess
import sys
import eventlet

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Command, Server as _Server, Option

from app import create_app, db, socketio

eventlet.monkey_patch()

app = create_app(os.getenv('CSSI_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


class Server(_Server):
    help = description = 'Runs the Socket.IO web server'

    def get_options(self):
        options = (
            Option('-h', '--host',
                   dest='host',
                   default=self.host),

            Option('-p', '--port',
                   dest='port',
                   type=int,
                   default=self.port),

            Option('-d', '--debug',
                   action='store_true',
                   dest='use_debugger',
                   help=('enable the Werkzeug debugger (DO NOT use in '
                         'production code)'),
                   default=self.use_debugger),
            Option('-D', '--no-debug',
                   action='store_false',
                   dest='use_debugger',
                   help='disable the Werkzeug debugger',
                   default=self.use_debugger),

            Option('-r', '--reload',
                   action='store_true',
                   dest='use_reloader',
                   help=('monitor Python files for changes (not 100%% safe '
                         'for production use)'),
                   default=self.use_reloader),
            Option('-R', '--no-reload',
                   action='store_false',
                   dest='use_reloader',
                   help='do not monitor Python files for changes',
                   default=self.use_reloader),
        )
        return options

    def __call__(self, app, host, port, use_debugger, use_reloader):
        # override the default runserver command to start a Socket.IO server
        if use_debugger is None:
            use_debugger = app.debug
            if use_debugger is None:
                use_debugger = True
        if use_reloader is None:
            use_reloader = app.debug
        socketio.run(app,
                     host=host,
                     port=port,
                     debug=use_debugger,
                     use_reloader=use_reloader,
                     **self.server_options)


manager.add_command("runserver", Server())


class CeleryWorker(Command):
    """Starts the celery worker."""
    name = 'celery'
    capture_all_args = True

    def run(self, argv):
        ret = subprocess.call(
            ['celery', 'worker', '-A', 'app.celery', '--loglevel=info'] + argv)
        sys.exit(ret)


manager.add_command("celery", CeleryWorker())


@manager.command
def create_metadata():
    """Create the table metadata.

    Application types and Genres need to be added to the database
    in order for new applications to be added.
    """
    from app.models import Genre, ApplicationType

    Genre.seed()
    ApplicationType.seed()


@manager.command
def test():
    """Run the unit tests.

    This function will run the unit tests in the tests package.
    """
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def recreate_db(drop_first=False):
    """Recreates a local database

    Not safe to use in production.
    """
    if drop_first:
        db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    if sys.argv[1] == 'test' or sys.argv[1] == 'lint':
        # small hack, to ensure that Flask-Script uses the testing
        # configuration if we are going to run the tests
        os.environ['CSSI_CONFIG'] = 'testing'
    manager.run()
