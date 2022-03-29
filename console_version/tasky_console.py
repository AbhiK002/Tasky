import datetime
from os import makedirs, startfile, system
from pathlib import Path
from random import randint
from sys import exit as sysend


class Functions:
    def __init__(self):
        self.log_prefix = self.log_dated_names()
        self.home_path = Path.home()
        self.taskymain_path = self.home_path / "Tasky"
        self.tasks_path = self.taskymain_path / "tasks.txt"

        self.taskylog_path = self.taskymain_path / "taskylogs"

        self.cookie_folder_path = self.taskylog_path/ "cookie"

    def check_tasky_folders(self):
            self.taskylog_path.mkdir(parents=True,exist_ok=True)

    def cookie_dir(self):
        if not self.cookie_folder_path.is_dir() :
            return False, self.cookie_folder_path, 0
        if not (self.cookie_folder_path / "cookies.txt").is_file():
            return True, self.cookie_folder_path, 0
        with open(self.cookie_folder_path / "cookies.txt", "r") as cookiefile:
            count = cookiefile.readlines()
        while "\n" in count:
            count.remove("\n")
            for i in range(len(count)):
                count[i] = count[i].replace("\n", "")
        if len(count) != 1 or not count[0].isdecimal():
            return True, self.cookie_folder_path, 0
        if 0 <= int(count[0]) <= 15:
            return True, self.cookie_folder_path, int(count[0])
        elif int(count[0]) > 15:
            return True, self.cookie_folder_path, 15
        else:
            return True, self.cookie_folder_path, 0

    @staticmethod
    def log_dated_names():
        t = datetime.datetime.now()
        a = str(t)[:-10]
        a = a.replace("-", "_")
        a = a.replace(":", "")
        a = a.replace(" ", "__")
        return str(a)

    def check_tasky_log(self):
        try:
            log_file = open(self.taskylog_path / f"{self.log_prefix}.log", "r")
            log_file.close()
        except FileNotFoundError:
            log_file = open(self.taskylog_path / f"{self.log_prefix}.log", "w")
            log_file.close()

    def log(self, data):
        with open(self.taskylog_path / f"{self.log_prefix}.log", "a") as file:
            current_dt = str(datetime.datetime.now())[:-4]
            file.write(f"{current_dt} >> {str(data)}" + "\n")

    def check_tasks_txt(self):
        try:
            self.log("[INFO] attempted to open tasks.txt in read mode")
            with open(self.tasks_path, "r") as b:
                self.log("[INFO] attempt successful")
        except FileNotFoundError:
            self.log("[ERROR] attempt failed, can't find tasks.txt")
            with open(self.tasks_path, "w") as b:
                self.log("[INFO] created empty text file 'tasks.txt'")

    def make_dicts(self):
        months = {
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

        month_names = {
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
        self.log("[INFO] defined dict 2 (month_names)")

        return months, month_names

    def clear(self):
        self.log("[FUNCTION] starts -> clear()")
        system("cls")
        self.log("[INFO] output screen cleared")
        self.log("[FUNCTION] ends -> clear()")

    def info_bar(self, data, monthsdict):
        data = str(data)
        self.clear()
        self.status(monthsdict)
        print(f"<< {data.center(40)} >>" + "\n")

    def timediff(self, tt, monthsdict):
        self.log("[FUNCTION] starts -> timediff()")
        tt = tt.split(":")
        self.log(f"[INFO] split variable named 'tt' {tt} into 5 parts")
        # time now
        tn = datetime.datetime.now()
        self.log("[INFO] calculated current date-time as variables")
        tny = tn.strftime("%y")
        self.log(f"[INFO] year: {tny}")
        tnm = tn.strftime("%m")
        self.log(f"[INFO] month: {tnm}")
        tnd = tn.strftime("%d")
        self.log(f"[INFO] date: {tnd}")
        tnh = tn.strftime("%H")
        self.log(f"[INFO] hours: {tnh}")
        tnmin = tn.strftime("%M")
        self.log(f"[INFO] min: {tnmin}")

        # task time
        tty = tt[0]
        ttm = tt[1]
        ttd = tt[2]
        tth = tt[3]
        ttmin = tt[4]
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
            diffd = monthsdict.get(str(tnm)) + diffd
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
            diffy = str(diffy)
            diffm = str(diffm)
            diffd = str(diffd)
            diffh = str(diffh)
            diffmin = str(diffmin)
            self.log("[INFO] converted 'difference' numbers to strings")

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

    def read_and_sort_tasks_file(
            self,
    ):  # returns the current data sorted and separately in list
        self.log("[FUNCTION] starts -> read_and_sort_tasks_file()")
        with open(self.tasks_path, "r") as a:
            self.log("[INFO] opened 'tasks.txt' in read mode")
            x = a.readlines()
        self.log("[INFO] stored every raw line of 'tasks.txt' in a list called 'x'")
        self.log(x)
        y = []
        while "\n" in x:
            x.remove("\n")
        self.log("[INFO] removed newline characters from 'x'")
        self.log(x)
        for item in x:
            item = item.replace("\n", "")
            y += [item]

        self.log("[INFO] removed newline characters from every item of 'x'")
        self.log(y)
        tasklist = self.sort_tasks(y)
        self.log("[INFO] returned sorted list = tasklist")
        self.log("[FUNCTION] ends -> read_and_sort_tasks_file()")
        return tasklist

    def sort_tasks(self, tlist):
        self.log("[FUNCTION] starts -> sort_tasks(tlist, tdir)")
        nums = []
        self.log("[INFO] created empty list nums")
        temp_dict = {}
        self.log("[INFO] created empty dictionary temp_dict")
        for task in tlist:
            rawtime = task[:14]
            rawtime = rawtime.replace(":", "")
            nums += [int(rawtime)]
            temp_dict[tlist.index(task)] = int(rawtime)
        self.log(f"[INFO] nums = {nums}")
        self.log(f"[INFO] temp_dict = {temp_dict}")
        nums.sort()
        self.log(f"[INFO] sorted nums list = {nums}")
        for k, v in temp_dict.items():
            nums[nums.index(v)] = tlist[k]
        self.log(
            "[INFO] replaced respective numbers with tasks of same index as nums' initial index"
        )

        sorted_output = "\n".join(nums)
        with open(self.tasks_path, "w") as taskfile:
            taskfile.write(sorted_output)
        self.log("[INFO] sorted output written to tasks.txt")
        self.log(f"[INFO] returned nums = {nums}")
        self.log("[FUNCTION] ends -> sort_tasks()")
        return nums

    def status(self, monthsdict):
        self.log("[FUNCTION] starts -> status()")
        self.log("|||||||||||||||||||||||||||||||||||||||||||||||||||||||")
        print("\n~~~~~~~~ TASKS REMAINING ~~~~~~~~\n")
        task_list = self.read_and_sort_tasks_file()
        self.log("[INFO] stored returned 'y' as 'task_list'")
        outputs = []
        self.log("[INFO] started iterating through 'task_list'")
        for taskline in task_list:
            taskparts = taskline.split("=")
            self.log(f"[INFO] working with task number  {task_list.index(taskline) + 1}")
            rawtasktime = self.timediff(taskparts[0], monthsdict)
            self.log(f"[INFO] rawtasktime: {rawtasktime}")
            rawtaskinfo = taskparts[1]
            self.log(f"[INFO] rawtaskinfo: {rawtaskinfo}")
            taskoutput = [
                f"({task_list.index(taskline) + 1}) {rawtasktime} >>> {rawtaskinfo.title()}"
            ]
            outputs += taskoutput
        self.log(
            "[INFO] stored each task details separately as (task number) (task time remaining) >>> (task name)"
        )
        self.log(outputs)
        status_output = "\n".join(outputs)
        print(status_output + "\n")
        self.log("[INFO] all task details printed on output screen")
        self.log("|||||||||||||||||||||||||||||||||||||||||||||||||||||||")
        self.log("[FUNCTION] ends -> status()")

    def remove(self, num, monthsdict):
        self.log(f"[FUNCTION] starts -> remove({num})")
        last = self.read_and_sort_tasks_file()
        self.log("[INFO] stored returned 'y' as 'last'")
        self.log(f"[INFO] task {num} requested to be removed ")
        rem_index = int(num) - 1
        rem_task = last[rem_index]
        last.remove(rem_task)
        self.log(f"[INFO] removed requested task [{rem_task}] from the list")
        self.log(last)
        new_output = "\n".join(last)
        with open(self.tasks_path, "w") as taskfile:
            self.log("[INFO] opened 'tasks.txt' in write mode")
            taskfile.write(new_output)
            self.log("[INFO] wrote new output to 'tasks.txt'")
        self.log(f"[FUNCTION] ends -> remove({num})")
        self.info_bar(f"removed task {num} from the list", monthsdict)

    def edit_task(self, num, monthsdict, monthnamesdict):
        self.log(f"[FUNCTION] starts -> edit_task({num})")
        last = self.read_and_sort_tasks_file()
        self.log("[INFO] stored returned 'y' as 'last'")
        task_ind = int(num) - 1
        target_task = last[task_ind]
        self.log(f"[INFO] task number {num} requested for edit")
        ttask_time, ttask_name = target_task.split("=")
        self.log("[INFO] stored values of task to be edited as ttask_time and ttask_name")
        self.log(f"[INFO] original values: {ttask_time} and {ttask_name}")
        edit_task_help = f"\nWhat needs to be edited in task {num}? (Enter corresponding number)\n1. Date-Time\n2. Task Description\n3. Both\n4. Exit EDIT MODE\n"
        self.info_bar(f"edit mode for task {num}", monthsdict)
        print(edit_task_help)
        while True:
            try:
                edited = False
                exited = False
                self.log("[WAITING] FOR 'choice' INPUT")
                choice = int(input("> "))
                self.log(f"[INFO] received 'choice': {choice}")
                if choice == 1:
                    self.log("[INFO] user input 1 to edit date-time only")
                    self.info_bar(f"task {num} edit: type 'cancel' to cancel", monthsdict)
                    mn, hr, dt, mth, yr = self.new_task_time(monthsdict, monthnamesdict)
                    if (mn, hr, dt, mth, yr) != (0, 0, 0, 0, 0):
                        ttask_time = f"{yr}:{mth}:{dt}:{hr}:{mn}"
                        self.log("[INFO] updated task details saved")
                        edited = True
                    else:
                        self.info_bar(f"edit mode for task {num}", monthsdict)
                        print(edit_task_help)
                elif choice == 2:
                    self.log("[INFO] user input 2 to edit name only")
                    self.info_bar(f"task {num} edit: type 'cancel' to cancel", monthsdict)
                    ttask_name = self.new_task_name()
                    if ttask_name != "cancel":
                        self.log("[INFO] updated task details saved")
                        edited = True
                    else:
                        self.info_bar(f"edit mode for task {num}", monthsdict)
                        print(edit_task_help)
                elif choice == 3:
                    self.log("[INFO] user input 3 to edit both task name and date-time")
                    self.info_bar(f"task {num} edit: type 'cancel' to cancel", monthsdict)
                    ttask_name = self.new_task_name()
                    if ttask_name != "cancel":
                        self.log("[INFO] updated task details saved")
                        mn, hr, dt, mth, yr = self.new_task_time(
                            monthsdict, monthnamesdict
                        )
                        if (mn, hr, dt, mth, yr) != (0, 0, 0, 0, 0):
                            ttask_time = f"{yr}:{mth}:{dt}:{hr}:{mn}"
                            self.log("[INFO] updated task details saved")
                            edited = True
                        else:
                            self.info_bar(f"edit mode for task {num}", monthsdict)
                            print(edit_task_help)
                    else:
                        self.info_bar(f"edit mode for task {num}", monthsdict)
                        print(edit_task_help)
                elif choice == 4:
                    self.log(
                        f"[INFO] user input 4 to exit edit-mode for task number {num}"
                    )
                    exited = True
                else:
                    self.log(f"[ERROR] invalid value entered in edit mode: {choice}")
                    self.log("[INFO] allowed values = 1, 2, 3, 4")
                    self.info_bar("choose out of 1, 2, 3, 4 only", monthsdict)
                    print(edit_task_help)

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
                    self.info_bar("requested edit successful", monthsdict)
                    print(edit_task_help)
                    self.log("[INFO] refreshed")

                if exited:
                    self.log(f"[INFO] exiting edit mode for task {num}")
                    self.info_bar(f"exited edit mode for task {num}", monthsdict)
                    break

            except ValueError:
                self.log(
                    "[ERROR] user typed weird shit instead of numbers... it wasn't very effective"
                )
                self.info_bar("numbers 1, 2, 3, 4 allowed only", monthsdict)
                print(edit_task_help)
        self.log("[INFO] edited name/date-time of requested task")
        self.log(f"[FUNCTION] ends -> edit_task({num})")

    def new_task_name(self):
        self.log("[FUNCTION] starts -> new_task_name()")
        while True:
            self.log("[WAITING] for task description input")
            taskinfo = input("New Task description (50 chars): ").strip()
            self.log(f"[INFO] task description input: {taskinfo}")
            if taskinfo == "cancel":
                self.log("[INFO] user chose to cancel new task addition")
                self.log("[FUNCTION] ends -> new_task_name()")
                return taskinfo
            elif taskinfo != "":
                if len(taskinfo) <= 50:
                    if "=" not in taskinfo:
                        self.log("[INFO] stored input from user as task description")
                        self.log(f"[INFO] new task name: {taskinfo}")
                        self.log("[INFO] returned 'taskinfo'")
                        self.log("[FUNCTION] ends -> new_task_name()")
                        return taskinfo
                    else:
                        print("Task description cannot contain symbol =\n")
                        self.log("[ERROR] task description contains symbol =")
                else:
                    print("Task description cannot be more than 50 characters\n")
                    self.log("[ERROR] task description is more than 50 characters")
            else:
                print("Task description cannot be empty\n")
                self.log("[ERROR] task description cannot be empty")

    def new_task_time(self, monthsdict, monthnamesdict):
        self.log("[FUNCTION] starts -> new_task_time()")
        while True:
            while True:  # ask for date
                self.log("[WAITING] for date input")
                tdate = input("Date: ").strip()
                self.log(f"[INFO] date input: {tdate}")
                if tdate.lower() == "cancel":
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
                tmonth = input("Month (number/name): ").lower().strip()
                self.log(f"[INFO] month input: {tmonth}")
                twordmonth = None
                if tmonth == "cancel":
                    self.log("[INFO] user chose to cancel new task addition")
                    self.log("[FUNCTION] ends -> new_task_time()")
                    return 0, 0, 0, 0, 0
                elif tmonth.isalpha():
                    self.log("[INFO] input is alphabetic")
                    for k, v in monthnamesdict.items():
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
                    month_names_values = monthnamesdict.values()
                    tpos = list(month_names_values).index(int(tmonth))
                    twordmonth = list(monthnamesdict.keys())[tpos]
                    tmonth = tmonth.zfill(2)
                    self.log(f"[INFO] {tmonth}")
                    break
                else:
                    self.log(
                        f"[ERROR] something wrong with the month entered by the user: {tmonth}"
                    )
                    print("Invalid month entered\n")

            # check if this date exists in this month
            if int(tdate) > monthsdict[tmonth]:
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
                    tyear = input("Year (yyyy) (2000-99): ").strip()
                    self.log(f"[INFO] year input: {tyear}")
                    if tyear.lower() == "cancel":
                        self.log("[INFO] user chose to cancel new task addition")
                        self.log("[FUNCTION] ends -> new_task_time()")
                        return 0, 0, 0, 0, 0
                    elif tyear.isdecimal() and (int(tyear) in range(2000, 2100)):
                        self.log(f"[INFO] confirmed year lies between 2000 and 2100")
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
                        elif special_feb_case and int(tyear) % 4 != 0:
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
            thour = input("Hours (24h format): ").strip()
            self.log(f"[INFO] received hour input: {thour}")
            if thour.lower() == "cancel":
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
            tmin = input("Minutes: ").strip()
            self.log(f"[INFO] minute input received: {tmin}")
            if tmin == "cancel":
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

    def new_task(self, monthsdict, monthnamesdict):
        self.log("[FUNCTION] starts -> new_task()")
        self.log("[INFO] calling related functions...")
        taskinfo = self.new_task_name()
        if taskinfo == "cancel":
            self.info_bar("task addition cancelled", monthsdict)
        else:
            tmin, thour, tdate, tmonth, tyear = self.new_task_time(
                monthsdict, monthnamesdict
            )
            if (tmin, thour, tdate, tmonth, tyear) == (0, 0, 0, 0, 0):
                self.info_bar("task addition cancelled", monthsdict)
            else:
                taskcell = f"{tyear}:{tmonth}:{tdate}:{thour}:{tmin}={taskinfo}"
                self.log("[INFO] combined values of new_task_name() and new_task_time()")
                self.log(f"[INFO] {taskcell}")
                self.log("[INFO] calling function add(new)")
                self.add(taskcell)
                self.info_bar("new task added", monthsdict)
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
            months, month_names = self.make_dicts()
            self.log("[INFO] printing pending tasks details...")
            self.info_bar("type 'help' to view valid commands", months)
            n = 0

            while True:
                cookie, ckdir, cookie_count = self.cookie_dir()
                task_list = self.read_and_sort_tasks_file()
                total_tasks = len(task_list)
                self.log(f"[INFO] current total number of tasks: {total_tasks}")
                if cookie and cookie_count > 0:
                    print("Your cookies:" + " @" * cookie_count)
                self.log("[WAITING] FOR MAIN USER INPUT")
                user_inp = input("\n > ").lower().lstrip()
                self.log(f"[INFO] user input: {user_inp}")
                words = user_inp.split()
                if user_inp != "":
                    self.log("[INFO] user input empty = False")
                    if user_inp.startswith(("quit", "bye")):
                        self.log("[INFO] user chose to exit program")
                        sysend()
                    elif user_inp.startswith("debug"):
                        self.log("[DEBUG] opening logs folder for debugging")
                        self.info_bar("opening logs folder for debugging", months)
                        startfile(self.taskylog_path)
                    elif user_inp.startswith("help"):
                        self.log("[INFO] user chose help, displaying available commands")
                        self.info_bar("displaying available commands", months)
                        print(
                            "add / new / create".rjust(35)
                            + " : Add a new Task\n"
                            + "remove N / delete N / del N / rem N : Remove task number 'N'\n"
                            + "(press enter key) / status / ref".rjust(35)
                            + " : Refresh the remaining tasks list\n"
                            + "edit N / change N / ed N".rjust(35)
                            + " : Modify task number 'N' details"
                        )
                        print("quit / q / bye".rjust(35) + " : Exit Tasky")
                        if cookie:
                            if cookie_count > 0:
                                print("\n type 'eat cookie' to eat your cookie")
                            elif cookie_count == 0:
                                print(
                                    "\n you're out of cookies :(\n(type 'cookie' to hopefully get a cookie)"
                                )
                    elif user_inp.startswith(("add", "new", "create")):
                        self.log("[INFO] user requested to add a new task")
                        while True:
                            self.log("[WAITING] for confirmation")
                            confirm = input("\nConfirm new task? ").lower()
                            self.log(f"[INFO] confirmation input: {confirm}")
                            if confirm != "" and confirm[0] == "y":
                                self.log("[INFO] confirmed")
                                self.info_bar(
                                    "type 'cancel' to stop task addition", months
                                )
                                self.new_task(months, month_names)
                                n = 0
                                self.log("[INFO] output screen refreshed with tasks")
                                break
                            elif confirm != "" and confirm[0] == "n":
                                self.log("[INFO] cancelled")
                                self.info_bar("new task cancelled", months)
                                self.log("[INFO] output screen refreshed with tasks")
                                break
                            else:
                                self.log(
                                    f"[ERROR] oonga boonga man wrote '{confirm}' instead of yes/no"
                                )
                                self.info_bar("please enter yes/no", months)
                    elif (
                            ("remove" == words[0])
                            or ("delete" == words[0])
                            or ("del" == words[0])
                            or ("rem" == words[0])
                    ):
                        if len(words) == 2 and words[1].isdecimal():
                            self.log(
                                f"[INFO] user requested to remove task number {words[1]}"
                            )
                            if int(words[1]) in range(1, total_tasks + 1):
                                self.log(f"[INFO] task number confirmed valid")
                                while True:
                                    self.log("[WAITING] for confirmation")
                                    confirm = input(
                                        f"\nConfirm removal of task {words[1]}? "
                                    ).lower()
                                    self.log(f"[INFO] confirmation input: {confirm}")
                                    if confirm != "" and confirm[0] == "y":
                                        self.log("[INFO] confirmed")
                                        self.remove(words[1], months)
                                        n = 0
                                        self.log(
                                            "[INFO] refreshed output screen with new tasks"
                                        )
                                        break
                                    elif confirm != "" and confirm[0] == "n":
                                        self.log("[INFO] cancelled")
                                        self.info_bar("task removal cancelled", months)
                                        self.log(
                                            "[INFO] refreshed output screen with new tasks"
                                        )
                                        break
                                    else:
                                        self.log(
                                            f"[ERROR] oonga boonga man wrote '{confirm}' instead of yes/no"
                                        )
                                        self.info_bar("please enter yes/no", months)
                            else:
                                self.log(
                                    f"[ERROR] task {words[1]} doesn't exist, total tasks = {total_tasks}"
                                )
                                self.info_bar(
                                    f"invalid task number ({words[1]}) to be removed",
                                    months,
                                )
                        else:
                            self.log(f"[ERROR] command used incorrectly: {user_inp}")
                            self.info_bar("error! try again like 'remove 5'", months)
                    elif (
                            ("edit" == words[0])
                            or ("change" == words[0])
                            or ("ed" == words[0])
                    ):
                        if len(words) == 2 and words[1].isdecimal():
                            self.log(
                                f"[INFO] user requested to edit task number {words[1]}"
                            )
                            if int(words[1]) in range(1, total_tasks + 1):
                                self.log(f"[INFO] task number confirmed valid")
                                while True:
                                    self.log("[WAITING] for confirmation")
                                    confirm = input(
                                        f"\nConfirm edit of task {words[1]}? "
                                    ).lower()
                                    if confirm != "" and confirm[0] == "y":
                                        self.log("[INFO] confirmed")
                                        self.edit_task(words[1], months, month_names)
                                        n = 0
                                        self.log(
                                            "[INFO] refreshed output screen with new tasks"
                                        )
                                        break
                                    elif confirm != "" and confirm[0] == "n":
                                        self.log("[INFO] cancelled")
                                        print("Task edit cancelled")
                                        self.info_bar("task edit cancelled", months)
                                        self.log(
                                            "[INFO] refreshed output screen with new tasks"
                                        )
                                        break
                                    else:
                                        self.log(
                                            f"[ERROR] oonga boonga man wrote '{confirm}' instead of yes/no"
                                        )
                                        self.info_bar("please enter yes/no", months)
                            else:
                                self.log(
                                    f"[ERROR] task {words[1]} doesn't exist, total tasks = {total_tasks}"
                                )
                                self.info_bar(
                                    f"invalid task number ({words[1]}) to be edited",
                                    months,
                                )
                        else:
                            self.log(f"[ERROR] command used incorrectly: {user_inp}")
                            self.info_bar("error! try again like 'edit 4'", months)
                    elif user_inp.startswith(("ref", "status")):
                        self.log(f"[INFO] user requested updated task status: {user_inp}")
                        self.log("[INFO] refreshing output screen with new tasks")
                        self.info_bar("refreshed tasks list", months)

                    # (not so) secret commands
                    elif user_inp.startswith(("hi", "hello", "hey")):

                        hello_list = [
                            "hello there :)",
                            "hii :D",
                            "hey-hey user ;)",
                            "hola mi amigo ^-^",
                            "hi again? ;)",
                            "hey :)",
                            "hehe hello ^o^",
                            "hello! type 'help' for other commands",
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
                            "ugh, fine. you earned a cookie i guess",
                            "here take this cookie. keep it with you",
                            "I GAVE YOU A COOKIE, PLEASE STOP",
                            "dont look at my other cookies",
                            "no more cookies for you >:(",
                            "enough with these greetings >_<",
                            "i wont respond to these keywords now",
                            "nope. not doing it.",
                            "ill be here if you need me >:(",
                            "not responding to greetings for real now",
                            "go complete your tasks user :/",
                            "BYE",
                            "type 'help' ._.",
                        ]

                        self.log(f"[INFO] user greeted Tasky")

                        if not cookie:
                            if n == 31:
                                cookie = True
                                ckdir.mkdir(parents=True,exist_ok=True)
                                cookie_count += 1
                                cookiefile = open(self.cookie_folder_path / "cookies.txt", "w")
                                cookiefile.write(str(cookie_count))
                                cookiefile.close()
                            self.info_bar(hello_list[n], months)
                        else:
                            if n == 30:
                                self.info_bar(
                                    "you did get a cookie last time from me", months
                                )
                            elif n == 31:
                                if cookie_count == 0:
                                    self.info_bar("you ate it yourself...", months)
                                else:
                                    self.info_bar("dont ask for another cookie", months)
                            elif n == 32:
                                self.info_bar("im hungry too >:(", months)
                            else:
                                self.info_bar(hello_list[n], months)
                        if n != 42:
                            n += 1

                    elif (
                            user_inp.startswith(":)")
                            or user_inp.upper().startswith(":D")
                            or user_inp.startswith(":(")
                            or user_inp.startswith(":>")
                            or user_inp.startswith(":<")
                    ):
                        self.log(f"[INFO] {user_inp[:2]}")
                        self.info_bar(f"{user_inp[:2].upper()}", months)
                    elif (
                            user_inp.startswith(">:(")
                            or user_inp.upper().startswith(">:)")
                            or user_inp.startswith("._.")
                            or user_inp.startswith(".-.")
                            or user_inp.lower().startswith("o_o")
                    ):
                        self.log(f"[INFO] {user_inp[:3]}")
                        self.info_bar(f"{user_inp[:3].upper()}", months)

                    elif words[0] == "cookie":
                        if cookie:
                            if 0 <= cookie_count < 15:
                                find = randint(1, 23)
                                if find == 22:
                                    self.info_bar(
                                        "ooh! found a cookie. ugh fine take it", months
                                    )
                                    cookie_count += 1
                                    cookiefile = open(self.cookie_folder_path / "cookies.txt", "w")
                                    cookiefile.write(str(cookie_count))
                                    cookiefile.close()
                                else:
                                    self.info_bar(
                                        "didn't find any spare cookies, go away", months
                                    )
                            elif cookie_count == 15:
                                self.info_bar(
                                    "you have 15 cookies, eat them first", months
                                )
                        else:
                            self.info_bar(
                                "cookie? type 'help' for valid commands", months
                            )
                    elif words[0] == "eat" and words[1] == "cookie":
                        if cookie:
                            if cookie_count > 0:
                                self.info_bar("huh? what was that crunch sound", months)
                                cookie_count -= 1
                                cookiefile = open(self.cookie_folder_path / "cookies.txt", "w")
                                cookiefile.write(str(cookie_count))
                                cookiefile.close()
                            elif cookie_count == 0:
                                self.info_bar("you're out of cookies, lol so sad", months)
                        else:
                            self.info_bar("eat what again? type 'help'", months)
                    else:
                        self.log(f"[ERROR] command doesn't exist: {user_inp}")
                        self.info_bar("type 'help' to view valid commands", months)
                else:
                    self.log(
                        f"[ERROR] i feel empty inside :( just like the user's input..."
                    )
                    self.info_bar("type 'help' to view valid commands", months)
                self.log("[INFO] main loop rerunning...")
        except SystemExit:
            self.log(f"[EXIT] Program closed")


if __name__ == "__main__":
    app = App()
    app.console_loop()
