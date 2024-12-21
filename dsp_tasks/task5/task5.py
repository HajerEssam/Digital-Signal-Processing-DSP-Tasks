from dsp_tasks.common_functions import *
import tkinter as tk
from dsp_tasks.task5.Testing import *

avg_signal_dict = {}
d1signal_dict = {}
d2signal_dict = {}
conv_signal_dict = {}


def moving_avg(size,input_signal_dict):
    avg_signal_dict.clear()
    for i in range(len(input_signal_dict)):
        if i + size <= len(input_signal_dict):
            avg_signal_dict[i] = 0
            for j in range(i, i + size):
                avg_signal_dict[i] += input_signal_dict[j]
            avg_signal_dict[i] = round((avg_signal_dict[i] / size), 3)
    write_output_file('task5/avg_output', avg_signal_dict)
    plot_signals(input_signal_dict, avg_signal_dict)
    validate_moving_avg(size)


def validate_moving_avg(size):
    indices, samples = ReadSignalFile('task5/avg_output')
    if size == 3:
        Test(
            'task5/testcases/Moving Average testcases/MovingAvg_out1.txt',
            indices, samples)

    elif size == 5:
        Test(
            'task5/testcases/Moving Average testcases/MovingAvg_out2.txt',
            indices, samples)


def derivative(dtype,input_signal_dict):
    if dtype == 1:  # Y(n) = x(n)-x(n-1)
        for i in range(1, len(input_signal_dict)):
            d1signal_dict[i - 1] = input_signal_dict[i] - input_signal_dict.get(i - 1, 0)
        write_output_file('task5/1d_out', d1signal_dict)
        plot_signals(input_signal_dict, d1signal_dict)

        indices, samples = ReadSignalFile('task5/1d_out')
        Test(
            'task5/testcases/Derivative testcases/1st_derivative_out.txt',
            indices, samples)

    elif dtype == 2:  # Y(n)= x(n+1)-2x(n)+x(n-1)
        for i in range(2, len(input_signal_dict)):
            d2signal_dict[i - 2] = input_signal_dict[i] - 2 * input_signal_dict.get(i - 1, 0) + input_signal_dict.get(
                i - 2, 0)
        write_output_file('task5/2d_out', d2signal_dict)
        plot_signals(input_signal_dict, d2signal_dict)

        indices, samples = ReadSignalFile('task5/2d_out')
        Test(
            'task5/testcases/Derivative testcases/2nd_derivative_out.txt',
            indices, samples)


def apply_convolution(input_signal_dict,input_signal2_dict):
    convolution(input_signal_dict, input_signal2_dict)
    write_output_file('task5/conv_output.txt', conv_signal_dict)
    plot_signals(input_signal_dict, conv_signal_dict)
    indices, samples = ReadSignalFile('task5/conv_output.txt')
    Test('task5/testcases/Convolution testcases/Conv_output.txt', indices, samples)


def convolution(input_signal_dict,input_signal2_dict):
    conv_signal_dict.clear()
    len1 = len(input_signal_dict)
    len2 = len(input_signal2_dict)
    start_index = min(input_signal_dict) + min(input_signal2_dict)
    outputSignalLength = len1 + len2 - 1

    for n in range(outputSignalLength):
        dotProduct = 0
        for m in input_signal2_dict:
            input_idx = n - m + min(input_signal_dict) + min(input_signal2_dict)
            if input_idx in input_signal_dict:
                dotProduct += input_signal_dict[input_idx] * input_signal2_dict[m]
        conv_signal_dict[start_index + n] = float(dotProduct)

    return conv_signal_dict


def plot_signals(inputs, outputs):
    plt.figure(figsize=(10, 6))

    plt.plot(inputs.keys(), inputs.values(), label='input signal', marker='o', color='blue')
    plt.plot(outputs.keys(), outputs.values(), label='output Signal', marker='o', color='orange')

    plt.xlabel('index')
    plt.ylabel('value')
    plt.legend()
    plt.grid(True)
    plt.show()


def write_output_file(file_name, sig_dict):
    with open(file_name, 'w') as file:
        file.write(f"0\n")
        file.write(f"0\n")
        file.write(f"{len(sig_dict)}\n")

        for index in sig_dict:
            if sig_dict[index].is_integer():
                file.write(f"{index} {int(sig_dict[index])}\n")
            else:
                file.write(f"{index} {float(sig_dict[index])}\n")


def task5_gui(frame):
    task5_frame = frame

    input_signal_dict = {}
    input_signal2_dict = {}

    label1 = tk.Label(task5_frame, text="Signal :")
    label1.place(x=50, y=60)
    sig_btn = tk.Button(task5_frame, text="upload", command=lambda: upload_txt_file(input_signal_dict))
    sig_btn.place(x=100, y=60)
    label4 = tk.Label(task5_frame, text="Filter :")
    label4.place(x=200, y=60)
    sig_btn2 = tk.Button(task5_frame, text="upload", command=lambda: upload_txt_file(input_signal2_dict))
    sig_btn2.place(x=250, y=60)

    label2 = tk.Label(task5_frame, text="window size :")
    label2.place(x=50, y=110)
    num = tk.Entry(task5_frame, width=6)
    num.place(x=130, y=110)

    label3 = tk.Label(task5_frame, text="Operation :")
    label3.place(x=50, y=140)

    derivative_type = tk.IntVar()
    add = tk.Radiobutton(task5_frame, text='First Derivative', variable=derivative_type, value=1)
    add.place(x=80, y=170)

    sub = tk.Radiobutton(task5_frame, text='Second derivative', variable=derivative_type, value=2)
    sub.place(x=220, y=170)

    btn1 = tk.Button(task5_frame, text="Move Average", command=lambda: moving_avg(int(num.get()),input_signal_dict))
    btn1.place(x=60, y=250)
    btn2 = tk.Button(task5_frame, text="Apply Derivative", command=lambda: derivative(derivative_type.get(),input_signal_dict))
    btn2.place(x=200, y=250)
    btn3 = tk.Button(task5_frame, text="Convolution", command=lambda: apply_convolution(input_signal_dict,input_signal2_dict))
    btn3.place(x=350, y=250)
