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
