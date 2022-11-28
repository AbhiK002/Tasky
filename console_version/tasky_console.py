import datetime
from os import startfile, system
from pathlib import Path
from sys import exit as sysend


class Functions:
    def __init__(self):
        self.log_prefix = self.log_dated_names()

        self.home_path = Path.home()
        self.taskymain_path = self.home_path / "Tasky"

        self.tasks_path = self.taskymain_path / "tasks.txt"
        self.taskylog_path = self.taskymain_path / "taskylogs"

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
        self.log("[INFO] defined dict 1 (months)")

        self.month_names = {
            "january": 1,
            "february": 2,
            "march": 3,
            "april": 4,
            "may": 5,
            "june": 6,
            "july": 7,
            "august": 8,
            "september": 9,
            "october": 10,
            "november": 11,
            "december": 12,
        }

        self.spl = [":)", ":(", ":D", ":>", ":<", ":|", ":/", ":\\", ":O", ":P", "XD",
                    ">:(", ">:)", "._.", ".-.", "O_O", "LOL", "LMAO", "-_-",
                    ">_<", "(:", "):", "D:", ":^*", ";-;", ":'D", ":')", ":'("]

        self.log("[INFO] defined dict 2 (month_names)")

    def check_tasky_folders(self):
        self.taskylog_path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def log_dated_names():
        return datetime.datetime.now().strftime("%Y_%m_%d__%H%M")

    def check_tasky_log(self):
        try:
            log_file = open(self.taskylog_path / f"{self.log_prefix}.log", "r")
            log_file.close()
        except FileNotFoundError:
            log_file = open(self.taskylog_path / f"{self.log_prefix}.log", "w")
            log_file.close()

    def log(self, data):
        with open(self.taskylog_path / f"{self.log_prefix}.log", "a") as file:
            file.write(f"{str(datetime.datetime.now())[:-4]} >> {str(data)}\n")

    def check_tasks_txt(self):
        try:
            self.log("[INFO] attempted to open tasks.txt in read mode")
            with open(self.tasks_path, "r"):
                self.log("[INFO] attempt successful")
        except FileNotFoundError:
            self.log("[ERROR] attempt failed, can't find tasks.txt")
            with open(self.tasks_path, "w"):
                self.log("[INFO] created empty text file 'tasks.txt'")

    def clear(self):
        system("cls")
        self.log("[INFO] output screen cleared")

    def info_bar(self, data):
        data = str(data)
        self.clear()
        self.status()
        print(f"<< {data.center(54)} >>\n")

    def timediff(self, tt):
        self.log("[FUNCTION] starts -> timediff()")
        tt = tt.split(":")
        self.log(f"[INFO] split variable named 'tt' {tt} into 5 parts")
        # time now
        tn = datetime.datetime.now()
        self.log("[INFO] calculated current date-time as variables")
        tny, tnm, tnd = tn.strftime("%y"), tn.strftime("%m"), tn.strftime("%d")
        tnh, tnmin = tn.strftime("%H"), tn.strftime("%M")
        self.log(f"[INFO] year: {tny}")
        self.log(f"[INFO] month: {tnm}")
        self.log(f"[INFO] date: {tnd}")
        self.log(f"[INFO] hours: {tnh}")
        self.log(f"[INFO] min: {tnmin}")

        # task time
        tty, ttm, ttd, tth, ttmin = tt
        self.log("[INFO] stored 5 parts of var 'tt'")
        self.log(
            f"[INFO] year: {tty}, month: {ttm}, date: {ttd}, hours: {tth}, mins: {ttmin}"
        )

        diffy = int(tty) - int(tny)
        diffm = int(ttm) - int(tnm)
        diffd = int(ttd) - int(tnd)
        diffh = int(tth) - int(tnh)
        diffmin = int(ttmin) - int(tnmin)
        self.log(
            "[INFO] calculated differences between corresponding values of 'tt' and 'tn'"
        )

        if diffmin < 0:
            diffmin = 60 + diffmin
            diffh -= 1
        if diffh < 0:
            diffh = 24 + diffh
            diffd -= 1
        if diffd < 0:
            diffd = self.months.get(str(tnm)) + diffd
            if int(tnm) == 2 and int(tny) % 4 != 0:
                diffd -= 1
            diffm -= 1
        if diffm < 0:
            diffm = 12 + diffm
            diffy -= 1
        self.log("[INFO] adjusted negative differences 'diff'")
        if diffy < 0:
            output = "Task Expired".rjust(19)
        else:
            if int(diffy) >= 1:
                output = (
                    f"{diffy}y".rjust(3)
                    + f"{diffm}M".rjust(4)
                    + f"{diffd}d".rjust(4)
                    + f"{diffh}h".rjust(4)
                    + f"{diffmin}m".rjust(4)
                )
            elif int(diffm) >= 1:
                output = (
                    f"{diffm}M".rjust(4 + 3)
                    + f"{diffd}d".rjust(4)
                    + f"{diffh}h".rjust(4)
                    + f"{diffmin}m".rjust(4)
                )
            elif int(diffd) >= 1:
                output = (
                    f"{diffd}d".rjust(4 + 7)
                    + f"{diffh}h".rjust(4)
                    + f"{diffmin}m".rjust(4)
                )
            elif int(diffh) >= 1:
                output = f"{diffh}h".rjust(4 + 11) + f"{diffmin}m".rjust(4)
            elif int(diffmin) >= 1 and int(diffmin) >= 30:
                output = f"{diffmin}m".rjust(4 + 15)
            else:
                output = f"LESS THAN {diffmin} MIN".rjust(19)
            self.log("[INFO] calculated time remaining for output")
            self.log(f"[INFO] {output}")
        self.log("[INFO] returned output")
        self.log("[FUNCTION] ends -> timediff()")
        return output

    def is_valid_task(self, task):
        self.log(f"[INFO] CHECKING IF '{task}' IS VALID TASK STRING")
        # checks if the given string is of valid task form
        # XX:XX:XX:XX:XX=TTT...
        stage1 = task.split("=")
        s1_conditions = (
            not all(stage1),
            len(stage1) != 2,
            len(stage1[0]) != 14
        )

        self.log(f"[INFO] Stage1 = {stage1}")
        self.log(f"[INFO] S1 Conditions = {s1_conditions}")

        if any(s1_conditions):
            self.log(f"[INFO] GIVEN TASK STRING IS INVALID")
            return False

        stage2 = stage1[0].split(":")
        s2_conditions = (
            not all(stage2),
            len(list(filter(lambda a: len(a) == 2, stage2))) != 5,
            not ''.join(stage2).isdecimal(),
            not '99' >= (stage2[0]) >= '22',
            not '12' >= (stage2[1]) >= '01',
            not '31' >= (stage2[2]) >= '01',
            not '23' >= (stage2[3]) >= '00',
            not '59' >= (stage2[4]) >= '00'
        )

        self.log(f"[INFO] Stage2 = {stage2}")
        self.log(f"[INFO] S2 Conditions = {s2_conditions}")

        if any(s2_conditions):
            self.log(f"[INFO] GIVEN TASK STRING IS INVALID")
            return False

        self.log(f"[INFO] GIVEN TASK STRING IS VALID")
        return True

    def read_and_sort_tasks_file(self):  # returns the current data sorted and separately in list
        self.log("[FUNCTION] starts -> read_and_sort_tasks_file()")

        with open(self.tasks_path, "r") as a:
            self.log("[INFO] opened 'tasks.txt' in read mode")
            taskslist = sorted(filter(self.is_valid_task, a.read().split('\n')))

            with open(self.tasks_path, "w") as taskfile:
                taskfile.write("\n".join(taskslist))
            self.log("[INFO] wrote sorted task list to tasks file")

        self.log("[INFO] tasks list filtered and sorted")
        self.log(taskslist)

        self.log("[FUNCTION] ends -> read_and_sort_tasks_file()")

        return taskslist

    def status(self):
        self.log("[FUNCTION] starts -> status()")
        self.log("|"*55)

        print(f"\n{' TASKS REMAINING '.center(60, '~')}\n")
        task_list = self.read_and_sort_tasks_file()
        self.log("[INFO] stored tasks in 'task_list'")

        outputs = list(
            map(
                lambda task:
                    f"{f'({task_list.index(task) + 1})'.rjust(4)} {self.timediff(task.split('=')[0])} >>>  {task.split('=')[1].title()}",
                task_list
            )
        )

        self.log('[INFO] outputs created from the tasks list')
        self.log(outputs)

        status_output = "\n".join(outputs) + "\n"
        print(status_output)
        self.log("[INFO] all task details printed on output screen")
        self.log("|"*55)
        self.log("[FUNCTION] ends -> status()")

    def view_task(self, num):
        self.log(f"[FUNCTION] starts -> view_task({num})")
        task_list = self.read_and_sort_tasks_file()
        self.log("[INFO] stored returned 'y' as 'task_list'")
        target_task = task_list[num - 1]
        self.log(f"[INFO] target task : {target_task}")
        dt, t_desc = target_task.split("=")
        tYY, tMM, tDD, tHH, tmm = dt.split(":")
        self.log(f"[INFO] retrieved details of target task")
        tYY = 2000 + int(tYY)
        tMM = list(self.month_names.keys())[list(self.month_names.values()).index(int(tMM))]
        self.log("[INFO] changed year to YYYY form and month number to Name")
        tt12h = int(tHH) % 12
        ttampm = ("AM", "PM")[int(tHH) // 12 == 1]
        if tt12h == 0:
            tt12h = 12
            if int(tmm) == 0:
                if tHH == "00":
                    ttampm = f"MIDNIGHT ({int(tDD) - 1} | {int(tDD)})"
                else:
                    ttampm = "NOON"
        self.log("[INFO] changed hours to 12h format with AM/PM/NOON/MIDNIGHT")
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
        self.log("[INFO] task view output printed")
        self.log(f"[FUNCTION] ends -> view_task({num})")

    def remove(self, num):
        self.log(f"[FUNCTION] starts -> remove({num})")
        last = self.read_and_sort_tasks_file()
        self.log("[INFO] stored returned 'y' as 'last'")
        self.log(f"[INFO] task {num} requested to be removed ")
        last.remove(last[int(num) - 1])
        self.log(f"[INFO] removed requested task from the list")
        self.log(last)
        new_output = "\n".join(last)
        with open(self.tasks_path, "w") as taskfile:
            self.log("[INFO] opened 'tasks.txt' in write mode")
            taskfile.write(new_output)
            self.log("[INFO] wrote new output to 'tasks.txt'")
        self.log(f"[FUNCTION] ends -> remove({num})")
        self.info_bar(f"removed task {num} from the list")

    def edit_task(self, num):
        self.log(f"[FUNCTION] starts -> edit_task({num})")
        last = self.read_and_sort_tasks_file()
        self.log("[INFO] stored returned 'y' as 'last'")
        task_ind = int(num) - 1
        target_task = last[int(num) - 1]
        self.log(f"[INFO] task number {num} requested for edit")
        ttask_time, ttask_name = target_task.split("=")
        self.log("[INFO] stored values of task to be edited as ttask_time and ttask_name")
        self.log(f"[INFO] original values: {ttask_time} and {ttask_name}")

        edit_task_help = (
            '-' * 60, f" EDIT TASK {num} ".center(60, '-'), '',
            '(Enter the corresponding number)'.center(60),
            "1. Date-Time",
            "2. Task Description",
            "3. Both",
            "4. Exit EDIT MODE"
        )
        self.info_bar(f"edit mode for task {num}")
        print(*edit_task_help, sep='\n', end='\n\n')
        while True:
            try:
                edited = False
                exited = False
                self.log("[WAITING] FOR 'choice' INPUT")
                edit_choice = int(input("> "))
                self.log(f"[INFO] received 'choice': {edit_choice}")
                if edit_choice == 1:
                    self.log("[INFO] user input 1 to edit date-time only")
                    self.info_bar(f"task {num} edit: type '/cancel' to cancel")
                    print('-' * 60, f" EDIT TASK {num} ".center(60, '-'), sep='\n', end='\n\n')
                    mn, hr, dt, mth, yr = self.new_task_time()
                    if (mn, hr, dt, mth, yr) != (0, 0, 0, 0, 0):
                        ttask_time = f"{yr}:{mth}:{dt}:{hr}:{mn}"
                        self.log("[INFO] updated task details saved")
                        edited = True
                    else:
                        self.info_bar(f"edit mode for task {num}")
                        print(*edit_task_help, sep='\n', end='\n\n')
                elif edit_choice == 2:
                    self.log("[INFO] user input 2 to edit name only")
                    self.info_bar(f"task {num} edit: type '/cancel' to cancel")
                    print('-' * 60, f" EDIT TASK {num} ".center(60, '-'), sep='\n', end='\n\n')
                    ttask_name = self.new_task_name()
                    if ttask_name != "/cancel":
                        self.log("[INFO] updated task details saved")
                        edited = True
                    else:
                        self.info_bar(f"edit mode for task {num}")
                        print(*edit_task_help, sep='\n', end='\n\n')
                elif edit_choice == 3:
                    self.log("[INFO] user input 3 to edit both task name and date-time")
                    self.info_bar(f"task {num} edit: type '/cancel' to cancel")
                    print('-' * 60, f" EDIT TASK {num} ".center(60, '-'), sep='\n', end='\n\n')
                    ttask_name = self.new_task_name()
                    if ttask_name != "/cancel":
                        self.log("[INFO] updated task details saved")
                        mn, hr, dt, mth, yr = self.new_task_time()
                        if (mn, hr, dt, mth, yr) != (0, 0, 0, 0, 0):
                            ttask_time = f"{yr}:{mth}:{dt}:{hr}:{mn}"
                            self.log("[INFO] updated task details saved")
                            edited = True
                        else:
                            self.info_bar(f"edit mode for task {num}")
                            print(*edit_task_help, sep='\n', end='\n\n')
                    else:
                        self.info_bar(f"edit mode for task {num}")
                        print(*edit_task_help, sep='\n', end='\n\n')
                elif edit_choice == 4:
                    self.log(
                        f"[INFO] user input 4 to exit edit-mode for task number {num}"
                    )
                    exited = True
                else:
                    self.log(f"[ERROR] invalid value entered in edit mode: {edit_choice}")
                    self.log("[INFO] allowed values = 1, 2, 3, 4")
                    self.info_bar("choose out of 1, 2, 3, 4 only")
                    print(*edit_task_help, sep='\n', end='\n\n')

                if edited:
                    edited_task = f"{ttask_time}={ttask_name}"
                    self.log(f"[INFO] old task: {last[task_ind]}")
                    last[task_ind] = edited_task
                    self.log("[INFO] replaced old task in 'last' with edited task")
                    self.log(f"[INFO] new task: {edited_task}")
                    with open(self.tasks_path, "w") as taskfile:
                        new_output = "\n".join(last)
                        taskfile.write(new_output)
                        self.log("[INFO] updated output written to 'tasks.txt'")
                        self.log(last)
                    self.log(
                        "[INFO] refreshing output screen with updated values of tasks"
                    )
                    self.info_bar("requested edit successful")
                    print(*edit_task_help, sep='\n', end='\n\n')
                    self.log("[INFO] refreshed")

                if exited:
                    self.log(f"[INFO] exiting edit mode for task {num}")
                    self.info_bar(f"exited edit mode for task {num}")
                    break

            except ValueError:
                self.log(
                    "[ERROR] user typed weird shit instead of numbers... it wasn't very effective"
                )
                self.info_bar("numbers 1, 2, 3, 4 allowed only")
                print(*edit_task_help, sep='\n', end='\n\n')
        self.log("[INFO] edited name/date-time of requested task")
        self.log(f"[FUNCTION] ends -> edit_task({num})")

    def new_task_name(self):
        self.log("[FUNCTION] starts -> new_task_name()")
        while True:
            self.log("[WAITING] for task name input")
            taskinfo = input(f"{'New Task Name (30 chars)'.ljust(27)}:  ").strip()
            self.log(f"[INFO] task name input: {taskinfo}")
            if taskinfo == "/cancel":
                self.log("[INFO] user chose to cancel new task addition")
                self.log("[FUNCTION] ends -> new_task_name()")
                return taskinfo
            elif taskinfo != "":
                if len(taskinfo) <= 30:
                    if "=" not in taskinfo:
                        self.log("[INFO] stored input from user as task name")
                        self.log(f"[INFO] new task name: {taskinfo}")
                        self.log("[INFO] returned 'taskinfo'")
                        self.log("[FUNCTION] ends -> new_task_name()")
                        return taskinfo
                    else:
                        print("Task Name cannot contain symbol '='\n")
                        self.log("[ERROR] task name contains symbol =")
                else:
                    print("Task Name cannot be more than 30 characters\n")
                    self.log("[ERROR] task name is more than 30 characters")
            else:
                print("Task Name cannot be empty\n")
                self.log("[ERROR] task description cannot be empty")

    def new_task_time(self):
        self.log("[FUNCTION] starts -> new_task_time()")
        while True:
            while True:  # ask for date
                self.log("[WAITING] for date input")
                tdate = input(f"{'Date (DD)'.ljust(27)}:  ").strip()
                self.log(f"[INFO] date input: {tdate}")
                if tdate.lower() == "/cancel":
                    self.log("[INFO] user chose to cancel new task addition")
                    self.log("[FUNCTION] ends -> new_task_time()")
                    return 0, 0, 0, 0, 0
                elif tdate.isdecimal() and (int(tdate) in range(1, 32)):
                    self.log(f"[INFO] date number valid")
                    if len(tdate) > 2:
                        tdate = tdate[-2:]
                    tdate = tdate.zfill(2)
                    self.log(
                        "[INFO] converted (if any) single digit date to double digit"
                    )
                    self.log(f"[INFO] {tdate}")
                    break
                else:
                    self.log(
                        f"[ERROR] user doesn't know dates naturally go from 1 to 31, wrote: {tdate}"
                    )
                    print("Invalid date entered\n")

            while True:  # ask for month
                self.log("[WAITING] for month input (num/words)")
                tmonth = input(f"{'Month (MM/Name)'.ljust(27)}:  ").lower().strip()
                self.log(f"[INFO] month input: {tmonth}")
                twordmonth = None
                if tmonth == "/cancel":
                    self.log("[INFO] user chose to cancel new task addition")
                    self.log("[FUNCTION] ends -> new_task_time()")
                    return 0, 0, 0, 0, 0
                elif tmonth.isalpha():
                    self.log("[INFO] input is alphabetic")
                    for k, v in self.month_names.items():
                        self.log(f"[INFO] checking table month_names item = {k}: {v}")
                        if tmonth in k:
                            self.log(f"[INFO] {tmonth} in {k} = True")
                            twordmonth = k
                            tmonth = str(v).zfill(2)
                            self.log(
                                f"[INFO] corresponding number to the month {k} = {tmonth}"
                            )
                            break
                        self.log(f"[INFO] {tmonth} in {k} = False")
                    if tmonth.isdecimal():
                        self.log(
                            f"[INFO] tmonth modified to a number successfully: {tmonth}"
                        )
                        break
                    else:
                        self.log(f"[ERROR] seriously, what month is this: {tmonth}")
                        print("Invalid month entered\n")

                elif str(tmonth).isdecimal() and (int(tmonth) in range(1, 13)):
                    self.log("[INFO] converting month number to a 2 digit number")
                    if len(tmonth) > 2:
                        tmonth = tmonth[-2:]
                    month_names_values = self.month_names.values()
                    tpos = list(month_names_values).index(int(tmonth))
                    twordmonth = list(self.month_names.keys())[tpos]
                    tmonth = tmonth.zfill(2)
                    self.log(f"[INFO] {tmonth}")
                    break
                else:
                    self.log(
                        f"[ERROR] something wrong with the month entered by the user: {tmonth}"
                    )
                    print("Invalid month entered\n")

            # check if this date exists in this month
            if int(tdate) > self.months[tmonth]:
                self.log(
                    f"[ERROR] umm, month {tmonth} a.k.a {twordmonth} doesn't have {tdate} days..."
                )
                print("Invalid date entered for the given month\n")
            else:
                self.log("[INFO] confirmed valid date for given month")
                valid_date = True
                special_feb_case = False
                # special Feb 29 case
                if int(tmonth) == 2 and int(tdate) == 29:
                    special_feb_case = True
                    valid_date = False
                    self.log(
                        "[INFO] user has entered the date 29 for the month 02 (February), year yet to be checked"
                    )

                while True:  # ask for year
                    self.log("[WAITING] for year input")
                    tyear = input(f"{'Year (YYYY) (2022-99)'.ljust(27)}:  ").strip()
                    self.log(f"[INFO] year input: {tyear}")
                    if tyear.lower() == "/cancel":
                        self.log("[INFO] user chose to cancel new task addition")
                        self.log("[FUNCTION] ends -> new_task_time()")
                        return 0, 0, 0, 0, 0
                    elif tyear.isdecimal() and (int(tyear) in range(2022, 2100)):
                        self.log(f"[INFO] confirmed year lies between 2022 and 2100")
                        if special_feb_case and int(tyear) % 4 == 0:
                            self.log(
                                f"[INFO] entered year is confirmed leap year: {tyear}"
                            )
                            valid_date = True
                            tyear = tyear[-2:]
                            self.log(
                                f"[INFO] last 2 digits of input year stored: {tyear}"
                            )
                            break
                        elif special_feb_case and (int(tyear) % 4 != 0 or (
                            int(tyear) % 100 == 0 and int(tyear) % 400 != 0
                        )):
                            self.log(
                                "[ERROR] entered year is not a leap year while date-month given by user is 29 Feb"
                            )
                            print("Non-Leap Year cannot have Feb 29\n")
                            break
                        else:
                            tyear = tyear[-2:]
                            self.log(
                                f"[INFO] last 2 digits of input year stored: {tyear}"
                            )
                            break
                    else:
                        self.log(f"[ERROR] invalid year received: {tyear}")
                        print("Invalid Year entered\n")
                if valid_date:
                    break

        while True:  # ask for hours
            self.log("[WAITING] for hours input")
            thour = input(f"{'Hours (HH)(24h)'.ljust(27)}:  ").strip()
            self.log(f"[INFO] received hour input: {thour}")
            if thour.lower() == "/cancel":
                self.log("[INFO] user chose to cancel new task addition")
                self.log("[FUNCTION] ends -> new_task_time()")
                return 0, 0, 0, 0, 0
            elif thour.isdecimal() and (int(thour) in range(24)) and thour != "":
                self.log("[INFO] confirmed valid input for hours")
                if len(thour) > 2:
                    thour = thour[-2:]
                thour = thour.zfill(2)
                self.log(f"[INFO] stored hours: {thour}")
                break
            else:
                self.log(
                    f"[ERROR] Earth doesn't have these amount of hours in a day: {thour}"
                )
                print("Invalid hours entered\n")

        while True:  # ask for minutes
            self.log("[WAITING] for minutes input")
            tmin = input(f"{'Minutes (mm)'.ljust(27)}:  ").strip()
            self.log(f"[INFO] minute input received: {tmin}")
            if tmin == "/cancel":
                self.log("[INFO] user chose to cancel new task addition")
                self.log("[FUNCTION] ends -> new_task_time()")
                return 0, 0, 0, 0, 0
            elif tmin.isdecimal() and (int(tmin) in range(60)) and tmin != "":
                self.log("[INFO] confirmed valid input for minutes")
                if len(tmin) > 2:
                    tmin = tmin[-2:]
                tmin = tmin.zfill(2)
                self.log(f"[INFO] stored mins: {tmin}")
                break
            else:
                self.log(f"[ERROR] invalid minutes value entered: {tmin}")
                print("Invalid minutes entered\n")

        self.log(f"[INFO] 5 values returned: {tmin}, {thour}, {tdate}, {tmonth}, {tyear}")
        self.log("[FUNCTION] ends -> new_task_time()")
        return tmin, thour, tdate, tmonth, tyear

    def new_task(self):
        self.log("[FUNCTION] starts -> new_task()")
        self.log("[INFO] calling related functions...")
        taskinfo = self.new_task_name()
        if taskinfo == "/cancel":
            self.info_bar("task addition cancelled")
        else:
            tmin, thour, tdate, tmonth, tyear = self.new_task_time()
            if (tmin, thour, tdate, tmonth, tyear) == (0, 0, 0, 0, 0):
                self.info_bar("task addition cancelled")
            else:
                taskcell = f"{tyear}:{tmonth}:{tdate}:{thour}:{tmin}={taskinfo}"
                self.log("[INFO] combined values of new_task_name() and new_task_time()")
                self.log(f"[INFO] {taskcell}")
                self.log("[INFO] calling function add(new)")
                self.add(taskcell)
                self.info_bar("new task added")
        self.log("[FUNCTION] ends -> new_task()")

    def add(self, new):
        self.log("[FUNCTION] starts -> add(new)")
        self.log(f"[INFO] appending [{new}] to 'tasks.txt'")
        taskfile = open(self.tasks_path, "a")
        taskfile.write("\n" + new)
        taskfile.close()
        self.log("[INFO] appended successfully")
        self.log("[FUNCTION] ends -> add(new)")


class App(Functions):
    def console_loop(self):
        try:
            self.check_tasky_folders()
            self.log(f">> >> >> >> >> >> >> >> >> >> >> >> >> >>")
            self.log(f"[PROGRAM STARTED]")
            self.check_tasky_log()
            self.check_tasks_txt()
            self.log("[INFO] imported datetime and os modules")
            self.log("[INFO] printing pending tasks details...")
            self.info_bar("enter 'help' to view valid commands")
            n = 0  # used variable, do not remove :D

            while True:
                task_list = self.read_and_sort_tasks_file()
                total_tasks = len(task_list)
                self.log(f"[INFO] current total number of tasks: {total_tasks}")
                self.log("[WAITING] FOR MAIN USER INPUT")
                user_inp = input(f"\n  >  ").lower().strip()
                self.log(f"[INFO] user input: {user_inp}")
                words = user_inp.split()
                if user_inp == '':
                    self.log(
                        f"[ERROR] i feel empty inside :( just like the user's input..."
                    )
                    self.info_bar("enter 'help' to view valid commands")
                    self.log("[INFO] main loop rerunning...")
                    continue

                self.log("[INFO] user input empty = False")
                if user_inp in ("quit", "bye"):
                    self.log("[INFO] user chose to exit program")
                    sysend()
                elif user_inp == "tasky-debug":
                    self.log("[DEBUG] opening logs folder for debugging")
                    self.info_bar("request for logs folder")
                    startfile(self.taskylog_path)
                elif user_inp in ("help", "h"):
                    self.log("[INFO] user chose help, displaying available commands")
                    self.info_bar("DISPLAYING HELP MENU")
                    print(
                        '-' * 60,
                        "(Press ENTER to refresh the tasks list)\n".center(56),
                        f"{'Add a New Task'.ljust(20)} --  add / new / create",
                        f"{'Delete Task N'.ljust(20)} --  delete N / del N / remove N / rem N",
                        f"{'Edit Task N'.ljust(20)} --  edit N / ed N / change N",
                        f"{'Task Details'.ljust(20)} --  (ENTER TASK NUMBER)",
                        f"{'Open Help Menu'.ljust(20)} --  help / h",
                        f"{'Exit Tasky'.ljust(20)} --  quit / bye",
                        sep="\n"
                    )
                    print("-" * 60)
                elif user_inp.isdecimal() and int(user_inp) in range(1, total_tasks + 1):
                    self.log(f"[INFO] user requested to view task {int(user_inp)}")
                    self.info_bar(f"viewing task {int(user_inp)}")
                    self.view_task(int(user_inp))
                elif user_inp in ("add", "new", "create"):
                    self.log("[INFO] user requested to add a new task")
                    while True:
                        self.log("[WAITING] for confirmation")
                        confirm = input("\nConfirm new task? (enter y/n):  ").lower().strip()
                        self.log(f"[INFO] confirmation input: {confirm}")
                        if confirm != "" and confirm[0] == "y":
                            self.log("[INFO] confirmed")
                            self.info_bar(
                                "type '/cancel' to stop task addition"
                            )
                            print(
                                "-" * 60,
                                " NEW TASK DETAILS ".center(60, '-'),
                                sep='\n', end='\n\n'
                            )
                            self.new_task()
                            n = 0
                            self.log("[INFO] output screen refreshed with tasks")
                            break
                        elif confirm != "" and confirm[0] == "n":
                            self.log("[INFO] cancelled")
                            self.info_bar("new task cancelled")
                            self.log("[INFO] output screen refreshed with tasks")
                            break
                        else:
                            self.log(
                                f"[ERROR] oonga boonga man wrote '{confirm}' instead of yes/no"
                            )
                            self.info_bar("please enter y/n")
                elif words[0] in ("delete", "del", "remove", "rem"):
                    if len(words) == 2 and words[1].isdecimal():
                        self.log(
                            f"[INFO] user requested to remove task number {words[1]}"
                        )
                        if int(words[1]) in range(1, total_tasks + 1):
                            self.log(f"[INFO] task number confirmed valid")
                            while True:
                                self.log("[WAITING] for confirmation")
                                confirm = input(
                                    f"\nConfirm removal of task {words[1]}? (enter y/n):  "
                                ).lower()
                                self.log(f"[INFO] confirmation input: {confirm}")
                                if confirm != "" and confirm[0] == "y":
                                    self.log("[INFO] confirmed")
                                    self.remove(words[1])
                                    n = 0
                                    self.log(
                                        "[INFO] refreshed output screen with new tasks"
                                    )
                                    break
                                elif confirm != "" and confirm[0] == "n":
                                    self.log("[INFO] cancelled")
                                    self.info_bar("task removal cancelled")
                                    self.log(
                                        "[INFO] refreshed output screen with new tasks"
                                    )
                                    break
                                else:
                                    self.log(
                                        f"[ERROR] oonga boonga man wrote '{confirm}' instead of yes/no"
                                    )
                                    self.info_bar("please enter y/n")
                        else:
                            self.log(
                                f"[ERROR] task {words[1]} doesn't exist, total tasks = {total_tasks}"
                            )
                            self.info_bar(
                                "invalid task number to be removed",
                            )
                    else:
                        self.log(f"[ERROR] command used incorrectly: {user_inp}")
                        self.info_bar(f"error! try again like '{words[0]} 1'")
                elif words[0] in ("edit", "ed", "change"):
                    if len(words) == 2 and words[1].isdecimal():
                        self.log(
                            f"[INFO] user requested to edit task number {words[1]}"
                        )
                        if int(words[1]) in range(1, total_tasks + 1):
                            self.log(f"[INFO] task number confirmed valid")
                            while True:
                                self.log("[WAITING] for confirmation")
                                confirm = input(
                                    f"\nConfirm edit of task {int(words[1])}? (enter y/n):  "
                                ).lower()
                                if confirm != "" and confirm[0] == "y":
                                    self.log("[INFO] confirmed")
                                    self.edit_task(int(words[1]))
                                    n = 0
                                    self.log(
                                        "[INFO] refreshed output screen with new tasks"
                                    )
                                    break
                                elif confirm != "" and confirm[0] == "n":
                                    self.log("[INFO] cancelled")
                                    print("Task edit cancelled")
                                    self.info_bar("task edit cancelled")
                                    self.log(
                                        "[INFO] refreshed output screen with new tasks"
                                    )
                                    break
                                else:
                                    self.log(
                                        f"[ERROR] oonga boonga man wrote '{confirm}' instead of yes/no"
                                    )
                                    self.info_bar("please enter y/n")
                        else:
                            self.log(
                                f"[ERROR] task {words[1]} doesn't exist, total tasks = {total_tasks}"
                            )
                            self.info_bar(
                                f"invalid task number to be edited",
                            )
                    else:
                        self.log(f"[ERROR] command used incorrectly: {user_inp}")
                        self.info_bar(f"error! try again like '{words[0]} 4'")
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
                    self.log(f"[INFO] user greeted Tasky")
                    self.info_bar(hello_list[n])
                    n += 1
                    if n > 42:
                        n = 0
                elif words[0].upper() in self.spl:
                    self.log(f"[INFO] Special Input: {words[0]}")
                    self.info_bar(words[0].upper())
                else:
                    self.log(f"[ERROR] command doesn't exist: {user_inp}")
                    self.info_bar("enter 'help' to view valid commands")

                self.log("[INFO] main loop rerunning...")
        except SystemExit:
            self.log(f"[EXIT] Program closed")


if __name__ == "__main__":
    app = App()
    app.console_loop()
