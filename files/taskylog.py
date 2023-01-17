"""
    Tasky is a task deadline tracker application
    Copyright (C) 2022-2023  Abhineet Kelley (AbhiK002)

    This file is part of Tasky.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from pathlib import Path
import datetime


class TaskyLog:
    _default_file_name = datetime.datetime.now().strftime("%Y_%m_%d__%H%M") + ".log"
    _default_file_path = Path.home() / "Tasky" / "taskylogs"

    def __init__(self, filename=_default_file_name, filepath=_default_file_path):
        self.filename = filename
        self.filepath = filepath

        self.filepath.mkdir(parents=True, exist_ok=True)
        self.file = filepath / filename
        self.now = datetime.datetime.now

    def writelog(self, level, *args):
        self.filepath.mkdir(parents=True, exist_ok=True)
        with open(self.file, 'a') as lf:
            lf.write(f"{str(self.now())[:-4]} >> [{level.upper()}] {' '.join(map(str, args))}\n")
            lf.close()

    def info(self, *text):
        self.writelog("info", *text)

    def function(self, *text):
        self.writelog("function", *text)

    def error(self, *text):
        self.writelog("error", *text)

    def waiting(self, *text):
        self.writelog("waiting", *text)
