from tkinter import filedialog
from matplotlib import pyplot as plt


def upload_txt_file(signal_dict):
    signal_dict.clear()
    file_path = filedialog.askopenfilename(
        title="Select a Text File",
        filetypes=(("Text files", "*.txt"),)
    )

    if file_path:
        with open(file_path, 'r') as file:
            lines = file.readlines()

            N = int(lines[2].strip())
            for i in range(3, (N + 3)):
                line = lines[i].strip().split()
                index, value = int(line[0]), float(line[1])
                signal_dict[index] = value


def draw_signal(points):
    indexes = list(points.keys())
    values = list(points.values())
    plt.figure(figsize=(10, 6))
    plt.plot(indexes, values, marker='o', color='blue', label='Signal')
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.grid(True)
    plt.show()
