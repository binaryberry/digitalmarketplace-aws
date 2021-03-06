import sys

import click

from ..cli import cli_command
from ..stacks import StackPlan
from ..build import get_application_name


@click.argument('repository_path', nargs=1, type=click.Path(exists=True))
@cli_command('deploy', max_apps=0)
def deploy_cmd(ctx, repository_path):
    """Deploy a new application version to the Elastic Beanstalk environment.

    """

    app = get_application_name(repository_path)
    ctx.add_apps(app)
    deploy = StackPlan.from_ctx(ctx).get_deploy(repository_path)

    version, created = deploy.create_version(app, with_sha=True)
    url = deploy.deploy(version)

    if not url:
        sys.exit(1)

    ctx.log("URL: http://%s/", url)
