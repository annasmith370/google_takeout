"""Load data into sqlite"""
import logging

LOG = logging.getLogger(__name__)


def init_db(refresh: bool = False):
    LOG.info("Initializing database")


def init_tables(refresh: bool = False):
    LOG.info("Initializing tables")
