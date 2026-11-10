# Getting Started with Visual Studio Code (VS Code)

This guide is for anyone opening this project (**ShipmentDesk**) in Visual Studio Code for the first time and who has little or no prior programming experience. It walks through installing VS Code, opening this project, understanding the file structure you'll see on the left, and the few things you'll need to do to run and edit the code.

---

## 1. What is VS Code?

Visual Studio Code (VS Code) is a free code editor made by Microsoft. Think of it like a very powerful version of Notepad or Microsoft Word, but built specifically for writing and running code. It doesn't "run" your project by itself — it's the place where you read, write, and organize code files, and it gives you tools (like a built-in terminal) to run that code.


---

## 2. Installing VS Code

1. Go to the official VS Code website: https://code.visualstudio.com/
2. Click the **Download** button for your operating system (Windows, macOS, or Linux).
3. Open the downloaded installer and follow the on-screen steps (keep the default options unless you have a reason to change them).
4. Once installed, open VS Code from your Applications folder (Mac) or Start Menu (Windows).


---

## 3. Opening This Project in VS Code

There are two common ways to open this project:

**Option A — From within VS Code:**
1. Open VS Code.
2. Go to `File > Open Folder...` (on Mac it may say `File > Open...`).
3. Navigate to and select the `Shipment-Desk` folder.
4. Click **Open**.

**Option B — From your file explorer / Finder:**
1. Right-click the `Shipment-Desk` folder.
2. Select **Open with Code** (if that option isn't there, use Option A instead).

Once opened, VS Code will show the project's file structure in a panel on the left called the **Explorer**.

---

## 4. Understanding the File Structure (Explorer Panel)

The panel on the left side of VS Code is called the **Explorer**. It lists every file and folder in the project, similar to how Finder (Mac) or File Explorer (Windows) shows files, except it's built into the editor.


For this project, here's what you'll see at the top level and what each item means:

| Name | What it is |
|---|---|
| `starter_kit/` | A folder containing an incomplete version of the project — meant as a starting point to build from. |
| `solution/` | A folder containing the completed, working version of the project — useful as a reference. |
| `Instructor_Class_Script.md` | A written script/notes, likely used for teaching or walking through the material. |
| `Problem_Statement_and_Milestones.md` | A document describing the problem this project solves and the milestones/steps to complete it. |
| `.gitignore` | A configuration file that tells Git (version control) which files to ignore — you generally won't need to edit this. |

Inside `starter_kit/` and `solution/`, you'll find files like:

| File | Purpose (in plain terms) |
|---|---|
| `README.md` | Instructions specific to that folder — always a good first read. |
| `app.py`, `main.py` | The main program files — where the application starts running. |
| `chains.py`, `pipeline.py`, `tools.py`, `session.py`, `llm.py`, `triage_check.py` | Supporting code files, each handling a specific piece of the program's logic. |
| `requirements.txt` | A list of external packages/libraries the program needs in order to run. |
| `.env.example` | A template showing what secret settings (like API keys) the program expects — you copy this to a new file named `.env` and fill in real values. |

You don't need to understand every file right away — folders and files can be expanded/collapsed by clicking the arrow or name next to them.


---

## 5. Opening and Reading a File

Click any file name in the Explorer panel, and it will open in the main editing area to the right.


- Files ending in `.md` (like this one!) are **Markdown** files — plain text with simple formatting. VS Code can show a nicely formatted "preview" of them: open the file, then click the small preview icon in the top-right corner of the editor (or right-click the file tab and choose "Open Preview").
- Files ending in `.py` are **Python** code files.
- Files ending in `.txt` are plain text files.


---

## 6. The Built-in Terminal

VS Code has a built-in terminal — a place to type text commands to run the program, install requirements, etc. You don't need to open a separate application for this.

To open it: go to the top menu and select `Terminal > New Terminal`, or use the keyboard shortcut `` Ctrl+` `` (Windows/Linux) or `` Cmd+` `` (Mac).



Common things you might be asked to type here (your instructor or README will specify the exact commands):

```
pip install -r requirements.txt
python main.py
```


---

## 7. Useful Things to Know

- **Saving files:** VS Code usually shows a white/filled dot on a file's tab if it has unsaved changes. Press `Ctrl+S` (Windows/Linux) or `Cmd+S` (Mac) to save.
- **Search across the project:** Press `Ctrl+Shift+F` (Windows/Linux) or `Cmd+Shift+F` (Mac) to search for text across all files in the project — helpful for finding where something is defined.
- **Extensions:** VS Code supports add-ons called "Extensions" (found in the sidebar, the icon that looks like four squares). For Python projects, installing the official **Python** extension (by Microsoft) is recommended — it adds helpful features like error highlighting.


- **Colored dots/numbers in the Explorer:** These usually relate to Git (version control) status — e.g. showing which files have been changed. This project is already set up with Git, so you may see these appear as you edit files.


---

## 8. Where to Go From Here

1. Read `README.md` inside `starter_kit/` (or `solution/`) for project-specific setup steps.
2. Read `Problem_Statement_and_Milestones.md` in the root folder to understand what the project is trying to achieve.
3. Read `Instructor_Class_Script.md` if you're following along with a class or walkthrough.
4. Use the terminal to install requirements and run the program, following the steps in the relevant README.

