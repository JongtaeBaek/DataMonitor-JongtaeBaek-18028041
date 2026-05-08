import os
import runpy
from unittest.mock import patch
from main import main


def test_main_all_choices(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    choices = ["1", "2", "3", "4", "invalid", "0"]
    with patch("builtins.input", side_effect=choices), patch("builtins.print"):
        main()


def test_main_entry_point(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with patch("builtins.input", return_value="0"), patch("builtins.print"):
        runpy.run_path(os.path.join(root, "main.py"), run_name="__main__")
