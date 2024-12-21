from dsp_tasks.task1.task1 import task1_gui
from dsp_tasks.task2.task2 import task2_gui
from dsp_tasks.task3.task3 import task3_gui
from dsp_tasks.task5.task5 import task5_gui
from dsp_tasks.task6.task6 import task6_gui
from dsp_tasks.task7.task7 import task7_gui
from dsp_tasks.PracticalTask.Filters import last_gui
import tkinter as tk
from tkinter import ttk

W = tk.Tk()
W.title('DSP Tasks ')
W.geometry("500x400")

notebook = tk.ttk.Notebook(W)
notebook.pack(pady=10, expand=True)

task1_frame = tk.Frame(notebook, width=600, height=500)
task1_frame.pack(fill="both", expand=True)
notebook.add(task1_frame, text="Task 1")

task2_frame = tk.Frame(notebook, width=600, height=500)
task2_frame.pack(fill="both", expand=True)
notebook.add(task2_frame, text="Task 2")

task3_frame = tk.Frame(notebook, width=600, height=500)
task3_frame.pack(fill="both", expand=True)
notebook.add(task3_frame, text="Task 3")

task5_frame = tk.Frame(notebook, width=600, height=500)
task5_frame.pack(fill="both", expand=True)
notebook.add(task5_frame, text="Task 5")

task6_frame = tk.Frame(notebook, width=600, height=500)
task6_frame.pack(fill="both", expand=True)
notebook.add(task6_frame, text="Task 6")

task7_frame = tk.Frame(notebook, width=600, height=500)
task7_frame.pack(fill="both", expand=True)
notebook.add(task7_frame, text="Task 7")

practical_frame = tk.Frame(notebook, width=600, height=500)
practical_frame.pack(fill="both", expand=True)
notebook.add(practical_frame, text="Practical Task")

task1_gui(task1_frame)
task2_gui(task2_frame)
task3_gui(task3_frame)
task5_gui(task5_frame)
task6_gui(task6_frame)
task7_gui(task7_frame)
last_gui(practical_frame)

W.mainloop()
