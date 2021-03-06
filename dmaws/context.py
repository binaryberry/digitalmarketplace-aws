import os

import click
import six

from .utils import merge_dicts, dict_from_path, read_yaml_file
from .stacks import Stack


class Context(object):
    def __init__(self, home=os.getcwd(), dry_run=False):
        self.home = home
        self.dry_run = dry_run

        self.stage = None
        self.environment = None
        self.apps = []
        self.variables = {}
        self.stacks = {}
        self.create_dependencies = False

    def add_apps(self, app):
        if isinstance(app, six.string_types):
            app = [app]
        elif not app:
            app = []
        self.apps.extend([app_name.replace('-', '_') for app_name in app])

    def add_variables(self, variables):
        self.variables = merge_dicts(self.variables, variables)

    def add_variables_file(self, path):
        self.variables = merge_dicts(self.variables, read_yaml_file(path))

    def add_dotted_variable(self, path, value):
        self.variables = merge_dicts(self.variables,
                                     dict_from_path(path, value))

    def load_variables(self, files=None, pairs=None, variables=None):
        self.add_variables(variables or {})
        for path in (files or []):
            self.add_variables_file(path)
        for pair in (pairs or []):
            self.add_dotted_variable(*pair)

    def load_stacks(self, path):
        stacks = read_yaml_file(path)
        for key, val in stacks.items():
            if isinstance(val, dict):
                self.stacks[key] = Stack(**val)
            else:
                self.stacks[key] = val

    def log(self, msg, *args, **kwargs):
        """Logs a message to stderr."""
        if args:
            msg %= args
        if 'color' in kwargs:
            msg = click.style(msg, fg=kwargs['color'])
        click.echo(msg, err=True)


pass_context = click.make_pass_decorator(Context, ensure=True)
