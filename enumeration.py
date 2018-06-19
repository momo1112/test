import random
import numpy as np
import matplotlib.pyplot as plt
import math
from operator import itemgetter
import time


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
        # y = round(random.uniform(0, 100), 2)
        # x = round(random.uniform(0, 100), 2)
        y = round(random.randint(0, 100))
        x = round(random.randint(0, 100))
        points.append((x, y))
    print(points)
    return points


# 去掉重复点
def remove_same(points):
    remove_number = []
    for i in range(0, len(points)):
        for j in range(i+1, len(points)):
            if points[i] == points[j]:
                remove_number.append(i)
    remove_number.reverse()
    for number in remove_number:
        points.remove(points[number])
    return points

#共线时找到中间的点
def middle_point(point1, point2, point3):
    p = []
    p.append(point1)
    p.append(point2)
    p.append(point3)
    for i in range(len(p)-1):
        for j in range(i+1, len(p)):
            if p[i][0]+p[i][1] > p[j][0]+p[j][1]:
                p[i], p[j] = p[j], p[i]
    return p[1]


def convex(points):
    points = remove_same(points)
    flag = [False] * len(points)
    con = set()
    for i in range(0, len(points)):
        if flag[i]:
            continue
        for j in range(i + 1, len(points)):
            if flag[j]:
                continue
            num = 0
            common_line_point = []
            middle_flag = False
            middle_index = 0
            for k in range(0, len(points)):
                if k == i or k == j:
                    continue
                if calculate(points[i], points[j], points[k]) > 0:
                    num += 1
                if calculate(points[i], points[j], points[k]) == 0:
                    common_line_point.append(k)
                    m_p = middle_point(points[i], points[j], points[k])
                    if m_p == points[k]:
                        flag[k] = True
                    else:
                        middle_flag = True
                        if m_p == points[i]:
                            middle_index = i
                        else:
                            middle_index = j
            if num == 0 or num == len(points) - 2 - len(common_line_point):
                if middle_flag:
                    if middle_index == i:
                        flag[i] = True
                        con.add(points[j])
                    else:
                        flag[j] = True
                        con.add(points[i])
                else:
                    con.add(points[i])
                    con.add(points[j])
                for point in common_line_point:
                    if not flag[point]:
                        con.add(points[point])
    for i in range(len(points)):
        if flag[i] and points[i] in con:
            con.remove(points[i])
    con = angle_sort_hull(list(con))
    return con


def sort_hull(points):
    x_min = 100
    x_max = 0
    point_x_min = points[0]
    point_x_max = points[0]
    for point in points:
        if point[0] < x_min:
            x_min = point[0]
            point_x_min = point
        elif point[0] == x_min and point[1] <= point_x_min[1]:
            x_min = point[0]
            point_x_min = point
        if point[0] > x_max:
            x_max = point[0]
            point_x_max = point
        elif point[0] == x_max and point[1] >= point_x_max[1]:
            x_max = point[0]
            point_x_max = point
    print("min_p: ", point_x_min)
    print("max_p: ", point_x_max)
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
            elif point_up[i][0] == point_up[j][0] and point_up[i][1] >= point_up[j][1]:
                point_up[i], point_up[j] = point_up[j], point_up[i]
    for i in range(0, len(point_down)-1):
        for j in range(i+1, len(point_down)):
            if point_down[i][0] < point_down[j][0]:
                point_down[i], point_down[j] = point_down[j], point_down[i]
            elif point_up[i][0] == point_up[j][0] and point_up[i][1] >= point_up[j][1]:
                point_down[i], point_down[j] = point_down[j], point_down[i]
    hull_points = point_up+point_down
    return hull_points


# 根据角度排序
def angle_sort_hull(points):
    sorted_points = sorted(points, key=itemgetter(0))
    x_center = (sorted_points[0][0] + sorted_points[len(points)-1][0])/2.0
    sorted_points = sorted(points, key=itemgetter(1))
    y_center = (sorted_points[0][1] + sorted_points[len(points)-1][1])/2.0
    point_right = []
    point_left = []
    for point in points:
        if point[0] >= x_center:
            point_right.append(point)
        else:
            point_left.append(point)
    point_r_cor = []
    point_l_cor = []
    for i in range(len(point_left)):
        point_l_cor.append((i, corner(point_left[i], (x_center, y_center))))
    for i in range(len(point_right)):
        point_r_cor.append((i, corner(point_right[i], (x_center, y_center))))
    sorted_r_cor = sorted(point_r_cor, key=itemgetter(1))
    sorted_l_cor = sorted(point_l_cor, key=itemgetter(1), reverse=True)
    hull_points = []
    for p in sorted_r_cor:
        hull_points.append(point_right[p[0]])
    for p in sorted_l_cor:
        hull_points.append(point_left[p[0]])
    return hull_points


# 计算sin值
def corner(point, center):
    x = point[0] - center[0]
    y = point[1] - center[1]
    l = math.sqrt(x**2 + y**2)
    return y/float(l)


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
    for i in range(0, len(points2)):
        if i == len(points2)-1:
            plt.plot([points2[len(points2)-1][0], points2[0][0]], [points2[len(points2)-1][1], points2[0][1]], color='r')
        else:
            plt.plot([points2[i][0], points2[i+1][0]], [points2[i][1], points2[i+1][1]], color='r')
    plt.show()


if __name__ == '__main__':
    points = data(5000)
    start = time.clock()
    cons = list(convex(points))
    end = time.clock()
    draw_scatter(points, cons)
    print(cons)
    print("running time: ", end-start)
