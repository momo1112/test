import random
import numpy as np
import matplotlib.pyplot as plt

#叉乘计算方法
def multiply(p1, p2, p0):
    return (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1])


#判断点和直线间的位置关系
def calculate(point1, point2, point3):
    result = point1[0]*point2[1]+point3[0]*point1[1]+point2[0]*point3[1]-point3[0]*point2[1]-point2[0]*point1[1]-point1[0]*point3[1]
    return result


def data(n):
    points = []
    for i in range(n):
        y = round(random.uniform(0, 100), 2)
        x = round(random.uniform(0, 100), 2)
        # y = round(random.randint(0, 100))
        # x = round(random.randint(0, 100))
        points.append((x, y))
    print(points)
    return points


def convex(points):
    con = set()
    for i in range(len(points)):
        for j in range(i, len(points)):
            num = 0
            for k in range(len(points)):
                if k == i or k == j:
                    continue
                if calculate(points[i], points[j], points[k]) > 0:
                    num += 1
            if num == len(points)-2 or num == 0:
                con.add(points[i])
                con.add(points[j])
            num = 0
            for k in range(len(points)):
                if k == i or k == j:
                    continue
                if calculate(points[i], points[j], points[k]) < 0:
                    num += 1
            if num == len(points)-2 or num == 0:
                con.add(points[i])
                con.add(points[j])
    return con


def sort_hull(points):
    x_min = 100
    x_max = 0
    point_x_min = []
    point_x_max = []
    for point in points:
        if point[0] < x_min:
            x_min = point[0]
            point_x_min = point
        if point[0] > x_max:
            x_max = point[0]
            point_x_max = point
    point_up = []
    point_down = []
    for i in range(0, len(points)):
        if multiply(points[i], point_x_max, point_x_min) > 0:
            point_down.append(points[i])
        else:
            point_up.append(points[i])
    hull_points = []
    for i in range(0, len(point_up)-1):
        for j in range(i+1, len(point_up)):
            if point_up[i][0] > point_up[j][0]:
                point_up[i], point_up[j] = point_up[j], point_up[i]
    for i in range(0, len(point_down)-1):
        for j in range(i+1, len(point_down)):
            if point_down[i][0] < point_down[j][0]:
                point_down[i], point_down[j] = point_down[j], point_down[i]
    hull_points = point_up+point_down
    return hull_points


def draw_scatter(points1, points2):
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
    plt.xlim(xmax=100, xmin=0)
    plt.ylim(ymax=100, ymin=0)
    plt.scatter(ox, oy, color='b', marker='x', s=5)
    plt.scatter(x, y, color='r', marker='x', s=5)
    hull_points = sort_hull(points2)
    print("after sort:")
    print(hull_points)
    for i in range(0, len(hull_points)):
        if i == len(hull_points)-1:
            plt.plot([hull_points[len(hull_points)-1][0], hull_points[0][0]], [hull_points[len(hull_points)-1][1], hull_points[0][1]], color='r')
        else:
            plt.plot([hull_points[i][0], hull_points[i+1][0]], [hull_points[i][1], hull_points[i+1][1]], color='r')
    plt.show()


if __name__ == '__main__':
    points = data(100)
    cons = list(convex(points))
    draw_scatter(points, cons)
    print(cons)
