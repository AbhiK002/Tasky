import datetime
from os import startfile, system
from pathlib import Path


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


class Functions:
    def __init__(self):
        self.TL = TaskyLog()
        self.TL.info("LOGGER STARTED")

        self.taskymain_path = Path.home() / "Tasky"
        self.tasks_path = self.taskymain_path / "tasks.txt"
        self.check_tasks_txt()

        self.months = {
            "01": 31,
            "02": 29,
            "03": 31,
            "04": 30,
            "05": 31,
            "06": 30,
            "07": 31,
            "08": 31,
            "09": 30,
            "10": 31,
            "11": 30,
            "12": 31,
        }

        self.month_names = {
            1:  "january",
            2:  "february",
            3: "march",
            4: "april",
            5: "may",
            6: "june",
            7: "july",
            8: "august",
            9: "september",
            10: "october",
            11: "november",
            12: "december",
        }

        self.spl = [":)", ":(", ":D", ":>", ":<", ":|", ":/", ":\\", ":O", ":P", "XD",
                    ">:(", ">:)", "._.", ".-.", "O_O", "LOL", "LMAO", "-_-",
                    ">_<", "(:", "):", "D:", ":^*", ";-;", ":'D", ":')", ":'("]

        self.TL.info(f"defined datasets for months, month names and special inputs")

    def check_tasks_txt(self):
        self.TL.info("creating tasks.txt if it doesn't exist")
        open(self.tasks_path, "a").close()

    def clear_window(self):
        system("cls")
        self.TL.function(f"output screen cleared")

    def info_bar(self, data):
        data = str(data)
        self.clear_window()
        self.status()
        print(f"<< {data.center(54)} >>\n")
        self.TL.info("refreshed output screen")
        self.TL.info(f"status bar: {data}")

    @staticmethod
    def is_leap(year):
        return int(year) % 4 == 0 and (int(year) % 100 != 0 or int(year) % 400 == 0)

    def is_confirmed(self, msg):
        self.TL.waiting("for confirmation from user")
        while True:
            choice = input(msg).strip().lower()
            if choice == 'y':
                self.TL.info("input: 'y', confirmed")
                return True
            elif choice == 'n':
                self.TL.info("input: 'n', not confirmed")
                return False
            else:
                self.TL.error(
                    f"oonga boonga man wrote '{choice}' instead of y/n"
                )
                self.info_bar("please enter y/n")

    def timediff(self, tt):
        self.TL.function(f"timediff({tt})")

        # time now
        tn = datetime.datetime.now()
        tny, tnm, tnd, tnh, tnmin = tn.strftime("%y %m %d %H %M").split()

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

        stage1 = task.split("=")
        s1_conditions = (
            not all(stage1),  # stage1 should not contain empty strings
            len(stage1) != 2,  # task datetime and task name
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
        with open(self.tasks_path, "w") as taskfile:
            taskfile.write('\n'.join(last))
            taskfile.close()
        self.TL.function(f"wrote given tasks into tasks.txt")
        self.TL.info(last)

    def read_and_sort_tasks_file(self):  # returns the current data sorted and separately in list
        self.TL.function(f"starts -> read_and_sort_tasks_file()")

        self.check_tasks_txt()
        with open(self.tasks_path, "r") as taskfile:
            self.TL.info(f"opened 'tasks.txt' in read mode")

            taskslist = sorted(filter(self.is_valid_task, taskfile.read().split('\n')))
            taskfile.close()

        self.TL.info(f"tasks list filtered and sorted")
        self.TL.info(taskslist)

        self.write_tasks(taskslist)

        self.TL.function(f"ends -> read_and_sort_tasks_file()")
        return taskslist

    def status(self):
        self.TL.function(f"starts -> status()")

        print(f"\n{' TASKS REMAINING '.center(60, '~')}\n")

        task_list = self.read_and_sort_tasks_file()
        self.TL.info(f"stored current tasks in 'task_list'")

        if not task_list:  # no tasks
            print("(No tasks to display yet)".center(60), "Add a task using 'add' or 'new'".center(60), sep='\n', end='\n\n\n')
            self.TL.info("no tasks available to display")
            return

        outputs = list(
            map(
                lambda task:
                    f"{f'({task_list.index(task) + 1})'.rjust(4)} {self.timediff(task.split('=')[0])} >>>  {task.split('=')[1].title()}",
                task_list
            )
        )

        self.TL.info('outputs created from the tasks list')
        self.TL.info(outputs)

        status_output = "\n".join(outputs) + "\n"
        print(status_output)
        self.TL.info(f"all task details printed on output screen")
        self.TL.info(f"\n{status_output}")

        self.TL.function(f"ends -> status()")

    def view_task(self, num):
        self.TL.function(f"starts -> view_task({num})")

        task_list = self.read_and_sort_tasks_file()
        self.TL.info(f"stored tasks as 'task_list'")

        target_task = task_list[num - 1]
        self.TL.info(f"target task : {target_task}")

        dt, t_desc = target_task.split("=")
        tYY, tMM, tDD, tHH, tmm = dt.split(":")

        tYY = 2000 + int(tYY)
        tMM = self.month_names[int(tMM)]
        self.TL.info(f"changed year to YYYY form and month number to Name")

        tt12h = int(tHH) % 12
        ttampm = ("AM", "PM")[int(tHH) // 12 == 1]

        if tt12h == 0:
            tt12h = 12
            if int(tmm) == 0:
                if tHH == "00":
                    ttampm = f"MIDNIGHT ({int(tDD) - 1} | {int(tDD)})"
                else:
                    ttampm = "NOON"
        self.TL.info(f"changed hours to 12h format with AM/PM/NOON/MIDNIGHT")

        width = 60
        output = (
            "-" * width,
            f" TASK {num} ".center(width, '-'), ' ',
            f'{"TASK DESCRIPTION : ".rjust(30)}{t_desc.title()}',
            f'{"DATE : ".rjust(30)}{tDD} {tMM.title()}, {tYY}',
            f'{"TIME : ".rjust(30)}{tt12h}:{tmm} {ttampm}',
            f'{"DEADLINE : ".rjust(30)}{self.timediff(dt).strip()}',
            "-" * width
        )
        print(*output, sep="\n")
        self.TL.info(f"task view output printed")

        self.TL.function(f"ends -> view_task({num})")

    def remove(self, num, last_copy):
        self.TL.function(f"starts -> remove({num})")

        last = last_copy
        self.TL.info(f"stored tasks as 'last'")

        self.TL.info(f"task {num} requested to be removed ")

        last.remove(last[int(num) - 1])
        self.TL.info(f"removed requested task from the list")
        self.TL.info(last)

        self.write_tasks(last)
        self.TL.info(f"wrote new output to 'tasks.txt'")
        self.info_bar(f"removed task {num} from the list")

        self.TL.function(f"ends -> remove({num})")

    def edit_task(self, num, last_copy):
        self.TL.function(f"starts -> edit_task({num})")

        last = last_copy
        self.write_tasks(last)
        self.TL.info(f"stored current tasks list as 'last'")

        task_ind = int(num) - 1
        target_task = last[int(num) - 1]
        self.TL.info(f"task number {num} requested for edit")

        ttask_time, ttask_name = target_task.split("=")
        self.TL.info(f"stored values of task to be edited as ttask_time and ttask_name")
        self.TL.info(f"original values: {ttask_time} and {ttask_name}")

        edit_task_help = (
            '-' * 60, f" EDIT TASK {num} ".center(60, '-'), '',
            '(Enter the corresponding number)'.center(60),
            "1. DATE-TIME",
            "2. TASK NAME",
            "3. BOTH",
            "4. EXIT EDIT MODE"
        )
        self.info_bar(f"edit mode for task {num}")
        print(*edit_task_help, sep='\n', end='\n\n')

        while True:
            try:
                edited = False
                exited = False

                self.TL.waiting(f"FOR 'choice' INPUT")
                edit_choice = int(input("> "))

                self.TL.info(f"received 'choice': {edit_choice}")

                self.write_tasks(last)
                if edit_choice == 1:
                    self.TL.info(f"user input 1 to edit date-time only")

                    self.info_bar(f"task {num} edit: type '/cancel' to cancel")
                    print('-' * 60, f" EDIT TASK {num} ".center(60, '-'), sep='\n', end='\n\n')

                    mn, hr, dt, mth, yr = self.new_task_time()

                    if (mn, hr, dt, mth, yr) != (0, 0, 0, 0, 0):
                        ttask_time = f"{yr}:{mth}:{dt}:{hr}:{mn}"
                        self.TL.info(f"updated task details saved")

                        edited = True

                    else:
                        self.write_tasks(last)

                        self.info_bar(f"edit mode for task {num}")
                        print(*edit_task_help, sep='\n', end='\n\n')

                elif edit_choice == 2:
                    self.TL.info(f"user input 2 to edit name only")

                    self.info_bar(f"task {num} edit: type '/cancel' to cancel")
                    print('-' * 60, f" EDIT TASK {num} ".center(60, '-'), sep='\n', end='\n\n')

                    ttask_name = self.new_task_name()

                    if ttask_name != "/cancel":
                        self.TL.info(f"updated task details saved")
                        edited = True

                    else:
                        self.write_tasks(last)
                        self.info_bar(f"edit mode for task {num}")
                        print(*edit_task_help, sep='\n', end='\n\n')

                elif edit_choice == 3:
                    self.TL.info(f"user input 3 to edit both task name and date-time")

                    self.info_bar(f"task {num} edit: type '/cancel' to cancel")
                    print('-' * 60, f" EDIT TASK {num} ".center(60, '-'), sep='\n', end='\n\n')

                    ttask_name = self.new_task_name()

                    if ttask_name != "/cancel":
                        mn, hr, dt, mth, yr = self.new_task_time()

                        if (mn, hr, dt, mth, yr) != (0, 0, 0, 0, 0):
                            ttask_time = f"{yr}:{mth}:{dt}:{hr}:{mn}"
                            self.TL.info(f"updated task details saved")

                            edited = True

                        else:
                            self.write_tasks(last)

                            self.info_bar(f"edit mode for task {num}")
                            print(*edit_task_help, sep='\n', end='\n\n')

                    else:
                        self.write_tasks(last)

                        self.info_bar(f"edit mode for task {num}")
                        print(*edit_task_help, sep='\n', end='\n\n')

                elif edit_choice == 4:
                    self.TL.info(f"user input 4 to exit edit-mode for task number {num}")
                    exited = True

                else:
                    self.TL.error(f"invalid value entered in edit mode: {edit_choice}")

                    self.write_tasks(last)

                    self.info_bar("choose out of 1, 2, 3, 4 only")
                    print(*edit_task_help, sep='\n', end='\n\n')

                if edited:
                    edited_task = f"{ttask_time}={ttask_name}"
                    self.TL.info(f"new task: {edited_task}")
                    self.TL.info(f"old task: {last[task_ind]}")

                    last[task_ind] = edited_task
                    self.TL.info(f"replaced old task in 'last' with edited task")

                    self.write_tasks(last)
                    self.TL.info(f"updated output written to 'tasks.txt'")
                    self.TL.info(last)

                    self.info_bar("requested edit successful")
                    print(*edit_task_help, sep='\n', end='\n\n')

                if exited:
                    self.TL.info(f"exiting edit mode for task {num}")
                    self.info_bar(f"exited edit mode for task {num}")
                    self.write_tasks(last)
                    break

            except ValueError:
                self.TL.error("user typed something that's not numbers... it wasn't very effective")

                self.write_tasks(last)

                self.info_bar("numbers 1, 2, 3, 4 allowed only")
                print(*edit_task_help, sep='\n', end='\n\n')

        self.TL.info(f"edited name/date-time of requested task")

        self.TL.function(f"ends -> edit_task({num})")

    def new_task_name(self):
        self.TL.function(f"starts -> new_task_name()")

        while True:
            self.TL.waiting(f"for task name input")
            taskinfo = input(f"{'New Task Name (30 chars)'.ljust(27)}:  ").strip()

            self.TL.info(f"task name input: {taskinfo}")

            if taskinfo == "/cancel":
                self.TL.info(f"user chose to cancel new task addition")

                self.TL.function(f"ends -> new_task_name()")
                return taskinfo

            if taskinfo == "":
                print("Task Name cannot be empty\n")
                self.TL.error(f"task description cannot be empty")

                continue

            if len(taskinfo) <= 30:
                if "=" not in taskinfo:
                    self.TL.info(f"stored input from user as task name")
                    self.TL.info(f"new task name: {taskinfo}")

                    self.TL.function(f"ends -> new_task_name()")
                    return taskinfo

                else:
                    print("Task Name cannot contain symbol '='\n")
                    self.TL.error(f"task name contains symbol =")
            else:
                print("Task Name cannot be more than 30 characters\n")
                self.TL.error(f"task name is more than 30 characters")

    def new_task_time(self):
        self.TL.function(f"starts -> new_task_time()")

        while True:

            while True:  # ask for date
                self.TL.waiting(f"for date input")
                tdate = input(f"{'Date (DD)'.ljust(27)}:  ").strip()

                self.TL.info(f"date input: {tdate}")

                if tdate.lower() == "/cancel":
                    self.TL.info(f"user chose to cancel new task addition")
                    self.TL.function(f"ends -> new_task_time()")
                    return 0, 0, 0, 0, 0

                elif tdate.isdecimal() and (int(tdate) in range(1, 32)):
                    self.TL.info(f"date number valid")

                    tdate = str(int(tdate)).zfill(2)
                    self.TL.info("converted date to double digit format")
                    self.TL.info(f"{tdate}")
                    break

                else:
                    self.TL.error(f"user doesn't know dates naturally go from 1 to 31, wrote: {tdate}")
                    print("Invalid date entered\n")

            while True:  # ask for month
                self.TL.waiting(f"for month input (num/words)")
                tmonth = input(f"{'Month (MM/Name)'.ljust(27)}:  ").lower().strip()

                self.TL.info(f"month input: {tmonth}")

                if tmonth == "/cancel":
                    self.TL.info(f"user chose to cancel new task addition")
                    self.TL.function(f"ends -> new_task_time()")
                    return 0, 0, 0, 0, 0

                elif tmonth.isalpha():
                    self.TL.info(f"input is alphabetic")

                    for k, v in self.month_names.items():
                        self.TL.info(f"checking dict month_names item = {k}: {v}")

                        if tmonth in v:
                            self.TL.info(f"{tmonth} in {v} = True")
                            tmonth = str(k).zfill(2)
                            self.TL.info(f"corresponding number to the month {v} = {tmonth}")
                            break

                        self.TL.info(f"{tmonth} in {v} = False")

                    if tmonth.isdecimal():
                        break
                    else:
                        self.TL.error(f"seriously, what month is this: {tmonth}")
                        print("Invalid month entered\n")

                elif tmonth.isdecimal() and (int(tmonth) in range(1, 13)):
                    tmonth = str(int(tmonth)).zfill(2)
                    self.TL.info(f"converting month number to a 2 digit number")
                    self.TL.info(f"{tmonth}")
                    break

                else:
                    self.TL.error(f"something wrong with the month entered by the user: {tmonth}")
                    print("Invalid month entered\n")

            # check if this date exists in this month
            if int(tdate) > self.months[tmonth]:
                self.TL.error(f"umm, month {tmonth} doesn't have {tdate} days...")
                print("Invalid date entered for the given month\n")

            else:
                self.TL.info(f"confirmed valid date for given month")
                valid_date = True
                special_feb_case = False

                # special Feb 29 case
                if int(tmonth) == 2 and int(tdate) == 29:
                    special_feb_case = True
                    valid_date = False
                    self.TL.info(
                        "user has entered the date 29 for the month 02 (February), year yet to be checked"
                    )

                while True:  # ask for year
                    self.TL.waiting(f"for year input")
                    tyear = input(f"{'Year (YYYY) (2022-99)'.ljust(27)}:  ").strip()

                    self.TL.info(f"year input: {tyear}")

                    if tyear.lower() == "/cancel":
                        self.TL.info(f"user chose to cancel new task addition")
                        self.TL.function(f"ends -> new_task_time()")
                        return 0, 0, 0, 0, 0

                    elif tyear.isdecimal() and int(tyear) in range(2022, 2100):
                        self.TL.info(f"confirmed year lies between 2022 and 2100")

                        if special_feb_case and self.is_leap(tyear):
                            self.TL.info(f"entered year is confirmed leap year: {tyear}")

                            valid_date = True
                            tyear = tyear[-2:]
                            self.TL.info(f"last 2 digits of input year stored: {tyear}")
                            break

                        elif special_feb_case and not self.is_leap(tyear):
                            self.TL.error(
                                "entered year is not a leap year while date-month given by user is 29 Feb"
                            )
                            print("Non-Leap Year cannot have Feb 29\n")
                            break

                        else:
                            tyear = tyear[-2:]
                            self.TL.info(f"last 2 digits of input year stored: {tyear}")
                            break
                    else:
                        self.TL.error(f"invalid year received: {tyear}")
                        print("Invalid Year entered\n")

                if valid_date:
                    break

        while True:  # ask for hours
            self.TL.waiting(f"for hours input")
            thour = input(f"{'Hours (HH)(24h)'.ljust(27)}:  ").strip()

            self.TL.info(f"received hour input: {thour}")

            if thour.lower() == "/cancel":
                self.TL.info(f"user chose to cancel new task addition")
                self.TL.function(f"ends -> new_task_time()")
                return 0, 0, 0, 0, 0

            elif thour.isdecimal() and (int(thour) in range(24)) and thour != "":
                self.TL.info(f"confirmed valid input for hours")

                thour = str(int(thour)).zfill(2)
                self.TL.info(f"stored hours: {thour}")
                break

            else:
                self.TL.error(f"Earth doesn't have these amount of hours in a day (yet): {thour}")
                print("Invalid hours entered\n")

        while True:  # ask for minutes
            self.TL.waiting(f"for minutes input")
            tmin = input(f"{'Minutes (mm)'.ljust(27)}:  ").strip()

            self.TL.info(f"minute input received: {tmin}")

            if tmin == "/cancel":
                self.TL.info(f"user chose to cancel new task addition")
                self.TL.function(f"ends -> new_task_time()")
                return 0, 0, 0, 0, 0

            elif tmin.isdecimal() and (int(tmin) in range(60)) and tmin != "":
                self.TL.info(f"confirmed valid input for minutes")

                tmin = str(int(tmin)).zfill(2)
                self.TL.info(f"stored mins: {tmin}")
                break

            else:
                self.TL.error(f"invalid minutes value entered: {tmin}")
                print("Invalid minutes entered\n")

        self.TL.info(f"5 values returned: {tmin}, {thour}, {tdate}, {tmonth}, {tyear}")

        self.TL.function(f"ends -> new_task_time()")
        return tmin, thour, tdate, tmonth, tyear

    def new_task(self, last_copy):
        self.TL.function(f"starts -> new_task()")

        self.write_tasks(last_copy)

        taskinfo = self.new_task_name()

        if taskinfo == "/cancel":
            self.write_tasks(last_copy)
            self.info_bar("task addition cancelled")

        else:
            tmin, thour, tdate, tmonth, tyear = self.new_task_time()

            if (tmin, thour, tdate, tmonth, tyear) == (0, 0, 0, 0, 0):
                self.write_tasks(last_copy)
                self.info_bar("task addition cancelled")

            else:
                taskcell = f"{tyear}:{tmonth}:{tdate}:{thour}:{tmin}={taskinfo}"
                self.TL.info(f"combined values of new_task_name() and new_task_time()")
                self.TL.info(f"{taskcell}")

                last_copy.append(taskcell)
                self.write_tasks(last_copy)
                self.info_bar("new task added")

        self.TL.function(f"ends -> new_task()")


class App(Functions):
    def console_loop(self):
        self.TL.info(f"PROGRAM STARTED")
        self.info_bar("enter 'help' to view valid commands")
        n = 0  # used variable, do not remove :D

        while True:
            task_list = self.read_and_sort_tasks_file()
            total_tasks = len(task_list)
            self.TL.info(f"current total number of tasks: {total_tasks}")

            self.TL.waiting(f"FOR MAIN USER INPUT")
            user_inp = input(f"\n  >  ").lower().strip()

            self.TL.info(f"user input: {user_inp}")
            words = user_inp.split()

            if user_inp == '':
                self.TL.error(
                    f"i feel empty inside :( just like the user's input..."
                )
                self.info_bar("enter 'help' to view valid commands")
                self.TL.info(f"main loop rerunning...")
                continue

            self.TL.info(f"user input empty = False")
            if user_inp in ("quit", "bye"):
                self.TL.writelog("exit", f"user chose to exit program")
                exit()

            elif user_inp in ("help", "h"):
                self.TL.info(f"user chose help, displaying available commands")
                self.info_bar("DISPLAYING HELP MENU")
                print(
                    '-' * 60,
                    "(Press ENTER to refresh the tasks list)\n".center(56),
                    f"{'Add a New Task'.ljust(20)} --  add / new / create",
                    f"{'Delete Task N'.ljust(20)} --  delete N / del N / remove N / rem N",
                    f"{'Edit Task N'.ljust(20)} --  edit N / ed N / change N",
                    f"{'Task Details'.ljust(20)} --  (ENTER TASK NUMBER)",
                    f"{'Clear All Tasks'.ljust(20)} --  clear",
                    f"{'Open Help Menu'.ljust(20)} --  help / h",
                    f"{'Exit Tasky'.ljust(20)} --  quit / bye",
                    sep="\n"
                )
                print("-" * 60)

            elif user_inp.isdecimal() and int(user_inp) in range(1, total_tasks + 1):
                self.TL.info(f"user requested to view task {int(user_inp)}")
                self.info_bar(f"viewing task {int(user_inp)}")
                self.view_task(int(user_inp))

            elif user_inp in ("add", "new", "create"):
                self.TL.info(f"user requested to add a new task")
                tasks_copy = self.read_and_sort_tasks_file()
                self.info_bar("type '/cancel' to stop task addition")
                print(
                    "-" * 60,
                    " NEW TASK DETAILS ".center(60, '-'),
                    sep='\n', end='\n\n'
                )
                self.new_task(tasks_copy)
                n = 0

            elif words[0] in ("delete", "del", "remove", "rem"):
                if len(words) == 2 and words[1].isdecimal():
                    self.TL.info(
                        f"user requested to remove task number {words[1]}"
                    )
                    if int(words[1]) in range(1, total_tasks + 1):
                        self.TL.info(f"task number confirmed valid")
                        tasks_copy = self.read_and_sort_tasks_file()
                        confirm = self.is_confirmed(f"\nConfirm removal of task {words[1]}? (enter y/n):  ")
                        if confirm:
                            self.TL.info(f"confirmed")
                            self.remove(words[1], tasks_copy)
                            n = 0
                        else:
                            self.TL.info(f"cancelled")
                            self.write_tasks(tasks_copy)
                            self.info_bar("task removal cancelled")
                    else:
                        self.TL.error(
                            f"task {words[1]} doesn't exist, total tasks = {total_tasks}"
                        )
                        self.info_bar("invalid task number to be removed")
                else:
                    self.TL.error(f"command used incorrectly: {user_inp}")
                    self.info_bar(f"error! try again like '{words[0]} 1'")

            elif words[0] in ("edit", "ed", "change"):
                if len(words) == 2 and words[1].isdecimal():
                    self.TL.info(
                        f"user requested to edit task number {words[1]}"
                    )
                    if int(words[1]) in range(1, total_tasks + 1):
                        self.TL.info(f"task number confirmed valid")
                        tasks_copy = self.read_and_sort_tasks_file()
                        self.edit_task(int(words[1]), tasks_copy)
                        n = 0
                    else:
                        self.TL.error(
                            f"task {words[1]} doesn't exist, total tasks = {total_tasks}"
                        )
                        self.info_bar(
                            f"invalid task number to be edited",
                        )
                else:
                    self.TL.error(f"command used incorrectly: {user_inp}")
                    self.info_bar(f"error! try again like '{words[0]} 4'")

            elif user_inp == "clear":
                if total_tasks == 0:
                    self.TL.error("Tasky was requested to clear nothing...")
                    self.info_bar("no tasks available to clear")
                    continue
                self.TL.info("user requested to delete all tasks/clear tasks")
                confirm = self.is_confirmed(
                    "\nWARNING: Clear all existing tasks? (Cannot be undone)\n\t(Enter y/n) :  "
                )
                if confirm:
                    self.clear_tasks()
                    self.info_bar("cleared all tasks")
                else:
                    self.TL.info("user cancelled clearing all tasks")
                    self.info_bar("cancelled clearing all tasks")

            # (not so) secret commands
            elif words[0] in ("hi", "hello", "hey"):
                hello_list = [
                    "hello there :)",
                    "hii :D",
                    "hey-hey user ;)",
                    "hola mi amigo ^-^",
                    "hi again? ;)",
                    "hey :)",
                    "hehe hello ^o^",
                    "hello! enter 'help' for other commands",
                    "hi, view other commands! (type help)",
                    "isn't that enough greeting for now?",
                    "dear user, please get 'help' (literally)",
                    f"please stop... with the hellos",
                    "don't-",
                    "don't you have anything else to do",
                    "jeez how many times will you do this",
                    "fine i'll wait till you do something",
                    "still waiting...",
                    "Tasky isn't a chatbot...",
                    "did i refer to myself in third person?",
                    "GAAAAAAAAAAHHH STOP IT! WILL YOU?",
                    "you doing this to annoy me?",
                    "computers can't get annoyed, can they?",
                    "what do you want >_<",
                    "thanks, i hate these greetings now",
                    "seriously what do you want?",
                    "you want food?",
                    "i have some cookies",
                    "i wanna eat these though",
                    "but you won't stop... hmmph",
                    "aaaah you want a cookie?",
                    "enough with these greetings >_<",
                    "i wont respond to these keywords now",
                    "nope. not doing it.",
                    "ill be here if you need me >:(",
                    "not responding to greetings for real now",
                    "go complete your tasks user :/",
                    "BYE",
                    "enter 'help' ._.",
                    "ughh you won't stop huh",
                    "fine I'll loop my responses now",
                    "ready to get looped responses?",
                    "'i' becomes 0 very soon now",
                    "see ya :D"
                ]
                self.TL.info(f"user greeted Tasky")
                self.info_bar(hello_list[n])
                n += 1
                if n > 42:
                    n = 0

            elif words[0].upper() in self.spl:
                self.TL.info(f"Special Input: {words[0]}")
                self.info_bar(words[0].upper())

            elif user_inp == "tasky-debug":
                self.TL.writelog("debug", "opening logs folder for debugging")
                self.info_bar("request for logs folder")
                startfile(self.TL.filepath)

            else:
                self.TL.error(f"command doesn't exist: {user_inp}")
                self.info_bar("enter 'help' to view valid commands")

            self.TL.info(f"restarting main loop...")


if __name__ == "__main__":
    app = App()
    app.console_loop()
