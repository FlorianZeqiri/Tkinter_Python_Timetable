import csv
import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
from turtle import back
# CSV File Columns (departmentAndYear, course, days, times)
root = tk.Tk()
DEPARTMENT_AND_YEAR = 0
COURSE = 1
DAYS = 2
TIMES = 3
warnings = []
warningList = StringVar()
coursesList = StringVar()
last_event: Event
courses_to_save = []
# =============================================================================


def display():
    global courses
    global warnings
    global rows
    global last_event
    is_global = "last_event" in globals()
    path = os.path.abspath(entryCsv.get())
    if path == "":
        warnings.append("File path is required!")
    else:
        file = open(path)
        reader = csv.reader(file)
        data = list(reader)
        courses = data
        rows = data
        year = vitiZgjedhur.get().lower()
        department = dpEntry.get().lower()
        if year != "":
            courses = [course for course in courses if list(
                course)[DEPARTMENT_AND_YEAR].split(' ')[1][0].lower() == year]
        if department != "":
            courses = [course for course in courses if list(
                course)[DEPARTMENT_AND_YEAR].split(' ')[0].lower() == department]
        if is_global:
            listbox.selection_clear(0, 'end')
        coursesList.set(value=courses)
    warningList.set(value=warnings)


def set_selection(items_to_select):
    for item in items_to_select:
        listbox.select_set(item)


def on_select(evt):
    global courses
    global warnings
    global last_event
    global listbox
    event = evt.widget.curselection()
    is_global = "last_event" in globals()
    index = -1
    if not is_global:
        index = event[0]
    else:
        selected_item_index = list(
            (set(event).symmetric_difference(set(last_event))))
        if len(selected_item_index) > 0:
            index = selected_item_index[0]
    schedule_mismatch = False
    if len(warnings) > 0 and (courses[index][DEPARTMENT_AND_YEAR] not in warnings):
        selected_item = courses[index]
        selected_item_days = list(selected_item[DAYS].split(' '))
        selected_item_schedules = list(selected_item[TIMES].split(' '))
        selected_item_ds = list(
            zip(selected_item_days, selected_item_schedules))
        if selected_item_ds != [('', '')]:
            for schedule in selected_item_ds:
                for item in courses_to_save:
                    temp_course = [course for course in courses
                                   if list(course)[DEPARTMENT_AND_YEAR] == item.lstrip("Added ")][0]
                    item_schedules = list(temp_course[TIMES].split(' '))
                    item_days = list(temp_course[DAYS].split(' '))
                    item_ds = list(zip(item_days, item_schedules))
                    for ds in item_ds:
                        if schedule[0] == ds[0]:
                            start1 = list(schedule[1].split('-'))[0]
                            end1 = list(schedule[1].split('-'))[1]
                            start2 = list(ds[1].split('-'))[0]
                            end2 = list(ds[1].split('-'))[1]
                            if end1 >= start2 and end2 >= start1:
                                schedule_mismatch = True
                                warnings.append(
                                    'Could not add: ' + selected_item[DEPARTMENT_AND_YEAR])
                                listbox.selection_clear(index)
                                set_selection(last_event)
    if not schedule_mismatch:
        if len(courses_to_save) == 6 and index not in last_event:
            for i in event:
                if i not in warnings:
                    listbox.selection_clear(i)
                    set_selection(last_event)
        else:
            selected_item = 'Added ' + courses[index][DEPARTMENT_AND_YEAR]
            if selected_item in courses_to_save:
                warnings.remove(selected_item)
                courses_to_save.remove(selected_item)
            elif len(courses_to_save) == 6:
                listbox.select_clear(index)
            else:
                warnings.append(selected_item)
                courses_to_save.append(selected_item)
            last_event = event
    warningList.set(value=warnings)


def save_courses():
    global courses_to_save
    fp = open('savedCourses.txt', 'w')
    to_write = []
    for c in courses_to_save:
        to_write.append([course for course in courses if list(course)[
                        DEPARTMENT_AND_YEAR] == c.lstrip("Added ")][0])
    to_write = ["{}\n".format(i) for i in to_write]
    fp.writelines(to_write)


def clear():
    global warnings
    global courses
    global last_event
    global courses_to_save
    is_global = "last_event" in globals()
    if is_global:
        del last_event
    warnings = []
    courses = []
    courses_to_save = []
    warningList.set(value=warnings)
    coursesList.set(value=courses)
    entryCsv.delete(0, 'end')
    vitiZgjedhur.delete(0, 'end')
    dpEntry.delete(0, 'end')


# ==================================================================
root.geometry('940x620')
root.title('Timetable')
root.config(background="#252525")
pathLabel = Label(root,
                  text='Enter the csv file name: ',
                  font=('Arial', 16, 'bold'),
                  bg=('#252525'),
                  fg=('#ffffff')
                  )
pathLabel.pack()
pathLabel.place(x=1, y=20)
content = tk.StringVar()
entryCsv = Entry(root, 
                font=('Arial', 16), 
                width=50, 
                textvariable=content, 
                background='#191919',
                fg='#ffffff'
                )
entryCsv.pack(side=LEFT)
entryCsv.place(x=250, y=20)
vitiCombo = ttk.Label(root, 
                    text="Year :",
                    font=('Arial', 15, 'bold'), 
                    background="#252525",
                    foreground='#ffffff' )
vitiCombo.place(x=20, y=100)
# Combobox creation
n = tk.StringVar()
vitiZgjedhur = ttk.Combobox(root, width=20, textvariable=n, font=('Arial', 15))
# Adding combobox drop down list
vitiZgjedhur['values'] = (1, 2, 3, 4)
vitiZgjedhur.place(x=90, y=100)
vitiZgjedhur.current()
departamentLabel = Label(root,
                         text='Departament: ',
                         font=('Arial', 15, 'bold'),
                         background='#252525',
                         foreground='#ffffff'
                         )
departamentLabel.pack()
departamentLabel.place(x=450, y=100)

dp = tk.StringVar()
dpEntry = ttk.Combobox(root, 
            font=('Arial', 16),
            background="#191919",
            textvariable=dp
            )
dpEntry['values'] = ('CSE', 'MEKSS', 'FAR')
dpEntry.pack(side=LEFT)
dpEntry.place(x=585, y=100)

displayBtn = Button(
    root,
    text='Display',
    font=('Arial', 15, 'bold'),
    fg=('#ffffff'),
    bg=('#191919'),
    command=display
)
displayBtn.pack()
displayBtn.place(x=20, y=200)


clearBtn = Button(
    root,
    text='Clear',
    font=('Arial', 15, 'bold'),
    command=clear,
    fg=('#ffffff'),
    bg=('#191919'),
    width=7
)
clearBtn.pack()
clearBtn.place(x=120, y=200)


saveButton = Button(
    root,
    text='Save',
    font=('Arial', 15, 'bold'),
    fg=('#ffffff'),
    bg=('#191919'),
    width=7,
    command=save_courses
)
saveButton.pack()
saveButton.place(x=220, y=200)

warningViewLabel = Label(
    root,
    text='Warnings: ',
    font=('Arial', 15, 'bold'),
    background=('#252525'),
    foreground=('#ffffff')
)
warningViewLabel.pack(side=LEFT)
warningViewLabel.place(x=10, y=260)

selectedListBox = Listbox(
    root,
    width=50,
    height=60,
    selectmode=MULTIPLE,
    listvariable=warningList,
    background='#191919',
    foreground='#ffffff'
)
selectedListBox.pack(side=BOTTOM)
selectedListBox.place(x=2, y=300)

listViewLabel = Label(
    root,
    text='Courses: ',
    font=('Arial', 15, 'bold'),
    fg='#ffffff',
    bg='#252525'
)
listViewLabel.pack(side=RIGHT)
listViewLabel.place(x=650, y=260)

listbox = Listbox(
    root, 
    width=50,
    height= 60,
    selectmode=MULTIPLE,
    background='#191919',
    foreground='#ffffff',
    listvariable=coursesList
)
listbox.pack(side=BOTTOM)
listbox.place(x=650, y=300)
listbox.bind('<<ListboxSelect>>')
listbox.bind('<<ListboxSelect>>', on_select)
root.mainloop()
