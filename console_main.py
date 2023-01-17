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

from os import startfile
from files.console_ops import ConsoleFunctions


class App(ConsoleFunctions):
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
                    f"{'Delete All Tasks'.ljust(20)} --  clear",
                    f"{'Edit Task N'.ljust(20)} --  edit N / ed N / change N",
                    f"{'View Task Details'.ljust(20)} --  ENTER TASK NUMBER",
                    f"{'Open Help Menu'.ljust(20)} --  help / h",
                    f"{'About Tasky'.ljust(20)} --  version / about",
                    f"{'Exit Tasky'.ljust(20)} --  quit / bye",
                    sep="\n"
                )
                print("-" * 60)

            elif user_inp.isdecimal():
                if int(user_inp) in range(1, total_tasks + 1):
                    self.TL.info(f"user requested to view task {int(user_inp)}")
                    self.info_bar(f"viewing task {int(user_inp)}")
                    self.view_task(int(user_inp), task_list)
                else:
                    self.TL.error(f"user requested to view an invalid task number {int(user_inp)}")
                    self.info_bar(f"invalid task number to view")

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
                        tasks_copy = task_list.copy()
                        confirm = self.is_confirmed(f"\nConfirm removal of task {words[1]}? (enter y/n):  ", tasks_copy)
                        if confirm:
                            self.TL.info(f"confirmed")
                            self.remove(words[1], tasks_copy)
                            self.info_bar(f"removed task {int(words[1])} from the list")
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
                        tasks_copy = task_list.copy()
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
                    "\nWARNING: Clear all existing tasks? (Cannot be undone)\n\t(Enter y/n) :  ",
                    last=task_list
                )
                if confirm:
                    self.clear_tasks()
                    self.info_bar("cleared all tasks")
                else:
                    self.TL.info("user cancelled clearing all tasks")
                    self.info_bar("cancelled clearing all tasks")

            elif user_inp in ("version", "about"):
                self.TL.info("user requested to check the version of Tasky")
                self.info_bar("viewing current version")
                print(self.tasky_version())

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
