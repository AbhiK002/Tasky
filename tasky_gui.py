from datetime import datetime
from os import makedirs
from pathlib import Path
from tkinter import (
    Tk,
    PhotoImage,
    TclError,
    Frame,
    Button,
    NSEW,
    E, W,
    EW,
    Label,
    CENTER,
    DISABLED, NORMAL,
    StringVar,
    Toplevel,
    Entry,
    OptionMenu,
)


class Functions:
    def __init__(self):
        # paths defined
        self.home_path = Path.home()
        self.taskymain_path = f'{self.home_path}\\Tasky'

        self.check_sourcefiles()

        self.months_maxdays = {
            "01": 31, "02": 29, "03": 31, "04": 30,
            "05": 31, "06": 30, "07": 31, "08": 31,
            "09": 30, "10": 31, "11": 30, "12": 31
        }

        self.month_names = {
            "January": 1, "February": 2, "March": 3, "April": 4,
            "May": 5, "June": 6, "July": 7, "August": 8,
            "September": 9, "October": 10, "November": 11, "December": 12
        }

    def check_tasky_folders(self):
        try:
            makedirs(self.taskymain_path)
        except FileExistsError:
            pass

    def check_tasks_txt(self):
        try:
            b = open(f'{self.taskymain_path}\\tasks.txt', 'r')
            b.close()
        except FileNotFoundError:
            b = open(f'{self.taskymain_path}\\tasks.txt', 'w')
            b.close()

    def check_settings(self):
        try:
            b = open(f'{self.taskymain_path}\\settings.txt', 'r')
            if "light" in ''.join(b.read()) or "dark" in ''.join(b.read()):
                b.close()
            else:
                c = open(f'{self.taskymain_path}\\settings.txt', 'w')
                c.write("dark")
                c.close()
        except FileNotFoundError:
            b = open(f'{self.taskymain_path}\\settings.txt', 'w')
            b.write("dark")
            b.close()

    def check_sourcefiles(self):
        self.check_tasky_folders()
        self.check_tasks_txt()
        self.check_settings()

    def timediff(self, tt):
        tt = tt.split(':')
        # time now
        tn = datetime.today()
        tny = tn.strftime('%y')
        tnm = tn.strftime('%m')
        tnd = tn.strftime('%d')
        tnh = tn.strftime('%H')
        tnmin = tn.strftime('%M')

        # task time
        tty = tt[0]
        ttm = tt[1]
        ttd = tt[2]
        tth = tt[3]
        ttmin = tt[4]

        diffy = int(tty) - int(tny)
        diffm = int(ttm) - int(tnm)
        diffd = int(ttd) - int(tnd)
        diffh = int(tth) - int(tnh)
        diffmin = int(ttmin) - int(tnmin)

        if diffmin < 0:
            diffmin = 60 + diffmin
            diffh -= 1
        if diffh < 0:
            diffh = 24 + diffh
            diffd -= 1
        if diffd < 0:
            diffd = self.months_maxdays.get(str(tnm)) + diffd
            if int(tnm) == 2 and int(tny) % 4 != 0:
                diffd -= 1
            diffm -= 1
        if diffm < 0:
            diffm = 12 + diffm
            diffy -= 1
        if diffy < 0:
            output = "Task Expired".rjust(19)
        else:
            diffy = str(diffy)
            diffm = str(diffm)
            diffd = str(diffd)
            diffh = str(diffh)
            diffmin = str(diffmin)

            if int(diffy) >= 1:
                output = f"{diffy}y".rjust(3) + f"{diffm}M".rjust(4) + f"{diffd}d".rjust(4) + f"{diffh}h".rjust(4) + f"{diffmin}m".rjust(4)
            elif int(diffm) >= 1:
                output = f"{diffm}M".rjust(4 + 3) + f"{diffd}d".rjust(4) + f"{diffh}h".rjust(4) + f"{diffmin}m".rjust(4)
            elif int(diffd) >= 1:
                output = f"{diffd}d".rjust(4 + 7) + f"{diffh}h".rjust(4) + f"{diffmin}m".rjust(4)
            elif int(diffh) >= 1:
                output = f"{diffh}h".rjust(4 + 11) + f"{diffmin}m".rjust(4)
            elif int(diffmin) >= 1 and int(diffmin) >= 30:
                output = f"{diffmin}m".rjust(4 + 15)
            else:
                output = "LESS THAN 30 MIN".rjust(19)
        return output

    def read_and_sort_tasks_file(self):  # returns the current data sorted and separately in list
        self.check_sourcefiles()
        a = open(f'{self.taskymain_path}\\tasks.txt', 'r')
        x = a.readlines()
        a.close()
        y = []
        while '\n' in x:
            x.remove('\n')
        for item in x:
            item = item.replace('\n', '')
            y += [item]

        tasklist = self.sort_tasks(y)
        return tasklist

    def sort_tasks(self, tlist):
        nums = []
        temp_dict = {}
        for task in tlist:
            rawtime = task[:14]
            rawtime = rawtime.replace(":", "")
            nums += [int(rawtime)]
            temp_dict[task] = int(rawtime)
        nums.sort()
        for k, v in temp_dict.items():
            nums[nums.index(v)] = k
        for o in nums:
            if str(o).isdecimal():
                while o in nums:
                    nums.remove(o)
        sorted_output = '\n'.join(nums)
        taskfile = open(f"{self.taskymain_path}\\tasks.txt", 'w')
        taskfile.write(sorted_output)
        taskfile.close()
        return nums

    def remove_task(self, ind):
        tasklist = self.read_and_sort_tasks_file()
        target_task = tasklist[ind]
        tasklist.remove(target_task)
        new_output = '\n'.join(tasklist)
        taskfile = open(f'{self.taskymain_path}\\tasks.txt', 'w')
        taskfile.write(new_output)
        taskfile.close()

    def add_task(self, task):
        tasklist = self.read_and_sort_tasks_file()
        tasklist.append(task)
        new_output = '\n'.join(tasklist)
        taskfile = open(f'{self.taskymain_path}\\tasks.txt', 'w')
        taskfile.write(new_output)
        taskfile.close()


class App:
    def __init__(self):
        self.fn = Functions()

        # colors
        self.yellow = "#FFDA59"
        self.dark_yellow = "#9B7D42"

        self.light_red = "#FF7D6F"
        self.dark_gray = "#303030"
        self.gray = "#7F7F7F"
        self.light_gray = "#C3C3C3"

        self.blue = "#00A2E8"
        self.dark_blue = "#006B9B"
        self.red = "#ED1C24"
        self.dark_red = "#8E1218"

        # active colors
        self.major_bg = self.yellow
        self.major_abg = self.dark_yellow
        self.minor_bg = self.light_red
        self.text_fg = "black"

        self.mode_fg = self.yellow
        self.mode_bg = self.dark_gray

        # main window
        self.root = Tk()
        self.root.title("Tasky - Deadline Tracker")
        self.root.config(bg=self.minor_bg)

        try:
            tasky_logo = PhotoImage(file="tlogo.png")
            self.root.iconphoto(True, tasky_logo)
        except TclError:
            # logo not found locally
            pass

        # sizes
        tasky_width = 600
        tasky_height = 720
        self.title_font_size = 18
        self.text_font_size = 14
        self.task_height = 30

        user_y = self.root.winfo_screenheight()
        if user_y < 900:
            tasky_width = 500
            tasky_height = 652
            self.title_font_size = 16
            self.text_font_size = 12
            self.task_height = 27

        self.root.geometry(f"{tasky_width}x{tasky_height}+{int(self.root.winfo_screenwidth()/2 - tasky_width/2)}+{int(self.root.winfo_screenheight()/2 - tasky_height/2)}")
        self.root.resizable(False, False)

        # main frame and menu frame
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.mainframe = Frame(self.root, bg=self.major_bg, highlightbackground="black", highlightthickness=3)
        self.menuframe = Frame(self.root, height=50, bg=self.minor_bg)

        self.mainframe.grid(row=0, column=0, sticky=NSEW, padx=5, pady=5)
        self.menuframe.grid(row=1, column=0, sticky=EW)

        # menu frame
        self.menuframe.rowconfigure(0, weight=1)

        self.new_task_button = Button(self.menuframe, disabledforeground="red", text="New Task", fg=self.text_fg, activeforeground=self.text_fg, font=('calibri', self.text_font_size, 'bold'), bg=self.major_bg, activebackground=self.major_abg, width=9, border=1, command=lambda n_e_inp="new": self.task_details_window(n_e_inp))
        self.new_task_button.grid(row=0, column=0, padx=5, pady=6, sticky=W)

        self.mode_button = Button(self.menuframe, text="Dark Mode", fg=self.mode_fg, activeforeground=self.mode_fg, font=('calibri', self.text_font_size, 'bold'), bg=self.mode_bg, activebackground=self.mode_bg, width=10, border=1, command=self.dark_mode)
        self.mode_button.grid(row=0, column=1, padx=2, pady=6, sticky=W)

        self.menuframe.columnconfigure(2, weight=1)

        self.status_frame = Frame(self.menuframe, bg=self.minor_bg)
        self.status_frame.grid_propagate(False)
        self.status_frame.grid(row=0, column=2, padx=5, pady=6, sticky=NSEW)
        self.question_label = Label(self.root, bg=self.major_bg)

        # main frame
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(1, weight=1)

        # title frame in main frame
        self.title_frame = Frame(self.mainframe, bg=self.major_bg)
        self.title_frame.grid(row=0, column=0, sticky=EW)

        self.title_frame.rowconfigure(0, weight=1)
        self.title_frame.columnconfigure(0, weight=1)
        self.title_label = Label(self.title_frame, text="~  TASKS REMAINING  ~", fg=self.text_fg, bg=self.major_bg, anchor=CENTER, font=('Calibri', self.title_font_size, 'bold'))
        self.title_label.grid(row=0, column=0, pady=5, sticky=NSEW)

        # tasks frame
        self.tasks_frame = Frame(self.mainframe, bg=self.major_bg, highlightthickness=1, highlightbackground=self.major_bg)
        self.tasks_frame.grid(row=1, column=0, padx=3, sticky=NSEW)
        self.tasks_frame.columnconfigure(0, weight=1)

        self.tasks_list = []

        # check for prevailing settings
        if self.is_light():
            self.light_mode()
        else:
            self.dark_mode()

        self.msg_label = None

        # live update
        curr_time = datetime.today()
        curr_secs = int(curr_time.strftime('%S'))
        self.root.after((60 - curr_secs) * 1000, self.update_time_remaining)

    def sync_tasks_display(self):
        task_list = self.fn.read_and_sort_tasks_file()

        if len(task_list) >= 20:
            self.new_task_button.config(state=DISABLED)
            while len(task_list) > 20:
                ind = len(task_list) - 1
                self.fn.remove_task(ind)
                task_list = self.fn.read_and_sort_tasks_file()
        else:
            if self.new_task_button.cget('state') == DISABLED:
                self.new_task_button.config(state=NORMAL)

        for i in self.tasks_frame.winfo_children():
            i.destroy()

        task_list = self.fn.read_and_sort_tasks_file()

        self.tasks_list = []

        for rawtask in task_list:
            ind = task_list.index(rawtask)
            rawtaskinfo = rawtask[15:]
            final_task_info = rawtaskinfo.title()
            rawtasktime = rawtask[:14]
            final_task_time = self.fn.timediff(rawtasktime)
            frame = Frame(self.tasks_frame, height=self.task_height, bg=self.major_bg)
            frame.grid_propagate(False)
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(2, weight=1)

            numlabel = Label(frame, text=str(ind + 1) + ".", width=2, bg=self.major_bg, fg=self.text_fg, font=('calibri', self.text_font_size, 'normal'), anchor=E)
            numlabel.grid(row=0, column=0, sticky=W)

            timelabel = Label(frame, text=final_task_time, width=19, bg=self.major_bg, fg=self.text_fg, font=('calibri', self.text_font_size, 'bold'), anchor=E)
            timelabel.grid(row=0, column=1, padx=4)

            textlabel = Label(frame, text=final_task_info[:35], width=30, fg=self.text_fg, font=('calibri', self.text_font_size, 'normal'), bg=self.major_bg, anchor=W)
            textlabel.grid(row=0, column=2, sticky=W)

            a = Button(frame, text="...", width=1, fg="black", bg=self.blue, activebackground=self.dark_blue, font=('calibri', self.text_font_size, 'bold'), activeforeground="black", command=lambda n_e_inp=ind: self.task_details_window(n_e_inp))
            b = Button(frame, text="x", width=1, fg="black", bg=self.red, activebackground=self.dark_red, font=('calibri', self.text_font_size, 'bold'), activeforeground="black", command=lambda j=ind: self.delete_confirmation(j))

            frame.bind('<Enter>', lambda event="<Enter>", a=a, b=b: self.show_task_actions(event, a, b))
            frame.bind('<Leave>', lambda event="<Leave>", a=a, b=b: self.hide_task_actions(event, a, b))

            frame.grid(row=ind, column=0, sticky=EW)
            self.tasks_list.append(frame)

    def show_task_actions(self, event, a, b):
        a.grid(row=0, column=3, sticky=NSEW, padx=2, pady=4)
        b.grid(row=0, column=4, sticky=NSEW, padx=2, pady=4)

    def hide_task_actions(self, event, a, b):
        a.grid_forget()
        b.grid_forget()

    def is_light(self):
        a = open(f"{self.fn.taskymain_path}\\settings.txt", "r")
        b = a.read()
        a.close()
        if ''.join(b) == "light":
            return True
        else:
            return False

    def dark_mode(self):
        self.major_bg = self.dark_gray
        self.major_abg = "black"
        self.minor_bg = self.gray
        self.text_fg = self.yellow
        self.mode_fg = "black"
        self.mode_bg = self.yellow

        self.update_colors()
        self.mode_button.config(text="Light Mode", command=self.light_mode, bg=self.mode_bg, fg=self.mode_fg, activebackground=self.mode_bg, activeforeground=self.mode_fg)
        a = open(f"{self.fn.taskymain_path}\\settings.txt", "w")
        a.write("dark")
        a.close()

    def light_mode(self):
        self.major_bg = self.yellow
        self.major_abg = self.dark_yellow
        self.minor_bg = self.light_red
        self.text_fg = "black"
        self.mode_fg = self.yellow
        self.mode_bg = self.dark_gray

        self.update_colors()
        self.mode_button.config(text="Dark Mode", command=self.dark_mode, bg=self.mode_bg, fg=self.mode_fg, activebackground=self.mode_bg, activeforeground=self.mode_fg)
        a = open(f"{self.fn.taskymain_path}\\settings.txt", "w")
        a.write("light")
        a.close()

    def update_colors(self):
        self.root.config(bg=self.minor_bg)

        self.mainframe.config(bg=self.major_bg)
        self.title_frame.config(bg=self.major_bg)
        self.title_label.config(bg=self.major_bg, fg=self.text_fg)
        self.tasks_frame.config(bg=self.major_bg, highlightbackground=self.major_bg)

        self.sync_tasks_display()

        self.menuframe.config(bg=self.minor_bg)
        self.new_task_button.config(bg=self.major_bg, activebackground=self.major_abg, fg=self.text_fg, activeforeground=self.text_fg)
        self.status_frame.config(bg=self.minor_bg)

        try:
            self.question_label.config(bg=self.minor_bg)
        except:
            pass

    def update_time_remaining(self):
        self.sync_tasks_display()
        self.root.after(60000, self.update_time_remaining)

    def delete_task(self, ind):
        try:
            self.fn.remove_task(ind)
        except:
            pass

        self.sync_tasks_display()

        for i in self.status_frame.winfo_children():
            i.destroy()

    def cancel_delete_task(self):
        for i in self.status_frame.winfo_children():
            i.destroy()

    def delete_confirmation(self, j):
        self.status_frame.rowconfigure(0, weight=1)
        self.status_frame.columnconfigure(0, weight=1)

        self.question_label = Label(self.status_frame, bg=self.minor_bg, fg="black", text=f"Delete Task {j + 1} ?", anchor=E, font=('Calibri', 15, 'bold'))
        self.question_label.grid(row=0, column=0, sticky=NSEW)

        yes_button = Button(self.status_frame, width=6, bg="red", fg="black", activeforeground="black", text="DELETE", font=('Calibri', 13, 'bold'), command=lambda ind=j: self.delete_task(ind))
        yes_button.grid(row=0, column=1, sticky=W, padx=3, pady=2)

        no_button = Button(self.status_frame, width=6, bg="green", fg="black", activeforeground="black", text="CANCEL", font=('Calibri', 13, 'bold'), command=self.cancel_delete_task)
        no_button.grid(row=0, column=2, sticky=W, padx=3, pady=2)

    def task_details_window(self, n_e_inp):
        self.cancel_delete_task()
        tasky_new_x = self.root.winfo_x() + int(self.root.winfo_width() / 2 - 245)
        tasky_new_y = self.root.winfo_y() + int(self.root.winfo_height() / 2 - 200)

        desc_var_tk = StringVar()
        date_var_tk = StringVar()
        month_var_tk = StringVar()
        year_var_tk = StringVar()
        hours_var_tk = StringVar()
        mins_var_tk = StringVar()
        am_pm_var = StringVar()

        current_dt = datetime.today()
        self.sync_tasks_display()

        td_window = Toplevel()
        td_window.title("New Task")
        td_window.minsize(490, 400)
        td_window.resizable(False, False)
        td_window.geometry(f"490x400+{tasky_new_x}+{tasky_new_y}")
        td_window.config(bg=self.major_bg)

        td_window.grab_set()
        td_window.focus_set()

        td_window.rowconfigure(0, weight=1)
        td_window.columnconfigure(0, weight=1)

        mainframe = Frame(td_window, bg=self.major_bg)
        mainframe.grid(row=0, column=0, sticky=NSEW)
        mainframe.rowconfigure(10, weight=1)

        mainframe.columnconfigure(1, weight=1)
        title = Label(mainframe, text="New Task Details", height=2, bg=self.major_bg, anchor=CENTER, fg="orange", font=('Calibri', 20, 'bold'))
        title.grid(row=0, column=0, columnspan=2, sticky=EW)

        desc_label = Label(mainframe, width=16, text="Task Description: ", bg=self.major_bg, anchor=E, fg=self.text_fg, font=('Calibri', 14, 'bold'))
        desc_label.grid(row=1, column=0, sticky=W)

        desc_var_tk.set(f"Task{len(self.tasks_list) + 1}")
        desc_entry = Entry(mainframe, textvariable=desc_var_tk, bg=self.major_bg, fg="white", font=('Calibri', 14, 'normal'))
        desc_entry.grid(row=1, column=1, sticky=NSEW, padx=8)
        desc_entry.focus_set()

        Frame(mainframe, height=20, bg=self.major_bg).grid(row=2, column=0, columnspan=2, sticky=EW)

        current_date = current_dt.strftime("%d")
        date_var_tk.set(str(current_date))
        date_label = Label(mainframe, width=16, text="Date: ", bg=self.major_bg, anchor=E, fg=self.text_fg, font=('Calibri', 14, 'bold'))
        date_label.grid(row=3, column=0, sticky=W)

        date_entry = Entry(mainframe, width=3, textvariable=date_var_tk, bg=self.major_bg, fg="white", font=('Calibri', 14, 'normal'))
        date_entry.grid(row=3, column=1, sticky=W, padx=8)

        month_label = Label(mainframe, width=16, text="Month: ", bg=self.major_bg, anchor=E, fg=self.text_fg, font=('Calibri', 14, 'bold'))
        month_label.grid(row=4, column=0, sticky=W)

        current_month = current_dt.strftime("%B")
        month_var_tk.set(current_month)
        month_menu = OptionMenu(mainframe, month_var_tk, *self.fn.month_names.keys(), command=lambda event="<KeyRelease>", typ="month", data=month_var_tk: live_input(event, typ, data))
        month_menu.config(width=8, bg=self.major_bg, fg="white", font=('Calibri', 14, 'normal'), highlightthickness=0)
        month_menu["menu"].config(bg=self.major_bg, fg="white", font=('Calibri', 14, 'normal'))
        month_menu.grid(row=4, column=1, sticky=W, padx=8, pady=3)

        year_label = Label(mainframe, width=16, text="Year: ", bg=self.major_bg, anchor=E, fg=self.text_fg, font=('Calibri', 14, 'bold'))
        year_label.grid(row=5, column=0, sticky=W)

        current_year = current_dt.strftime("%Y")
        year_var_tk.set(str(current_year))
        year_entry = Entry(mainframe, width=5, textvariable=year_var_tk, bg=self.major_bg, fg="white", font=('Calibri', 14, 'normal'))
        year_entry.grid(row=5, column=1, sticky=W, padx=8)

        Frame(mainframe, height=20, bg=self.major_bg).grid(row=6, column=0, columnspan=2, sticky=EW)

        hours_label = Label(mainframe, width=16, text="Hours: ", bg=self.major_bg, anchor=E, fg=self.text_fg, font=('Calibri', 14, 'bold'))
        hours_label.grid(row=7, column=0, sticky=W)

        current_hours = current_dt.strftime("%H")
        am_pm_var.set("AM/Noon")

        if int(current_hours) > 12:
            current_hours = str(int(current_hours) - 12).zfill(2)
            am_pm_var.set("PM/Night")
        elif int(current_hours) == 0:
            current_hours = "12"
            am_pm_var.set("PM/Night")

        hours_var_tk.set(current_hours)
        hours_entry = Entry(mainframe, width=3, textvariable=hours_var_tk, bg=self.major_bg, fg="white", font=('Calibri', 14, 'normal'))
        hours_entry.grid(row=7, column=1, sticky=W, padx=8)

        mins_label = Label(mainframe, width=16, text="Minutes: ", bg=self.major_bg, anchor=E, fg=self.text_fg, font=('Calibri', 14, 'bold'))
        mins_label.grid(row=8, column=0, sticky=W)

        current_mins = current_dt.strftime("%M")
        mins_var_tk.set(current_mins)
        mins_entry = Entry(mainframe, width=3, textvariable=mins_var_tk, bg=self.major_bg, fg="white", font=('Calibri', 14, 'normal'))
        mins_entry.grid(row=8, column=1, sticky=W, padx=8)

        am_pm_label = Label(mainframe, width=16, text="AM or PM: ", bg=self.major_bg, anchor=E, fg=self.text_fg, font=('Calibri', 14, 'bold'))
        am_pm_label.grid(row=9, column=0, sticky=W)

        am_pm_option = OptionMenu(mainframe, am_pm_var, *["AM/Noon", "PM/Night"])
        am_pm_option.config(bg=self.major_bg, fg="white", width=8, highlightthickness=0, font=('Calibri', 14, 'bold'))
        am_pm_option["menu"].config(bg=self.major_bg, fg="white", font=('Calibri', 14, 'bold'))
        am_pm_option.grid(row=9, column=1, sticky=W, pady=3, padx=8)

        msg_frame = Frame(mainframe, height=30, bg=self.major_bg)
        msg_frame.grid(row=10, column=0, columnspan=2, sticky=EW)
        msg_frame.grid_propagate(False)
        msg_frame.rowconfigure(0, weight=1)
        msg_frame.columnconfigure(0, weight=1)

        msg_label = Label(msg_frame, bg=self.major_bg, fg="cyan", text="", anchor=CENTER, font=('Calibri', 13, 'normal'))
        msg_label.grid(row=0, column=0, sticky=NSEW)

        button_frame = Frame(mainframe, bg=self.major_bg, height=30)
        button_frame.grid(row=11, column=0, columnspan=2, sticky=EW, pady=8)
        button_frame.rowconfigure(0, weight=1)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.grid_propagate(False)

        save_button = Button(button_frame, bg="green", activebackground="green", fg="white", activeforeground="white", text="SAVE", width=6, font=('Calibri', 16, 'bold'))
        save_button.grid(row=0, column=0, sticky=E, padx=4)

        cancel_button = Button(button_frame, bg=self.light_red, activebackground=self.light_red, fg="black", text="CANCEL", width=7, font=('Calibri', 16, 'bold'), command=td_window.destroy)
        cancel_button.grid(row=0, column=1, sticky=W, padx=4)

        if self.is_light():
            title.config(fg="black")
            for i in mainframe.winfo_children():
                if "entry" in (str(i).lower()):
                    i.config(fg="black", bg="white")

            month_menu.config(fg="black", bg="white")
            month_menu["menu"].config(fg="black", bg="white")
            am_pm_option.config(fg="black", bg="white")
            am_pm_option["menu"].config(fg="black", bg="white")
            msg_label.config(fg="red")

        if n_e_inp != "new":
            tasklist = self.fn.read_and_sort_tasks_file()
            target_task = tasklist[n_e_inp]
            p1 = target_task[:14]
            p2 = target_task[15:]

            title.config(text=f"Edit Task {n_e_inp+1} Details")
            td_window.title(f"Edit Mode for Task {n_e_inp+1}")

            p1s = p1.split(":")
            year_var_tk.set(f"20{p1s[0]}")
            month_var_tk.set(list(self.fn.month_names.keys())[(list(self.fn.month_names.values()).index(int(p1s[1])))])
            date_var_tk.set(p1s[2])
            mins_var_tk.set(p1s[4])
            desc_var_tk.set(p2)

            if int(p1s[3]) in range(0, 12):
                hours_var_tk.set(p1s[3])
                am_pm_var.set("AM/Noon")
                if p1s[3] == "00":
                    hours_var_tk.set("12")
                    if p1s[4] == "00":
                        am_pm_var.set("PM/Night")
            elif int(p1s[3]) in range(12, 23):
                hours_var_tk.set(str(int(p1s[3])-12).zfill(2))
                if p1s[3] == "12":
                    hours_var_tk.set("12")
                am_pm_var.set("PM/Night")
                if p1s[4] == "00" and p1s[3] == "12":
                    am_pm_var.set("AM/Noon")
            else:
                hours_var_tk.set("00")
                mins_var_tk.set("00")
                am_pm_var.set("PM/Night")

        def live_input(event, typ, data):
            raw_data = data.get().strip()
            c_dt = datetime.today()
            c_date = c_dt.strftime("%d")
            c_year = c_dt.strftime("%Y")
            c_hours = c_dt.strftime("%H")
            c_mins = c_dt.strftime("%M")

            if typ == "desc":
                if len(raw_data) > 35:
                    msg_label.config(text="Maximum Characters Allowed: 35")
                    data.set(raw_data[:35])
                elif len(raw_data) == 0:
                    msg_label.config(text="Task Description Cannot Be Empty")
                    data.set("")
                else:
                    msg_label.config(text="")

            elif typ == "date":
                if not raw_data.isdecimal():
                    msg_label.config(text="Date Must Be A Number")
                    temp = ""
                    for char in list(raw_data):
                        if char.isdecimal():
                            temp += str(char)
                    data.set(temp)
                else:
                    if len(raw_data) >= 2:
                        temp = int(str(self.fn.months_maxdays[str(self.fn.month_names[month_var_tk.get()]).zfill(2)]))
                        if 1 <= int(raw_data) <= temp:
                            data.set(str(int(raw_data)).zfill(2))
                            if month_var_tk.get() == "February":
                                if int(raw_data) == 29:
                                    if int(year_var_tk.get()) % 4 != 0:
                                        data.set("28")
                        elif int(raw_data) > temp:
                            msg_label.config(text="Invalid Date for Given Month")
                            if 1 <= int(raw_data[:2]) <= temp:
                                data.set(raw_data[:2])
                            else:
                                data.set(c_date)
                        else:
                            if int(raw_data) == 0:
                                data.set("01")
                            msg_label.config(text="")
                    else:
                        msg_label.config(text="")

            elif typ == "month":
                temp = int(str(self.fn.months_maxdays[str(self.fn.month_names[month_var_tk.get()]).zfill(2)]))
                try:
                    if int(date_var_tk.get()) > temp:
                        date_var_tk.set(str(temp).zfill(2))
                except ValueError:
                    pass
                msg_label.config(text="")

            elif typ == "year":
                if not raw_data.isdecimal():
                    msg_label.config(text="Year Must Be A Number")
                    temp = ""
                    for char in list(raw_data):
                        if char.isdecimal():
                            temp += str(char)
                    data.set(temp)
                else:
                    if len(raw_data) >= 4:
                        if int(raw_data) not in range(int(c_year), 2100):
                            msg_label.config(text="Year Should Lie Between 2022 and 2099")
                            data.set(str(c_year))
                        else:
                            msg_label.config(text="")
                        if month_var_tk.get() == "February":
                            if int(date_var_tk.get()) == 29:
                                if int(raw_data) % 4 != 0:
                                    date_var_tk.set("28")
                    else:
                        msg_label.config(text="Year Too Short (Correct Format: YYYY)")

            elif typ == "hours":
                if not raw_data.isdecimal():
                    msg_label.config(text="Hours Must Be A Number")
                    temp = ""
                    for char in list(raw_data):
                        if char.isdecimal():
                            temp += str(char)
                    data.set(temp)
                else:
                    if len(raw_data) >= 2:
                        if 12 >= int(raw_data) > 0:
                            data.set(str(int(raw_data)).zfill(2))
                        elif 23 >= int(raw_data) > 12:
                            msg_label.config(text="Converted 24h To 12h Format")
                            data.set(str(int(raw_data) - 12).zfill(2))
                            am_pm_var.set("PM/Night")
                        elif int(raw_data) == 0:
                            msg_label.config(text="Converted 24h To 12h Format")
                            data.set(str(int(raw_data) + 12).zfill(2))
                            if int(date_var_tk.get()) == 0:
                                am_pm_var.set("AM/Noon")
                            else:
                                am_pm_var.set("PM/Night")
                        else:
                            msg_label.config(text="Hours Should Lie Between 1 And 12")
                            data.set(str(c_hours).zfill(2))
                            am_pm_var.set("AM/Noon")
                    else:
                        msg_label.config(text="")

            elif typ == "mins":
                if not raw_data.isdecimal():
                    msg_label.config(text="Minutes Must Be A Number")
                    temp = ""
                    for char in list(raw_data):
                        if char.isdecimal():
                            temp += str(char)
                    data.set(temp)
                else:
                    if len(raw_data) >= 2:
                        if int(raw_data) not in range(0, 60):
                            msg_label.config(text="Minutes Should Lie Between 0 and 59")
                            if int(raw_data[:2]) in range(0, 60):
                                data.set(raw_data[:2])
                            else:
                                data.set(str(c_mins))
                        else:
                            if int(raw_data) == 0:
                                data.set("00")
                            else:
                                data.set(str(int(raw_data)).zfill(2))
                            msg_label.config(text="")
                    else:
                        msg_label.config(text="")

        def check_inputs():
            raw_desc = desc_var_tk.get().strip()
            raw_date = date_var_tk.get().strip()
            raw_month = month_var_tk.get().strip()
            raw_year = year_var_tk.get().strip()
            raw_hour = hours_var_tk.get().strip()
            raw_mins = mins_var_tk.get().strip()
            raw_ampm = am_pm_var.get().strip()

            if raw_desc == "":
                msg_label.config(text="Task Description Cannot Be Empty")
                desc_entry.focus_set()
            elif raw_date == "" or (not raw_date.isdecimal()):
                date_var_tk.set("")
                msg_label.config(text="Date Input Cannot Be Empty")
                date_entry.focus_set()
            elif int(raw_date) == 0:
                msg_label.config(text="Invalid Date Entered")
            elif raw_year == "" or (not raw_year.isdecimal()):
                year_var_tk.set("")
                msg_label.config(text="Year Input Cannot Be Empty")
                year_entry.focus_set()
            elif len(raw_year) < 4:
                msg_label.config(text=f"Year Should Lie Between {current_year} And 2099")
                year_entry.focus_set()
            elif raw_hour == "" or (not raw_hour.isdecimal()):
                hours_var_tk.set("")
                msg_label.config(text="Hours Input Cannot Be Empty")
                hours_entry.focus_set()
            elif raw_hour == "0":
                msg_label.config(text='Hours Should Be In 12h Format'.title())
                hours_var_tk.set("12")
            elif raw_mins == "" or (not raw_mins.isdecimal()):
                mins_var_tk.set("")
                msg_label.config(text="Minutes Input Cannot be Empty".title())
                mins_entry.focus_set()
            else:
                if len(raw_desc) > 35:
                    desc_var_tk.set(raw_desc[:35])
                if raw_ampm == "PM/Night" and raw_hour != "12":
                    raw_hour = str(int(raw_hour) + 12).zfill(2)
                elif raw_hour == "12":
                    if raw_mins.zfill(2) == "00":
                        if raw_ampm == "PM/Night":
                            raw_hour = "00"
                    else:
                        if raw_ampm == "AM/Noon":
                            raw_hour = "00"
                temp = f"{raw_year[-2:]}:{str(self.fn.month_names[raw_month]).zfill(2)}:{raw_date.zfill(2)}:{raw_hour.zfill(2)}:{raw_mins.zfill(2)}={raw_desc.title()}"
                msg_label.config(text=f"OK")

                task = temp

                if n_e_inp == "new":
                    self.fn.add_task(task)
                    self.sync_tasks_display()
                    td_window.destroy()
                else:
                    self.fn.remove_task(n_e_inp)
                    self.fn.add_task(task)
                    self.sync_tasks_display()
                    td_window.destroy()

        desc_entry.bind('<KeyRelease>', lambda event="<KeyRelease>", typ="desc", data=desc_var_tk: live_input(event, typ, data))
        date_entry.bind('<KeyRelease>', lambda event="<KeyRelease>", typ="date", data=date_var_tk: live_input(event, typ, data))
        year_entry.bind('<KeyRelease>', lambda event="<KeyRelease>", typ="year", data=year_var_tk: live_input(event, typ, data))
        hours_entry.bind('<KeyRelease>', lambda event="<KeyRelease>", typ="hours", data=hours_var_tk: live_input(event, typ, data))
        mins_entry.bind('<KeyRelease>', lambda event="<KeyRelease>", typ="mins", data=mins_var_tk: live_input(event, typ, data))

        save_button.config(command=check_inputs)

        td_window.mainloop()

    def get_var(self, tk_var):
        var = tk_var.get()
        return var

    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
