import os
import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from io import StringIO
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

## draw the shape of different planning step
# filenames = os.listdir("/home/cybernp/git/lanefollow/cmake-build-debug/text")
# filenames.sort(key=str.lower)
#
# cmap = plt.get_cmap('rainbow')
# colors = [cmap(i) for i in np.linspace(0, 1, len(filenames))]
#
# num = int(np.ceil(np.sqrt(len(filenames))))
#
# # for i, file in enumerate(filenames,start=0):
# #     df = pd.read_csv("/home/cybernp/git/lanefollow/cmake-build-debug/text/" + file, delimiter=";", header=None)
# #     plt.plot(df[0], df[1], linestyle='-', color=colors[i], label=file)
# plt.figure()
# i = 1
# for file in filenames:
#     plt.subplot(num, num, i)
#     df = pd.read_csv("/home/cybernp/git/lanefollow/cmake-build-debug/text/" + file, delimiter=";", header=None)
#     plt.plot(df[0], df[1], linestyle='-', color=colors[i-1], label=file)
#     i += 1
#     plt.legend()
#
# plt.show()


## draw all results in one step
# filenames = os.listdir("/home/cybernp/git/lanefollow/cmake-build-debug/text")
# filenames.sort(key=lambda x: os.path.getmtime("/home/cybernp/git/lanefollow/cmake-build-debug/text/"+x))
# new_filenames = filenames[-18:]
# new_filenames.sort(key=str.lower)
#
# cmap = plt.get_cmap('rainbow')
# colors = [cmap(i) for i in np.linspace(0, 1, len(new_filenames))]
#
# num = int(np.ceil(np.sqrt(len(new_filenames))))
#
# # for i, file in enumerate(filenames,start=0):
# #     df = pd.read_csv("/home/cybernp/git/lanefollow/cmake-build-debug/text/" + file, delimiter=";", header=None)
# #     plt.plot(df[0], df[1], linestyle='-', color=colors[i], label=file)
# plt.figure()
# i = 1
# for file in new_filenames:
#     plt.subplot(num, num, i)
#     df = pd.read_csv("/home/cybernp/git/lanefollow/cmake-build-debug/text/" + file, delimiter=";", header=None)
#     plt.plot(df[0], df[1], linestyle='-', color=colors[i-1], label=file)
#     i += 1
#     plt.legend()
#     plt.ylim([1130, 1160])
#
# plt.show()


## draw 3d scatter
# df = pd.read_csv("/home/cybernp/git/lanefollow/cmake-build-debug/cost.txt", delimiter=";", header=None)
# cmap = plt.get_cmap('rainbow')
# colors = [cmap(i) for i in np.linspace(0, 1, len(df))]
#
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# i = 0
# for i in range(len(df)):
#     data = df.loc[i]
#     xs = data[0]
#     ys = data[1]
#     zs = data[4]
#     ax.scatter(xs, ys, zs, c=colors[i], marker='o')
#     i += 1
#
# ax.set_xlabel('dis')
# ax.set_ylabel('vel')
# ax.set_zlabel('cost')
# plt.show()

read_path = "/tmp/cost_fifo.pipe"

cm = plt.get_cmap('rainbow')
def draw_cost_image(data):
    df = pd.read_csv(StringIO(data.decode('utf-8')), delimiter=";", header=None)
    df_collision = df[np.abs(df[3]) > 500]

    sc = plt.scatter(df[0], df[1], c=df[2], vmin=min(df[2]), vmax=max(df[2]), cmap=cm)
    print(df_collision)
    sc2 = plt.scatter(df_collision[0], df_collision[1], c='r', marker='^', s=3)
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
        # print("running")
        # except:
        #     plt.ioff()
        #     os.close(rf)
        #     break


read_car_path = "/tmp/car_fifo.pipe"


def draw_predict_image(data):
    df = pd.read_csv(StringIO(data.decode('utf-8')), delimiter=";", header=None)
    df = df.dropna()
    if len(df) < 1:
        return
    print(df)

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
            draw_predict_image(data)
        time.sleep(0.2)

show_predict()