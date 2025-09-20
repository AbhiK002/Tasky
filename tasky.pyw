"""
    Tasky is a task deadline tracker application
    Copyright (C) 2022-2025  Abhineet Kelley (AbhiK002)

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

        self.tasks_parted_list = []
        self.tasks_list = []
        self.task_boxes = []
        self.last_read = ''
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

        # About Tasky
        self.about_tasky = QtWidgets.QPushButton()
        self.about_tasky.setIcon(QIcon(TStyle.tlogo_path))
        self.about_tasky.setObjectName("AboutButton")
        self.about_tasky.setToolTip("About Tasky")
        self.about_tasky.clicked.connect(self.show_about_tasky)

        self.buttons_layout.addStretch()
        self.buttons_layout.addWidget(self.new_task_button)
        self.buttons_layout.addWidget(self.switch_mode_button)
        self.buttons_layout.addStretch()
        self.buttons_layout.addWidget(self.about_tasky)

        # place top and bottom frames
        self.mainlayout.addWidget(self.tasks_frame, 1)
        self.mainlayout.addWidget(self.buttons_frame)

        # run main loop and periodically update tasks list
        self.last_datetime = TBackEnd.return_datetime_now_parts()
        self.gui_refresh_timer = QTimer()
        self.gui_refresh_timer.timeout.connect(self.refresh_gui)
        self.gui_refresh_timer.setInterval(500)
        self.gui_refresh_timer.start()

        # add tasks into the GUI
        self.refresh_tasks()

        self.show()
        sys.exit(app.exec_())

    def show_about_tasky(self):
        QtWidgets.QMessageBox.information(
            self,
            'Tasky',
            f"<FONT>{TBackEnd.tasky_version(1, link=True)}</FONT>",
            QtWidgets.QMessageBox.Ok
        )

    def add_tasks_container(self):
        self.tasks_container = QWidget(self.tasks_frame)
        self.tasks_container.setObjectName("TasksContainer")

        self.tasks_layout = QtWidgets.QVBoxLayout(self.tasks_container)
        self.tasks_container.setLayout(self.tasks_layout)

        self.tasks_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.tasks_layout.setContentsMargins(12, 12, 5, 12)

        tasks_scroll_area = QtWidgets.QScrollArea()
        tasks_scroll_area.setObjectName("TasksScrollArea")
        tasks_scroll_area.setWidgetResizable(True)
        tasks_scroll_area.setWidget(self.tasks_container)

        self.tasks_frame_layout.addWidget(tasks_scroll_area, 1)

    def refresh_tasks(self):  # read and display tasks from tasks file
        print("refreshing tasks")
        self.gui_refresh_timer.stop()

        while self.tasks_layout.count():
            child = self.tasks_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.task_boxes.clear()

        # get tasks
        self.tasks_list = TBackEnd.read_and_sort_tasks_file()
        self.tasks_parted_list = TBackEnd.return_deadlines(self.tasks_list)
        self.last_read = open(TBackEnd.tasks_path).read()

        for task in self.tasks_parted_list:
            *task_items, task_desc = task

            task_box = TaskBox(*task_items, self)
            task_box.delete_button.pressed.connect(lambda p=int(task[0]), q=self.tasks_list: [self.direct_delete(p, q)])

            if task_desc:
                tooltip_text = f"<FONT color=black> {task_desc} </FONT>"
                task_box.setToolTip(tooltip_text)

            self.tasks_layout.addWidget(task_box)
            self.task_boxes.append(task_box)

        self.clear_all = QtWidgets.QPushButton("CLEAR ALL TASKS")
        self.clear_all.setObjectName("ClearAllButton")
        self.clear_all.setCursor(QCursor(Qt.PointingHandCursor))
        self.clear_all.clicked.connect(self.clear_all_tasks)

        if not self.tasks_parted_list:
            self.clear_all.setEnabled(False)

        self.tasks_layout.addWidget(self.clear_all, alignment=Qt.AlignCenter)
        self.tasks_layout.addStretch()

        self.gui_refresh_timer.start()

    def refresh_gui(self):  # update only task deadlines in the GUI, or update tasks in case any changes in file
        if TBackEnd.read_tasks_file() != self.last_read:
            self.refresh_tasks()
            return

        time_now = TBackEnd.return_datetime_now_parts()
        if self.last_datetime == time_now:
            return

        self.last_datetime = time_now

        print("refreshing gui")
        if len(self.tasks_parted_list) != len(self.task_boxes):
            self.refresh_tasks()
            return

        self.tasks_parted_list = TBackEnd.return_deadlines(self.tasks_list)
        for i, taskbox in enumerate(self.task_boxes):
            taskbox.td.setText(self.tasks_parted_list[i][1])

    def open_task(self, num=False):
        if num:
            print(f"request to open task {num}")
        else:
            print("request to add new task")

        if self.task_window is None:  # if no other task window open, open the requested one
            self.gui_refresh_timer.stop()

            self.setEnabled(False)
            self.task_window = TaskWindow(num, self)
            win_timer = QTimer(self.task_window)
            win_timer.setSingleShot(True)
            win_timer.timeout.connect(self.task_window.show)
            win_timer.setInterval(200)
            win_timer.start()
        else:
            print("another window already open")

    def direct_delete(self, tasknum, tlist):
        if tasknum - 1 in range(len(tlist)):
            self.gui_refresh_timer.stop()

            tname = tlist[tasknum - 1].split("\t", 2)[1]
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

        self.refresh_tasks()

    def closeEvent(self, e):
        sys.exit()

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
        self.setStyleSheet(TStyle.stylesheet())

        task_lay = QtWidgets.QHBoxLayout(self)
        task_lay.setContentsMargins(0, 0, 0, 0)
        self.setLayout(task_lay)

        t = QtWidgets.QLabel(task_number)
        t.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        t.setObjectName("TaskNum")

        self.td = QtWidgets.QLabel(task_deadline.strip())
        self.td.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.td.setObjectName("TaskDead")

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
        task_lay.addWidget(self.td, 5)
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
    def __init__(self, task_num=False, mainWindow: App = None):
        super(TaskWindow, self).__init__()
        self.window_style = TStyle.twindow_stylesheet()
        self.mainWindow = mainWindow

        self.task_number = task_num
        self.tlist = mainWindow.tasks_list.copy()

        if task_num in range(1, len(self.tlist) + 1):
            title = f"Edit Task {task_num}"
        else:
            title = "New Task"
            self.task_number = False

        self.setWindowTitle(title)

        self.setWindowIcon(QIcon(TStyle.tlogo_path))
        self.setStyleSheet(self.window_style)
        self.setMinimumSize(630, 600)
        self.setMaximumSize(700, 670)
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

        temp_layout = QtWidgets.QHBoxLayout(self.tnf_entry)
        temp_layout.setContentsMargins(0, 0, 8, 0)
        temp_layout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tnf_entry.setLayout(temp_layout)
        self.name_char_indicator = QtWidgets.QLabel("30")
        self.name_char_indicator.setObjectName("CharIndicator")
        self.name_char_indicator.setAlignment(Qt.AlignCenter)
        temp_layout.addWidget(self.name_char_indicator)

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

        # Task Description Frame
        self.task_desc_frame = QWidget(self.win_items)
        self.task_desc_frame.setContentsMargins(0, 10, 0, 0)
        self.task_desc_layout = QtWidgets.QHBoxLayout(self.task_desc_frame)
        self.task_desc_frame.setLayout(self.task_desc_layout)

        self.tdesc_label = QtWidgets.QLabel("Task Description\n(Optional)", self.task_name_frame)
        self.tdesc_label.setAlignment(Qt.AlignTop)

        temp_layout = QtWidgets.QVBoxLayout(self.tdesc_label)
        self.tdesc_label.setLayout(temp_layout)
        help_label = QtWidgets.QLabel("<b>?</b>")
        help_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        help_label.setObjectName("DescHelpLabel")
        help_label.setToolTip(
            "<FONT><i>The task description is displayed when "
            "you hover your mouse over the task</i></FONT>")
        temp_layout.addWidget(help_label)

        self.tdesc_entry = QtWidgets.QTextEdit(self.task_name_frame)
        self.tdesc_entry.setObjectName("DescriptionEntry")
        self.tdesc_entry.setTabChangesFocus(True)
        self.tdesc_entry.setPlaceholderText("Describe the task in max 168 characters")

        temp_layout = QtWidgets.QHBoxLayout(self.tdesc_entry)
        temp_layout.setContentsMargins(0, 0, 8, 0)
        temp_layout.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.tdesc_entry.setLayout(temp_layout)
        self.desc_char_indicator = QtWidgets.QLabel("168")
        self.desc_char_indicator.setObjectName("DescCharIndicator")
        self.desc_char_indicator.setAlignment(Qt.AlignCenter)
        temp_layout.addWidget(self.desc_char_indicator)

        self.task_desc_layout.addWidget(self.tdesc_label)
        self.task_desc_layout.addWidget(self.tdesc_entry, 1)

        # Items Frames Placement
        self.items_layout.addWidget(self.task_name_frame)
        self.items_layout.addWidget(self.task_date_frame)
        self.items_layout.addWidget(self.task_time_frame)
        self.items_layout.addWidget(self.task_desc_frame)

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

        # Window Frames Placement
        self.win_layout.addWidget(self.win_title)
        self.win_layout.addWidget(self.win_items, 1)
        self.win_layout.addWidget(self.buttons_frame)

        self.tnf_entry.textEdited.connect(self.validate_entries)
        self.tdf_date_entry.textEdited.connect(self.validate_entries)
        self.tdf_month_entry.currentTextChanged.connect(self.validate_entries)
        self.tdf_year_entry.textEdited.connect(self.validate_entries)
        self.ttf_hours_entry.textEdited.connect(self.validate_entries)
        self.ttf_mins_entry.textEdited.connect(self.validate_entries)
        self.tdesc_entry.textChanged.connect(self.validate_entries)

        # sync date-time entries to live date-time until user enters anything
        self.time_checker = QTimer()
        self.time_checker.timeout.connect(self.update_entries_time)
        self.time_checker.setInterval(500)
        if not self.task_number:
            self.time_checker.start()

        self.fill_task_details()

    def fill_task_details(self):
        yy, mm, dd, HH, MM = TBackEnd.return_datetime_now_parts()
        self.tnf_entry.setPlaceholderText(f"Task {len(self.tlist) + 1}")

        if self.task_number:
            index = self.task_number - 1
            task = self.tlist[index]

            ttime, name, desc = task.split("\t", 2)
            yy, mm, dd, HH, MM = ttime.split(":")

            self.tnf_entry.setPlaceholderText(f"Task {self.task_number}")
            self.tdesc_entry.setText(desc)
            self.tnf_entry.setText(name.strip())

        month = TBackEnd.month_names[int(mm)].title()
        yyyy = str(int(yy) + 2000)

        self.tdf_year_entry.setText(yyyy)
        self.tdf_month_entry.setCurrentText(month)
        self.tdf_date_entry.setText(dd)
        self.ttf_hours_entry.setText(HH)
        self.ttf_mins_entry.setText(MM)

        self.validate_entries()

    def update_entries_time(self):
        y = self.tdf_year_entry.text().strip()[-2:]
        m = str(TBackEnd.month_name_to_num[self.tdf_month_entry.currentText().lower()]).zfill(2)
        d = self.tdf_date_entry.text().strip().zfill(2)
        h = self.ttf_hours_entry.text().strip().zfill(2)
        mi = self.ttf_mins_entry.text().strip().zfill(2)

        try:
            TBackEnd.str_to_date_obj(f'{y} {m} {d} {h} {mi}', '%y %m %d %H %M')
        except ValueError:
            print("stopping entries checking timer")
            self.time_checker.stop()

        current_entry_times = [y, m, d, h, mi]
        current_time = TBackEnd.return_datetime_now_parts()

        if current_time == current_entry_times:
            return

        current_time = ":".join(current_time)

        diff = TBackEnd.timediff(current_time, diff_of=current_entry_times, tasky_output=False)
        if sum(diff) == 1 and diff[-1] == 1:
            print("1 min diff = updating entries to live time")
            yy, mm, dd, HH, MM = TBackEnd.return_datetime_now_parts()
            self.tdf_year_entry.setText(str(2000 + int(yy)))
            self.tdf_month_entry.setCurrentText(TBackEnd.month_names[int(mm)].title())
            self.tdf_date_entry.setText(dd)
            self.ttf_hours_entry.setText(HH)
            self.ttf_mins_entry.setText(MM)
        else:
            print("stopping entries checking timer")
            self.time_checker.stop()

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
            task_month = str(TBackEnd.month_name_to_num[
                            self.tdf_month_entry.currentText().lower()
                        ]).zfill(2)
            task_year = self.tdf_year_entry.text().strip()[-2:]
            task_hours = self.ttf_hours_entry.text().strip().zfill(2)
            task_mins = self.ttf_mins_entry.text().strip().zfill(2)
            task_desc = self.tdesc_entry.toPlainText().strip().replace('\n', ' ')

            task_string = f"{task_year}:{task_month}:{task_date}:{task_hours}:{task_mins}" \
                          f"\t{task_name}\t{task_desc}"
            print("final task:", task_string)

            if self.task_number:
                task_index = self.task_number - 1
                try:
                    self.tlist[task_index] = task_string
                except IndexError:
                    print("index error while saving task")
            else:
                self.tlist.append(task_string)

            print("NEW:", self.tlist)
            TBackEnd.write_tasks(self.tlist)

            self.close()

    def validate_entries(self):
        check = True
        self.name_char_indicator.setStyleSheet("border: 0")
        self.desc_char_indicator.setStyleSheet("border: 0")
        self.save_task_button.setEnabled(True)
        if check:
            self.tnf_entry.setStyleSheet(f"border: 1px solid black;")
            self.tdf_date_entry.setStyleSheet(f"border: 1px solid black;")
            self.tdf_year_entry.setStyleSheet(f"border: 1px solid black;")
            self.ttf_hours_entry.setStyleSheet(f"border: 1px solid black;")
            self.ttf_mins_entry.setStyleSheet(f"border: 1px solid black;")
            self.tdesc_entry.setStyleSheet("border: 1px solid black;")

        self.name_char_indicator.setText(f"{30 - len(self.tnf_entry.text().strip())}")
        tdate = self.tdf_date_entry.text().strip().zfill(2)

        tmonth = self.tdf_month_entry.currentText()
        tmonth_num = str(TBackEnd.month_name_to_num[tmonth.lower()]).zfill(2)
        days_in_month = TBackEnd.months[tmonth_num]

        tyear = self.tdf_year_entry.text().strip()
        thour = self.ttf_hours_entry.text().strip().zfill(2)
        tmins = self.ttf_mins_entry.text().strip().zfill(2)
        tdesc = self.tdesc_entry.toPlainText().strip().replace('\n', ' ')
        self.desc_char_indicator.setText(str(168 - len(tdesc)))

        if not tdate.isdecimal() or int(tdate) not in range(1, days_in_month+1):
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

        if len(tdesc) > 168:
            self.tdesc_entry.setStyleSheet("border: 4px solid red;")
            check = False

        self.name_char_indicator.setStyleSheet("border: 0")
        self.desc_char_indicator.setStyleSheet("border: 0")
        if check:
            self.tnf_entry.setStyleSheet(f"border: 1px solid black;")
            self.tdf_date_entry.setStyleSheet(f"border: 1px solid black;")
            self.tdf_year_entry.setStyleSheet(f"border: 1px solid black;")
            self.ttf_hours_entry.setStyleSheet(f"border: 1px solid black;")
            self.ttf_mins_entry.setStyleSheet(f"border: 1px solid black;")
            self.tdesc_entry.setStyleSheet("border: 1px solid black;")
            self.save_task_button.setEnabled(True)
            return True
        else:
            self.save_task_button.setEnabled(False)
            return False

    def delete_task(self):
        task_index = self.task_number - 1

        if task_index in range(len(self.tlist)):
            tname = self.tlist[self.task_number - 1].split("\t", 2)[1]
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
