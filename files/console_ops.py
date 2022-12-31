from os import system
from .tasky_ops import Functions


class ConsoleFunctions(Functions):
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

    def status(self):
        self.TL.function(f"starts -> status()")

        print(f"\n{' TASKS REMAINING '.center(60, '~')}\n")

        task_list = self.read_and_sort_tasks_file()
        self.TL.info(f"stored current tasks in 'task_list'")

        if not task_list:  # no tasks
            print("(No tasks to display yet)".center(60), "Add a task using 'add' or 'new'".center(60), sep='\n', end='\n\n\n')
            self.TL.info("no tasks available to display")
            return

        outputs = list(map(lambda task: f"{f'({task[0]})'.rjust(4)} {task[1]} >>>  {task[2]}", self.return_deadlines(task_list)))
        # task = [("[TASK NUMBER]", "[TASK DEADLINE]", "[TASK NAME]"), (...) ... ]

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

        dt, t_desc = target_task.split("=", 1)
        tYY, tMM, tDD, tHH, tmm = dt.split(":")

        tYY = 2000 + int(tYY)
        prevMM = str((int(tMM) - 1) % 12).zfill(2)
        if prevMM == "00":
            prevMM = "12"
        tMM = self.month_names[int(tMM)]
        self.TL.info(f"changed year to YYYY form and month number to Name")

        tt12h = int(tHH) % 12
        ttampm = ("AM", "PM")[int(tHH) // 12 == 1]

        if tt12h == 0:
            tt12h = 12
            if int(tmm) == 0 and tHH == "00":
                ttampm = f"MIDNIGHT ({int(tDD) - 1} | {int(tDD)})"
                if int(tDD) == 1:
                    ttampm = f"MIDNIGHT ({self.months[prevMM]} | {int(tDD)})"
            elif int(tmm) == 0 and tHH == "12":
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

    def edit_task(self, num, last_copy):
        self.TL.function(f"starts -> edit_task({num})")

        last = last_copy
        self.write_tasks(last)
        self.TL.info(f"stored current tasks list as 'last'")

        task_ind = int(num) - 1
        target_task = last[int(num) - 1]
        self.TL.info(f"task number {num} requested for edit")

        ttask_time, ttask_name = target_task.split("=", 1)
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

            if 1 <= len(taskinfo) <= 30:
                self.TL.info(f"stored input from user as task name")
                self.TL.info(f"new task name: {taskinfo}")

                self.TL.function(f"ends -> new_task_name()")
                return taskinfo
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
                    yr_curr = self.current_year
                    yr_limit = 2099
                    self.TL.waiting(f"for year input")
                    tyear = input(f"{f'Year (YYYY) ({yr_curr}-{yr_limit})'.ljust(27)}:  ").strip()

                    self.TL.info(f"year input: {tyear}")

                    if tyear.lower() == "/cancel":
                        self.TL.info(f"user chose to cancel new task addition")
                        self.TL.function(f"ends -> new_task_time()")
                        return 0, 0, 0, 0, 0

                    elif tyear.isdecimal() and int(tyear) in range(yr_curr, yr_limit+1):
                        self.TL.info(f"confirmed year lies between {yr_curr} and {yr_limit}")

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
