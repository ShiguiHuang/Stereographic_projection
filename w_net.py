# -*- coding: utf-8 -*-
# @Time : 2023/3/4 20:37
# @Author : husky
# @FileName: w_net.py
# @Software: PyCharm
# @ProjectName: SlopeAnalysis

import math
from pickletools import markobject
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.patches import Arc
from matplotlib.lines import Line2D
from matplotlib.path import Path
from matplotlib.patches import PathPatch

import numpy as np

fig = plt.figure(figsize=(10, 10))
ax_ = fig.add_subplot(111)
ax_.set_aspect(1)
# 绘制基圆
angle = np.linspace(0, 2 * np.pi, 1000)
x_base = np.cos(angle)
y_base = np.sin(angle)
ax_.plot(x_base, y_base, color="#1f77b4")
ax_.plot(0, 0, marker="+")
ax_.set_xlim(-1.1, 1.1)
ax_.set_ylim(-1.1, 1.1)

# team_logo = Image.open("../res/ui_file/team_logo.png")
# ax_.imshow(team_logo, extent=(0.71, 1, 0.71, 1), zorder=5)


# # 假设倾角等于45°, 倾向为0
# dip = 90
# dip_d = 90

# 绘制经线
def draw_longitude():
    dip_array = [i for i in range(0, 91, 10)]
    dip_d_array = [90, 270]

    count = 0

    for dip in dip_array:
        for dip_d in dip_d_array:
            dip_d_rad = math.radians(dip_d)
            dip_rad = math.radians(dip)

            center_ = (0, np.sin(dip_rad) / np.cos(dip_rad))
            r_of_joint = 1 / np.cos(dip_rad)

            # 当倾向变化后
            center_late = (np.cos(dip_d_rad) * center_[0] + np.sin(dip_d_rad) * center_[1],
                           -np.sin(dip_d_rad) * center_[0] + np.cos(dip_d_rad) * center_[1])

            # 起始角度
            theta_1 = 90 + dip
            theta_2 = 270 - dip
            # 绘制圆心
            # ax_.scatter(center_[0], center_[1], marker="+")
            # ax_.scatter(center_late[0], center_late[1], marker="+")

            # 绘制投影圆弧
            if dip == 90:
                count += 1
                if count == 2:
                    continue
                arc_joint = Line2D([np.sin(math.radians(dip_d - 90)),
                                    np.sin(math.radians(dip_d + 90))],
                                   [np.cos(math.radians(dip_d - 90)),
                                    np.cos(math.radians(dip_d + 90))], linewidth=1, color="black")
                ax_.add_line(arc_joint)
            else:
                arc_joint = Arc((center_late[0], center_late[1]), width=2 * r_of_joint,
                                height=2 * r_of_joint, angle=90 - dip_d, theta1=theta_1, theta2=theta_2)
                ax_.add_patch(arc_joint)

                # ax_.text(0, 0.05, "O Point", fontsize=20, transform=ax_.transAxes)


# 绘制纬线
def draw_weft():
    beta_array = [i for i in range(0, 91, 10)]
    # beta_array_ = [-i for i in range(0, 91, 10)]
    # beta_array.extend(beta_array_)
    for beta in beta_array:
        alpha = 90 - beta

        beta_rad = math.radians(beta)
        alpha_rad = math.radians(alpha)
        R = 1

        center = np.array([0, R / math.cos(beta_rad)])
        point_a = np.array([R * math.sin(beta_rad), R * math.cos(beta_rad)])
        r = np.sqrt(sum(np.power((center - point_a), 2)))

        theta_1_up = 360 - 2 * alpha - beta
        theta_2_up = 360 - beta

        theta_1_down = beta
        theta_2_down = 2 * alpha + beta

        if beta == 0:
            arc_joint = Line2D([-1, 1], [0, 0], linewidth=1, color="black")
            ax_.add_line(arc_joint)
        else:
            arc_joint_up = Arc(
                (center[0], center[1]),
                width=2 * r, height=2 * r,
                theta1=theta_1_up, theta2=theta_2_up)
            ax_.add_patch(arc_joint_up)

            arc_joint_down = Arc(
                (center[0], -center[1]),
                width=2 * r, height=2 * r,
                theta1=theta_1_down, theta2=theta_2_down)
            ax_.add_patch(arc_joint_down)


draw_longitude()
draw_weft()
plt.savefig("w_net.pdf", dpi=1200)
plt.show()
