from dsp_tasks.PracticalTask.CompareSignal import *
from dsp_tasks.common_functions import *
from dsp_tasks.task5.task5 import convolution
from dsp_tasks.task6.task6 import DFT, IDFT
import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib import pyplot as plt
import os
import math

signal_dict = {}


def rectangular(N):
    w = {}
    for n in range(math.floor(N / 2) + 1):
        w[n] = 1
    return w


def hanning(N):
    w = {}
    for n in range(math.floor(N / 2) + 1):
        w[n] = 0.5 + 0.5 * np.cos(2 * np.pi * n / N)
    return w


def hamming(N):
    w = {}
    for n in range(math.floor(N / 2) + 1):
        w[n] = 0.54 + 0.46 * np.cos(2 * np.pi * n / N)
    return w


def blackman(N):
    w = {}
    for n in range(math.floor(N / 2) + 1):
        w[n] = 0.42 + 0.5 * np.cos(2 * np.pi * n / (N - 1)) + 0.08 * np.cos(4 * np.pi * n / (N - 1))
    return w


def window_func(s_att):
    if s_att <= 21:
        return rectangular, 0.9
    elif s_att <= 44:
        return hanning, 3.1
    elif s_att <= 53:
        return hamming, 3.3
    else:
        return blackman, 5.5


def high_pass(fs, fc, f1, f2, df, N):
    fc_d_N = (fc - (df / 2)) / fs
    h_d = {}
    for n in range(math.floor(N / 2) + 1):
        if n == 0:
            h_d[n] = 1 - 2 * fc_d_N
        else:
            h_d[n] = -2 * fc_d_N * (math.sin(n * 2 * np.pi * fc_d_N) / (n * 2 * np.pi * fc_d_N))
    return h_d


def low_pass(fs, fc, f1, f2, df, N):
    fc_d_N = (fc + (df / 2)) / fs
    h_d = {}
    for n in range(math.floor(N / 2) + 1):
        if n == 0:
            h_d[n] = 2 * fc_d_N
        else:
            h_d[n] = 2 * fc_d_N * (math.sin(n * 2 * np.pi * fc_d_N) / (n * 2 * np.pi * fc_d_N))
    return h_d


def band_pass(fs, fc, f1, f2, df, N):
    fc1_d_N = (f1 - (df / 2)) / fs
    fc2_d_N = (f2 + (df / 2)) / fs
    h_d = {}

    for n in range(math.floor(N / 2) + 1):
        if n == 0:
            h_d[n] = 2 * (fc2_d_N - fc1_d_N)
        else:
            LHS = 2 * fc2_d_N * (math.sin(n * 2 * np.pi * fc2_d_N) / (n * 2 * np.pi * fc2_d_N))
            RHS = 2 * fc1_d_N * (math.sin(n * 2 * np.pi * fc1_d_N) / (n * 2 * np.pi * fc1_d_N))
            h_d[n] = LHS - RHS
    return h_d


def band_reject(fs, fc, f1, f2, df, N):
    fc1_d_N = (f1 + (df / 2)) / fs
    fc2_d_N = (f2 - (df / 2)) / fs
    h_d = {}

    for n in range(math.floor(N / 2) + 1):
        if n == 0:
            h_d[n] = 1 - 2 * (fc2_d_N - fc1_d_N)
        else:
            LHS = 2 * fc1_d_N * (math.sin(n * 2 * np.pi * fc1_d_N) / (n * 2 * np.pi * fc1_d_N))
            RHS = 2 * fc2_d_N * (math.sin(n * 2 * np.pi * fc2_d_N) / (n * 2 * np.pi * fc2_d_N))
            h_d[n] = LHS - RHS
    return h_d


def filter_calc(filter_type):
    match filter_type:
        case 'High Pass':
            return high_pass
        case 'Low Pass':
            return low_pass
        case 'Band Pass':
            return band_pass
        case 'Band Reject':
            return band_reject
        case _:
            raise ValueError(f"Invalid filter type")


def design_filter(filter_type, fs, fc, f1, f2, s_att, df, case_num):
    window, num = window_func(s_att)
    N = math.ceil((num * fs) / df)
    if N % 2 == 0:
        N += 1

    h_d = filter_calc(filter_type)(fs, fc, f1, f2, df, N)
    w = window(N)

    h = {}
    for n in range(math.floor(N / 2) + 1):
        h[n] = h_d[n] * w[n]
        if n != 0:
            h[-n] = h[n]

    sorted_h = dict(sorted(h.items()))
    plot_filter(sorted_h)
    if case_num % 2 != 0:
        Compare_Signals(test(case_num), list(sorted_h.keys()), list(sorted_h.values()))
    else:
        out1, out2 = apply_filter(signal_dict, sorted_h)
        print("In Time Domain")
        Compare_Signals(test(case_num), list(out1.keys()), list(out1.values()))
        print("\nIn Frequency Domain")
        Compare_Signals(test(case_num), list(out2.keys()), list(out2.values()))
        plot_sig(out1)


def apply_filter(input_sig, h):
    # first: in time domain
    out1 = convolution(input_sig, h)

    # second: in frequency domain
    length = len(h) + len(input_sig) - 1  # 455
    padding_length = length - (math.floor(len(h) / 2))

    for k in range(padding_length):  # 53 [-26,26] 455
        if k not in h:
            h[k] = 0

    for k in range(length):  # 400 -> 455
        if k not in input_sig:
            input_sig[k] = 0

    f_input_signal = DFT(length, input_sig)
    f_filter = DFT(length, h)

    mul = []
    input = list(f_input_signal.values())
    h_f = list(f_filter.values())
    for point, fpoint in zip(input, h_f):
        mul.append(point * fpoint)

    F = {}
    for i, item in zip(f_filter.keys(), mul):
        F[i] = item

    t_out = IDFT(length, F)
    out2 = dict(sorted(t_out.items()))

    return out1, out2


def write_output_file(file_name, dict):
    with open(file_name, 'w') as file:
        file.write(f"0\n")
        file.write(f"0\n")
        file.write(f"{len(dict)}\n")

        for index in dict:
            file.write(f"{index} {round(float(dict[index]), 10)}\n")


def plot_filter(filter):

    plt.figure(figsize=(12, 6))
    plt.plot(filter.keys(), filter.values(), marker='o', color='#1d817e', label='Filter')
    plt.title('Filter')
    plt.xlabel('Time')
    plt.ylabel('Val')
    plt.grid()
    plt.show()


def plot_sig(t_out):

    plt.figure(figsize=(12, 7))
    plt.plot(t_out.keys(), t_out.values(), color='#1d817e', label='Filter')
    plt.title('Filtered Signal')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.grid()
    plt.show()


def test(case_num):
    root = 'PracticalTask/FIR test cases/'
    filters_paths = ['', 'Testcase 1/LPFCoefficients.txt', 'Testcase 2/ecg_low_pass_filtered.txt',
                     'Testcase 3/HPFCoefficients.txt', 'Testcase 4/ecg_high_pass_filtered.txt',
                     'Testcase 5/BPFCoefficients.txt', 'Testcase 6/ecg_band_pass_filtered.txt',
                     'Testcase 7/BSFCoefficients.txt', 'Testcase 8/ecg_band_stop_filtered.txt']
    return os.path.join(root, filters_paths[case_num])


def last_gui(frame):
    last_frame = frame

    label1 = tk.Label(last_frame, text="Signal :")
    label1.place(x=50, y=30)
    sig1_btn = tk.Button(last_frame, text="upload", command=lambda: upload_txt_file(signal_dict))
    sig1_btn.place(x=110, y=30)

    values = list(range(1, 9))
    label = tk.Label(last_frame, text="test case num :")
    label.place(x=200, y=30)
    case_num = ttk.Combobox(last_frame, values=values)
    case_num.set(1)
    case_num.place(x=300, y=30)

    label2 = tk.Label(last_frame, text="Filter Type :")
    label2.place(x=50, y=70)

    selected_filter = tk.StringVar(value='High Pass')

    add = tk.Radiobutton(last_frame, text='High Pass', variable=selected_filter, value='High Pass')
    add.place(x=70, y=90)

    sub = tk.Radiobutton(last_frame, text='Low Pass', variable=selected_filter, value='Low Pass')
    sub.place(x=70, y=120)

    label3 = tk.Label(last_frame, text="fc :")
    label3.place(x=200, y=105)
    fc = tk.Entry(last_frame, width=6, textvariable=tk.StringVar(value="0"))
    fc.place(x=260, y=105)

    sl = tk.Radiobutton(last_frame, text='Band Pass', variable=selected_filter, value='Band Pass')
    sl.place(x=70, y=150)

    sr = tk.Radiobutton(last_frame, text='Band Reject', variable=selected_filter, value='Band Reject')
    sr.place(x=70, y=180)

    label4 = tk.Label(last_frame, text="f1 :")
    label4.place(x=200, y=165)
    f1 = tk.Entry(last_frame, width=6, textvariable=tk.StringVar(value="0"))
    f1.place(x=230, y=165)

    label4 = tk.Label(last_frame, text="f2 :")
    label4.place(x=300, y=165)
    f2 = tk.Entry(last_frame, width=6, textvariable=tk.StringVar(value="0"))
    f2.place(x=330, y=165)

    label5 = tk.Label(last_frame, text="Fs :")
    label5.place(x=110, y=220)
    fs = tk.Entry(last_frame, width=6)
    fs.place(x=150, y=220)

    label6 = tk.Label(last_frame, text="stop attenuation :")
    label6.place(x=50, y=260)
    s_att = tk.Entry(last_frame, width=6)
    s_att.place(x=150, y=260)

    label7 = tk.Label(last_frame, text="transition band :")
    label7.place(x=50, y=300)
    delta_f = tk.Entry(last_frame, width=6)
    delta_f.place(x=150, y=300)

    output_btn = tk.Button(last_frame, text="Output",
                           command=lambda: design_filter(selected_filter.get(), int(fs.get()), int(fc.get()),
                                                         int(f1.get()), int(f2.get()), float(s_att.get()),
                                                         float(delta_f.get()), int(case_num.get())))
    output_btn.place(x=300, y=250)
