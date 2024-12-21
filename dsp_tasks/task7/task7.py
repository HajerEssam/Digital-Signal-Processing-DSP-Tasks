import numpy as np

from dsp_tasks.task7.CompareSignal import *
import tkinter as tk
from tkinter import filedialog
from matplotlib import pyplot as plt
import os
import math

input_signal1_dict = []
input_signal2_dict = []


def read_file_path(sig):
    file_path = filedialog.askopenfilename(
        title="Select a Text File",
        filetypes=(("Text files", "*.txt"),)
    )
    read_sig(sig, file_path)


def read_sig(sig, file_path):
    if file_path:
        with open(file_path, 'r') as f:
            line = f.readline()
            line = f.readline()
            line = f.readline()
            line = f.readline()
            while line:
                L = line.strip()
                if len(L.split(' ')) == 2:
                    L = line.split(' ')
                    V2 = float(L[1])
                    sig.append(V2)
                    line = f.readline()
                elif len(L.split(' ')) == 1:
                    L = line.split(' ')
                    V = float(L[0])
                    sig.append(V)
                    line = f.readline()
                else:
                    break


def calc_correlation(info_text, display_info):
    global input_signal1_dict, input_signal2_dict
    len_signal = len(input_signal1_dict)
    result = []

    for l in range(len_signal):
        dot_product = 0
        for n in range(len_signal):
            shifted_index = (n + l) % len_signal
            if len_signal > shifted_index < len_signal:
                dot_product += input_signal1_dict[n] * input_signal2_dict[shifted_index]
        result.append(float(round((dot_product / len_signal), 8)))

    max_value = max(result) * len_signal
    std_signal1 = sum(x ** 2 for x in input_signal1_dict)
    std_signal2 = sum(x ** 2 for x in input_signal2_dict)
    result = [x / (math.sqrt(std_signal1 * std_signal2) * 1 / len_signal) for x in result]

    if display_info:
        print(result)
        info_text.insert(tk.END, f"Max absolute value: {max_value}\n")

        plt.figure(figsize=(10, 6))
        plt.plot(result, marker='o', color='#1d817e', label='Cross-Correlation')
        plt.title('Cross-Correlation')
        plt.xlabel('Time')
        plt.ylabel('Normalized Correlation')
        plt.grid()
        plt.legend()
        plt.show()

        Compare_Signals('task7\Point1 Correlation\CorrOutput.txt', list(range(len_signal)), result)

    return result


def time_analysis(info_text, Fs=100):
    result = calc_correlation(info_text, False)
    max_value = max(result)
    j = result.index(max_value)
    time_delay = j * 1 / Fs
    info_text.insert(tk.END, f"Time delay: {time_delay}")


def classify_signal(info_text):
    folder_paths = ['task7\point3 Files\Class 1', 'task7\point3 Files\Class 2']
    class1_corr = []
    class2_corr = []
    for index, folder_path in enumerate(folder_paths):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path) and file_name.endswith('.txt'):
                print(f"Reading file: {file_name}")
                input_signal2_dict.clear()
                read_sig(input_signal2_dict, file_path)
                result = calc_correlation(info_text, False)
                class1_corr.append(max(result)) if index == 0 else class2_corr.append(max(result))
    class1_mean = np.mean(class1_corr)
    class2_mean = np.mean(class2_corr)
    if class1_mean > class2_mean:
        info_text.insert(tk.END, "IT is DOWN movement of EOG signal")
    else:
        info_text.insert(tk.END, "IT is UP movement of EOG signal")


def task7_gui(frame):
    task7_frame = frame

    label1 = tk.Label(task7_frame, text="Signal 1 :")
    label1.place(x=70, y=50)
    sig_btn = tk.Button(task7_frame, text="upload", command=lambda: read_file_path(input_signal1_dict))
    sig_btn.place(x=120, y=50)
    label4 = tk.Label(task7_frame, text="Signal 2 :")
    label4.place(x=220, y=50)
    sig_btn2 = tk.Button(task7_frame, text="upload", command=lambda: read_file_path(input_signal2_dict))
    sig_btn2.place(x=270, y=50)

    info_text = tk.Text(task7_frame, height=5, width=30, font=("Arial", 12))
    info_text.place(x=90, y=100)

    btn1 = tk.Button(task7_frame, text="Correlation", command=lambda: calc_correlation(info_text, True))
    btn1.place(x=60, y=250)
    btn2 = tk.Button(task7_frame, text="Time Analysis", command=lambda: time_analysis(info_text))
    btn2.place(x=200, y=250)
    btn3 = tk.Button(task7_frame, text="Classify Signal", command=lambda: classify_signal(info_text))
    btn3.place(x=350, y=250)
