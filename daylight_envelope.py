# -*- coding: utf-8 -*-
# @Time        : 2023/12/17 21:43
# @Author      : husky
# @FileName    : daylight_envelope.py
# @Software    : PyCharm
# @ProjectName : pythonProject
# @Email       : shiguihuang1874@qq.com

from email.mime import image
import numpy as np
import matplotlib.pyplot as plt

dip_d = 90
dip = 20


# get_r_max(dip_d, dip)

# 定义一个函数，根据倾向和倾角绘制出daylight_envelope曲线，并返回x_array和y_array数组，用于判断点是否在该曲边形内
def draw_daylight(dip_d, dip):
    """根据边坡的倾向和倾角绘制daylight_envelope曲线

    Args:
        dip_d (float): 倾向
        dip (float): 倾角
    """
    # 定义初始变量
    # r_array = [i/10 for i in range(1801)]
    r_array = np.linspace(0, 180, 180)
    print(len(r_array))
    # 将初始变量由角度值转换为弧度值
    r_array_rad = [r_array[i] / 180 * np.pi for i in range(len(r_array))]
    dip_d_rad = dip_d / 180 * np.pi
    dip_rad = dip / 180 * np.pi

    # 定义需要的变量
    x_e_array = []
    y_e_array = []

    # 记录一个r等于30的x, y，用于绘制点
    degree_judge = 30
    rad_judge = 30 / 180 * np.pi
    x_point_array = []
    y_point_array = []

    # 按照循环进行绘制
    for i in range(len(r_array_rad)):
        r = r_array_rad[i]
        a = np.sin(dip_rad) * np.sin(r)
        b = np.sqrt(1 - np.sin(dip_rad) ** 2 * np.sin(r) ** 2)
        c = 1 + np.sqrt(1 - np.sin(dip_rad) ** 2 * np.sin(r) ** 2)
        k = (a / b) * np.sqrt(1 / c)
        x_e = k * np.cos(dip_rad) * np.sin(r)
        y_e = k * np.cos(r)

        # 计算需要旋转的角度theta
        theta = (90 - dip_d) / 180 * np.pi

        # 重新计算旋转后x_e, y_e
        x_e_route = np.cos(theta) * x_e + np.sin(theta) * y_e
        y_e_route = np.sin(theta) * x_e + np.cos(theta) * y_e

        if i % 10 == 0:
            x_point_array.append(x_e_route)
            y_point_array.append(y_e_route)

        x_e_array.append(x_e_route)
        y_e_array.append(y_e_route)

    # 新建画布，该部分在后面程序中应为在原来的画布中增加
    fig = plt.figure(figsize=(10, 10))
    ax_1 = fig.add_subplot(111)

    # 设置x, y的比例为1
    ax_1.set_aspect(1)
    ax_1.set_xlim(-1.1, 1.1)
    ax_1.set_ylim(-1.1, 1.1)
    print("x_e_max:", str(max(x_e_array)))
    print("y_e_max:", str(max(y_e_array)))
    ax_1.plot(x_e_array, y_e_array)
    # ax_1.scatter(-0.5, 0.8153931399438756, marker='*')
    ax_1.scatter(x_point_array, y_point_array, marker=".")

    # 绘制一个圆
    theta = np.linspace(0, 2 * np.pi, 360)
    x_circle = np.cos(theta)
    y_circle = np.sin(theta)
    ax_1.plot(x_circle, y_circle)
    # ax_1.text(-1.1,1.1, str(dip_array[j]))
    plt.show()
    plt.savefig("daylight_envelope.pdf", format="pdf")


dip_d_array = [270]
dip_array = [45]
for i in range(len(dip_d_array)):
    for j in range(len(dip_array)):
        dip_d = dip_d_array[i]
        dip = dip_array[j]
        draw_daylight(dip_d, dip)
