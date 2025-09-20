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

from pathlib import Path

from files.tasky_ops import OSFunctions


class Colors:
    dark_yellow = "#9B7D42"
    yellow = "#FFDA59"
    light_yellow = "#FFF297"

    golden = "#E8B953"
    orange = "#D86950"
    bright_orange = "#FB371C"

    dark_red = "#6A0800"
    red = "#C80009"
    light_red = "#FF3443"

    darkest_gray = "#151515"
    darker_gray = "#303030"
    dark_gray = "#404040"
    gray = "#505050"
    light_gray = "#656565"
    lighter_gray = "#808080"

    black = "#000000"
    white = "#FFFFFF"

    # Tasks
    task_orange = "rgba(232, 105, 105, 1)"
    task_orange_trans = "rgba(232, 105, 105, 0.4)"

    g_val = 90
    task_gray = f"rgba({g_val}, {g_val}, {g_val}, 1)"
    task_gray_trans = f"rgba({g_val}, {g_val}, {g_val}, 0.3)"


class TaskyStyle:
    def __init__(self):
        self.files_path = Path(OSFunctions.resource_path("files")).resolve()
        self.resources_path = Path(self.files_path / "resources").resolve()
        self.colors = Colors()

        self.tlogo_path = str(self.resources_path / "tlogo.png")
        self.delete_button_icon = str(self.resources_path / "delicon.svg")

        self.text_size = 18
        self.task_text_size = 20
        self.big_text_size = 24

        self.theme = None

        self.taskydir = taskydir = Path.home() / "Tasky"
        taskydir.mkdir(parents=True, exist_ok=True)

        open(taskydir / "settings.txt", 'a').close()
        with open(taskydir / "settings.txt") as f:
            self.theme = f.read().replace("\n", "")
            if self.theme not in ("dark", "light"):
                with open(taskydir / "settings.txt", "w") as a:
                    a.write("light")
                self.theme = "light"

        self.new_task_icon, self.switch_mode_icon = None, None
        self.change_colors()

    def switch_mode(self):
        if self.theme == "light":
            self.theme = "dark"
        else:
            self.theme = "light"

        self.taskydir.mkdir(parents=True, exist_ok=True)
        with open(self.taskydir / "settings.txt", "w") as f:
            f.write(self.theme)

        self.change_colors()

    def change_colors(self):
        if self.theme == "light":
            self.major_bg = Colors.yellow
            self.major_hg = Colors.light_yellow
            self.major_abg = Colors.dark_yellow
            self.minor_bg = Colors.orange

            self.task_bg = Colors.task_orange
            self.task_bg_trans = Colors.task_orange_trans

            self.text_fg = Colors.black

            self.mode_fg = Colors.yellow
            self.mode_bg = Colors.darker_gray
            self.mode_hg = Colors.dark_gray
            self.mode_abg = Colors.darkest_gray

            self.new_task_icon = str(self.resources_path / "add_task_light_icon.png")
            self.switch_mode_icon = str(self.resources_path / "dark_mode_icon.png")

        else:
            self.major_bg = Colors.darker_gray
            self.major_hg = Colors.dark_gray
            self.major_abg = Colors.darkest_gray
            self.minor_bg = Colors.gray

            self.task_bg = Colors.task_gray
            self.task_bg_trans = Colors.task_gray_trans

            self.text_fg = Colors.white

            self.mode_fg = Colors.black
            self.mode_bg = Colors.yellow
            self.mode_hg = Colors.light_yellow
            self.mode_abg = Colors.dark_yellow

            self.new_task_icon = str(self.resources_path / "add_task_dark_icon.png")
            self.switch_mode_icon = str(self.resources_path / "light_mode_icon.png")

    def stylesheet(self):
        return (
            "QWidget {"
            f"color: {self.text_fg};"
            "}"

            "QMessageBox QLabel, QMessageBox QPushButton {"
            f"color: black;"
            "}"

            "QWidget#MainWindow, QWidget#TasksFrame {"
            f"background-color: {self.minor_bg};"
            "}"

            "QPushButton#NewTaskButton, "
            "QPushButton#SwitchModeButton {"
            f"background-color: {self.major_bg};"
            f"border: 2px solid black; border-radius: 20px;"
            f"padding: 8px; font-size: {self.text_size}px;"
            "font-weight: bold; font-family: \'Segoe UI\';"
            "min-width: 150px;"
            "}"

            "QPushButton#SwitchModeButton {"
            f"background-color: {self.mode_bg};"
            f"color: {self.mode_fg}"
            "}"


            "QPushButton#NewTaskButton:hover {"
            f"background-color: {self.major_hg};"
            "}"
            "QPushButton#SwitchModeButton:hover {"
            f"background-color: {self.mode_hg};"
            "}"

            "QPushButton#NewTaskButton:pressed {"
            f"background-color: {self.major_abg};"
            "}"
            "QPushButton#SwitchModeButton:pressed {"
            f"background-color: {self.mode_abg};"
            "}"
            
            "QPushButton#AboutButton {"
            f"background-color: {self.major_hg};"
            f"min-width: 40px; min-height: 40px;"
            f"border-radius: 20px;"
            "}"
            "QPushButton#AboutButton:hover, QPushButton#AboutButton:pressed {"
            f"background-color: {self.major_bg};"
            "}"

            "QLabel#TasksHeadingLabel {"
            f"font-size: {self.big_text_size}px; font-weight: bolder;"
            f"max-height: {self.big_text_size + 4}px;"
            f"min-height: {self.big_text_size + 4}px;"
            "}"

            "QWidget#TaskItem {"
            f"min-height: 40px; "  # max-height: 40px;"
            f"border-radius: 15px;"
            "}"
            "QWidget#TaskItem:hover {"
            f"background-color: {self.task_bg};"
            "}"
            
            "QToolTip {"
            "border: 2px solid black; font-size: 20px;"
            f"background: {Colors.white}; color: black;"
            "}"

            "QLabel#TaskNum, QLabel#TaskDead, QLabel#TaskName {"
            f"font-size: {self.task_text_size}px; padding: 2px;"
            "}"

            "QLabel#TaskNum {"
            f"max-width: 30px; min-width: 30px; border-radius: 15px;"
            f"background-color: {self.task_bg_trans};"
            f"font-size: {self.task_text_size - 2}px"
            "}"

            "QLabel#TaskDead {"
            "min-width: 240px; max-width: 400px; font-family: 'Consolas';"
            f"font-weight: bold; font-size: {self.task_text_size + 2}px; border-radius: 10px;"
            f"border: 2px solid {self.task_bg};"
            f"color: {self.mode_bg}"
            "}"

            "QLabel#TaskName {"
            "min-width: 300px; max-width: 800px; border-radius: 15px;"
            f"font-size: {self.task_text_size - 1};"
            f"background-color: {self.task_bg_trans};"
            "}"

            "QPushButton#DeleteButton {"
            f"background-color: {Colors.lighter_gray};"
            f"border: 3px solid black; border-radius: 15px;"
            f"min-width: 15px; max-width: 20px; "
            "padding: 6px;"
            "}"
            "QPushButton#DeleteButton:hover {"
            f"background-color: #AAAAAA;"
            "}"
            "QPushButton#DeleteButton:pressed, QPushButton#DeleteButton:disabled {"
            f"background-color: {Colors.light_gray};"
            "}"

            "QScrollArea#TasksScrollArea {"
            f"background-color: {self.major_bg};"
            "border: 2px solid black; border-radius: 20px;"
            "}"

            "QWidget#TasksContainer {"
            f"background-color: transparent;"
            "}"

            "QScrollBar {"
            f"background-color: {self.major_bg};"
            "}"

            "QScrollBar:vertical, QScrollBar:horizontal {"
            "width: 14px; margin: 10px 2px 10px 0px;"
            "}"

            "QScrollBar::handle:vertical, QScrollBar::handle:horizontal {"
            f"background-color: {self.mode_bg};"
            f"border: 1px solid {self.mode_bg};"
            "border-radius: 6px;"
            "}"

            "QScrollBar::add-line {"
            "border: none;"
            "background: none;"
            "}"

            "QScrollBar::sub-line {"
            "border: none;"
            "background: none;"
            "}"

            "QPushButton#ClearAllButton {"
            f"background: transparent; color: {self.text_fg}; font-weight: bold; border-radius: 15px;"
            "font-size: 14px; min-width: 150px; border: 0px; min-height: 30px"
            "}"
            "QPushButton#ClearAllButton:hover {"
            f"background: {self.major_hg};"
            "}"
            "QPushButton#ClearAllButton:disabled {"
            "color: transparent;"
            "}"
        )

    def twindow_stylesheet(self):
        return (
            "TaskWindow {"
            f"background-color: {self.minor_bg};"
            "}"

            "QLabel {"
            f"color: {self.mode_bg};"
            f"font-size: {self.task_text_size}px"
            "}"

            "QMessageBox QLabel, QMessageBox QPushButton {"
            f"color: black;"
            "}"
            "QMessageBox QLabel {"
            "font-size: 18px;"
            "}"

            "QLabel#TaskWindowTitle {"
            f"max-height: 40px; font-size: {self.task_text_size + 6}px;"
            f"color: {self.text_fg}"
            "}"

            "QWidget#TaskWindowItems {"
            f"background-color: {self.major_bg};"
            f"border-radius: 30px; border: 2px solid black;"
            "}"

            "QLineEdit, QComboBox {"
            f"font-size: {self.task_text_size}px;"
            "}"

            "QLineEdit {"
            "border-radius: 8px; padding: 6px;"
            "border: 1px solid black; max-width: 60px;"
            "}"

            "QLineEdit#NameEntry {"
            "max-width: 1800px;"
            "}"
            
            "QTextEdit#DescriptionEntry {"
            "font-size: 20px; border-radius: 18px; padding: 4px;"
            "border: 1px solid black; background: white"
            "}"

            "QPushButton#DeleteButton {"
            f"background-color: {Colors.white};"
            f"border: 4px solid black; border-radius: 26px;"
            f"padding: 8px; min-width: 30px; max-width: 30px; "
            f"min-height: 30px; max-height: 30px;"
            "}"
            "QPushButton#DeleteButton:hover {"
            f"background-color: #AAAAAA;"
            "}"
            "QPushButton#DeleteButton:pressed, QPushButton#DeleteButton:disabled {"
            f"background-color: {Colors.light_gray};"
            "}"
            
            "QToolTip {"
            "border: 2px solid black;"
            f"background: {Colors.white}; color: black;"
            f"font-size: 20px;"
            "}"

            "QPushButton#SaveButton, QPushButton#CancelButton {"
            f"background-color: {self.mode_bg}; color: {self.mode_fg};"
            f"border: 2px solid black; border-radius: 20px;"
            f"padding: 8px; font-size: {self.text_size}px;"
            "font-weight: bold; max-width: 150px; min-width: 150px;"
            "}"

            "QPushButton#CancelButton {"
            f"color: {Colors.white};"
            f"background-color: {Colors.red}"
            "}"

            "QPushButton#SaveButton:hover {"
            f"background-color: {self.mode_hg}"
            "}"
            "QPushButton#CancelButton:hover {"
            f"background-color: {Colors.light_red};"
            "}"

            "QPushButton#SaveButton:pressed {"
            f"background-color: {self.mode_abg};"
            "}"
            "QPushButton#CancelButton:pressed {"
            f"background-color: {Colors.dark_red};"
            "}"

            "QPushButton#SaveButton:disabled {"
            f"background-color: {Colors.gray};"
            "}"
            
            "QLabel#DescHelpLabel {"
            f"color: {self.mode_bg}; border: 2px solid {self.mode_bg};"
            f"font-size: {self.big_text_size}px; border-radius: 15px;"
            f"max-height: 30px; max-width: 30px;"
            "}"
            
            "QLabel#CharIndicator, QLabel#DescCharIndicator {"
            f"color: blue; font-size:{self.text_size-2}px;"
            f"border: 0px solid black; min-width: 40px;"
            f"min-height: 30px; background: white; border-radius: 10px;"
            "}"
            
            "QLabel#CharIndicator {"
            "min-width: 30px; max-width: 30px;"
            "}"
        )
