# TODO before start the app, please run
# pip install calendar
# in your terminal with activated venv for the project


from tkinter import messagebox

from tkcalendar import DateEntry
from tkinter.ttk import *
from tkinter import *
from tkinter.scrolledtext import *
import os
import json
import webbrowser

mapper = {1: "Minor", 2: "Medium", 3: "High"}


def clear_view(tk_window):
    for el in tk_window.grid_slaves():
        el.destroy()


def get_id(tasks):
    ids = sorted(tasks, key=lambda x: x['id'], reverse=True)
    if ids:
        last_id = ids[0]['id'] + 1
        return last_id
    return 1


def create_task(name, date, description, priority, is_completed, task=None):
    with open('db.txt', 'r+') as file:
        if os.path.getsize('db.txt'):
            all_tasks = json.load(file)
        else:
            all_tasks = []
        if not task:
            task_id = get_id(all_tasks)
        else:
            task_id = task
        task = {'id': task_id, 'name': name, 'date': date, 'description': description, 'priority': priority,
                'is_completed': is_completed}

        all_tasks.append(task)
        file.seek(0)
        file.truncate(0)
        json.dump(all_tasks, file)
    clear_view(window)
    main_view(window)


def create_task_view(tk_window):
    clear_view(tk_window)
    Label(window, text="Enter your task name: ").grid(row=0, column=0, padx=20, pady=20)
    name = Entry(window)
    name.grid(row=0, column=1, padx=20, pady=20)
    Label(window, text="Due date: ").grid(row=1, column=0, padx=20, pady=20)
    date = DateEntry(window)
    date.grid(row=1, column=1, padx=20, pady=20)
    Label(window, text="Description: ").grid(row=2, column=0, padx=20, pady=20)
    description = ScrolledText(window, width=20, height=10)
    description.grid(row=2, column=1, padx=20, pady=20)
    Label(window, text="Select priority: ").grid(row=3, column=0, padx=20, pady=20)
    selected = IntVar()
    rad1 = Radiobutton(window, text='Low', value=1, variable=selected)
    rad2 = Radiobutton(window, text='Medium', value=2, variable=selected)
    rad3 = Radiobutton(window, text='High', value=3, variable=selected)
    rad1.grid(column=1, row=3)
    rad2.grid(column=2, row=3)
    rad3.grid(column=3, row=3)
    Label(window, text="Check if completed: ").grid(row=4, column=0, padx=20, pady=20)
    chk_state = BooleanVar()
    chk_state.set(False)  # set check state
    chk = Checkbutton(window, text='Choose', var=chk_state)
    chk.grid(column=1, row=4)
    all_fields = [name, date, description, selected, chk_state]
    Button(window, text="Create new task", bg="green", fg="white",
           command=lambda: create_task(name.get(), date.get(), description.get("1.0", END), selected.get(),
                                       chk_state.get())).grid(row=5, column=0)
    Button(window, text="Cancel", bg="black", fg="white", command=lambda: main_view(window)).grid(row=5, column=1,
                                                                                                  padx=100,
                                                                                                  pady=100)


def triger_edit(selected, all_tasks, all_fields):
    m = messagebox.askquestion("Edit", "Are you sure you want to edit?")
    if m == "yes":
        all_tasks.remove(selected)
        task = {'id': selected['id'], 'name': all_fields[0], 'date': all_fields[1], 'description': all_fields[2],
                'priority': all_fields[3],
                'is_completed': all_fields[4]}

        all_tasks.append(task)
        with open('db.txt', 'w+') as file:
            file.seek(0)
            file.truncate(0)
            json.dump(all_tasks, file)
        main_view(window)


def edit_task(task):
    task_id = int(re.match(r"{'id': (?P<id>\d+)", task).groupdict()['id'])
    with open('db.txt', 'r+') as file:
        all_tasks = json.load(file)
        selected = list(filter(lambda x: x['id'] == task_id, all_tasks))[0]
    clear_view(window)
    Label(window, text="Enter your task name: ").grid(row=0, column=0, padx=20, pady=20)
    name = Entry(window)
    name.delete(0, END)
    name.insert(0, selected['name'])
    name.grid(row=0, column=1, padx=20, pady=20)
    Label(window, text="Due date: ").grid(row=1, column=0, padx=20, pady=20)
    date = DateEntry(window)
    date.delete(0, END)
    date.insert(0, selected['date'])
    date.grid(row=1, column=1, padx=20, pady=20)
    Label(window, text="Description: ").grid(row=2, column=0, padx=20, pady=20)
    description = ScrolledText(window, width=20, height=10)
    description.insert(INSERT, selected['description'])
    description.insert(END, "")
    description.grid(row=2, column=1, padx=20, pady=20)
    Label(window,
          text=f"Select priority, current is {mapper[selected['priority']] if selected['priority'] else None}").grid(
        row=3, column=0, padx=20, pady=20)
    s = IntVar()
    rad1 = Radiobutton(window, text='Low', value=1, variable=s)
    rad2 = Radiobutton(window, text='Medium', value=2, variable=s)
    rad3 = Radiobutton(window, text='High', value=3, variable=s)

    rad1.grid(column=1, row=3)
    rad2.grid(column=2, row=3)
    rad3.grid(column=3, row=3)
    Label(window, text="Check if completed: ").grid(row=4, column=0, padx=20, pady=20)
    Label(window, text="Check if completed: ").grid(row=4, column=0, padx=20, pady=20)
    chk_state = BooleanVar()
    chk_state.set(selected["is_completed"])  # set check state
    chk = Checkbutton(window, text='Choose', var=chk_state)
    chk.grid(column=1, row=4)

    Button(window, text="Edit task", bg="yellow", fg="black",
           command=lambda: triger_edit(window, selected, all_tasks)).grid(
        row=5, column=0)
    Button(window, text="Cancel", bg="black", fg="white", command=lambda: main_view(window)).grid(row=5, column=1,
                                                                                                  padx=100,
                                                                                                  pady=100)


def delete_task(task):
    task_id = int(re.match(r"{'id': (?P<id>\d+)", task).groupdict()['id'])
    with open('db.txt', 'r+') as file:
        all_tasks = json.load(file)
        selected = list(filter(lambda x: x['id'] == task_id, all_tasks))[0]
        m = messagebox.askquestion("Action: Delete!", "Are you sure you want to remove this task?")
        if m == "yes":
            all_tasks.remove(selected)
        file.seek(0)
        file.truncate(0)
        json.dump(all_tasks, file)
    list_tasks_view(window)


def list_tasks_view(tk):
    clear_view(tk)
    dd = Combobox(tk, width=100)
    with open('db.txt', 'r') as file:
        try:
            all_tasks = json.load(file)
        except:
            all_tasks = []
    dd['values'] = all_tasks
    dd.grid(row=0, column=0)
    Label(tk, text="Select a task and action: ").grid(row=1, column=0, padx=20, pady=20)
    Button(tk, text="Edit task", bg="yellow", fg="black", command=lambda: edit_task(dd.get())).grid(row=2, column=0)
    Button(tk, text="Delete task", bg="red", fg="white", command=lambda: delete_task(dd.get())).grid(row=2, column=1)
    Button(tk, text="Cancel", bg="black", fg="white", command=lambda: main_view(tk)).grid(row=3, column=0, padx=100,
                                                                                          pady=100)


def openurl():
    webbrowser.open("https://likegeeks.com/python-gui-examples-tkinter-tutorial/")


def main_view(tk_window):
    clear_view(tk_window)
    Button(tk_window, text="List all tasks", bg="blue", fg="white", command=lambda: list_tasks_view(tk_window)).grid(
        row=1, column=0,
        padx=100,
        pady=100)
    Button(tk_window, text="Create new task", bg="green", fg="white", command=lambda: create_task_view(tk_window)).grid(
        row=1,
        column=1,
        padx=100,
        pady=100)
    Button(window, text='Tkinter Tutorial', bg="yellow", fg="black", command=lambda: openurl()).grid(row=10, column=2)


if __name__ == "__main__":
    global window
    window = Tk()
    window.geometry("700x600")
    window.title('My task')
    window.iconbitmap(r"favicon.ico")
    window.configure(bg="ivory")

    main_view(window)
    window.mainloop()