import os
import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from io import StringIO
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

cm = plt.get_cmap('rainbow')
read_path = "/tmp/cost_fifo.pipe"

def draw_cost_image(data):
    df = pd.read_csv(StringIO(data.decode('utf-8')), delimiter=";", header=None)
    df = df.dropna()
    df_collision = df[np.abs(df[3]) > 0.5]

    sc = plt.scatter(df[0], df[1], c=df[2], vmin=min(df[2]), vmax=max(df[2]), cmap=cm)
    print(df_collision)
    sc2 = plt.scatter(df_collision[0], df_collision[1], c='k', marker='^', s=50)
    plt.colorbar(sc)
    plt.xlabel("dis")
    plt.ylabel("vel")
    plt.draw()
    plt.pause(0.0001)
    plt.clf()


def show_cost():
    try:
        os.mkfifo(read_path)
    except OSError as e:
        print("Pipe error:", e)

    rf = os.open(read_path, os.O_RDONLY)
    plt.ion()
    while True:
        # try:
        data = os.read(rf, 4096)
        if len(data) == 0:
            print("No data!")
        else:
            # print(data)
            draw_cost_image(data)
        time.sleep(0.2)

show_cost()
