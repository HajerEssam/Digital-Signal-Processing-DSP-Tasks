from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk


def generate_signal(typeOfSignal, amplitude, theta, f, fs, duration=1):
    t = np.arange(0, duration, 1 / fs)

    if typeOfSignal == "sinusoidal":
        signal = amplitude * np.sin(2 * np.pi * f * t + theta)

    elif typeOfSignal == "cosinusoidal":
        signal = amplitude * np.cos(2 * np.pi * f * t + theta)
    else:
        return None, "invalid signal type"

    return t, signal


def plot_signals(t_cont, signal_cont, t_discrete, signal_discrete):
    plt.figure(figsize=(12, 10))

    plt.plot(t_cont, signal_cont, label='Continuous Signal', color='blue')
    plt.stem(t_discrete, signal_discrete, linefmt='orange', markerfmt='o', basefmt='--', label='Discrete Signal')

    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    plt.title("Continuous Signal")
    plt.title("Discrete Signal")
    plt.show()


def draw_signals():
    if sine_var.get() == 0 and cosine_var.get() == 0:
        messagebox.showwarning("Warning", "Please select at least one signal type.")
        return

    try:
        amplitude = float(amplitude_entry.get())
        theta = float(theta_entry.get())
        f = float(f_entry.get())
        fs = float(fs_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values.")
        return

    if fs < 2 * f:
        messagebox.showerror("Error", "Sampling frequency must be at least 2 times the analog frequency.")

    t_cont = None
    t_discrete = None

    signal_cont = None
    signal_discrete = None

    if sine_var.get() == 1:
        t_cont, signal_cont = generate_signal('sinusoidal', amplitude, theta, f, 1000)
        t_discrete, signal_discrete = generate_signal('sinusoidal', amplitude, theta, f, fs)

    elif cosine_var.get() == 1:
        t_cont, signal_cont = generate_signal('cosinusoidal', amplitude, theta, f, 1000)
        t_discrete, signal_discrete = generate_signal('cosinusoidal', amplitude, theta, f, fs)

    plot_signals(t_cont, signal_cont, t_discrete, signal_discrete)


def task2_gui(frame):
    global task2_frame
    task2_frame = frame

    tk.Label(task2_frame, text="Amplitude:").grid(row=0, column=0, padx=10, pady=5)
    global amplitude_entry
    amplitude_entry = tk.Entry(task2_frame)
    amplitude_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(task2_frame, text="Theta (phase shift):").grid(row=1, column=0, padx=10, pady=5)
    global theta_entry
    theta_entry = tk.Entry(task2_frame)
    theta_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(task2_frame, text="Analog Frequency (f):").grid(row=2, column=0, padx=10, pady=5)
    global f_entry
    f_entry = tk.Entry(task2_frame)
    f_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(task2_frame, text="Sampling Frequency (fs):").grid(row=3, column=0, padx=10, pady=5)
    global fs_entry
    fs_entry = tk.Entry(task2_frame)
    fs_entry.grid(row=3, column=1, padx=10, pady=5)

    global sine_var, cosine_var
    sine_var = tk.IntVar()
    cosine_var = tk.IntVar()

    tk.Checkbutton(task2_frame, text="Sine Wave", variable=sine_var).grid(row=4, column=0, padx=10, pady=5)
    tk.Checkbutton(task2_frame, text="Cosine Wave", variable=cosine_var).grid(row=4, column=1, padx=10, pady=5)

    draw_btn = tk.Button(task2_frame, text="Draw Signal", command=draw_signals)
    draw_btn.grid(row=5, column=0, columnspan=2, pady=20)