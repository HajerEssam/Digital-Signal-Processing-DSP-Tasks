from dsp_tasks.task1.testing import *
from dsp_tasks.common_functions import *
import tkinter as tk
from tkinter import ttk

signal1_dict = {}
signal2_dict = {}
Out_signal_dict = {}


def execute_op(op, num_e):
    Out_signal_dict.clear()
    match op:
        case 'Addition':
            add_signals()
            write_output_file('out_add')
            indicies, samples = ReadSignalFile('out_add')
            AddSignalSamplesAreEqual("Signal1.txt", "Signal2.txt", indicies,samples)

            draw_signal(Out_signal_dict)
        case 'Subtraction':
            sub_signals()
            write_output_file('out_sub')
            indicies, samples = ReadSignalFile('out_sub')
            SubSignalSamplesAreEqual("Signal1.txt", "Signal2.txt", indicies,samples)
            draw_signal(Out_signal_dict)

        case 'Shift Left':
            shift_signal(int(num_e.get()), '+')
            write_output_file('out_advanced')
            indicies, samples = ReadSignalFile('out_advanced')
            ShiftSignalByConst(3, indicies, samples)
            draw_signal(Out_signal_dict)

        case 'Shift Right':
            shift_signal(int(num_e.get()), '-')
            write_output_file('out_delay')
            indicies, samples = ReadSignalFile('out_delay')
            ShiftSignalByConst(-3, indicies, samples)
            draw_signal(Out_signal_dict)

        case 'Multiply by Const':
            mul_signal(int(num_e.get()))
            write_output_file('out_mul')
            indicies, samples = ReadSignalFile('out_mul')
            MultiplySignalByConst(5, indicies, samples)
            draw_signal(Out_signal_dict)

        case 'Reverse':
            reverse_signal()
            write_output_file('out_folding')
            indicies, samples = ReadSignalFile('out_folding')
            Folding(indicies, samples)
            draw_signal(Out_signal_dict)

        case 'Show Sig1':
            draw_signal(signal1_dict)

        case 'Show Sig2':
            draw_signal(signal2_dict)

        case _:
            print("Choose an operation")


def add_signals():
    keys = sorted(set(signal1_dict.keys()).union(set(signal2_dict.keys())))
    for i in keys:
        Out_signal_dict[i] = signal1_dict.get(i, 0) + signal2_dict.get(i, 0)


def sub_signals():
    keys = sorted(set(signal1_dict.keys()).union(set(signal2_dict.keys())))
    for i in keys:
        Out_signal_dict[i] = signal1_dict.get(i, 0) - signal2_dict.get(i, 0)


def mul_signal(num):
    for i in signal1_dict.keys():
        Out_signal_dict[i] = signal1_dict.get(i) * num


def shift_signal(num, sign):
    if sign == '+':
        for i in signal1_dict.keys():
            Out_signal_dict[i - num] = signal1_dict.get(i)
    elif sign == '-':
        for i in signal1_dict.keys():
            Out_signal_dict[i + num] = signal1_dict.get(i)


def reverse_signal():
    Out_signal_dict.clear()
    temp_dict = {}
    for i in signal1_dict.keys():
        temp_dict[i * -1] = signal1_dict.get(i)
    Out_signal_dict.update(dict(sorted(temp_dict.items())))


def write_output_file(file_name):
    with open(file_name, 'w') as file:
        file.write(f"0\n")
        file.write(f"0\n")
        file.write(f"{len(Out_signal_dict)}\n")

        for index in Out_signal_dict:
            file.write(f"{index} {int(Out_signal_dict[index])}\n")


def task1_gui(frame):
    task1_frame = frame

    label1 = tk.Label(task1_frame, text="Signal 1 :")
    label1.place(x=50, y=60)
    Sig1_btn = tk.Button(task1_frame, text="upload", command=lambda: upload_txt_file(signal1_dict))
    Sig1_btn.place(x=110, y=60)

    label2 = tk.Label(task1_frame, text="Signal 2 :")
    label2.place(x=50, y=100)
    Sig2_btn = tk.Button(task1_frame, text="upload", command=lambda: upload_txt_file(signal2_dict))
    Sig2_btn.place(x=110, y=100)

    label3 = tk.Label(task1_frame, text="Operation :")
    label3.place(x=50, y=140)

    selected_op = tk.StringVar(value='Addition')

    add = tk.Radiobutton(task1_frame, text='Addition', variable=selected_op, value='Addition')
    add.place(x=70, y=170)

    sub = tk.Radiobutton(task1_frame, text='Subtraction', variable=selected_op, value='Subtraction')
    sub.place(x=70, y=190)

    label4 = tk.Label(task1_frame, text="num :")
    label4.place(x=200, y=240)
    num_e = ttk.Entry(task1_frame, width=4)
    num_e.place(x=235, y=240)

    sl = tk.Radiobutton(task1_frame, text='Advanced', variable=selected_op, value='Shift Left')
    sl.place(x=180, y=170)

    sr = tk.Radiobutton(task1_frame, text='Delay', variable=selected_op, value='Shift Right')
    sr.place(x=180, y=190)

    mul_const = tk.Radiobutton(task1_frame, text='Multiply by Const', variable=selected_op, value='Multiply by Const')
    mul_const.place(x=180, y=210)

    reverse = tk.Radiobutton(task1_frame, text='Reverse', variable=selected_op, value='Reverse')
    reverse.place(x=320, y=170)

    draw_sig1 = tk.Radiobutton(task1_frame, text='Show signal 1', variable=selected_op, value='Show Sig1')
    draw_sig1.place(x=320, y=190)

    draw_sig2 = tk.Radiobutton(task1_frame, text='Show signal 2', variable=selected_op, value='Show Sig2')
    draw_sig2.place(x=320, y=210)

    Output_btn = tk.Button(task1_frame, text="Output", command=lambda: execute_op(selected_op.get(), num_e))
    Output_btn.place(x=210, y=290)