"""Common CLI methods"""
import logging
import click

DEFAULT_VERBOSITY = 1

opt_verbosity = click.option(
    "-v",
    "--verbosity",
    count=True,
    default=DEFAULT_VERBOSITY,
    help="Increase the logging verbosity",
)


def configure_logging(verbose: int) -> bool:
    """Consistently configure logging."""

    if verbose == 1:
        level = logging.INFO
    elif verbose >= 2:
        level = logging.DEBUG
    else:
        level = logging.WARN

    logging.basicConfig(level=level)
