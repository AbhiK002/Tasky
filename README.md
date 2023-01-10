<p align='center'>
<img src='https://user-images.githubusercontent.com/68178267/210774045-c83e75ae-a2f2-40e3-b260-e24139271aec.png' height=100>
<img src='https://user-images.githubusercontent.com/68178267/210774312-416d35a3-ad67-46f1-9f46-693e2592fd48.png' height=100>
<h1 align='center'> Tasky </h1>

<p align='center'> 📜 Have a lot of tasks you need to complete within their deadlines? ⏰ </p>

<br>
Tasky is a simple deadline tracker program that displays a pretty list showing the time remaining for each task, making it easier to prioritize tasks to complete.


# Download
[Click here to download](https://github.com/AbhiK002/Tasky/releases/latest) the latest version of Tasky (v2.0.1)

Includes:
- Tasky
- Tasky CLI Version (Command Line Interface)

# Features

- 🐤 Simple and easy to use application
- ⚜ Modern and interactive graphical user interface
- 👁 Visual track of task deadlines
- 🔁 Live updates of the time remaining for upto 100 tasks
- 💻 Has a console version for people who prefer CLI

- 💫 Offers 2 themes:

  - 🖤 Dark mode (Grayscale)
  - 🧡 Light mode (Gold and Orange)
 
- ⚙ Add, edit or remove tasks
- 💬 Enter a task description for each task to store more helpful details

# How To Use
- Click the 'New Task' button to add a new task
- Click the 'Dark Theme' or 'Light Theme' button to switch color themes
- Click on a task to edit its details
- Hover over a task to view the task description
- To delete a task, you can either:
  - Click the 'TRASH' icon button in the 'Edit Task' window, OR 
  - Hover over the task and click the 'TRASH' icon button in the far right
- Click the 'Clear All' button in the end of the tasks list to delete all tasks

#### 'TRASH' icon buttons: 
![de2](https://user-images.githubusercontent.com/68178267/210439366-4876bdc5-0a1a-441f-a7ae-9d8a09bd0ff8.png)
![de](https://user-images.githubusercontent.com/68178267/210439196-1b8e0773-625d-4463-bc63-39905b38752f.png)


# Tasky CLI Commands
Note:  
  ▷ Here `X` refers to the task number (`1`, `2`, `3` ...) of any task you want to operate on (task numbers are displayed with the tasks in the output)  
  ▷ None of the commands shown below are case-sensitive  

### Commands
- Add Task             -  `add` `new` `create`
- Delete Task          -  `delete X` `del X` `remove X` `rem X`
- Delete All Tasks     -  `clear`
- Edit Task            -  `edit X` `ed X` `change X`
- View Task Details    -  `ENTER TASK NUMBER` (Examples: `1`, `2`, `3`, `4` ...)
- Open Help Menu       -  `help` `h`
- About Tasky          -  `version` `about`
- Exit Tasky           -  `quit` `bye`

# Requirements
Only required if you want to run the `.pyw` or `.py` file directly. Otherwise use the binary (ZIP, EXE) files in releases.
* 🐍 [Python 3.9.x or 3.10.x](https://www.python.org/downloads/)
* 🟣 [PyQt5](https://pypi.org/project/PyQt5/)

Install PyQt5 using `pip` via terminal
```
pip install PyQt5
```
#### (NOTE: Tasky's CLI version does not require any additional modules other than in-built Python modules & libraries)

# Usage
### Repository
- Clone the repository or download the repository ZIP file
- Make sure you have met the requirements above
  - Run `gui_main.pyw` to use Tasky
  - Run `console_main.py` to use the CLI (Command Line Interface) version of Tasky

### Releases
- [Download the ZIP file from the latest release of Tasky](https://github.com/AbhiK002/Tasky/releases/latest)
- Extract contents from the ZIP file using WinRAR or other software
- In the extracted folder,
  - Run `Tasky.exe` to use Tasky
  - Run `Tasky Console.exe` to use the CLI (Command Line Interface) version of Tasky

# Screenshots
- Light mode and Dark mode of Tasky

![modes](https://user-images.githubusercontent.com/68178267/210431442-47c1f2c3-3be4-438f-b8a1-f77ba6f6d25a.png)

- Edit Task window and visible task description on hovering mouse over a task

![edit_desc](https://user-images.githubusercontent.com/68178267/210434733-ce5ccc60-54ee-4eb9-9b5a-f59012ea4b3b.png)

## Tasky CLI
- (Left to Right) These commands have been used: `help` and `new`

![cli_help_new](https://user-images.githubusercontent.com/68178267/210443417-900e0fb1-d0e9-4171-a60c-4e6c1b5bf897.png)

- (Left to Right) These commands have been used: `edit 9` then `remove 1`

![cli_edit_delete](https://user-images.githubusercontent.com/68178267/210443484-aa285595-8df0-46f7-9d9b-1ef421091417.png)

- The command `5` has been used to view the details of task number 5 in the list

![cli_view](https://user-images.githubusercontent.com/68178267/210443633-6425281a-ef04-4829-bf98-fc574b1001cb.png)


### Created by Abhineet Kelley (Github: AbhiK002)
Enjoy!
