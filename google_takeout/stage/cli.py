"""For all commands related to staging data"""

import click

from google_takeout import common_cli
from google_takeout.stage import extract, load


@click.command()
@common_cli.opt_verbosity
@click.option(
    "--skip-extraction/--run-extraction",
    default=False,
    help="Skip zipfile extraction.",
)
@click.option(
    "--full-refresh/--incremental",
    default=False,
    help="Do a full refresh on the database.",
)
def stage(verbosity: int, skip_extraction: bool, full_refresh: bool):
    common_cli.configure_logging(verbosity)

    if not skip_extraction:
        extract.extract_data_from_zipfiles()
