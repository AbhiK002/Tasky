from pathlib import Path
import datetime
from .taskylog import TaskyLog


class Functions:
    def __init__(self):
        self.TL = TaskyLog()
        self.TL.info("Tasky's functions accessed")

        self.taskymain_path = Path.home() / "Tasky"
        self.tasks_path = self.taskymain_path / "tasks.txt"
        self.check_tasks_txt()

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

        self.current_year = int(datetime.datetime.today().strftime("%Y"))

        self.spl = [":)", ":(", ":D", ":>", ":<", ":|", ":/", ":\\", ":O", ":P", "XD",
                    ">:(", ">:)", "._.", ".-.", "O_O", "LOL", "LMAO", "-_-",
                    ">_<", "(:", "):", "D:", ":^*", ";-;", ":'D", ":')", ":'("]

        self.TL.info(f"defined datasets for months, month names and special inputs")

    @staticmethod
    def return_datetime_now_parts():
        return datetime.datetime.now().strftime("%y %m %d %H %M").split()

    def check_tasks_txt(self):
        self.TL.info("creating tasks.txt if it doesn't exist")
        open(self.tasks_path, "a").close()

    @staticmethod
    def reversed_dict(d):
        result = {}
        for k, v in d.items():
            result[v] = k
        return result

    @staticmethod
    def is_leap(year):
        return int(year) % 4 == 0 and (int(year) % 100 != 0 or int(year) % 400 == 0)

    def timediff(self, tt):
        self.TL.function(f"timediff({tt})")

        # time now
        tny, tnm, tnd, tnh, tnmin = self.return_datetime_now_parts()

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
        # YY:mm:HH:MM:ss=[text]

        stage1 = task.split("=", 1)
        s1_conditions = (
            not all(stage1),  # stage1 should not contain empty strings
            len(stage1) != 2,  # task datetime and task name
            not 1 <= len(stage1[1].strip()) <= 30,  # task name between 1 and 30 chars
            len(stage1[0]) != 14,  # "yy:mm:dd:HH:MM"
            not '22' <= stage1[0][:2] <= '99'  # year -> 2022 to 2099
        )

        if any(s1_conditions):
            self.TL.error(f"GIVEN TASK STRING IS INVALID")
            return False

        try:
            datetime.datetime.strptime(stage1[0], "%y:%m:%d:%H:%M")
        except ValueError:
            self.TL.error(f"GIVEN TASK STRING IS INVALID")
            return False

        self.TL.info(f"GIVEN TASK STRING IS VALID")
        return True

    def write_tasks(self, last):
        for i, task in enumerate(last):
            ttime, tname = task.split("=", 1)
            last[i] = f"{ttime}={tname.strip()}"

        with open(self.tasks_path, "w") as taskfile:
            taskfile.write('\n'.join(last))

        self.TL.function(f"wrote given tasks into tasks.txt")
        self.TL.info(last)

    def read_and_sort_tasks_file(self):  # returns the current data sorted and separately in list
        self.TL.function(f"starts -> read_and_sort_tasks_file()")

        self.check_tasks_txt()
        with open(self.tasks_path, "r") as taskfile:
            self.TL.info(f"opened 'tasks.txt' in read mode")

            taskslist = sorted(filter(self.is_valid_task, taskfile.read().split('\n')))

        self.TL.info(f"tasks list filtered and sorted")
        self.TL.info(taskslist)

        if len(taskslist) > 100:  # maximum tasks allowed = 100
            taskslist = taskslist[:100]

        self.write_tasks(taskslist)

        self.TL.function(f"ends -> read_and_sort_tasks_file()")
        return taskslist

    def remove(self, num, last_copy):
        self.TL.function(f"starts -> remove({num})")

        last = last_copy
        self.TL.info(f"stored tasks as 'last'")

        self.TL.info(f"task {num} requested to be removed ")

        last.pop(int(num) - 1)
        self.TL.info(f"removed requested task from the list")
        self.TL.info(last)

        self.write_tasks(last)
        self.TL.info(f"wrote new output to 'tasks.txt'")

        self.TL.function(f"ends -> remove({num})")

    def return_deadlines(self, given_tasks_list=False):
        tasks = given_tasks_list
        if not given_tasks_list:
            tasks = self.read_and_sort_tasks_file()

        deadlines = []

        for i, task in enumerate(tasks):
            ttime, tname = task.split("=", 1)
            deadline = self.timediff(ttime)
            num = str(i + 1)

            deadlines.append((num, deadline, tname.strip()))

        return deadlines


if __name__ == '__main__':
    print(Functions().return_deadlines())
