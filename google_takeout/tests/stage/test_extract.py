
import pathlib
import pytest
from google_takeout.stage import extract

def test_get_all_files(tmpdir):
    # Create some fake files
    tmpdir.join("textfile1.txt").write("blah")
    tmpdir.join("textfile2.txt.zip").write("blah")
    tmpdir.join("not_textfile.note").write("blah")

    # fetch the fake files
    files_txt = extract.get_all_files(tmpdir, ".txt")
    assert len(files_txt) == 2

    # confirm case doesn't matter
    files_TXT = extract.get_all_files(tmpdir, ".TXT")
    assert files_txt == files_TXT

    # should not find anything
    files_beets = extract.get_all_files(tmpdir, ".beets")
    assert len(files_beets) == 0
