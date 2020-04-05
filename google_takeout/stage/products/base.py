"""base product data extract method
"""


import logging
from pathlib import Path
import typing
import abc
from google_takeout.stage import extract


MAIN_TAKEOUT_FOLDER = "google_takeout/data/Takeout"

LOG = logging.getLogger(__name__)


class ProductExtractor(abc.ABC):
    @property
    @abc.abstractmethod
    def folder_location(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def tables(self) -> typing.List[str]:
        pass

    @abc.abstractmethod
    def parse_file(self, rawfile: Path) -> dict:
        pass

    def list_files(self) -> typing.List[Path]:
        folder = Path(MAIN_TAKEOUT_FOLDER) / self.folder_location
        res = extract.get_all_files(folder)
        LOG.info(f"Found {len(res)} files in {folder}")
        return res

    def initiate_tables(self):
        LOG.info(f"Initiating tables")
        # todo init tables

    def load_into_tables(self, data):
        for key, value in data.items():
            if not value:
                continue
            # todo load into tables

    def run(self):
        self.initiate_tables()
        for f in self.list_files():
            data = self.parse_file(f)
            self.load_into_tables(data)

            # LOG.info("Breaking early")
            # break
