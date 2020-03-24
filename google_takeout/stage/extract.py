"""Extract data from zipfiles"""

import logging
from pathlib import Path
import typing
import zipfile

DATA_ZIPPED = "google_takeout/data/raw"
DATA_UNZIPPED = "google_takeout/data"  # unzipped results will combine into "google_takeout/data/Takeout"

LOG = logging.getLogger(__name__)


def get_all_files(directory: str, ext: str) -> typing.List[Path]:
    directory = Path(directory)
    ext = ext.lower()
    return [f for f in directory.iterdir() if f and ext in f.suffixes]


def extract_file(filename: Path, destination: Path):
    with zipfile.ZipFile(filename, "r") as zipped:
        zipped.extractall(destination)


def extract_data_from_zipfiles():
    all_files = get_all_files(DATA_ZIPPED, ".zip")
    LOG.info(
        "found {n_files} file(s) in {zipped} to unzip".format(
            n_files=len(all_files), zipped=DATA_ZIPPED
        )
    )
    output_folder = Path(DATA_UNZIPPED)
    for f in all_files:
        LOG.info("unzipping {f}".format(f=str(f)))
        extract_file(f, output_folder)
    LOG.info(
        "Successfully unzipped {n_files} files into {output}".format(
            n_files=len(all_files), output=output_folder
        )
    )
