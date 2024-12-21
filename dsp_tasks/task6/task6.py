import numpy as np
from tkinter import filedialog
from matplotlib import pyplot as plt
from dsp_tasks.task6.signalcompare import *
from dsp_tasks.common_functions import draw_signal
import tkinter as tk


def select_info_source():
    global file_path
    file_path = filedialog.askopenfilename(
        title="Select a Text File",
        filetypes=(("Text files", "*.txt"),)
    )


def upload_signal(file_path):
    input_signal_dict = {}
    if file_path:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            N = int(lines[2].strip())
            for i in range(3, (N + 3)):
                line = lines[i].strip().split()
                v1 = line[0].replace('f', '')
                v1 = float(v1)
                v2 = line[1].replace('f', '')
                v2 = float(v2)
                input_signal_dict[v1] = v2
    return input_signal_dict


def DFT(N, input_signal_dict):
    min_index = min(input_signal_dict.keys())
    index_shift = 0
    shifted_signal_dict = {}

    if min_index < 0:
        index_shift = -min_index
        for idx in input_signal_dict:
            shifted_signal_dict[idx + index_shift] = input_signal_dict[idx]
    else:
        shifted_signal_dict = input_signal_dict

    dft_signal_dict = {}

    for k in range(N):
        dft_signal_dict[k] = 0
        for n in range(N):
            dft_signal_dict[k] += shifted_signal_dict[n] * np.exp(-2j * np.pi * k * n / N)

    if min_index < 0:
        final_dft_output = {}
        for k in dft_signal_dict:
            final_dft_output[k - index_shift] = dft_signal_dict[k]
    else:
        final_dft_output = dft_signal_dict

    return final_dft_output


def IDFT(N, input_signal_dict):
    min_index = min(input_signal_dict.keys())
    index_shift = 0
    shifted_signal_dict = {}

    if min_index < 0:
        index_shift = -min_index
        for idx in input_signal_dict:
            shifted_signal_dict[idx + index_shift] = input_signal_dict[idx]
    else:
        shifted_signal_dict = input_signal_dict

    idft_signal_dict = {}
    real_output = {}

    for n in range(N):
        idft_signal_dict[n] = 0
        for k in range(N):
            if k in shifted_signal_dict:
                idft_signal_dict[n] += shifted_signal_dict[k] * np.exp(2j * np.pi * k * n / N)
        idft_signal_dict[n] /= N
        real_output[n] = np.real(idft_signal_dict[n])

    if min_index < 0:
        final_output = {}
        for idx in real_output:
            final_output[idx - index_shift] = real_output[idx]
    else:
        final_output = real_output

    return final_output


def DFT_IDFT(op, N, file_path):
    if op == 'DFT':
        input_signal_dict = upload_signal(file_path)
        dft_signal_dict = DFT(N, input_signal_dict)
        a, ph_shift = calc_amplitude_phase_shift(dft_signal_dict)
        freq = calc_freq_points(N)
        write_output_file('task6/Output_Sig', a, ph_shift, op)
        print(dft_signal_dict)
        validate_DFT_output(a, ph_shift)
        plot_signal_info(freq, a, ph_shift)

    else:
        magnitude, phase = ReadSignalFile(file_path)
        x = {}
        i = 0
        for mag, ph in zip(magnitude, phase):
            if i < len(magnitude):
                x[i] = mag * np.exp(1j * ph)
                i += 1

        idft_signal_dict = IDFT(N, x)
        for key, value in idft_signal_dict.items():
            idft_signal_dict[key] = round(value)
        keys_list = list(idft_signal_dict.keys())
        values_list = list(idft_signal_dict.values())
        write_output_file('task6/Output2_Sig', keys_list, values_list, op)
        print(idft_signal_dict)
        validate_IDFT_output(values_list)
        draw_signal(idft_signal_dict)


def calc_amplitude_phase_shift(output_signal_dict):
    amplitude = []
    phase_shift = []
    for i in range(len(output_signal_dict)):
        amplitude.append(round(np.sqrt(output_signal_dict[i].real ** 2 + output_signal_dict[i].imag ** 2), 13))
        phase_shift.append(round(np.arctan2(output_signal_dict[i].imag, output_signal_dict[i].real), 13))
    return amplitude, phase_shift


def calc_freq_points(N):
    freq = []
    step = (2 * np.pi) / (N * (1 / N))
    for point in range(N):
        freq.append(step + (point * step))
    return freq


def write_output_file(file_name, inf1, inf2, op):
    with open(file_name, 'w') as file:
        if op == 'IDFT':
            file.write(f"0\n")
            file.write(f"0\n")
            file.write(f"{len(inf1)}\n")
            for v1, v2 in zip(inf1, inf2):
                file.write(f"{v1} {v2}\n")
        else:
            file.write(f"1\n")
            file.write(f"0\n")
            file.write(f"{len(inf1)}\n")
            for v1, v2 in zip(inf1, inf2):
                v1_formatted = f"{int(v1)}" if v1.is_integer() else f"{v1}f"
                v2_formatted = f"{int(v2)}" if v2.is_integer() else f"{v2}f"
                file.write(f"{v1_formatted} {v2_formatted}\n")


def plot_signal_info(freq, amplitude, phase_shift):
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    axes[0].stem(freq, amplitude, linefmt='orange', markerfmt='o', basefmt='--', label='Amplitude')
    axes[0].set_title('Amplitude vs Frequency')
    axes[0].set_xlabel('Frequency (Hz)')
    axes[0].set_ylabel('Amplitude')
    axes[0].legend()
    axes[0].grid(True)

    axes[1].stem(freq, phase_shift, linefmt='blue', markerfmt='o', basefmt='--', label='Phase Shift')
    axes[1].set_title('Phase Shift vs Frequency')
    axes[1].set_xlabel('Frequency (Hz)')
    axes[1].set_ylabel('Phase Shift (radians)')
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()


def validate_DFT_output(calculated_amplitude, calculated_phase_shift):
    true_amplitude, true_phase_shift = ReadSignalFile('task6/Output_Signal_DFT_A,Phase.txt')
    valid_amplitude = SignalComapreAmplitude(true_amplitude, calculated_amplitude)
    valid_phase_shift = SignalComaprePhaseShift(true_phase_shift, calculated_phase_shift)
    print("test case passed SUCCESSFULLY!!") if valid_amplitude and valid_phase_shift else print("test case Failed")


def validate_IDFT_output(calculated_amplitude):
    _, true_amplitude = ReadSignalFile('task6/Output_Signal_IDFT.txt')
    valid_amplitude = SignalComapreAmplitude(true_amplitude, calculated_amplitude)
    print("test case passed SUCCESSFULLY!!") if valid_amplitude else print("test case Failed")


def task6_gui(frame):
    task6_frame = frame
    global file_path
    label1 = tk.Label(task6_frame, text="Signal :")
    label1.place(x=50, y=60)
    sig_btn = tk.Button(task6_frame, text="upload", command=lambda: select_info_source())
    sig_btn.place(x=100, y=60)

    label2 = tk.Label(task6_frame, text="Fs :")
    label2.place(x=190, y=60)
    N = tk.Entry(task6_frame, width=5)
    N.place(x=220, y=60)

    label3 = tk.Label(task6_frame, text="Operation :")
    label3.place(x=50, y=110)

    op = tk.StringVar(value='DFT')
    dft = tk.Radiobutton(task6_frame, text='DFT', variable=op, value='DFT')
    dft.place(x=80, y=150)

    idft = tk.Radiobutton(task6_frame, text='IDFT', variable=op, value='IDFT')
    idft.place(x=220, y=150)

    btn = tk.Button(task6_frame, text="Apply Derivative",
                    command=lambda: DFT_IDFT(op.get(), int(N.get()), file_path))
    btn.place(x=300, y=200)
