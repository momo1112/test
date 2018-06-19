import math
import util
import random
import matplotlib.pyplot as plt
import time


def get_median(p):
    p.sort(key=lambda a: a[0])
    half = int(len(p)/2)
    median = (p[half][0]+p[~half][0])/2
    return median


#划分
def partition(arr, left, right):
    if left >= right:
        return left
    i = left
    j = right
    m = int((i+j)/2)
    pivot = arr[m][0]
    while i < j:
        while i < j and arr[i][0] < pivot:
            i += 1
        while i < j and arr[j][0] > pivot:
            j -= 1
        if i < j:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
            j -= 1
    if i == j and arr[j][0] > pivot:
        arr[i], arr[j-1] = arr[i], arr[j-1]
        j -= 1
    return j


#利用快排求第k个最小值
def k_median(arr, left, right, k):
    if left >= right:
        return arr[left]
    p = partition(arr, left, right)
    i = p-left+1
    if i < k:
        return k_median(arr, p+1, right, k-i)
    return k_median(arr, left, p, k)


#时间复杂度O(n)的取中位数
def get_on_median(data):
    if len(data) == 1:
        return data[0]
    if len(data) % 2 == 0:
        m = len(data) / 2
        point1 = k_median(data, 0, len(data) - 1, m)
        point2 = k_median(data, 0, len(data) - 1, m + 1)
        medi = round((point1[0] + point2[0]) / 2, 3)
    if len(data) % 2 == 1:
        m = (len(data) - 1) / 2
        point1 = k_median(data, 0, len(data) - 1, m)
        medi = point1[0]
    print("length: ", len(data))
    print("data", data)
    print("median: ", medi)
    return medi


#获取极角，通过求反正切得出，考虑pi / 2的情况
def get_arc(p1, p0):
    # 兼容sort_points_tan的考虑
    if (p1[1] - p0[1]) == 0:
        if (p1[0] - p0[0]) == 0:
            return -1
        else:
            return math.pi / 2
    tan = float((p1[0] - p0[0])) / float((p1[1] - p0[1]))
    arc = math.atan(tan)
    if arc <= 0:
        return -arc
    else:
        return math.pi - arc
    return -1


#右侧划分两个序列
def find_min_max_point(p0, p):
    min_arc = math.pi
    max_arc = 0.0
    min_p = 0
    max_p = 0
    for i in range(0, len(p)):
        arc = get_arc(p[i], p0)
        if arc >= max_arc:
            max_arc = arc
            max_p = i
        if arc <= min_arc:
            min_arc = arc
            min_p = i
    return min_p, max_p


#找到左边凸包的最左边的点
def find_point(p):
    min_x = 100
    min_point = []
    for i in range(len(p)):
        if p[i][0] < min_x:
            min_x = p[i][0]
            min_point = i
        if p[i][0] == min_x:
            if p[i][1] < p[min_point][1]:
                min_point = i
    return min_point


#左边凸包进行极角排序
def sort_points_tan(p, pk):
    p2 = []
    for i in range(len(p)):
        arc = get_arc(p[i], pk)
        p2.append({"index": i, "arc": arc})
    p2.sort(key=lambda s: s.get('arc', 0))
    p_out = []
    for i in range(0, len(p2)):
        p_out.append({"point": p[p2[i]["index"]], "arc": p2[i]["arc"]})
    return p_out


def merge_sort(p, q):
    res = []
    while p and q:
        if p[0]["arc"] > q[0]["arc"]:
            res.append(q.pop(0))
        else:
            res.append(p.pop(0))
    res = res + p + q
    return res


#处理右侧凸包，生成两个有序序列
def deal_right_hull(min_qr, max_qr, qr):
    ac_qr = []
    cw_qr = []
    cw_qr1 = []
    cw_qr2 = []
    if min_qr < max_qr:
        if max_qr < len(qr) - 1:
            ac_qr = qr[min_qr:max_qr+1]
            cw_qr2 = qr[max_qr + 1:]
            cw_qr2 = cw_qr2[::-1]
        else:
            ac_qr = qr[min_qr:]
            cw_qr2 = []
        if min_qr > 0:
            cw_qr1 = qr[0:min_qr]
            cw_qr1 = cw_qr1[::-1]
        else:
            cw_qr1 = []
        cw_qr = cw_qr1 + cw_qr2
    if min_qr > max_qr:
        tmp1 = qr[min_qr:]
        tmp2 = qr[0:max_qr+1]
        ac_qr = tmp1+tmp2
        cw_qr = qr[max_qr+1:min_qr]
        cw_qr = cw_qr[::-1]
    return ac_qr, cw_qr


def convex_hull(p):
    if len(p) <= 3:
        return util.convex_for_divide(p)
    pp = p[:]
    median = get_on_median(pp)
    # median = get_median(p)
    pl = []
    pr = []
    for point in p:
        if point[0] <= median:
            pl.append(point)
        else:
            pr.append(point)
    ql = convex_hull(pl)
    qr = convex_hull(pr)
    #在左边找到横坐标最小的点
    p0 = find_point(ql)
    # 把三个序列找到，然后合并凸包
    ql1 = sort_points_tan(ql, ql[p0])
    min_qr, max_qr = find_min_max_point(ql[p0], qr)
    ac_qr = []
    cw_qr = []
    ac_qr, cw_qr = deal_right_hull(min_qr, max_qr, qr)
    ac_qr = sort_points_tan(ac_qr, ql[p0])
    if cw_qr is not None:
        cw_qr = sort_points_tan(cw_qr, ql[p0])
    tmp = merge_sort(ql1, ac_qr)
    tmp = merge_sort(tmp, cw_qr)
    w = []
    for i in range(len(tmp)):
        w.append(tmp[i]["point"])
    return util.convex_for_divide(w)


if __name__ == '__main__':
    test_data = []
    ox = []
    oy = []
    for i in range(5000):
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        ox.append(x)
        oy.append(y)
        test_data.append((x, y))

    # dat = test_data[:]
    # k = k_median(test_data, 0, len(test_data)-1, 5)
    # l = k_median(test_data, 0, len(test_data)-1, 6)
    # me = get_median(dat)
    # print(test_data)
    # print("divide: ", float((k[0]+l[0])/2))
    # print("sort: ", me)

    print(test_data)
    start = time.clock()
    result = convex_hull(test_data)
    end = time.clock()
    print(result)
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
        if i == len(result) - 1:
            plt.plot([result[len(result) - 1][0], result[0][0]], [result[len(result) - 1][1], result[0][1]], color='r')
        else:
            plt.plot([result[i][0], result[i + 1][0]], [result[i][1], result[i + 1][1]], color='r')
    plt.show()
    print("used time: ", end - start)
