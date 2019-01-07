import os
import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from io import StringIO
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

cm = plt.get_cmap('rainbow')

read_car_path = "/tmp/car_fifo.pipe"


def draw_predict_image(data):
    df = pd.read_csv(StringIO(data.decode('utf-8')), delimiter=";", header=None)
    df = df.dropna()
    if len(df) < 1:
        return
    # print(df)

    ax = plt.gca()
    ts = np.arange(0, 8, 0.5)
    colors = [cm(i) for i in np.linspace(0, 1, len(df))]
    colors[0] = (0.0, 0.0, 0.0, 1.0)

    alphas = np.linspace(1, 0.1, len(ts))
    for i in range(len(df)):
        car_s = df.loc[i][0]
        car_s_dot = df.loc[i][1]
        car_d = df.loc[i][3]
        car_d_dot = df.loc[i][4]
        car_half_width = df.loc[i][6]
        car_half_length = df.loc[i][7]
        for t, a in zip(ts, alphas):
            ax.add_patch(patches.Rectangle((-car_d-car_d_dot*t, car_s+car_s_dot*t),
                                           car_half_width*2, car_half_length*2,
                                           color=colors[i], fill=False, alpha=a))

    plt.xlabel("d")
    plt.ylabel("s")
    plt.xlim([-12, 12])
    plt.ylim([df.loc[0][0], df.loc[0][0]+100])
    plt.draw()
    plt.pause(0.0001)
    plt.clf()

def draw_predict_image_new(data):
    df = pd.read_csv(StringIO(data.decode('utf-8')), delimiter=";", header=None)
    df = df.dropna()
    if len(df) < 1:
        return
    # print(df)

    ax = plt.gca()
    ts = np.arange(0, 8, 0.5)
    colors = [cm(i) for i in np.linspace(0, 1, len(df))]
    colors[0] = (0.0, 0.0, 0.0, 1.0)

    for t in ts:
        loc_buf = []
        for i in range(len(df)):
            car_s = df.loc[i][0]
            car_s_dot = df.loc[i][1]
            car_d = df.loc[i][3]
            car_d_dot = df.loc[i][4]
            car_half_width = df.loc[i][6]
            car_half_length = df.loc[i][7]
            center = (-car_d - car_d_dot * t, car_s + car_s_dot * t)
            distance = [np.linalg.norm(center - buf_center ) for buf_center in loc_buf]
            loc_buf.append(np.array(center))
            if len(distance) != 0 and min(distance) < 5.0:
                ax.add_patch(patches.Rectangle(center,
                    car_half_width * 2, car_half_length * 2,
                    color=colors[i], fill=True, alpha=1.0))
            else:
                ax.add_patch(patches.Rectangle(center,
                   car_half_width * 2, car_half_length * 2,
                   color=colors[i], fill=False, alpha=0.05))

    plt.xlabel("d")
    plt.ylabel("s")
    plt.xlim([-12, 16])
    plt.ylim([df.loc[0][0]-50, df.loc[0][0]+150])
    plt.draw()
    plt.pause(0.0001)
    plt.clf()

def show_predict():
    try:
        os.mkfifo(read_car_path)
    except OSError as e:
        print("Pipe error:", e)

    rf = os.open(read_car_path, os.O_RDONLY)
    plt.ion()
    while True:
        data = os.read(rf, 4096)
        if len(data) == 0:
            print("No data!")
        else:
            # print(data)
            draw_predict_image_new(data)
        time.sleep(0.2)

show_predict()