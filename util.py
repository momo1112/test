#-*- coding:utf-8 -*-
'''
凸包问题是指在n个点中，寻找一个凸多边形，使所有的点在凸多边形的边界或者内部。这是一个很有意思的计算机图形学问题，一种常用的解法是Graham扫描法，运行时间为O(nlgn)。
维基百科地址：https://en.wikipedia.org/wiki/Graham_scan
笔者拿processing语言对整个算法过程进行了模拟，上动态图：
![processing语言模拟Graham扫描法]("模拟Graham扫描法")
注意processing拿左上为(0,0)原点，与一般数学的原点位置不同。
从动态图上可以看出整个算法分三个部分：
**1、寻找y轴最小的点，如果y轴位置是相同的，那个找x轴位置最小的，称之为基准点。**
**2、计算1中找到基准点与其他点的极角（即过此2点的直线与x轴正方向的夹角，代码中以弧度表示），将这些点按极角的大小正序排列。**
**3、进行基准点与2中点的连线迭代，对新连线的点计算其是否符合凸多边形的定义，如果不满足舍弃此点。判断的方法是计算三点组成线段的叉乘，值为正表示满足条件。**
叉乘维基百科地址：https://zh.wikipedia.org/zh-cn/%E5%90%91%E9%87%8F%E7%A7%AF
'''

import sys
##sys.path.append(".")
##sys.path.append("..")
##sys.path.append("../..")
import math
import time
import random
import matplotlib.pyplot as plt

#获取基准点的下标
def get_leftbottompoint(p):
    k = 0
    for i in range(1, len(p)):
        if p[i][1] < p[k][1] or (p[i][1] == p[k][1] and p[i][0] < p[k][0]):
            k = i
    return k

#获取最左边的点
def get_left_point(p):
    k = 0
    for i in range(1, len(p)):
        if p[i][0] < p[k][0] or (p[i][0] == p[k][0] and p[i][1] < p[k][1]):
            k = i
    return k


#叉乘计算方法
def multiply(p1, p2, p0):
    return (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1])


#获取极角，通过求反正切得出，考虑pi / 2的情况
def get_arc(p1, p0):
    # 兼容sort_points_tan的考虑
    if (p1[0] - p0[0]) == 0:
        if (p1[1] - p0[1]) == 0:
            return -1
        else:
            return math.pi / 2
    tan = float((p1[1] - p0[1])) / float((p1[0] - p0[0]))
    arc = math.atan(tan)
    if arc >= 0:
        return arc
    else:
        return math.pi + arc
    return -1


#求两点之间的欧氏距离
def get_dis(p0, p1):
    dis = math.sqrt(math.pow(p0[0] - p1[0], 2) + math.pow(p0[1] - p1[1], 2))
    return dis


#对极角进行排序
def sort_points_tan(p, k):
    p2 = []
    for i in range(0, len(p)):
        distance = get_dis(p[i], p[k])
        arc = get_arc(p[i], p[k])
        p2.append({"index": i, "arc": arc, "dis": distance})
    p2.sort(key=lambda s: s.get('arc', 0))
    #去除极角相同但是距离小的点
    tmp = 0.0
    dis = 0.0
    p3 = []
    p3.append(p2[0])
    for i in range(1, len(p2)):
        if i > 0 and p2[i]["arc"] == tmp:
            if p2[i]["dis"] > dis:
                p3.pop()
                p3.append(p2[i])
        else:
            p3.append(p2[i])
        tmp = p2[i]["arc"]
        dis = p2[i]["dis"]
    p_out = []
    for i in range(0, len(p3)):
        p_out.append(p[p3[i]["index"]])
    return p_out


def convex_hull(p):
    p = list(set(p))
    #获取极坐标的原点
    k = get_leftbottompoint(p)
    p_sort = sort_points_tan(p, k)
    p_result = [None] * len(p_sort)
    p_result[0] = p_sort[0]
    p_result[1] = p_sort[1]
    p_result[2] = p_sort[2]
    top = 2
    for i in range(3, len(p_sort)):
        #叉乘为正则符合条件，如果大于零，新点在栈顶点的右侧，弹出栈顶元素
        while top >= 1 and multiply(p_sort[i], p_result[top], p_result[top - 1]) > 0:
            top -= 1
            p_result.pop()
        top += 1
        p_result[top] = p_sort[i]

    for i in range(len(p_result) - 1, -1, -1):
        if p_result[i] is None:
            p_result.pop()

    return p_result


def convex_for_divide(p_sort):
    tmp = p_sort[:]
    #针对三个点
    if len(p_sort) <=1:
        return tmp
    if len(p_sort) <= 3:
        k = get_left_point(p_sort)
        p = []
        p.append(p_sort[k])
        if len(p_sort) == 2:
            for i in range(len(p_sort)):
                if i != k:
                    p.append(p_sort[i])
        if len(p_sort) == 3:
            t = []
            for i in range(len(p_sort)):
                if i != k:
                    t.append(p_sort[i])
            if multiply(t[0], t[1], p_sort[k]) > 0:
                p.append(t[0])
                p.append(t[1])
            elif multiply(t[0], t[1], p_sort[k]) < 0:
                p.append(t[1])
                p.append(t[0])
            elif multiply(t[0], t[1], p_sort[k]) == 0:
                if t[0][0] > t[1][0]:
                    p.append(t[0])
                elif t[0][0] < t[1][0]:
                    p.append(t[1])
                else:
                    if t[0][1] > t[1][1]:
                        p.append(t[0])
                    elif t[0][1] < t[1][1]:
                        p.append(t[1])
                    else:
                        if t[0] != p_sort[k]:
                            p.append(t[0])
        return p
        # for i in range(len(tmp)-1):
        #     for j in range(len(tmp)):
        #         if multiply(tmp[j], tmp[i], tmp[k]) > 0:
        #             tmp[j], tmp[i] = tmp[i], tmp[j]
        # return tmp
    p_result = [None] * len(p_sort)
    p_result[0] = p_sort[0]
    p_result[1] = p_sort[1]
    p_result[2] = p_sort[2]
    top = 2
    for i in range(3, len(p_sort)):
        # 叉乘为正则符合条件，如果大于零，新点在栈顶点的右侧，弹出栈顶元素
        while top >= 1 and multiply(p_sort[i], p_result[top], p_result[top - 1]) > 0:
            top -= 1
            p_result.pop()
        top += 1
        p_result[top] = p_sort[i]

    for i in range(len(p_result) - 1, -1, -1):
        if p_result[i] is None:
            p_result.pop()

    return p_result


if __name__ == '__main__':
    test_data = []
    ox = []
    oy = []
    for i in range(5000):
        # x = round(random.uniform(0, 100), 2)
        # y = round(random.uniform(0, 100), 2)
        y = round(random.randint(0, 100))
        x = round(random.randint(0, 100))
        ox.append(x)
        oy.append(y)
        test_data.append((x, y))
    print(test_data)
    start = time.clock()
    result = convex_hull(test_data)
    end = time.clock()
    x = []
    y = []
    for i in range(len(result)):
        x.append(result[i][0])
        y.append(result[i][1])
    plt.xlim(xmax=100, xmin=0)
    plt.ylim(ymax=100, ymin=0)
    plt.scatter(ox, oy, color='b', marker='x', s=5)
    plt.scatter(x, y, color='r', marker='x', s=5)
    for i in range(0, len(result)):
        if i == len(result)-1:
            plt.plot([result[len(result)-1][0], result[0][0]], [result[len(result)-1][1], result[0][1]], color='r')
        else:
            plt.plot([result[i][0], result[i+1][0]], [result[i][1], result[i+1][1]], color='r')

    plt.show()
    print(result)
    print("running time: ", end - start)
