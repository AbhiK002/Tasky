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
import os
import sys
import subprocess
import datetime
from .taskylog import TaskyLog


class AboutTasky:
    # ------------------  About Tasky -------------------- #
    version = 'v2.1'
    creator = 'Abhineet Kelley'
    release = '20th September 2025'
    github = 'https://github.com/AbhiK002/Tasky'
    license = 'https://github.com/AbhiK002/Tasky/blob/main/LICENSE'
    # ---------------------------------------------------- #


class OSFunctions:
    @staticmethod
    def is_windows_system():
        return sys.platform.startswith("win")

    @staticmethod
    def is_system_mac():
        return sys.platform.startswith("darwin")

    @staticmethod
    def is_linux_system():
        return sys.platform.startswith("linux")

    @staticmethod
    def open_file(path):
        if OSFunctions.is_windows_system():
            os.startfile(path)
        elif OSFunctions.is_system_mac():
            subprocess.call(["open", path])
        else:
            subprocess.call(["xdg-open", path])

    @staticmethod
    def clear_terminal():
        if OSFunctions.is_windows_system():
            os.system('cls')
        else:
            os.system('clear')

    @staticmethod
    def resource_path(relative_path):
        """
    - This function returns the absolute path from a given relative path of a file/folder
    - However, here it has been defined to facilitate embedding asset files into the bundled EXE file made using `pyinstaller` module
    - This is a workaround for `pyinstaller` to easily find asset files while bundling the EXE file

        :param relative_path:
        :return absolute_path:
        """

        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    @staticmethod
    def exit_program():
        sys.exit(0)

    @staticmethod
    def set_terminal_title(title: str):
        if OSFunctions.is_windows_system():
            os.system(f"title {title}")
        else:
            sys.stdout.write(f"\33]0;{title}\a")
            sys.stdout.flush()


class Functions:
    def __init__(self):
        self.TL = TaskyLog()
        self.TL.info("Tasky's functions accessed")

        self.taskymain_path = Path.home() / "Tasky"
        self.tasks_path = self.taskymain_path / "newtasks.txt"
        self.old_tasks_path = self.taskymain_path / 'tasks.txt'
        self.check_tasks_txt()

        self.old_tasks = []

        self.months = {
            "01": 31, "02": 29, "03": 31, "04": 30,
            "05": 31, "06": 30, "07": 31, "08": 31,
            "09": 30, "10": 31, "11": 30, "12": 31,
        }

        self.month_names = {
            1:  "january", 2:  "february", 3: "march", 4: "april",
            5: "may", 6: "june", 7: "july", 8: "august",
            9: "september", 10: "october", 11: "november", 12: "december",
        }

        self.month_name_to_num = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8,
            'september': 9, 'october': 10, 'november': 11, 'december': 12
        }

        self.current_year = int(datetime.datetime.today().strftime("%Y"))
        self.str_to_date_obj = datetime.datetime.strptime

        self.spl = [":)", ":(", ":D", ":>", ":<", ":|", ":/", ":\\", ":O", ":P", "XD",
                    ">:(", ">:)", "._.", ".-.", "O_O", "LOL", "LMAO", "-_-",
                    ">_<", "(:", "):", "D:", ":^*", ";-;", ":'D", ":')", ":'("]

        self.TL.info(f"defined datasets for months, month names and special inputs")

    def tasky_version(self, left_width=23, link=False):
        t_width = 60
        l_width = left_width
        github = AboutTasky.github
        licc = AboutTasky.license
        if link:
            github = f"<a href='{github}'> AbhiK002/Tasky </a>"
            licc = f"<a href='{licc}'> View License </a>"

        about = '\n'.join((
            '-' * t_width + "<br>"*link,
            '  About Tasky  '.center(t_width, '-') + "<br>"*link,
            f'\n{"VERSION".ljust(l_width)} = {AboutTasky.version}{"<br>"*link}',
            f'{"RELEASE DATE".ljust(l_width)} = {AboutTasky.release}{"<br>"*link}',
            f'{"CREATOR".ljust(l_width)} = {AboutTasky.creator}{"<br>"*link}',
            f'{"SOURCE CODE".ljust(l_width)} = {github}{"<br>"*link}',
            f'{"LICENSE".ljust(l_width)} = {licc}{"<br>"*link}',
            '-' * t_width
        ))
        return about

    @staticmethod
    def return_datetime_now_parts():
        return datetime.datetime.now().strftime("%y %m %d %H %M").split()

    def check_tasks_txt(self):
        self.taskymain_path.mkdir(parents=True, exist_ok=True)
        open(self.tasks_path, "a").close()
        open(self.old_tasks_path, "a").close()

    def read_tasks_file(self):
        self.check_tasks_txt()
        return open(self.tasks_path).read()

    @staticmethod
    def is_leap(year):
        return int(year) % 4 == 0 and (int(year) % 100 != 0 or int(year) % 400 == 0)

    def timediff(self, tt, diff_of: list = False, tasky_output=True):
        self.TL.function(f"timediff({tt})")

        # time now
        if not diff_of:
            tny, tnm, tnd, tnh, tnmin = self.return_datetime_now_parts()
        else:
            tny, tnm, tnd, tnh, tnmin = diff_of

        # task time, tt -> "yy:mm:dd:HH:MM"
        tty, ttm, ttd, tth, ttmin = tt.split(":")

        diffy = int(tty) - int(tny)
        diffm = int(ttm) - int(tnm)
        diffd = int(ttd) - int(tnd)
        diffh = int(tth) - int(tnh)
        diffmin = int(ttmin) - int(tnmin)

        if diffmin < 0:
            diffmin += 60
            diffh -= 1
            # e.g. 2:20 - 1:40,
            # diffh = 2 - 1 = 1, diffmin = 20 - 40 = -20
            # implies => diffh - 1 = 0 hours, and diffmin = -20 + 60 = 40 minutes

        if diffh < 0:
            diffh += 24
            diffd -= 1

        if diffd < 0:
            diffd += self.months.get(tnm)
            if int(tnm) == 2 and not self.is_leap(tny):  # self.months[2] = 29 by default
                diffd -= 1
            diffm -= 1

        if diffm < 0:
            diffm += 12
            diffy -= 1

        if not tasky_output:
            return [diffy, diffm, diffd, diffh, diffmin]

        if diffy < 0:
            output = "Task Expired".rjust(19)
        else:
            output = f"{(f'{diffy}y' * any((diffy,))).rjust(3)} " \
                     f"{(f'{diffm}M' * any((diffy, diffm))).rjust(3)} " \
                     f"{(f'{diffd}d' * any((diffy, diffm, diffd))).rjust(3)} " \
                     f"{(f'{diffh}h' * any((diffy, diffm, diffd, diffh))).rjust(3)} " \
                     f"{(f'{diffmin}m' * any((diffy, diffm, diffd, diffh, diffmin))).rjust(3)}"

            if diffmin <= 30 and sum((diffy, diffm, diffd, diffh)) == 0:
                output = f"LESS THAN {diffmin} MIN".rjust(19)

        self.TL.info(f"{output}")

        return output

    def clear_tasks(self):
        open(self.tasks_path, 'w').close()
        self.TL.function("all current tasks cleared")

    def is_valid_task(self, task):
        self.TL.function(f"CHECKING IF '{task}' IS VALID TASK STRING")
        # checks if the given string is of valid task form
        # YY:mm:HH:MM:ss{TAB}[text]{TAB}[text]
        try:
            ttime, tname, tdesc = task.split("\t", 2)
        except ValueError:  # not enough values to unpack
            self.TL.error("GIVEN TASK STRING IS INVALID (unpack error)")
            return False
        try:
            s1_conditions = (
                not all((ttime, tname.strip())),  # name and time cannot be empty
                not 1 <= len(tname.strip()) <= 30,  # task name between 1 and 30 chars
                len(tdesc.strip()) > 168,  # task description cannot be more than 168 characters
                len(ttime) != 14,  # "yy:mm:dd:HH:MM"
                not str(self.current_year)[-2:] <= ttime[:2] <= '99',  # year -> CURRENT to 2099
            )
        except IndexError:
            self.TL.error("GIVEN TASK STRING IS INVALID (index error)")
            return False

        self.TL.info(s1_conditions)
        if any(s1_conditions):
            self.TL.error(f"GIVEN TASK STRING IS INVALID (any cond1)")
            return False

        try:
            datetime.datetime.strptime(ttime, "%y:%m:%d:%H:%M")
        except ValueError:
            self.TL.error(f"GIVEN TASK STRING IS INVALID (date conversion)")
            return False

        self.TL.info(f"GIVEN TASK STRING IS VALID")
        return True

    def strip_tasks(self, tlist):
        for i, task in enumerate(tlist):
            ttime, tname, tdesc = task.split("\t", 2)
            tlist[i] = f"{ttime}\t{tname.strip()}\t{tdesc.strip()}"

        return tlist

    def write_tasks(self, last):
        with open(self.tasks_path, "w") as taskfile:
            taskfile.write('\n'.join(last))

        self.TL.function(f"wrote given tasks into newtasks.txt (new format)")
        self.TL.info(last)

    def read_and_sort_tasks_file(self):  # returns the current data sorted and separately in list
        self.TL.function(f"starts -> read_and_sort_tasks_file()")

        self.check_tasks_txt()
        with open(self.tasks_path, "r") as taskfile:
            self.TL.info(f"opened 'newtasks.txt' in read mode")
            read_data = taskfile.read().split('\n')
            taskslist = sorted(filter(self.is_valid_task, read_data))  # sorts filtered valid tasks from file

        if not self.converted():
            self.TL.info("adding old tasks to new version")
            self.get_old_tasks()
            taskslist = sorted(set(taskslist) | set(self.old_tasks))  # union of unique old and new tasks
            check_path = self.taskymain_path / 'old_checked'
            check_path.mkdir(parents=True, exist_ok=True)

        taskslist = self.remove_duplicates(self.strip_tasks(taskslist))
        # remove old tasks that have a description in the new tasks file

        self.TL.info(f"tasks list filtered and sorted")
        self.TL.info(taskslist)

        if len(taskslist) > 100:  # maximum tasks allowed = 100
            self.TL.error("more than 100 tasks detected")
            taskslist = taskslist[:100]

        self.write_tasks(taskslist)

        self.TL.function(f"ends -> read_and_sort_tasks_file()")
        return taskslist

    def converted(self):
        check_path = self.taskymain_path / 'old_checked'
        return check_path.exists()

    def get_old_tasks(self):  # tasks stored by previous versions of tasky, which cannot be directly read
        self.TL.function("starts -> get_old_tasks()")

        self.check_tasks_txt()
        with open(self.old_tasks_path, "r") as taskfile:
            self.TL.info(f"opened 'tasks.txt' in read mode")

            read_data = taskfile.read().split('\n')
            self.TL.info(f"old tasks: {read_data}")

            if not read_data:
                self.TL.info("old tasks file empty")
                self.old_tasks = []

            converted_data = list(map(lambda task: '\t'.join(task.split("=", 2) + ['']), read_data))
            self.TL.info(f"converted old tasks: {converted_data}")

        self.old_tasks = sorted(filter(self.is_valid_task, converted_data))  # sorts filtered valid tasks from file

    def remove_duplicates(self, tlist):
        final = []
        descriptions = {}
        for task in tlist:
            ttime, tname, tdesc = task.split('\t', 2)
            key = f"{ttime}\t{tname}\t"
            if tdesc != '':
                descriptions[key] = tdesc
            if key not in final:
                final.append(key)

        for i, key in enumerate(final):
            final[i] = key + descriptions.get(key, '')

        return final

    def remove(self, num, last_copy):
        self.TL.function(f"starts -> remove({num})")

        last = last_copy
        self.TL.info(f"stored tasks as 'last'")

        self.TL.info(f"task {num} requested to be removed ")
        try:
            last.pop(int(num) - 1)
        except IndexError:
            self.TL.error("invalid task number to be removed")
            return
        self.TL.info(f"removed requested task from the list")
        self.TL.info(last)

        self.write_tasks(last)
        self.TL.info(f"wrote new output to 'newtasks.txt'")

        self.TL.function(f"ends -> remove({num})")

    def return_deadlines(self, given_tasks_list=False):
        tasks = given_tasks_list
        if not given_tasks_list:
            tasks = self.read_and_sort_tasks_file()

        deadlines = []

        for i, task in enumerate(tasks):
            ttime, tname, tdesc = task.split("\t", 2)
            deadline = self.timediff(ttime)
            num = str(i + 1)

            deadlines.append((num, deadline, tname, tdesc))

        return deadlines
