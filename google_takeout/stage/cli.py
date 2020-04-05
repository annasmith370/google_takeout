"""For all commands related to staging data"""

import re
import click

from google_takeout import common_cli
from google_takeout.stage import extract  # , load
from google_takeout.stage.products import PRODUCTS


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

    if not skip_extraction:
        # load.init_db()
        # load.init_tables()
        pass


def product_command_name(name: str) -> str:
    """Camel case to hyphened snake case"""
    return re.sub(
        "([a-z0-9])([A-Z])", r"\1-\2", re.sub("(.)([A-Z][a-z]+)", r"\1-\2", name)
    ).lower()


def get_all_products(products=PRODUCTS):
    return {product_command_name(product.__name__): product for product in products}


@click.group()
def product():
    pass


@product.command()
@common_cli.opt_verbosity
@click.option(
    "--full-refresh/--incremental",
    default=False,
    help="Do a full refresh on the database.",
)
@click.argument("name")
def load(verbosity: int, full_refresh: bool, name: str):
    common_cli.configure_logging(verbosity)

    all_products = get_all_products()
    try:
        all_products[name]().run()
    except KeyError:
        available = ", ".join(all_products.keys())
        raise KeyError(f"Unknown product name `{name}`. Available options: {available}")


@product.command()
def list():
    all_products = get_all_products()

    available = "\nAvailable product commands:\n   - " + "\n   - ".join(
        all_products.keys()
    )
    print(available)
