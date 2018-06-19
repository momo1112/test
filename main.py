import math
import time
import random
import matplotlib.pyplot as plt
import enumeration
import util
import divide
import test as enumer


def draw_scatter(points1, points2, title):
    ox = []
    oy = []
    x = []
    y = []
    for i in range(len(points1)):
        ox.append(points1[i][0])
        oy.append(points1[i][1])
    for i in range(len(points2)):
        x.append(points2[i][0])
        y.append(points2[i][1])
    plt.title(title)
    plt.xlim(xmax=100, xmin=0)
    plt.ylim(ymax=100, ymin=0)
    plt.scatter(ox, oy, color='b', marker='x', s=5)
    plt.scatter(x, y, color='r', marker='x', s=5)
    for i in range(0, len(points2)):
        if i == len(points2)-1:
            plt.plot([points2[len(points2)-1][0], points2[0][0]], [points2[len(points2)-1][1], points2[0][1]], color='r')
        else:
            plt.plot([points2[i][0], points2[i+1][0]], [points2[i][1], points2[i+1][1]], color='r')
    plt.show()


if __name__ == '__main__':
    test_data = []
    for i in range(100):
        x = round(random.uniform(0, 100), 2)
        y = round(random.uniform(0, 100), 2)
        # y = round(random.randint(0, 100))
        # x = round(random.randint(0, 100))
        test_data.append((x, y))
    test_data1 = test_data[:]
    test_data2 = test_data[:]
    test_data3 = test_data[:]
    convex_hull1 = enumeration.convex(test_data1)
    draw_scatter(test_data, convex_hull1, "enumeration")
    convex_hull2 = util.convex_hull(test_data2)
    draw_scatter(test_data, convex_hull2, "Graham Scan")
    convex_hull3 = divide.convex_hull(test_data3)
    draw_scatter(test_data, convex_hull3, "divide-conquer")