import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QTimer, QSize

from files.gui_ops import TaskyStyle
from files.tasky_ops import Functions

# style and backend class for Tasky
TStyle = TaskyStyle()
TBackEnd = Functions()


class App(QWidget):
    def __init__(self):
        app = QApplication(sys.argv)
        super(App, self).__init__()

        # hmm
        self.t_style = TStyle.stylesheet()

        # properties
        scr_width, scr_height = int(app.primaryScreen().size().width()), int(app.primaryScreen().size().height())
        tasky_width = 750
        tasky_height = 720

        # main window properties
        self.setWindowTitle("Tasky")
        self.setObjectName("MainWindow")
        self.setGeometry(
            int((scr_width - tasky_width) / 2),  # center of screen height
            int((scr_height - tasky_height) / 2),  # center of screen width
            tasky_width, tasky_height
        )
        self.setMinimumSize(750, 370)
        self.setWindowIcon(QIcon(TStyle.tlogo_path))
        self.setStyleSheet(self.t_style)

        self.mainlayout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.mainlayout)
        self.mainlayout.setSpacing(0)
        self.mainlayout.setContentsMargins(10, 10, 10, 0)

        # top frame - tasks
        self.tasks_frame = QWidget(self)
        self.tasks_frame.setObjectName("TasksFrame")
        self.tasks_frame_layout = QtWidgets.QVBoxLayout(self.tasks_frame)
        self.tasks_frame.setLayout(self.tasks_frame_layout)

        self.heading_label = QtWidgets.QLabel("TASKS REMAINING")
        self.heading_label.setObjectName("TasksHeadingLabel")
        self.heading_label.setAlignment(Qt.AlignCenter)

        self.tasks_frame_layout.setContentsMargins(8, 0, 8, 0)
        self.tasks_frame_layout.addWidget(self.heading_label)

        self.tasks_list = []
        self.tasks_container = None
        self.tasks_layout = None
        self.add_tasks_container()

        self.task_window = None

        # bottom frame - buttons
        self.buttons_frame = QWidget(self)
        self.buttons_layout = QtWidgets.QHBoxLayout(self.buttons_frame)
        self.buttons_frame.setLayout(self.buttons_layout)

        self.new_task_button = QtWidgets.QPushButton(" New Task")
        self.new_task_button.setIcon(QIcon(TStyle.new_task_icon))
        self.new_task_button.setObjectName("NewTaskButton")
        self.new_task_button.clicked.connect(self.open_task)

        self.switch_mode_button = QtWidgets.QPushButton(f" {'Dark' if TStyle.theme == 'light' else 'Light'} Theme")
        self.switch_mode_button.setIcon(QIcon(TStyle.switch_mode_icon))
        self.switch_mode_button.setObjectName("SwitchModeButton")
        self.switch_mode_button.clicked.connect(self.switch_theme)

        self.buttons_layout.addStretch()
        self.buttons_layout.addWidget(self.new_task_button)
        self.buttons_layout.addWidget(self.switch_mode_button)
        self.buttons_layout.addStretch()

        # place top and bottom frames
        self.mainlayout.addWidget(self.tasks_frame, 1)
        self.mainlayout.addWidget(self.buttons_frame)

        # run main loop and periodically update tasks list
        timer = QTimer()
        timer.timeout.connect(self.refresh_gui)
        timer.setInterval(10000)
        timer.start()

        self.show()
        sys.exit(app.exec_())

    def add_tasks_container(self):
        self.tasks_container = QWidget(self.tasks_frame)
        self.tasks_container.setObjectName("TasksContainer")

        self.tasks_layout = QtWidgets.QVBoxLayout(self.tasks_container)
        self.tasks_container.setLayout(self.tasks_layout)

        self.tasks_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.tasks_layout.setContentsMargins(12, 12, 5, 12)

        # adds tasks to the container
        self.refresh_tasks()

        tasks_scroll_area = QtWidgets.QScrollArea()
        tasks_scroll_area.setObjectName("TasksScrollArea")
        tasks_scroll_area.setWidgetResizable(True)
        tasks_scroll_area.setWidget(self.tasks_container)

        self.tasks_frame_layout.addWidget(tasks_scroll_area, 1)

    def refresh_tasks(self):
        print("refreshing")
        while self.tasks_layout.count():
            child = self.tasks_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # get tasks
        self.tasks_list = TBackEnd.return_deadlines()

        for task in self.tasks_list:
            task_box = TaskBox(*task, self)
            task_box.delete_button.pressed.connect(lambda p=int(task[0]): [self.direct_delete(p)])
            self.tasks_layout.addWidget(task_box)

        self.clear_all = QtWidgets.QPushButton("CLEAR ALL TASKS")
        self.clear_all.setObjectName("ClearAllButton")
        self.clear_all.setCursor(QCursor(Qt.PointingHandCursor))
        self.clear_all.clicked.connect(self.clear_all_tasks)

        if not self.tasks_list:
            self.clear_all.setEnabled(False)

        self.tasks_layout.addWidget(self.clear_all, alignment=Qt.AlignCenter)
        self.tasks_layout.addStretch()

    def open_task(self, num=False):
        if num:
            print(f"request to open task {num}")
        else:
            print("request to add new task")

        if self.task_window is None:  # if no other task window open, open the requested one
            self.setEnabled(False)
            self.task_window = TaskWindow(num, self)
            win_timer = QTimer(self.task_window)
            win_timer.setSingleShot(True)
            win_timer.timeout.connect(self.task_window.show)
            win_timer.setInterval(200)
            win_timer.start()
        else:
            print("another window already open")

    def direct_delete(self, tasknum):
        tlist = TBackEnd.read_and_sort_tasks_file()
        if tasknum - 1 in range(len(tlist)):
            tname = tlist[tasknum - 1].split("=", 1)[1]
            display_text = f"Are you sure you want to delete Task {tasknum}?\n\n" \
                           f"Task Name: {tname}\n"

            decision = QtWidgets.QMessageBox.question(
                self,
                "Delete Confirmation",
                display_text,
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )

            if decision == QtWidgets.QMessageBox.Yes:
                print(f"Task {tasknum} deletion requested")
                print(f"CURRENT: {tlist}")
                try:
                    TBackEnd.remove(tasknum, tlist)
                except IndexError:
                    print("index error occured while deleting")

                print("NEW:", tlist)
            else:
                print(f"Task {tasknum} deletion cancelled")
        self.refresh_tasks()

    def clear_all_tasks(self):
        display_text = f"Are you sure you want to DELETE ALL tasks?\n\n" \
                       f"(You cannot undo this)"

        decision = QtWidgets.QMessageBox.warning(
            self,
            "Clear All Confirmation",
            display_text,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )

        if decision == QtWidgets.QMessageBox.Yes:
            print(f"Clear Tasks requested")
            print(f"CURRENT: {TBackEnd.read_and_sort_tasks_file()}")
            TBackEnd.clear_tasks()
            print(f"NEW: {TBackEnd.read_and_sort_tasks_file()}")
        else:
            print(f"Clear Tasks cancelled")

    def closeEvent(self, e):
        exit()

    def refresh_gui(self):
        self.refresh_tasks()

    def switch_theme(self):
        self.switch_mode_button.setText(f" {TStyle.theme.title()} Theme")
        TStyle.switch_mode()
        self.t_style = TStyle.stylesheet()
        self.setStyleSheet(self.t_style)

        if self.task_window is not None:
            self.task_window.setStyleSheet(TStyle.twindow_stylesheet())

        self.new_task_button.setIcon(QIcon(TStyle.new_task_icon))
        self.switch_mode_button.setIcon(QIcon(TStyle.switch_mode_icon))

        self.refresh_tasks()


class TaskBox(QtWidgets.QPushButton):
    def __init__(self, task_number, task_deadline, task_name, mainwindow: App):
        super(TaskBox, self).__init__()
        self.main_window = mainwindow
        self.setStyleSheet(TStyle.stylesheet())
        task_lay = QtWidgets.QHBoxLayout(self)
        task_lay.setContentsMargins(0, 0, 0, 0)
        self.setLayout(task_lay)

        t = QtWidgets.QLabel(task_number)
        t.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        t.setObjectName("TaskNum")

        td = QtWidgets.QLabel(task_deadline.strip())
        td.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        td.setObjectName("TaskDead")

        tn = QtWidgets.QLabel(task_name)
        tn.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        tn.setObjectName("TaskName")
        tnlay = QtWidgets.QVBoxLayout(tn)
        tnlay.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        tnlay.setContentsMargins(0, 0, 4, 0)
        tn.setLayout(tnlay)

        self.delete_button = QtWidgets.QPushButton(tn)
        self.delete_button.setObjectName("DeleteButton")
        self.delete_button.setToolTip("Delete Task")
        del_icon = QIcon(TStyle.delete_button_icon)
        self.delete_button.setIcon(del_icon)
        iconsize = QSize()
        iconsize.setWidth(25)
        iconsize.setHeight(25)
        self.delete_button.setIconSize(iconsize)
        self.delete_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.delete_button.setVisible(False)

        tnlay.addWidget(self.delete_button)

        task_lay.addWidget(t)
        task_lay.addStretch()
        task_lay.addWidget(td, 5)
        task_lay.addWidget(tn, 8)
        task_lay.addStretch()

        # open task window on click
        self.pressed.connect(lambda p=int(task_number): [mainwindow.open_task(p)])

        self.setObjectName("TaskItem")
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def enterEvent(self, e):
        self.delete_button.setVisible(True)

    def leaveEvent(self, e):
        self.delete_button.setVisible(False)


class TaskWindow(QWidget):
    def __init__(self, task_num=False, mainWindow=None):
        super(TaskWindow, self).__init__()
        self.window_style = TStyle.twindow_stylesheet()
        self.mainWindow = mainWindow

        self.task_number = task_num
        self.tlist = TBackEnd.read_and_sort_tasks_file()

        if task_num in range(1, len(self.tlist) + 1):
            title = f"Edit Task {task_num}"
        else:
            title = "New Task"
            self.task_number = False

        self.setWindowTitle(title)

        self.setWindowIcon(QIcon(TStyle.tlogo_path))
        self.setStyleSheet(self.window_style)
        self.setMinimumSize(630, 370)
        self.setMaximumSize(740, 370)
        self.setObjectName("TaskWindow")
        self.win_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.win_layout)

        # Main Window Label
        self.win_title = QtWidgets.QLabel(title, self)
        self.win_title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.win_title.setObjectName("TaskWindowTitle")

        # Container for all the widgets
        self.win_items = QWidget(self)
        self.win_items.setObjectName("TaskWindowItems")
        self.items_layout = QtWidgets.QVBoxLayout(self.win_items)
        self.win_items.setLayout(self.items_layout)

        # Task Name Frame
        self.task_name_frame = QWidget(self.win_items)
        self.tnf_layout = QtWidgets.QHBoxLayout(self.task_name_frame)
        self.task_name_frame.setLayout(self.tnf_layout)

        self.tnf_label = QtWidgets.QLabel("Task Name", self.task_name_frame)
        self.tnf_entry = QtWidgets.QLineEdit(self.task_name_frame)
        self.tnf_entry.setObjectName("NameEntry")
        self.tnf_entry.setMaxLength(30)

        self.tnf_layout.addWidget(self.tnf_label)
        self.tnf_layout.addWidget(self.tnf_entry, 1)

        # Task Date Frame
        self.task_date_frame = QWidget(self.win_items)
        self.tdf_layout = QtWidgets.QHBoxLayout(self.task_date_frame)
        self.task_date_frame.setLayout(self.tdf_layout)

        self.tdf_date_label = QtWidgets.QLabel("Date", self.task_date_frame)
        self.tdf_date_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tdf_date_entry = QtWidgets.QLineEdit(self.task_date_frame)
        self.tdf_date_entry.setPlaceholderText("DD")
        self.tdf_date_entry.setMaxLength(2)

        self.tdf_month_label = QtWidgets.QLabel("Month", self.task_date_frame)
        self.tdf_month_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tdf_month_entry = QtWidgets.QComboBox(self.task_date_frame)

        for month in TBackEnd.month_names.values():
            self.tdf_month_entry.addItem(month.title())

        self.tdf_year_label = QtWidgets.QLabel("Year", self.task_date_frame)
        self.tdf_year_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tdf_year_entry = QtWidgets.QLineEdit(self.task_date_frame)
        self.tdf_year_entry.setPlaceholderText("YYYY")
        self.tdf_year_entry.setMaxLength(4)

        self.tdf_layout.addWidget(self.tdf_date_label)
        self.tdf_layout.addWidget(self.tdf_date_entry)
        self.tdf_layout.addStretch()
        self.tdf_layout.addWidget(self.tdf_month_label)
        self.tdf_layout.addWidget(self.tdf_month_entry)
        self.tdf_layout.addStretch()
        self.tdf_layout.addWidget(self.tdf_year_label)
        self.tdf_layout.addWidget(self.tdf_year_entry)

        # Task Time Frame
        self.task_time_frame = QWidget(self.win_items)
        self.ttif_layout = QtWidgets.QHBoxLayout(self.task_time_frame)
        self.task_time_frame.setLayout(self.ttif_layout)

        self.ttf_hours_label = QtWidgets.QLabel("Hours (24h)", self.task_time_frame)
        self.ttf_hours_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.ttf_hours_entry = QtWidgets.QLineEdit(self.task_time_frame)
        self.ttf_hours_entry.setPlaceholderText("HH")
        self.ttf_hours_entry.setMaxLength(2)

        self.ttf_mins_label = QtWidgets.QLabel("Mins", self.task_time_frame)
        self.ttf_mins_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.ttf_mins_entry = QtWidgets.QLineEdit(self.task_time_frame)
        self.ttf_mins_entry.setPlaceholderText("MM")
        self.ttf_mins_entry.setMaxLength(2)

        self.ttif_layout.addStretch()
        self.ttif_layout.addWidget(self.ttf_hours_label)
        self.ttif_layout.addWidget(self.ttf_hours_entry)
        self.ttif_layout.addStretch()
        self.ttif_layout.addWidget(self.ttf_mins_label)
        self.ttif_layout.addWidget(self.ttf_mins_entry)
        self.ttif_layout.addStretch()

        # Bottom Buttons Frame
        self.buttons_frame = QWidget(self)
        self.buttons_layout = QtWidgets.QHBoxLayout(self.buttons_frame)
        self.buttons_frame.setLayout(self.buttons_layout)

        self.delete_button = QtWidgets.QPushButton()
        self.delete_button.setObjectName("DeleteButton")

        del_icon = QIcon(TStyle.delete_button_icon)
        self.delete_button.setIcon(del_icon)
        iconsize = QSize()
        iconsize.setWidth(30)
        iconsize.setHeight(30)
        self.delete_button.setIconSize(iconsize)
        self.delete_button.setCursor(QCursor(Qt.PointingHandCursor))

        self.delete_button.clicked.connect(self.delete_task)
        if not self.task_number:
            self.delete_button.setEnabled(False)

        self.delete_button.setToolTip("Delete Task")

        self.save_task_button = QtWidgets.QPushButton("Save")
        self.save_task_button.setObjectName("SaveButton")
        self.save_task_button.clicked.connect(self.save_task)
        self.save_task_button.setAutoDefault(True)

        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setObjectName("CancelButton")
        self.cancel_button.clicked.connect(self.close)

        self.buttons_layout.addWidget(self.delete_button)
        self.buttons_layout.addStretch()
        self.buttons_layout.addWidget(self.save_task_button)
        self.buttons_layout.addWidget(self.cancel_button)
        self.buttons_layout.addStretch()

        # Main Frames Placement
        self.items_layout.addWidget(self.task_name_frame)
        self.items_layout.addWidget(self.task_date_frame)
        self.items_layout.addWidget(self.task_time_frame)

        self.win_layout.addWidget(self.win_title)
        self.win_layout.addWidget(self.win_items, 1)
        self.win_layout.addWidget(self.buttons_frame)

        self.tnf_entry.textEdited.connect(self.validate_entries)
        self.tdf_date_entry.textEdited.connect(self.validate_entries)
        self.tdf_year_entry.textEdited.connect(self.validate_entries)
        self.ttf_hours_entry.textEdited.connect(self.validate_entries)
        self.ttf_mins_entry.textEdited.connect(self.validate_entries)

        self.fill_task_details()

    def fill_task_details(self):
        yy, mm, dd, HH, MM = TBackEnd.return_datetime_now_parts()
        self.tnf_entry.setPlaceholderText(f"Task {len(self.tlist) + 1}")

        if self.task_number:
            index = self.task_number - 1
            task = self.tlist[index]

            ttime, name = task.split("=", 1)
            yy, mm, dd, HH, MM = ttime.split(":")

            self.tnf_entry.setPlaceholderText(f"Task {self.task_number}")
            self.tnf_entry.setText(name.strip())

        month = TBackEnd.month_names[int(mm)].title()
        yyyy = str(int(yy) + 2000)

        self.tdf_year_entry.setText(yyyy.strip())
        self.tdf_month_entry.setCurrentText(month.strip())
        self.tdf_date_entry.setText(dd.strip())
        self.ttf_hours_entry.setText(HH.strip())
        self.ttf_mins_entry.setText(MM.strip())

    def save_task(self):
        valid = self.validate_entries()

        if valid:
            tname = self.tnf_entry.text().strip()
            if not tname:
                self.tnf_entry.setText(f"Task {len(self.tlist) + 1}")
                if self.task_number:
                    self.tnf_entry.setText(f"Task {self.task_number}")
            else:
                self.tnf_entry.setText(tname)

            task_name = self.tnf_entry.text().strip()
            task_date = self.tdf_date_entry.text().strip().zfill(2)
            task_month = str(TBackEnd.reversed_dict(TBackEnd.month_names)[
                            self.tdf_month_entry.currentText().lower()
                        ]).zfill(2)
            task_year = self.tdf_year_entry.text().strip()[-2:]
            task_hours = self.ttf_hours_entry.text().strip().zfill(2)
            task_mins = self.ttf_mins_entry.text().strip().zfill(2)

            task_string = f"{task_year}:{task_month}:{task_date}:{task_hours}:{task_mins}" \
                          f"={task_name}"
            print("final task:", task_string)

            if self.task_number:
                task_index = self.task_number - 1
                try:
                    self.tlist[task_index] = task_string
                except IndexError:
                    print("index error while saving task")
            else:
                self.tlist = TBackEnd.read_and_sort_tasks_file()
                self.tlist.append(task_string)

            print("NEW:", self.tlist)
            TBackEnd.write_tasks(self.tlist)

            self.close()

    def validate_entries(self):
        check = True
        self.save_task_button.setEnabled(True)
        if check:
            self.tnf_entry.setStyleSheet(f"border: 1px solid black;")
            self.tdf_date_entry.setStyleSheet(f"border: 1px solid black;")
            self.tdf_year_entry.setStyleSheet(f"border: 1px solid black;")
            self.ttf_hours_entry.setStyleSheet(f"border: 1px solid black;")
            self.ttf_mins_entry.setStyleSheet(f"border: 1px solid black;")

        tdate = self.tdf_date_entry.text().strip()

        tmonth = self.tdf_month_entry.currentText()

        tyear = self.tdf_year_entry.text().strip()

        thour = self.ttf_hours_entry.text().strip()

        tmins = self.ttf_mins_entry.text().strip()

        if not tdate.isdecimal() or int(tdate) not in range(1, 32):
            self.tdf_date_entry.setStyleSheet(f"border: 4px solid red;")
            check = False

        if not tyear.isdecimal() or int(tyear) not in range(TBackEnd.current_year, 2100):
            self.tdf_year_entry.setStyleSheet(f"border: 4px solid red;")
            check = False

        if tmonth == 'February':
            if tdate and int(tdate) > 29:
                self.tdf_date_entry.setStyleSheet(f"border: 4px solid red;")
                check = False
            if all((tdate, tyear)) and int(tdate) == 29 and not TBackEnd.is_leap(tyear):
                self.tdf_date_entry.setStyleSheet(f"border: 4px solid red")
                self.tdf_year_entry.setStyleSheet("border: 4px solid red")
                check = False

        if not thour.isdecimal() or int(thour) not in range(0, 24):
            self.ttf_hours_entry.setStyleSheet(f"border: 4px solid red;")
            check = False

        if not tmins.isdecimal() or int(tmins) not in range(0, 60):
            self.ttf_mins_entry.setStyleSheet(f"border: 4px solid red;")
            check = False

        if check:
            self.tnf_entry.setStyleSheet(f"border: 1px solid black;")
            self.tdf_date_entry.setStyleSheet(f"border: 1px solid black;")
            self.tdf_year_entry.setStyleSheet(f"border: 1px solid black;")
            self.ttf_hours_entry.setStyleSheet(f"border: 1px solid black;")
            self.ttf_mins_entry.setStyleSheet(f"border: 1px solid black;")
            self.save_task_button.setEnabled(True)
            return True
        else:
            self.save_task_button.setEnabled(False)
            return False

    def delete_task(self):
        task_index = self.task_number - 1

        if task_index in range(len(self.tlist)):
            tname = self.tlist[self.task_number - 1].split("=", 1)[1]
            display_text = f"Are you sure you want to delete Task {self.task_number}?\n\n" \
                           f"Task name: {tname}\n"

            decision = QtWidgets.QMessageBox.question(
                self,
                "Delete Confirmation",
                display_text,
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if decision == QtWidgets.QMessageBox.Yes:
                print(f"Task {self.task_number} deletion requested")
                print(f"CURRENT: {self.tlist}")
                try:
                    TBackEnd.remove(self.task_number, self.tlist)
                except IndexError:
                    print("index error occured while deleting")

                print("NEW:", self.tlist)
                self.close()
            else:
                print(f"Task {self.task_number} deletion cancelled")

    def closeEvent(self, e):
        self.mainWindow.task_window = None
        self.mainWindow.setEnabled(True)
        self.mainWindow.refresh_tasks()


if __name__ == '__main__':
    App()
