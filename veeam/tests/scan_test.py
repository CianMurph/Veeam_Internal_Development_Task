import sync
import pathlib
import os

def scan_returns_dict():
    test_dir = str(pathlib.Path(__file__).parent.resolve())
    test_case_dir = test_dir + "/"
    assert sync.scan_folder