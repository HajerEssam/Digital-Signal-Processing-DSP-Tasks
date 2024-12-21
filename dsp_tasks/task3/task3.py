import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from dsp_tasks.common_functions import *
from dsp_tasks.task3.QuanTest1 import *
from dsp_tasks.task3.QuanTest2 import *

signal_dict = {}


def write_output_file(quantization_error, num_type):
    interval_indices = list(map(lambda x: x[0], quantization_error))
    encoded_values = list(map(lambda x: x[1], quantization_error))
    quantized_values = list(map(lambda x: x[2], quantization_error))
    samples_error = list(map(lambda x: x[3], quantization_error))

    with open(r'C:\Users\Hager Essam\OneDrive\Desktop\Collage\DSP\Tasks\DSP_Tasks_Package\dsp_tasks\task3\Output',
              'w') as file:
        file.write(f"0\n")
        file.write(f"0\n")
        file.write(f"{len(signal_dict)}\n")
        if num_type == 'Bits':
            for line in quantization_error:
                file.write(f"{line[1]} {line[2]:.2f}\n")

            QuantizationTest1(
                r'C:\Users\Hager Essam\OneDrive\Desktop\Collage\DSP\Tasks\DSP_Tasks_Package\dsp_tasks\task3\Quan1_Out.txt',
                encoded_values, quantized_values)

        else:
            for line in quantization_error:
                file.write(f"{line[0]} {line[1]} {line[2]:.3f} {line[3]:.3f}\n")

            #QuantizationTest2(r'C:\Users\Hager Essam\OneDrive\Desktop\Collage\DSP\Tasks\DSP_Tasks_Package\dsp_tasks\task3\Quan2_Out.txt', interval_indices, encoded_values, quantized_values, samples_error)


def calculate_quantization_error(ranges, levels, num_type):
    quantized_sig = {}
    quantization_error = []
    avg_error = 0
    num_bits = (len(ranges) - 1).bit_length()

    for ind in signal_dict.keys():
        val = signal_dict[ind]
        for i, r in enumerate(ranges):
            if r[0] <= val <= r[1] or (val < r[0] and i == 0) or (val > r[1] and i == len(ranges) - 1):
                quantized_sig[ind] = levels[i]
                binary_val = format(i, f'0{num_bits}b')
                quantization_error.append((i + 1, binary_val, levels[i], (levels[i] - val)))
                avg_error += pow((levels[i] - val), 2)
                break

    avg_error /= len(quantization_error)
    draw_signal(quantized_sig)
    write_output_file(quantization_error, num_type)
    messagebox.showinfo("Average Quantization Error", f"Average Quantization Error is: {avg_error}")


def quantization_levels(num_type, num):
    ranges = []
    levels = []

    minimum = min(signal_dict.values())
    maximum = max(signal_dict.values())

    if num_type == 'Bits':
        delta = (maximum - minimum) / pow(2, num)
    else:
        delta = (maximum - minimum) / num

    lower = minimum
    while lower + delta < maximum:
        ranges.append((lower, round((lower + delta), 5)))
        lower = lower + delta

    for interval in ranges:
        midpoint = (interval[0] + interval[1]) / 2
        levels.append(round(midpoint, 3))
    calculate_quantization_error(ranges, levels, num_type)


def task3_gui(frame):
    task3_frame = frame

    label1 = tk.Label(task3_frame, text="Signal :")
    label1.place(x=50, y=60)
    sig_btn = tk.Button(task3_frame, text="upload", command=lambda: upload_txt_file(signal_dict))
    sig_btn.place(x=110, y=60)

    label2 = tk.Label(task3_frame, text="num :")
    label2.place(x=50, y=130)
    num = tk.Entry(task3_frame, width=6)
    num.place(x=110, y=130)

    combo_box = ttk.Combobox(task3_frame, values=["Levels", "Bits"])
    combo_box.place(x=170, y=130)
    combo_box.set("Levels")

    btn = tk.Button(task3_frame, text="Output", command=lambda: quantization_levels(combo_box.get(), int(num.get())))
    btn.place(x=200, y=200)
